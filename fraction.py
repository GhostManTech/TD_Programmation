from __future__ import annotations

def pgcd(a : int, b: int) -> int:
	if b == 0:
		return a 
	return pgcd(b, a%b)

class Fraction :
	"""
	Type fraction permettant de représenter des 
	fractions d'entiers relatifs. Le numérateur doit
	être non nul. 
	"""
	def __init__(self, numerator : int, denominator : int):
		self.numerator = numerator
		assert(denominator != 0)
		self.denominator = denominator

	def add(self, fraction : Fraction):
		"""
		Fonction permettant d'additionner une autre fraction
		"""
		self.numerator = fraction.denominator*self.numerator+self.denominator*fraction.numerator
		self.denominator = self.denominator*fraction.denominator

	def add2(self, fraction):
		"""
		Fonction permettant de multiplier une autre fraction et de renvoyer une nouvelle fraction
		"""
		n = fraction.denominator*self.numerator+self.denominator*fraction.numerator
		d = self.denominator*fraction.denominator
		return Fraction(n, d)

	def mult(self, fraction):
		"""
		Fonction permettant de multiplier une autre fraction
		"""
		self.numerator = self.numerator*fraction.numerator
		self.denominator = self.denominator*fraction.denominator

	def mult2(self, fraction):
		"""
		Fonction permettant de multiplier une autre fraction et de renvoyer une nouvelle fraction
		"""
		n = self.numerator*fraction.numerator
		d = self.denominator*fraction.denominator
		return Fraction(n,d)

	def __str__(self):
		"""
		Fonction permettant d'afficher la représentation de la fraction
		"""
		return f"({self.numerator}/{self.denominator})"

	def simplify(self):
		"""
		Fonction permettant de simplifier une fraction de nombres entiers relatifs en calculant le pgcd du numérateur et du dénominateur
		"""
		PGCD = pgcd(self.numerator, self.denominator)
		self.numerator //= PGCD
		self.denominator //= PGCD

	def calcul(self) -> float:
		"""
		Fonction permettant de donner une valeur approchée de la valeur de la fraction
		"""
		return self.numerator/self.denominator




if __name__ == "__main__":
	fraction1 = Fraction(16,4)
	fraction1.simplify()
	fraction2 = Fraction(1,2)
	fraction1.mult(fraction2)
	print(fraction1)
