from __future__ import annotations
import math

class Polynomial:
	"""
	Classe permettant de définir des polynômes sous la forme de tableaux de coefficients en partant du terme de plus bas degré
	Attributs :
	Degré du polynôme : -infini pour le polynôme nul et sinon un entier naturel
	Tableau des coefficients du polynôme
	"""
	def __init__(self, coefs: list):
		self.coefs = coefs
		self.degre = len(coefs)-1

	def __str__(self) -> str:
		"""
		Fonction permettant de d'afficher l'écriture algébrique d'un polynôme
		"""
		affichage = ""
		for k in range(self.degre,0,-1):
			if self.coefs[k] != 0:
				affichage += f"{self.coefs[k]}X**{k}"
				if k != 1 or (k == 1 and self.coefs[0] != 0):
					affichage += " + "


		if self.coefs[0] != 0:
			affichage += f"{self.coefs[0]}"

		return affichage


	def add(self, polynom) -> Polynomial:
		"""
		Fonction qui additionne deux polynômes et qui renvoi le polynôme de la somme
		"""
		# Calcul du degré de la somme
		m = max(self.degre, polynom.degre)
		newPolynom = Polynomial([0 for k in range(m+1)])
		if m == self.degre:
			for k in range(0, self.degre+1):
				newPolynom.coefs[k] = self.coefs[k]
			for k in range(0, polynom.degre+1):
				newPolynom.coefs[k] +=  polynom.coefs[k]
		else:
			for k in range(0, polynom.degre+1):
				newPolynom.coefs[k] = polynom.coefs[k]
			for k in range(0, self.degre+1):
				newPolynom.coefs[k] += self.coefs[k]

		coefs = newPolynom.coefs[::-1]
		index = 0
		while coefs[index] == 0:
			index += 1 
		newPolynom.degre = m-index
		return newPolynom

	def deriv(self) -> Polynomial:
		"""
		Fonction permettant de donner la dérivée d'un polynôme
		"""
		newPolynom = Polynomial([0 for k in range(0, self.degre)])
		for k in range(1, self.degre+1):
			newPolynom.coefs[k-1] = k*self.coefs[k]
		return newPolynom

	def integrate(self, const) -> Polynomial:
		"""
		Fonction permettant de donner l'intégrale d'un polynôme à une constante près 
		"""
		newPolynom = Polynomial([0 for k in range(0, self.degre+2)])
		for k in range(1, self.degre+2):
			newPolynom.coefs[k] = self.coefs[k-1]/k
		# Ajout de la constante d'intégration
		newPolynom.coefs[0] = const
		return newPolynom

	def deg(self):
		"""
		Fonction permettant de calculer le degré d'un polynôme, par convention le degré du polynôme nul est -infini
		"""
		cond = True
		for c in self.coefs:
			if c != 0:
				cond = False
		if cond:
			self.degre = -math.inf
		else:
			coefs = self.coefs[::-1]
			index = 0
			while coefs[index] == 0:
				index += 1
			self.degre = len(coefs)-1-index
		return self.degre

	def troncature(self) -> Polynomial:
		"""
		Fonction permettant de donner un nouveau polynôme en ôtant les coefficients inutiles
		"""
		degre = self.deg()
		coefs = self.coefs[0:degre+1]
		return Polynomial(coefs)


if __name__ == "__main__":
	#Addition de deux polynômes
	polynome1 = Polynomial([3,2,0,4])
	polynome2 = Polynomial([-4,-2,2,-4])
	polynome3 = polynome1.add(polynome2)
	print(polynome3.degre)
	print(polynome1)
	print(polynome2)

	#Dérivation et intégration de polynômes
	polynome4 = polynome3.deriv()
	polynome5 = polynome3.integrate()
	polynome6 = Polynomial([0,4,5,6,0,0])
	print(polynome6)
	print(polynome4)
	print(polynome5)


