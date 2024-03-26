import random

f = open("frenchssaccent.dic", "r")
letters = "abcdefghijklmnopqrstuvwxyz"
words = []
for ligne in f:
	words.append(ligne[0:len(ligne)-1])
f.close()

def select_letters(n):
	l = []
	for k in range(n):
		l.append(random.choice(letters))
	return l

def transform_list_to_dict(l):
	n = len(l)
	d = dict()
	for k in range(n):
		if l[k] not in d:
			d[l[k]] = 1
		else:
			d[l[k]] += 1
	return d

def contains(l1, l2):
	d1 = transform_list_to_dict(l1)
	d2 = transform_list_to_dict(l2)
	cond = True
	for k,v in d2.items():
		if k in d1.keys():
			if d1[k] == v:
				cond = True
			else:
				return False
		else:
			return False
	return True

	

def seek_longest_word(l : list):
	n = len(l)
	m = 0
	word = ""
	for w in words:
		if contains(l,w) and m < len(w):
			m = len(w)
			word = w

	return word




if __name__ == "__main__":
	l = select_letters(8)
	l = ['h', 'n', 'g', 'r', 'a', 'x', 'b', 'r']
	print(transform_list_to_dict(l))
	print(seek_longest_word(l))



