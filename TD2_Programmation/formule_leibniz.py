try:
	import sys
	from fraction import *
except ImportError as exception:
	print(f"{exception}")
else:
	def LeibnizSum(n : int) -> Fraction:
		resultat = Fraction(0,1)
		assert(n >= 1)
		for k in range(0,n+1):
			if k % 2 == 0:
				resultat.add(Fraction(1,2*k+1))
			else:
				resultat.add(Fraction(-1,2*k+1))
		resultat.simplify()
		return resultat

	if __name__ == "__main__":
		sys.set_int_max_str_digits(10**6)
		sys.setrecursionlimit(10**6)
		resultat = LeibnizSum(10000)
		print(resultat.calcul())
		print(resultat)
