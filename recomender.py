import math
import numpy as np
from scipy import linalg as la 
#Calculates U,S and V (Components of svd of a matrix.
def SVD(a):

	#Calculate traspose of the matrix(A').
	b=a.transpose()
	#print b

	#Get A*A' and A'*A.
	ab=np.dot(a,b)
	ba=np.dot(b,a)

	#calculate eigen valus and eigen vectors for a*a' and retain only k princliple values and vectors. sort them in decsending order.
	ab_e,u=la.eigh(ab,eigvals=(len(ab)-500,len(ab)-1),eigvals_only=False)

	idx=ab_e.argsort()[::-1]
	ab_e=ab_e[idx]
	u=u[:,idx]
	for i in range(len(u)):
		for j in range(len(u[0])):
			u[i][j]=round(u[i][j],2)
	#print ab_e,u,len(u),len(u[0])
	
	
	#calculate eigen valus and eigen vectors for a*a' and retain only k princliple values and vectors. sort them in decsending order.
	ba_e,v=la.eigh(ba,eigvals=(len(ba)-500,len(ba)-1),eigvals_only=False)
	idx=ba_e.argsort()[::-1]
	v=v[:,idx]
	for i in range(len(v)):
		for j in range(len(v[0])):
			v[i][j]=round(v[i][j],2)

	#print len(v),len(v[0])

	#the matric s in svd is squre root of eigen values of a*a' or a'*a(both are equal).
	s=[round(math.sqrt(i),2) for i in ba_e]
	
	return u,s,v


def main():
	f1=open('u.data')
	users={}
	movies={}
	index1=0
	index2=0
	a=np.array([[0 for row in range(1983)] for col in range(944)])
	#print len(a),len(a[0])
	f1.readline()
	
	#reading the file content into a matrix.
	for line in f1:
		line=line.strip()
		line=line.split('\t')
		if line[1] not in movies and line[0] not in users:
			movies[line[1]]=index1
			index1+=1
			users[line[0]]=index2
			index2+=1
			a[users[line[0]]][movies[line[1]]]=float(line[2])
		elif line[1] in movies and line[0] not in users:
			users[line[0]]=index2
			index2+=1
			a[users[line[0]]][movies[line[1]]]=float(line[2])
		elif line[0] in users and line[1] not in movies:
			movies[line[1]]=index1
			index1+=1
			a[users[line[0]]][movies[line[1]]]=float(line[2])
	'''for i in a:
		count=0
		for j in i:
			if j!=0:
				count+=1'''
	
	#get svd of the matrix.
	U,S,V=SVD(a)

	#also we're gonna need a' for reconstruction.
	Vt=V.transpose()

	#Now take a user_id and reconstruct the rating matrix using the Decomposition.
	uid=raw_input("Enter UID: ")
	while(uid!=0):
		row=a[users[uid]]

		#To get the movies for recomendation, we compute user_row*V*Vt.
		#Then recomend movies with highest values.
		j=np.dot(row,V)
		uid_rating=np.dot(j,Vt)
	
		#Sorting the user_rating row.
		idx=uid_rating.argsort()[::-1]
		
		uid_rating=uid_rating[idx]
		movie=idx[0:20]

		#Check if the user has already seen the movie, if not then recomend it.(Max 5 movies)
		count=0
		for f in movie:
			for key in movies:
				if movies[key]==f:
					if not a[users[uid]][movies[key]]>0:
						if count<5:
							print "Recomended MovieID: ",key
							count+=1

		uid=raw_input("\n\nEnter UID: ")

main()

