"""
Name ......: main.py
Role ......: graph

Author ....: Max BOILLEDIEU
Version ...: V1.0.0 22/05/2024

Launch ....:
python3 main.py
"""

from tkinter import *
from tkinter import ttk
import numpy as np
from math import sqrt, sin, atan, cos, acos, pi, inf
from random import randint, sample, choice, random

root = Tk()
content = Frame(root)
w = 500
h = 500
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - w) // 2 
y = (screen_height - h) // 2
root.title("Coloration de graphes")
root.geometry(f"{w}x{h}+{x}+{y}")
root.resizable(width = False, height = False)

# Tableau des couleurs
COLORS = ['antiquewhite', 'aqua', 'aquamarine',  'bisque', 'black',  'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'coral', 'cornflowerblue', 'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgrey', 'darkgreen', 'darkkhaki', 'darkmagenta', 'darkolivegreen']

# Graphe 1
pos = ([131, 352], [464, 315], [254, 211], [393, 346], [381, 432], [343,  98], [298, 326], [187, 475], [245, 407], [483, 212], [365, 216], [149, 198])
graph = [[2, 7], [3], [5, 8], [10], [3, 1], [], [3, 10, 4], [], [], [10, 1], [3, 1], [0]]
col_index = [k for k in range(0,12)]

# Graphe 2
graph2 = [[2], [], [4], [1], [6], [3], [7], [5]]
pos2 = [[100, 200], [450, 200], [150, 200], [400, 200], [200, 200], [350, 200], [250, 200], [300, 200]]
col_index2 = [k for k in range(0, 8)]

def color_generator():
	"""
	Fonction permettant de générer une couleur aléatoire au format héxadécimal ("#FFFFFF")
	"""
	r, g, b = randint(0,255), randint(0,255), randint(0,255)
    #gris = 0.2125*r+0.7154*g+0.0721*b
	return (f"#{r:02x}{g:02x}{b:02x}", [r,g,b])

def generate_graphe_carre(M, N):
	"""
	Algorithme permettant de créer tous les outils permettant de définir un graphe carré, réseau carré, fait appel à la théorie de 
	la percolation.
	"""
	col_index1 = [[10*j+i for i in range(M)] for j in range(N)]
	pos1 = [[(int((i+1/2)*w/M), int((j+1/2)*h/M)) for i in range(M)] for j in range(N)]
	graph1 = dict()

	for i in range(M):
		for j in range(N):
			graph1[(i,j)] = []
			p, q = random(), random()
			if j != N-1:
				if p <= 0.4:
					graph1[(i,j)].append((i, j+1)) 
			if i != M-1:
				if q <= 0.4:
					graph1[(i,j)].append((i+1, j))
	return graph1, pos1, col_index1


class Graph:
	"""
	Classe permettant de repésenter les graphes sur Tkinter en vue 2d. La repésentation en machine 
	se fait via une liste d'adjacence
	"""
	def __init__(self, list_adjacence, pos : list, col_index : list, n : int):
		self.__nb_vertex = n 
		self.__list_adjacence = list_adjacence
		self.__pos = pos
		self.__col_index = col_index
		self.__appel = []
		self.__appel_carre = []

	def draw(self, can):
		"""
		Fonction permettant de dessiner un graphe dont les sommets sont étiquetés par des indices
		"""
		for e in can.find_all():
			can.delete(e)
		for i in range(self.__nb_vertex):
			for j in self.__list_adjacence[i]:
			 # sucs de i a j
					can.create_line(self.__pos[i][0], self.__pos[i][1], self.__pos[j][0], self.__pos[j][1])
		for i in range(self.__nb_vertex):
			x, y = self.__pos[i]
			can.create_oval(x-8, y-8, x+8, y+8, fill=COLORS[self.__col_index[i]])
			can.create_text(x-12,y,text=f"{i}")

	def draw_carre(self, can):
		"""
		Fonction permettant de dessiner un graphe dont les sommets sont étiquetés par des couples d'indices
		"""
		for e in can.find_all():
			can.delete(e)
		pasx = w/(4*sqrt(self.__nb_vertex))
		pasy = h/(4*sqrt(self.__nb_vertex))
		for (i,j) in self.__list_adjacence.keys():
			x, y = self.__pos[i][j]
			can.create_oval(x-pasx, y-pasy, x+pasx, y+pasy, fill=COLORS[self.__col_index[i][j] % len(COLORS)])
		for (i,j) in self.__list_adjacence.keys():
			for (k,p) in self.__list_adjacence[(i,j)]:
				can.create_line(self.__pos[i][j][0], self.__pos[i][j][1], self.__pos[k][p][0], self.__pos[k][p][1])

	def min_local_carre(self, i,j):
		"""
		Fonction permettant de déterminer la valeur de la composante connexe locale d'un sommet d'un graphe étiqueté par des couples d'indices
		"""
		if (i,j) not in self.__appel_carre:
			self.__appel_carre.append((i,j))

		minimum = self.__col_index[i][j]
		# Trouver tous les sommets voisins
		sommets = self.__list_adjacence[(i,j)]
		
		for (k,p) in self.__list_adjacence.keys():
			if (i,j) in self.__list_adjacence[(k,p)]:
				sommets.append((k,p))

		for (k,p) in sommets:
			if minimum > self.__col_index[k][p] :
				minimum = self.__col_index[k][p]

		self.__col_index[i][j] = minimum
		for (k,p) in sommets:
			self.__col_index[k][p] = self.__col_index[i][j]
			
			if (k,p) not in self.__appel_carre:
				self.min_local_carre(k,p)

	def composantes_connexes_carre(self):
		"""
		Fonction permettant de trouver les composantes connexes d'un graphe dont les sommets sont étiquetés par des couples d'indices
		"""
		for (i,j) in self.__list_adjacence.keys():
			self.min_local_carre(i,j)

	def min_local(self, i):
		"""
		Fonction permettant de déterminer la valeur de la composante connexe locale d'un sommet d'un graphe étiqueté par des indices
		"""
		if i not in self.__appel:
			self.__appel.append(i)
		minimum = self.__col_index[i]
		# Trouver tous les sommets voisins
		sommets = self.__list_adjacence[i]
		"""
		for k in range(self.__nb_vertex):
			if i in self.__list_adjacence[k]:
				sommets.append(k)
		"""
		for s in sommets:
			if minimum > self.__col_index[s]:
				minimum = self.__col_index[s]


		self.__col_index[i] = minimum
		for s in sommets:
			self.__col_index[s] = self.__col_index[i]
			if s not in self.__appel:
				self.min_local(s)

	def composantes_connexes(self):
		"""
		Fonction permettant de déterminer les composantes connexes d'un graphe étiqueté par des indices
		"""
		for i in range(self.__nb_vertex):
			self.min_local(i)


"""
Question 3) Il suffit de parcourir la liste des sommets et de leur appliquer à tous la fonction min_local en s'assurant que
la fonction min_local soit récursive pour que la localité des valeurs des composantes connexes devienne globale.
Question 4) L'algorithme fonctionne bien, il suffit de définir en amont des valeurs toutes différentes de composantes connexes
grâce à la bijection de R^2 dans R : 10x + y, ensuite après application, les composantes connexes sont bien reperés graphiquement 
car les couleurs sont déterminés modulo le nombre de couleurs disponibles dans COLORS
Question 5) A p = 0.5, on obtient une grande composante connexe, cela s'explique par la théorie de la percolation bien développée 
dans la vidéo d'Hugo Dominil-Copin.
"""

if __name__ == "__main__":
	M = 30
	N = 30

	graph1, pos1, col_index1 = generate_graphe_carre(M,N)
	g = Graph(graph1, pos1, col_index1, M*N)
	can = Canvas(content, width=w, height=h, bg="white")
	content.grid(row = 0, column = 0)
	can.grid(row = 0, column = 0)
	g.draw_carre(can)
	g.composantes_connexes_carre()
	g.draw_carre(can)
	root.mainloop()