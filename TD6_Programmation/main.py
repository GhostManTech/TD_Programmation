"""
Name ......: main.py
Role ......: graph

Author ....: Max BOILLEDIEU
Version ...: V1.0.0 15/05/2024

Launch ....:
python3 main.py
"""

from tkinter import *
from tkinter import ttk
import numpy as np
from math import sqrt, sin, atan, cos, acos, pi
from random import randint, sample, choice, random

root = Tk()
content = Frame(root)
w = 720
h = 480
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - w) // 2 
y = (screen_height - h) // 2
root.title("Dessin de graphes")
root.geometry(f"{w}x{h}+{x}+{y}")
root.resizable(width = False, height = False)

"""
Réponse aux questions : 
***********************

1) On crée une classe Graph permettant de stocker via une liste d'adjacence et représenter le graphe en 2d sur une fenêtre Tkinter.

2) On crée une méthode ressort dans la classe Graph qui agit sur les sommets avec des forces de rappel de ressort quand les sommets
sont interconnectés.

3) On applique une force barycentrique à l'ensemble des sommets pour les recentrer à chaque appel de la fonction f. Si la variation des
positions n'est pas très grande, le graphe est censé rester dans la fenêtre.

4) Pour stabiliser le graphe après application des forces de rappel, on rajoute une interaction électrostatique pour 
atténuer l'effet de la force de rappel des ressorts.

5) Il faut tester les intersections entre les différents sommets et déplacer les sommets en fonction.

"""
class Graph:
	def __init__(self, list_adjacence : list, n : int):
		self.__tau = 0.1
		self.__k = 1
		self.__K = 3000
		self.__r0 = 100
		self.__nb_vertex = n 
		self.__list_adjacence = list(list_adjacence)
		
		# Alétoire polaire
		self.__pos = [[0,0] for _ in range(self.__nb_vertex)]
		for i in range(self.__nb_vertex):
			r = randint(0, 100)
			theta = random()*2*pi
			self.__pos[i] = [w//2+r*cos(theta), h//2+r*sin(theta)]
		

		#self.__pos = [[w//2-50, h//2], [w//2+50, h//2]]
		self.__dist = [[-1 for _ in range(self.__nb_vertex)] for _ in range(self.__nb_vertex)]
		self.__vit = np.array([((random()-0.5)*10, (random()-0.5)*10) for i in range(self.__nb_vertex)])
		self.__barycentre = (sum(self.__pos[i][0] for i in range(self.__nb_vertex))/self.__nb_vertex, sum(self.__pos[i][1] for i in range(self.__nb_vertex))/self.__nb_vertex)

	def draw(self):
		can.create_rectangle(0,0,w,h, fill="white")
		for i in range(self.__nb_vertex):
			for j in self.__list_adjacence[i]: 
				can.create_line(self.__pos[i][0], self.__pos[i][1], self.__pos[j][0], self.__pos[j][1])
		for k in range(self.__nb_vertex):
			can.create_oval(self.__pos[k][0]-8,self.__pos[k][1]-8,self.__pos[k][0]+8,self.__pos[k][1]+8,fill="#f3e1d4")
			can.create_text(self.__pos[k][0],self.__pos[k][1], text=f"{k}", font=("Times", 10, "bold"), fill="black")

	def barycentre(self):
		self.__barycentre = (sum([self.__pos[i][0] for i in range(self.__nb_vertex)])/self.__nb_vertex, sum([self.__pos[i][1] for i in range(self.__nb_vertex)])/self.__nb_vertex)

	def ressort(self, *args):
		# Force de ressort
		for i in range(self.__nb_vertex):
			self.__vit[i][0] = 0
			self.__vit[i][1] = 0
			for j in range(self.__nb_vertex):
				if i != j:
					deltax = self.__pos[i][0]-self.__pos[j][0]
					deltay = self.__pos[i][1]-self.__pos[j][1]
					r = sqrt(deltax**2+deltay**2)
					cosinus = deltax/r
					sinus = deltay/r
					# Force électrostatique
					fx = self.__K*cosinus/(r**2)
					fy = self.__K*sinus/(r**2) 
					if j in self.__list_adjacence[i]:
						#Force de rappel du ressort
						fx -= self.__k*(r-self.__r0)*cosinus
						fy -= self.__k*(r-self.__r0)*sinus 

					self.__vit[j][0] -= fx*self.__tau
					self.__vit[j][1] -= fy*self.__tau
					self.__pos[j][0] += self.__tau*self.__vit[j][0]
					self.__pos[j][1] += self.__tau*self.__vit[j][1]
	
	
		self.barycentre()
		for k in range(self.__nb_vertex):
			self.__pos[k][0] = self.__pos[k][0] + w//2 - self.__barycentre[0]
			self.__pos[k][1] = self.__pos[k][1] + h//2 - self.__barycentre[1]
		self.draw()

	def ressort2(self, *args):
		for i in range(self.__nb_vertex):
			for j in self.__list_adjacence[i]:
				self.__vit[i][0] -= self.__k*(self.__pos[i][0]-self.__l0)*self.__tau*sin(self.angle(i, j))
				self.__vit[i][1] -= self.__k*(self.__pos[i][1]-self.__l0)*self.__tau*cos(self.angle(i, j))
				self.__pos[i][0] += self.__tau*self.__vit[i][0]
				self.__pos[i][1] += self.__tau*self.__vit[i][1]
				self.draw()

g1 = [[2, 7, 3], [3, 4, 9, 10], [5, 8, 0], [10, 1, 4, 6, 0], 
[3, 1, 6], [2], [3, 10, 4], [0], [2], [10, 1], [3, 1, 6, 9]]
g2 = [[1,2,3],[0,2,3],[0,1,3],[0,1,2]]
g3 = [[1],[0]]
g = Graph(g1,11)


can = Canvas(content, width=w, height=h, bg="white")
content.grid(row = 0, column = 0)
can.grid(row = 0, column = 0)
g.draw()
root.bind('<f>', g.ressort)
root.mainloop()