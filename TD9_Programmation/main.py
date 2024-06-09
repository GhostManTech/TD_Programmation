from __future__ import annotations



def modifier_polynome(coefs, q, n):
	"""
	Fonction permettant de modifier un polynôme en entrée pour qu'il soit dans Z_q[X]/(X^n+1)Z_q[X]
	"""
	coefs1 = list(coefs)
	degre1 = len(coefs1)-1


	# Modification des degrés
	for k in range(len(coefs1)):
		quotient,reste = divmod(degre1-k, n)	
		if degre1 - k >= n:
			if quotient > 0:
				if quotient % 2 == 0:
					coefs1[degre1 -reste] += coefs1[k]
				else:
					coefs1[degre1-reste] -= coefs1[k]
				coefs1[k] = 0


	# Modification des coefficients
	for k in range(len(coefs1)):
		coefs1[k] = round(coefs1[k] % q)

	# Troncature
	cnt = 0
	while coefs1[cnt] == 0:
		cnt += 1
	coefs1 = coefs1[cnt:]
	
	return coefs1

class Polynome:
	"""
	Classe permettant d'implémenter des polynômes qui sont dans Z_q[X]/(X^n+1)Z_q[X]
	Tout polynôme donné en entrée sera re-transformé quelque soit sa nature initiale
	"""
	def __init__(self, coefs, q, n):
		self.__coefs = modifier_polynome(coefs, q, n)
		self.__q = q 
		self.__n = n
		self.__degre = len(self.__coefs)-1

	def obtenir_q(self) -> int:
		"""
		Fonction permettant de donner le nombre d'éléments dans l'anneau Z/qZ associé aux coefficients du polynôme
		"""
		return self.__q

	def obtenir_n(self) -> int:
		"""
		Fonction permettant de donner l'entier n de l'anneau quotienté Z_q[X]/(X^n+1)Z_q[X] associé au polynôme représenté par self
		"""
		return self.__n

	def obtenir_degre(self):
		"""
		Fonction permettant de donner le degré du polynôme représenté par self
		"""
		return self.__degre

	def obtenir_coef(self, k : int) -> int:
		"""
		Fonction permettant de renvoyer le coefficient de degré k associé au polynôme représenté par self
		"""
		assert(k >= 0 && k <= self.__degre)
		return self.__coefs[self.__degre - k]

	def obtenir_coef2(self, k : int) -> int:
		"""
		Fonction permettant de renvoyer le coefficient de degré deg(self)-k du polynôme représenté par self
		"""
		return self.__coefs[k]

	def obtenir_coefs(self) -> list:
		"""
		Fonction permettant de renvoyer la liste des coefficients du polynôme représenté par self par degré décroissant
		"""
		return self.__coefs


	def __add__(self, poly : Polynome) -> Polynome:
		"""
		Fonction permettant d'additionner deux polynômes dans Z_q[X]/(X^n+1)Z_q[X]
		"""
		assert(self.__q == poly.obtenir_q() and self.__n == poly.obtenir_n())

		new_coefs = []
		if self.__degre > poly.obtenir_degre():
			new_coefs = list(self.__coefs)
			for k in range(poly.obtenir_degre()+1):
				new_coefs[self.__degre-k] += poly.obtenir_coef(k)
		else:
			new_coefs = list(poly.obtenir_coefs())
			for k in range(self.__degre+1):
				new_coefs[poly.obtenir_degre()-k] += self.__coefs[self.__degre-k]

		return Polynome(new_coefs, self.__q, self.__n)



	def __mul__(self, poly : Polynome) -> Polynome:
		"""
		Fonction permettant de multiplier deux polynômes dans l'anneau quotienté Z_q[X]/(X^n+1)Z_q[X]
		"""
		assert(self.__q == poly.obtenir_q() and self.__n == poly.obtenir_n())
		new_coefs = [0 for k in range(self.__degre + poly.obtenir_degre()+1)]

		for k in range(self.__degre + poly.obtenir_degre() + 1):
			summation = 0

			for i in range(self.__degre +1):
				for j in range(poly.obtenir_degre()+1):
					if i + j == k:
						summation += self.__coefs[self.__degre - i]*poly.obtenir_coef(j)

			new_coefs[self.__degre+poly.obtenir_degre()-k] = summation

		return Polynome(new_coefs, self.__q, self.__n)

	def scalar(self, c : int) -> Polynome:
		"""
		Fonction permettant de multiplier un polynôme dans Z_q[X]/(X^n+1)Z_q[X] par un scalaire entier
		"""
		for k in range(self.__degre+1):
			self.__coefs[k] = (self.__coefs[k] * c) % self.__q
		return Polynome(self.__coefs, self.__q, self.__n)

	def rescale(self, r : int) -> Polynome:
		"""
		Fonction permettant de transformer un polynôme de Z_q[X]/(X^n+1)Z_q[X] en un polynôme de Z_r[X]/(X^n+1)Z_r[X]
		"""
		return Polynome(self.__coefs, r, self.__n)

	def fscalar(self, r : int, alpha : float) -> Polynome:
		"""
		Fonction permettant de multiplier un polynôme dans Z_q[X]/(X^n+1)Z_q[X] par un scalaire flottant
		"""
		for k in range(self.__degre+1):
			self.__coefs[k] = round(self.__coefs[k] * alpha)
		return Polynome(self.__coefs, r, self.__n)

	def __str__(self) -> str:
		"""
		Fonction permettant d'afficher l'écriture algébrique du polynôme self
		"""
		affichage = ""
		for k in range(self.__degre):
			if self.__coefs[k] != 0:
				affichage += f"{self.__coefs[k]}X^{self.__degre-k}"
				if k != self.__degre-1 or (k == self.__degre-1 and self.__coefs[self.__degre] != 0):
					affichage += " + "
 

		if self.__coefs[self.__degre] != 0:
			affichage += f"{self.__coefs[self.__degre]}"
		affichage += f" [X^{self.__n}+1]"
		return affichage



# Cryptographie
def gen_uniform_random(q : int, n : int, a, b ) -> Polynome:
	"""
	Fonction permettant de générer aléatoirement un polynôme dans Z_q[X]/(X^n+1)Z_q[X] et que les coefficients initiaux soient dans [a,b]
	"""
	coefs = [0 for _ in range(n)]
	for k in range(n):
		coefs[k] = random()*(b-a) + a
	return Polynome(coefs, q, n)

def gen_e(q, n) -> Polynome:
	coefs = [0 for _ in range(n)]
	tab = [0, 1, q-1]
	for k in range(n):
		coefs[k] = choice(tab)
	return Polynome(coefs, q, n)

def gen_private_key(q, n) -> Polynome:
	return gen_uniform_random(q, n, 0, 1)

def gen_public_key(q, n, sk : Polynome) -> tuple:
	a1 = gen_uniform_random(q, n, 0, q-1)
	e = gen_e(q, n)
	s = a1*sk+e
	b1 = s.fscalar(-1)
	return (a1,b1)



if __name__ == "__main__":
	poly1 = Polynome([89, 45, 12, 5, 2, 3], 7, 3)
	print(poly1)
	poly2 = Polynome([4,6,5], 7, 3)
	print(poly2)
	poly3 = poly1 * poly2
	print(poly3)



