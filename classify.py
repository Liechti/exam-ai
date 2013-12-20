import nltk
from nltk import word_tokenize
from nltk.corpus import wordnet as wn

CATEGORY=7

class Question:
	def __init__(self,Question):
		self.a=Question['a']
		self.b=Question['b']
		self.c=Question['c']
		self.d=Question['d']
		self.article=Question['article']
		self.question=Question['question']
		self.answer='N'
		self.category=[0]*CATEGORY
		
	def test(self):
		self.answer='B'
		return self.answer
	
	def cat_1(self,w):
		main=wn.Synset('main.s.01').lemma_names
		idea=wn.Synset('idea.01')+wn.Synset('purpose.n.01').lemma_names+wn.Synset ('theme.n.02').lemma_names+wn.Synset ('subject.n.02').lemma_names
		
		for v in main:
			if v in w:
				index = w.index(v)
				for v in idea:
					if w(index+1) == v:
						self.caegory[1] = 1
						return None
		return None
	
	def cat_2(self,w):
		true=wn.Synset('true.1.01')
				
		for v in true:
			if v in w:
				self.category[2] = 1
				return None
		return None
				
	def cat_3(self):
		pass
	#need to find a way to specify bold face words
	
	def cat_4(self,w):
		who=['who','Who']
		for v in who:
			if v in w:
				self.category[4] = 1
				return None
		return None
	
	def cat_5(self,w):
		why=['why','Why']
		for v in why:
			if v in w:
				self.category[5] = 1
				return None
		return None
	
	def cat_6(self,w):
		what=['what','What','which','Which']
		for v in what:
			if v in w:
				self.category[6] = 1
				return None
		return None
	
	def classifier(self):
		w=word_tokenize(self.question)
		self.cat_1(w)
		self.cat_2(w)
		self.cat_3(w)
		self.cat_4(w)
		self.cat_5(w)
		self.cat_6(w)
		
		if self.category == [0]*CATEGORY:
			self.category[0] = 1
			
		return None




