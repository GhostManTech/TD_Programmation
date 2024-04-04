from __future__ import annotations 
import unittest
import sys
"""
Exercice 1 :
La classe Arbre devrait comporter les méthodes suivantes :
-> Récupération de l'étiquette de la racine
-> Savoir si le noeud est une feuille
-> Donner les enfants d'un noeud
-> Donner un enfant spécifique d'un noeud
"""

def is_floatint(s):
	"""
	Fonction permettant de savoir si une chaîne de caractères est un flottant ou un entier
	"""
	return s.replace(".","").isdigit()

class Tree:
	"""
	Classe permettant de créer des arbres quelconques et de leur appliquer des opérations
	"""
	def __init__(self, label : str, *children):
		"""
		Constructeur de la classe
		"""
		self.__label = label
		self.__children = tuple(children)

	def label(self) -> str:
		"""
		Fonction permettant de récupérer l'étiquette de la racine
		"""
		return self.__label 

	def children(self) -> tuple:
		"""
		Fonction permettant de récupérer les enfants du noeud
		"""
		if self.__children == None:
			return ()
		return self.__children

	def nb_children(self) -> int:
		"""
		Fonction permettant de récupérer le nombre d'enfants d'un noeud
		"""
		if self.__children == None:
			return 0
		return len(self.__children)

	def child(self, i : int) -> Tree:
		"""
		Fonction permettant de récupérer le i-ième enfant d'un noeud	
		"""
		assert(self.nb_children() > i)
		return self.__children[i]

	def is_leaf(self) -> bool:
		"""
		Fonction permettant de savoir si un noeud est une feuille i.e. qu'il n'a pas d'enfants
		"""
		return self.__children == ()

	def depth(self) -> int:
		"""
		Fonction récursive permettant de donner la profondeur de l'arbre
		"""
		if self.is_leaf():
			return 0
		return 1+max([s.depth() for s in self.children()])

	def __str__(self) -> str:
		"""
		Fonction permettant de renvoyer la notation préfixée de l'arbre
		"""
		if self.is_leaf():
			return self.label()
		s = f"{self.label()}("
		if self.nb_children() == 1:
			s += f"{self.child(0).__str__()})"
			return s
		else:
			n = self.nb_children()
			for k in range(0,n-1):
				s+= f"{self.child(k).__str__()},"
			s+= f"{self.child(n-1).__str__()})"
			return s

	"""
	def __eq__(self, tree: Tree) -> bool:
		
		Fonction permettant de comparer deux arbres entre eux
		if self.is_leaf() and tree.is_leaf():
			return self.label() == tree.label()
		if self.nb_children() == tree.nb_children():
			if self.label() == tree.label():
				return self.children().__eq__(tree.children())
			else:
				return False
		else:
			return False

	"""
	def __eq__(self, tree : Tree) -> bool:
		return self.__label == tree.label() and self.__children == tree.children()


	def deriv(self, var : Tree) -> Tree:
		"""
		Fonction permettant de dériver un polynôme par rapport à une indéterminée. Le polynôme étant enregistré sous la 
		forme d'un arbre. Utiliser (fg)' = f'g + fg' pour la multiplication, méthode apparemment trop compliquée
		"""
		if self.is_leaf():
			if var.label() == self.label():
				return Tree("1")
			else:
				return Tree("0")
		if self.label() == "+":
			return Tree(self.label(),*tuple([s.deriv(var) for s in self.children()]))
		if self.label() == "*":
			l = []
			number = 1.
			index = 0 
			for s in self.children():
				if is_floatint(s.label()):
					number *= float(s.label())
				elif s.label() == var.label():
					index += 1
				else:
					l.append(Tree(s.label()))
			number *= index 
			if number.is_integer():		
				l.append(Tree(str(int(number))))
			else:
				l.append(Tree(str(number)))
			for k in range(index-1):
				l.append(var)
			return Tree("*",*l)

	def substitute(self, t1 : Tree, t2 : Tree) -> Tree:
		"""
		Fonction permettant de remplacer toutes les occurences de t1 par t2 dans l'arbre considéré
		"""
		if self == t1:
			return t2
		else:
			if self.is_leaf():
				if t1.is_leaf():
					if self.label() == t1.label():
						return t2
					else:
						return self
				else:
					return self
			else:
				if t1.is_leaf():
					if self.label() == t1.label():
						return Tree(t2.label(), *[s.substitute(t1,t2) for s in self.children()])
					else:
						return Tree(self.label(),*[s.substitute(t1,t2) for s in self.children()])
				else:
					return Tree(self.label(),*[s.substitute(t1,t2) for s in self.children()]) 

	def simplify(self) -> Tree:
		"""
		Fonction récursive permettant de simplifier des expressions polynomiales
		"""
		if not(self.is_leaf()):
			if self.label() == "+":
				l = []
				number = 0
				for s in self.children():
					if s.is_leaf() and is_floatint(s.label()):
						number += float(s.label())
					else:
						l.append(s.simplify())
				if number != 0:
					if number.is_integer():
						l.append(Tree(str(int(number))))
					else:
						l.append(Tree(str(number)))
				if len(l) >= 2:
					return Tree("+",*l)
				if len(l) == 1:
					return l[0]
				return Tree("0")

			if self.label() == "*":
				l = []
				number = 1
				cond = False
				for s in self.children():
					if s == Tree("0"):
						cond = True 
					elif s.is_leaf() and is_floatint(s.label()):
						number *= float(s.label())
					else:
						l.append(s.simplify())
				if cond:
					return Tree("0")
				else:
					if number.is_integer():
						l.append(Tree(str(int(number))))
					else:
						l.append(Tree(str(number)))
					if len(l) >= 2:
						return Tree("*", *l[::-1])
					return l[0]
		else:
			return self

	def evaluate_polynome(self, value : float | int) -> float | int:
		"""
		Fonction permettant d'évaluer un polynôme en un point stocké sous la forme d'un arbre n-aire après substitution et simplification
		"""
		v = self.substitute(Tree("X"),Tree(str(value)))
		c = v.simplify().simplify()
		if c.label().isdigit():
			return int(c.label())
		else:
			return float(c.label())

	def notation_infixe(self) -> str:
		"""	
		Fonction récursive permettant de donner la notation infixe d'un arbre
		"""
		if self.is_leaf():
			return self.label()
		st = ""
		for s in self.children():
			st +=  f" {s.notation_infixe()} "
		return st+self.label()

def monomial_tree(p : str) -> Tree:
	"""
	Fonction permettant de transformer un monôme en un arbre
	"""
	if "X" in p:
		m = p.split("X")
		if m == ["",""]:
			return Tree("X")
		elif "" in m:
			if "**" in m[0]:
				power = int(m[0].split("**")[1])
				return Tree("*",*[Tree("X") for _ in range(power)])
			else:
				return Tree("*", Tree(m[0]), Tree("X"))
		elif is_floatint(m[0]) and "**" in m[1]:
			m1 = m[0]
			m2 = int(m[1].split("**")[1])
			l = [Tree("X") for k in range(m2)]
			l.append(Tree(m1))
			return Tree("*", *l[::-1])
	else:
		return Tree(p)

def string_tree(p : str) -> Tree:
	"""
	Fonction permettant de transformer un polynôme en chaîne de caractères en un polynôme stocké sous la forme d'un arbre
	"""
	if p == "":
		return Tree("0")
	else:
		m = p.replace(" ", "").split("+")
		if len(m) == 1:
			return Tree(monomial_tree(m[0]))
		else:
			return Tree("+", *[monomial_tree(s) for s in m])

class testTree(unittest.TestCase):
	def test_nbchild(self):
		polynome = Tree("+", Tree("*",Tree("3"),Tree("X"),Tree("X")),Tree("*",Tree("5"),Tree("X")),Tree(7))		
		t1 = Tree("f", Tree("a"),Tree("b"))
		t2 = Tree("50", Tree("40", Tree("30", Tree("20")), Tree("45")), Tree("60", Tree("65")))
		self.assertTrue(t1.nb_children() == 2)
		self.assertTrue(t2.nb_children() == 2)

	def test_children(self):
		t1 = Tree("f", Tree("a"),Tree("b"))
		self.assertTrue(t1.children() == (Tree("a"),Tree("b")))

	def test_substitute(self):
		t1 = Tree("30", Tree("20"))
		t2 = Tree("50",Tree("30",Tree("20")))
		t3 = Tree("50", Tree("40", Tree("30", Tree("20")), Tree("45")), Tree("60", Tree("65")))
		t4 = Tree("50",Tree("40", Tree("50",Tree("30",Tree("20"))), Tree("45")),Tree("60",Tree("65")))
		self.assertEqual(t3.substitute(t1,t2),t4)
		self.assertTrue(t3.substitute(t1,t2) == t4)

	def test_simplify(self):
		polynome = Tree("+", Tree("*",Tree("3.5"),Tree("X"),Tree("X")),Tree("*",Tree("5"),Tree("X")),Tree(7))
		polynome1 = polynome.deriv(Tree("X")).simplify()
		polynome2 = Tree("+", Tree("*", Tree("7"), Tree("X")), Tree("5"))
		self.assertTrue(polynome1 == polynome2)

	def test_evaluate_polynome(self):
		polynome = Tree("+", Tree("*", Tree("7"), Tree("X")), Tree("5"))
		v = polynome.evaluate_polynome(1)
		self.assertTrue(v == 12)

	def test_equal(self):
		polynome1 = Tree("+", Tree("*", Tree("7"), Tree("X")), Tree("5"))
		polynome2 = Tree("+", Tree("*", Tree("7"), Tree("X")), Tree("5"))

		self.assertTrue(polynome1 == polynome2)

if __name__ == "__main__":
	unittest.main()
