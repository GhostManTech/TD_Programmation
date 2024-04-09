"""
Name ......: hashtable.py
Role ......: Implements a hashtable with a list of collisions and without collisions

Author ....: Max BOILLEDIEU
Version ...: V1.0.0 03/04/2024

Launch ....:
python hashtable.py or 
import hashtable.py
"""

from __future__ import annotations
import matplotlib.pyplot as plt
import time

"""
Question n°1 :
Pour définir la classe Hashtable, il est nécessaire d'avoir les attributs :
-> tableau de liste de tuples (clé,valeur)
-> nombre de cases
-> fonction de hachage
Il est également nécessaire d'avoir les méthodes:
-> obtenir un élément
-> placer un élément
"""



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


class Hashtable2:
	"""
	Table de hachage sans liste de collisions

	Classe non demandée en TD, version linéaire d'une table de hachage en utilisant l'algorithme du cours
	"""
	def __init__(self, hash_function : callable, N=97):
		self.__hash_function = hash_function 
		self.__taille = int(N)
		self.__tableau = [() for k in range(self.__taille)]
		self.__nb_element = 0

	def put(self, key : str, value) -> None:
		"""
		Fonction permettant d'enregistrer dans le tableau associé à la table de hachage le couple (clé, valeur)
		"""
		index = self.__hash_function(key) % self.__taille
		cond = False
		while not(cond):
			if self.__tableau[index] == ():
				self.__tableau[index] = (key, value)
				cond = True
				self.__nb_element += 1
			else:			
				index = (index+1) % self.__taille
				if index == self.__hash_function(key) % self.__taille:
					self.__taille *= 2
					tab = list(self.__tableau)
					self.__tableau = [() for k in range(self.__taille)]
					for (k,v) in tab:
						self.put(k,v)
					self.put(key, value)
				else:
					if self.__tableau[index] == []:
						self.__tableau[index] = (key,value)
						cond = True
						self.__nb_element += 1

	def get(self, key : str):
		"""
		Fonction permettant d'obtenir la valeur associée à une clé et None si cette clé n'existe pas
		"""
		index = self.__hash_function(key) % self.__taille
		while index != self.taille() and self.__tableau[index][0] != key:
			index = (index + 1) % self.__taille
		if index == self.taille():
			return None
		else:
			return self.__tableau[index][1]

	def __str__(self) -> str:
		return str(self.__tableau)

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

	def __setitem__(self, key : str, value) -> None:
		self.put(key, value)

	def __getitem__(self, key : str):
		return self.get(key)

class Hashtable:
	"""
	Table de hachage avec liste de collisions
	La table de hachage est enregistrée sous la forme d'un
	tableau où il peut y avoir des collisions.
	Chaque emplacement comprend une liste de couples (clé, valeur).
	"""
	def __init__(self, hash_function : callable, N = 97):
		self.__hash_function = hash_function 
		self.__taille = int(N)
		self.__tableau = [[] for k in range(self.__taille)]
		self.__nb_element = 0

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

	def resize(self) -> None:
		"""
		Doubler la taille du tableau de la table de hachage quand celle-ci est surchargée, on obtient la complexité
		en O(1) amortie en écriture et lecture.
		"""
		self.__taille *= 2
		tab = list(self.__tableau) # Copie de l'ancien tableau
		self.__tableau = [[] for k in range(self.__taille)]
		for l in tab: 
			for (k,v) in l:
				self.put(k,v)


	def put(self, key : str, value) -> float:
		"""
		Ajouter la valeur value associée à la clé key dans la table de hachage en gérant les listes de collisions
		"""
		t1 = time.perf_counter()
		index = self.__hash_function(key) % self.__taille
		
		if self.nb_element() >= 1.2*self.taille():
			self.__nb_element = 0
			self.resize()

		if key in [k for (k,v) in self.__tableau[index]]:
			ind = 0
			for k in range(len(self.__tableau[index])):
				key2,v = self.__tableau[index][k]
				if key2 == key:
					ind = k

			k,v = self.__tableau[index][ind]
			if v != value:
				self.__tableau[index][ind] = (key,value)
		else:
			self.__tableau[index].append((key,value))
			self.__nb_element += 1

		t2 = time.perf_counter()
		deltaT = t2 - t1
		return deltaT

	def get(self, key : str):
		"""
		Sous réserve d'existence, renvoyer la valeur associée à la clé donnée en argument
		"""
		index = self.__hash_function(key)%self.__taille 
		for (k,v) in self.__tableau[index]:
			if k == key:
				return v 
		return None

	def __str__(self):
		"""
		Affiche le tableau associé à la table de hachage
		"""
		return str(self.__tableau)

	def repartition(self) -> None:
		"""
		Affiche un histogramme du nombre d'éléments pour chaque emplacement du tableau
		"""
		liste_tailles = []
		for l in self.__tableau:
			liste_tailles.append(len(l))	

		x = [k for k in range(self.__taille)]
		width = 5
		plt.bar(x,liste_tailles, width, color="blue")
		plt.title("Nombre de collisions par emplacement dans le tableau")
		plt.show()

	def __setitem__(self, key : str, value) -> None:
		self.put(key, value)

	def __getitem__(self, key : str):
		return self.get(key)


def dict_file(file_name : str, hash_function : callable, N : int):
	"""
	Fonction qui crée un dictionnaire à partir des mots d'un fichier
	(un mot par ligne)
	"""
	hashtable = Hashtable(hash_function,N)
	file = open(file_name, "r")
	lines = file.readlines()
	time_ecriture = []*len(lines)
	time_lecture = []*len(lines)

	for line in lines:
		newLine = line[0:-1]
		time_ecriture.append(hashtable.put(newLine, len(newLine)))
		t1 = time.perf_counter()
		hashtable.get(newLine)
		t2 = time.perf_counter()
		time_lecture.append(t2-t1)
	
	return hashtable, time_ecriture, time_lecture, len(lines)

if __name__ == "__main__":
	hshtable = Hashtable2(hash_function_naive,97)
	hshtable.put("a", 17)
	print(hshtable.get("a"))
