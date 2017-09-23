import numpy
import heapq
from math import log,sqrt

class VectorSpaceModel():
	def __init__(self):
		self.__words={}
		self.__vectors=[]
		self.__ids=[]
		self.__wordcount=0
		self.__doccount=0

	def processDocuments(self,documents): #document is a list of tuples - 1st element contains id, 2nd element contains document as a list of words
		for document in documents:
			for word in document[1]:
				if word not in self.__words:
					self.__words[word]=self.__wordcount
					self.__wordcount+=1

		print(len(documents),self.__wordcount)
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
		
		#Convert each vector to unit vector
		for i in range(len(self.__vectors)):
			l=0
			l=sum(self.__vectors[i]*self.__vectors[i])
			l=sqrt(l)
			if l!=0:
				self.__vectors[i]/=l


	def __addDocument(self,document):
		self.__ids.append(document[0])
		for word in document[1]:
			self.__vectors[self.__doccount][self.__words[word]]+=1
		self.__doccount+=1

	def getSimilarDocuments(self,query,k):
		vector=numpy.zeros((self.__wordcount))
		for word in query:
			if word in self.__words:
				vector[self.__words[word]]+=1

		for i in range(self.__wordcount):
			if vector[i]!=0:
				vector[i]=1+log(vector[i])

		h=[]
		for i in range(self.__doccount):
			h.append((-1*self.__calcCosineSimilarity(vector,i),i))

		heapq.heapify(h)

		ans=[]
		for i in range(k):
			ans.append(heapq.heappop(h)[1])

		return ans

	def __calcCosineSimilarity(self,query,id):
		return query.dot(self.__vectors[id])
		

def main():
	pass

if __name__=="__main__":
	main()