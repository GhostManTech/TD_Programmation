"""
Name ......: main.py
Role ......: archery

Author ....: Max BOILLEDIEU
Version ...: V1.0.0 10/04/2024

Launch ....:
python3 main.py
"""

from tkinter import *
from tkinter import ttk
from random import randint, sample, choice

root = Tk()
content = Frame(root)
w = 400
h = 500
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - w) // 2 
y = (screen_height - h) // 2
root.title("Tir à l'arc")
root.geometry(f"{w}x{h}+{x}+{y}")
root.resizable(width = False, height = False)


def dist(x,y):
	"""
	Fonction calculant la norme au carré d'un vecteur en 2d
	"""
	return x*x + y*y

class Archery:
	"""
	Classe principale permettant de jouer au tir à l'arc
	"""
	def __init__(self, center : int, rayon : int):
		self.__rayon = rayon
		self.__center = center
		self.__score = 0
		self.__nb_shoot = 0
		self.__pos_target = (randint(self.__center-5*self.__rayon+10,self.__center+5*self.__rayon+10), randint(self.__center-5*self.__rayon+10,self.__center+5*self.__rayon+10)) 
		self.__pos_shoots = []
		self.__is_center = True if dist(self.__pos_target[0]-self.__center, self.__pos_target[1]-self.__center) <= (self.__rayon+10)**2 else False

	def score(self, x : int, y : int):
		"""
		Fonction permettant de calculer le score total
		"""
		r = 10
		for k in range(6):
			r += self.__rayon
			d = dist(self.__center-x, self.__center-y)
			if d <= r**2 and d >= (r-self.__rayon)**2:
				self.__score += 6-k

	def draw_score(self):
		"""
		Fonction permettant d'afficher le score
		"""
		if self.__score <= 1:
			displayScore.config(text=f"Score : {self.__score} point")
		else:
			displayScore.config(text=f"Score : {self.__score} points")

	def draw_shoots(self):
		"""
		Fonction permettant de tracer les points d'impact
		"""
		for (x,y) in self.__pos_shoots:
			can.create_oval(x-5,y-5,x+5,y+5, outline="black", fill="black")

	def shoot(self, *args):
		"""
		Fonction permettant de tirer si on appuie sur la touche f du clavier, limite : 5 tirs
		"""
		if self.__nb_shoot < 5 :
			self.__nb_shoot += 1
			self.score(self.__pos_target[0],self.__pos_target[1])
			self.__pos_shoots.append((self.__pos_target[0],self.__pos_target[1]))
			self.draw_score()
			self.draw_shoots()

	def fire(self):
		"""
		Fonction permettant de tirer cinq fois d'affilée
		"""
		boutonTir["state"] = DISABLED
		for k in range(5-self.__nb_shoot):
			x = randint(0,2*self.__center)
			y = randint(0,2*self.__center)
			self.score(x,y)
			self.__nb_shoot += 1
			self.__pos_shoots.append((x,y))
		self.draw_score()
		self.draw_shoots()

	def draw_circle(self,r : int, color1 : str, color2 : str) -> None:
		"""
		Fonction permettant de dessiner un cercle (centré au milieu) sur le canvas
		"""
		can.create_oval(self.__center-r, self.__center-r, self.__center+r, self.__center+r, outline=color1, fill=color2, width=1)

	def draw_cible(self):
		"""
		Fonction permettant de tracer la cible
		"""
		r = self.__center - 10
		for k in range(4):
			self.draw_circle(r, "red", "white")
			r -= self.__rayon
		self.draw_circle(r, "white", "red")
		r -= self.__rayon
		self.draw_circle(r, "red", "white")

	def draw_text(self):
		"""
		Fonction permettant d'afficher les points sur la cible
		"""
		r = self.__rayon
		for k in range(1,7,1):
			if k != 5:
				can.create_text(self.__center,r, text=f"{k}", font=("Times","20"),fill="red")
			else:
				can.create_text(self.__center,r,text=f"{k}", font=("Times", "20"), fill="ivory")
			r += self.__rayon

	def draw_lines(self):
		"""
		Fonction permettant d'afficher le pointeur
		"""
		can.create_line(self.__pos_target[0],self.__pos_target[1], self.__pos_target[0],10,fill="red", width=1)
		can.create_line(self.__pos_target[0],self.__pos_target[1], self.__center*2-10,self.__pos_target[1],fill="red", width=1)
		can.create_line(self.__pos_target[0],self.__pos_target[1], self.__pos_target[0],self.__center*2-10,fill="red", width=1)
		can.create_line(self.__pos_target[0],self.__pos_target[1], 10,self.__pos_target[1],fill="red", width=1)

	def move_target(self):
		"""
		Fonction initiale jusqu'à la question n°4 permettant de faire bouger le pointeur
		"""
		self.draw_cible()
		self.draw_text()
		moves = [(0,+5), (0,-5),(-5,0),(+5,0)]
		move = choice(moves)
		
		if dist(self.__pos_target[0]+move[0]-self.__center, self.__pos_target[1]+move[1]-self.__center) <= (6*self.__rayon+10)**2:
			self.__pos_target = (self.__pos_target[0] + move[0], self.__pos_target[1] + move[1])
		else:
			self.__pos_target = (self.__pos_target[0] - move[0], self.__pos_target[1] - move[1])
		
		self.draw_lines()
		self.draw_shoots()

	def move_target_2(self):
		"""
		Question n°5 : Faire en sorte que le pointeur aille rapidement vers le centre et en sorte rapidement de manière cyclique
		"""
		self.draw_cible()
		self.draw_text()
		self.__is_center = dist(self.__pos_target[0]-self.__center, self.__pos_target[1]-self.__center) <= (2*self.__rayon+10)**2
		move = ()
		if self.__is_center:
			moves = [(30,30),(-30,-30),(-30,30),(+30,-30)]
			move = choice(moves)
		else:
			if self.__pos_target[0] <= self.__center and self.__pos_target[1] <= self.__center:
				move = (5,5)
			elif self.__pos_target[0] <= self.__center and self.__pos_target[1] > self.__center:
				move = (5,-5)
			elif self.__pos_target[0] > self.__center and self.__pos_target[1] > self.__center:
				move = (-5,-5)
			else:
				move = (-5,5)
			
		if dist(self.__pos_target[0]+move[0]-self.__center, self.__pos_target[1]+move[1]-self.__center) <= (6*self.__rayon+10)**2:
			self.__pos_target = (self.__pos_target[0] + move[0], self.__pos_target[1] + move[1])
		else:
			self.__pos_target = (self.__pos_target[0] - move[0], self.__pos_target[1] - move[1])
		
		self.draw_lines()
		self.draw_shoots()
	
	def target(self):
		"""
		Fonction permettant de créer la boucle de déplacement du viseur
		"""
		self.move_target_2()
		root.after(100,self.target)


can = Canvas(content, width=w, height=w, bg="red")

# Définition du jeu
archery = Archery(w//2,30)
archery.draw_cible()
archery.draw_text()
archery.draw_lines()
archery.target()

# Objets graphiques
boutonTir = ttk.Button(content, text="Feu !", command=archery.fire)
boutonQuitter = ttk.Button(content, text="Quitte", command=root.destroy)
content.grid(row = 0, column = 0)
displayScore = ttk.Label(content, text=f"Score : 0 Point")
displayScore.grid(row = 1, column = 0)
can.grid(row = 0, column = 0)
boutonTir.grid(row = 1, column = 0, sticky=W)
boutonQuitter.grid(row = 1,column =0, sticky=E)
root.bind("<f>", archery.shoot)

# BOucle évenementielle
root.mainloop()