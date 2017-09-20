import numpy
from math import log

class VectorSpaceModel():
	def __init__(self):
		self.__words={}
		self.__vectors=[]
		self.__wordcount=0
		self.__doccount=0

	def processDocuments(self,documents): #as of now documents is assumed to be a list of words
		for document in documents:
			for word in document:
				if word not in self.__words:
					self.__words[word]=self.__wordcount
					self.__wordcount+=1

		self.__vectors=numpy.zeros((len(documents),self.__wordcount))
		
		for document in documents:
			self.__addDocument(document)

		idf=numpy.zeros((self.__wordcount))
		
		#first calculates df
		for word in self.__words:
			x=self.__words[word]
			for i in range(len(self.__vectors)):
				if self.__vectors[i][x]!=0:
					idf[x]+=1

		#calculates idf of all words as log(n/df)
		for i in range(self.__wordcount):
			idf[i]=log(len(self.__vectors)/idf[i])

		
		#assigns score as (1 + log(tf))*(idf)
		for i in range(len(self.__vectors)):
			for j in range(self.__wordcount):
				if self.__vectors[i][j]!=0:
					self.__vectors[i][j]=(1+log(self.__vectors[i][j]))*(idf[j])
		



	def __addDocument(self,document):
		for word in document:
			self.__vectors[self.__doccount][self.__words[word]]+=1
		self.__doccount+=1

	def calcSimilarity(self,query):
		pass

def main():
	pass

if __name__=="__main__":
	main()