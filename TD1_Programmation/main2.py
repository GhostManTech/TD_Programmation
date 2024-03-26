import random

f = open("frenchssaccent.dic", "r")
letters = "abcdefghijklmnopqrstuvwxyz"
words = []
for ligne in f:
	words.append(ligne[0:len(ligne)-1])
f.close()

SCORE = {'?' : 0, 'a' : 1, 'e' : 1, 'i' : 1, 'l' : 1, 'n' : 1, 'o' : 1,'r' : 1, 's' : 1, 't' : 1, 'u' : 1, 'd' : 2, 'g' : 2, 'm' :2, 'b' : 3, 'c' : 3, 'p' : 3, 'f' : 4, 'h' : 4, 'v' : 4, 'j' : 8, 'q' : 8, 'k' : 10, 'w' : 10, 'x' : 10, 'y' : 10, 'z' : 10}

def test_word(w,t):
	n = len(w)
	index = -1
	t = list(t)
	for k in range(n):
		m = len(t)
		for i in range(m):
			if w[k] == t[i]:
				index = i
		if index != -1: 
			del t[index]
			index = -1
		else: 
			return False
	return True

def test_word2(w,t):
	t = list(t) # Copie 
	for l in w:
		if l in t:
			t.remove(l)
		else:
			if '?' in t:
				t.remove('?')
			else:
				return False
	return True

def score(w):
	s = 0
	for l in w:
		s +=SCORE[l]
	return s



def seek_longest_word(w,l : list):
	m = 0
	word = ""
	for w in words:
		if test_word2(w,l) and m < len(w):
			m = len(w)
			word = w 
	return word

def max_score(t,w):
	m = 0
	word = ""
	for w in words:
		if test_word2(w,l) and m < score(w):
			m = score(w)
			word = w 
	return word, m

if __name__ == "__main__":
	l = ['h', 'n', '?', 'r', 'a', 'x', 'b', 'r']
	t = list("svucflia")
	print(seek_longest_word(words,t))
	print(max_score(t, words))