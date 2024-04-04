"""
Name ......: test.py
Role ......: Tests on the Hashtable class

Author ....: Max BOILLEDIEU
Version ...: V1.0.0 03/04/2024

Launch ....:
python hashtable.py or 
import hashtable.py
"""

from hashtable import *

if __name__ == "__main__":
	# Création de collisions
	hshtable2 = Hashtable(hash_function_naive)
	hshtable2.put("a",12)
	hshtable2.put("aaa", 15)
	hshtable2.put("abc", 17)

	print(hshtable2.get("a"))
	print(hshtable2.get("aaa"))
	print(hshtable2.get("abc"))
	hshtable2.repartition()

	# Changement de taille du tableau 
	hshtable3 = Hashtable(hash_function_naive ,97)
	hshtable3.put("chien", 17)

	print(hshtable3.get("chien"))
	print(hshtable3.taille())

	hshtable3.resize()

	print(hshtable3.get("chien"))
	print(hshtable3.taille())

	# Test de plusieurs fonctions de hachage
	hshtable, time_ecriture1, time_lecture1, number_lines = dict_file("frenchssaccent.dic", hash_jenkins, 320)
	hshtable.repartition()
	hshtable, time_ecriture2, time_lecture2, number_lines = dict_file("frenchssaccent.dic", hash_function_naive, 320)
	hshtable.repartition()

	#Temps d'écriture et de lecture
	t = [k for k in range(number_lines)]
	plt.plot(t,time_ecriture1)
	plt.title("Temps en écriture : fonction de hachage de Jenkins")
	plt.show()

	plt.plot(t,time_ecriture2)
	plt.title("Temps en écriture : fonction de hachage naïve")
	plt.show()


	plt.plot(t,time_lecture1)
	plt.title("Temps en lecture : fonction de hachage de Jenkins")
	plt.show()

	plt.plot(t,time_lecture2)
	plt.title("Temps en lecture : fonction de hachage naïve")
	plt.show()
