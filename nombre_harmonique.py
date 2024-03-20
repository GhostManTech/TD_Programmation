try:
	import sys
	from fraction import *
except ImportError as exception:
	print(f"{exception}")
else:
	def H(n : int) -> Fraction:
		resultat = Fraction(0,1)
		assert(n >= 1)
		for k in range(1,n+1):
			resultat.add(Fraction(1,k))
		resultat.simplify()
		return resultat

	if __name__ == "__main__":
		sys.set_int_max_str_digits(10**6)
		sys.setrecursionlimit(10**6)
		print(H(10000))