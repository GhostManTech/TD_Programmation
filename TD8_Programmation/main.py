import struct


# Exercice 1, pour extraire les données, il suffit d'utiliser la fonction struct.unpack_from et d'extraire les deux canaux séparemment
def extract_file(filename : str, *args) -> (list, list):
	# Ouverture du fichier filename
	f = open(filename, "rb")
	data = f.read()
	f.close()
	
	# Extraction des deux canaux à partir du fichier
	canal1 = []
	canal2 = []
	for i in range(44,len(data),4):
		canal1.append(struct.unpack_from("h", data, i)[0])
		canal2.append(struct.unpack_from("h", data, i+2)[0])
	return canal1, canal2

# Exercice 2, on redéfini proprement l'entête et on recopie les données en fonction de la méthode d'extraction passée en paramètres
def create_file(filename1 : str, filename2 : str, extract_function : callable, *args) -> None:
	f = open(filename2, "wb")
	canal1, canal2 = extract_function(filename1, *args)
	taille = 4*len(canal1)-8+44

	# Données d'en-tête, récupéré à partir de la documentation
	tab = [b"RIFF", 
		   struct.pack("i", taille), 
	       b"WAVE", 
	       b"fmt ", 
	       struct.pack("i", 16),
	       struct.pack("h", 1), 
	       struct.pack("h", 2), 
	       struct.pack("i", 44100), 
	       struct.pack("i", 176400),
	       struct.pack("h", 4), 
	       struct.pack("h", 16), 
	       b"data", 
	       struct.pack("i", 4*len(canal1))]

	for t in tab:
		f.write(t)

	for k in range(len(canal1)):
		f.write(struct.pack("hh", canal1[k], canal2[k]))
	
	f.close()

# Exercice 3, on enlève la moitié des données, donc ça accélère la musique et comme la fréquence augmente, le son est plus aigü
def extract_file_half(filename : str, *args) -> (list, list):
	# Ouverture du fichier filename
	f = open(filename, "rb")
	data = f.read()
	f.close()
	
	# Extraction des deux canaux à partir du fichier
	canal1 = []
	canal2 = []
	for i in range(44,len(data),8):
		canal1.append(struct.unpack_from("h", data, i)[0])
		canal2.append(struct.unpack_from("h", data, i+2)[0])
	return canal1, canal2

# Exercice 4, on double le nombre de données
def extract_file_double(filename : str, *args) -> (list, list):
	# Ouverture du fichier filename
	f = open(filename, "rb")
	data = f.read()
	f.close()
	
	# Extraction des deux canaux à partir du fichier
	canal1 = []
	canal2 = []
	for i in range(44,len(data)-4, 4):
		c11 = struct.unpack_from("h", data, i)[0]
		c12 = struct.unpack_from("h", data, i+4)[0]
		c21 = struct.unpack_from("h", data, i+2)[0]
		c22 = struct.unpack_from("h", data, i+6)[0]
		
		canal1.append(c11)
		canal1.append((c11+c12)//2)
		if i + 4 >= len(data):
			canal1.append(c12)

		canal2.append(c21)
		canal2.append((c21+c22)//2)
		if i + 4 >= len(data):
			canal2.append(c22)
	return canal1, canal2

# Exercice 5, modification de la cadence par un réel f, il suffit de modifier la fréquence d'échantillonage dans l'en-tête
def accelerer_f(filename1 : str, filename2 : str, f : float):
	# Ouverture du fichier filename
	file = open(filename1, "rb")
	data = file.read()
	file.close()
	
	# Extraction des deux canaux à partir du fichier
	canal1 = []
	canal2 = []
	for i in range(44,len(data), 4):
		c1 = struct.unpack_from("h", data, i)[0]
		c2 = struct.unpack_from("h", data, i+2)[0]
		canal1.append(c1)
		canal2.append(c2)

	file = open(filename2, "wb")

	taille = 4*len(canal1)-8+44

	# Données d'en-tête, récupéré à partir de la documentation
	tab = [b"RIFF", 
		   struct.pack("i", taille), 
	       b"WAVE", 
	       b"fmt ", 
	       struct.pack("i", 16),
	       struct.pack("h", 1), 
	       struct.pack("h", 2), 
	       struct.pack("i", int(44100*f)), 
	       struct.pack("i", 176400),
	       struct.pack("h", 4), 
	       struct.pack("h", 16), 
	       b"data", 
	       struct.pack("i", 4*len(canal1))]

	for t in tab:
		file.write(t)

	for k in range(len(canal1)):
		file.write(struct.pack("hh", canal1[k], canal2[k]))


	file.close()


"""
param: T retard
a: facteur d'atténuation
"""

# Exercice 6, création d'un écho de retard
def extract_file_echo(filename : str, T : int, a : float) -> (list, list):
	# Ouverture du fichier filename
	f = open(filename, "rb")
	data = f.read()
	f.close()

	canal1 = []
	canal2 = []
	# Extraction des deux canaux à partir du fichier4
	for i in range(44, len(data), 8):
		c1 = struct.unpack_from("h",data, i)[0]
		c2 = struct.unpack_from("h", data, i+2)[0]
		canal1.append(c1)
		canal2.append(c2)
		if i - T > 44:
			c1 = int(struct.unpack_from("h", data, i-T)[0]*a)
			c2 = int(struct.unpack_from("h", data, i+2-T)[0]*a)
			canal1.append(c1)
			canal2.append(c2)		
	return canal1, canal2


if __name__ == "__main__":
	create_file("the_wall.wav", "the_wall2.wav", extract_file_echo, 2**18, 1/2)