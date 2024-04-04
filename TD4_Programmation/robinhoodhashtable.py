"""
Name ......: hashtable.py
Role ......: Implements a hashtable with the robin hood approach

Author ....: Max BOILLEDIEU
Version ...: V1.0.0 04/04/2024

Launch ....:
python robinhoodhashtable.py or 
import robinhoodhashtable.py
"""

from __future__ import annotations
import time 
import matplotlib.pyplot as plt


def evaluate_polynome(polynomial : list, value : float) -> float:
	"""
	Donne la valeur d'un polynôme donné par sa liste de coefficients en utilisant la méthode de Hörner
	"""
	result = 0
	for coef in polynomial[1:]:
		result += (result + coef)*value
	return result+polynomial[0]

def hash_jenkins(key) -> int:
	"""
	Fonction de hash de wikipédia donnée en cours qui est censée répartir uniformément les ensembles (clé, valeur)
	dans la table de hachage, peu de collisions sont générés
	"""
	hsh = 0
	for c in key:
		hsh += ord(c)
		hsh += (hsh << 10)
		hsh ^= hsh >> 6

	hsh += (hsh << 3)
	hsh ^= (hsh >> 11)
	hsh += (hsh << 15)
	return hsh 

def hash_polynomial(key : str) -> int:
	"""
	Fonction de hachage donnée en cours permettant de limiter les collisions dans les hashs
	"""
	s = [ord(c) for c in key]
	return evaluate_polynome(s, 33)


def hash_function_naive(key : str) -> int:
	"""
	Donne un hash pour une chaîne de caractères, cette fonction crée beaucoup de collisions
	"""
	return sum([ord(c) for c in key])



class RobinHookHashTable:
	"""
	Table de hachage implémentée en Python réutilisant les principes de Robin Hook premièrement 
	présenté dans la thèse de Pedro Celis en 1986, coût en insertion : O(log(N))
	"""
	def __init__(self, hash_function : callable, N = 97):
		self.__hash_function = hash_function 
		self.__taille = int(N)
		self.__tableau = [()]*self.__taille
		self.__nb_element = 0

	def put(self, key : str, value) -> bool:
		"""
		Fonction permettant d'insérer un nouveau couple (clé, valeur) dans la table de hachage 
		en adoptant la stratégie de Robin des bois (On vole aux riches pour donner aux plus pauvres).
		L'idée consiste à minimiser pour l'ensemble des données, la distance entre la valeur de 
		hachage des clés et leur emplacement réel.
		"""

		index = self.__hash_function(key) % self.__taille
		pls = 0
		elementEchange, condEchange, pls2 = None, False, 0

		while pls < self.__taille:
			if self.__tableau[index] == ():
				self.__tableau[index] = (key, value, pls)
				self.__nb_element += 1
				if elementEchange:
					self.echangerElements(elementEchange, index, pls2)
				return True

			elif self.__tableau[index][0] == key:
				self.__tableau[index] = (key, value, pls)

			else:
				if not(condEchange) and self.__tableau[index][2] < pls:
					elementEchange, condEchange, pls2= index, True, pls
				index = (index + 1) % self.__taille
			pls += 1
		return False

	def echangerElements(self, index: int, nouvelIndex: int, newPls: int) -> None:
		"""
		Fonction permettant d'échanger deux élements dans le tableau de triplets
		tout en minimisant la distance probable (pls) donc en employant la stratégie de Robin des bois.
		"""
		if nouvelIndex - index < 0:
			deltaIndex = self.__taille - index + nouvelIndex
		else:
			deltaIndex = nouvelIndex - index 

		self.__tableau[index] = (self.__tableau[index][0],self.__tableau[index][1], self.__tableau[index][2] + deltaIndex)
		self.__tableau[nouvelIndex] = (self.__tableau[nouvelIndex][0], self.__tableau[nouvelIndex][1], newPls)
		self.__tableau[index], self.__tableau[nouvelIndex] = self.__tableau[nouvelIndex], self.__tableau[index]

	def get(self, key : str):
		"""
		Fonction permettant de récupérer la valeur associée à une clé sous réserve d'existence, si la 
		clé n'existe pas, on renvoie la valeur None
		"""
		index = self.__hash_function(key) % self.__taille
		while index != self.taille() and self.__tableau[index][0] != key:
			index = (index + 1) % self.__taille
		if index == self.taille():
			return None
		else:
			return self.__tableau[index][1]

	def taille(self) -> int:
		"""
		Renvoie la taille du tableau associée à la table de hachage
		"""
		return self.__taille
	
	def nb_element(self) -> int:
		"""
		Renvoie le nombre d'éléments du tableau associé à la table de hachage
		"""
		return self.__nb_element

	def __str__(self) -> str:
		"""
		Affiche le tableau associé à la table de hachage
		"""
		return str(self.__tableau)

	def __setitem__(self, key : str, value) -> None:
		self.put(key, value)

	def __getitem__(self, key : str):
		return self.get(key)

if __name__ == "__main__":
	hshtable = RobinHookHashTable(hash_function_naive,97)

	hshtable.put("a",12)
	hshtable.put("aaa", 12)
	print(hshtable.get("a"))