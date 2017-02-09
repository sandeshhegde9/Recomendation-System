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
	#print ab_e,u,len(u),len(u[0])
	
	
	#calculate eigen valus and eigen vectors for a*a' and retain only k princliple values and vectors. sort them in decsending order.
	ba_e,v=la.eigh(ba,eigvals=(len(ba)-500,len(ba)-1),eigvals_only=False)
	idx=ba_e.argsort()[::-1]
	v=v[:,idx]
	#print len(v),len(v[0])

	'''#get the eigen values and eigen vectors of a*a' and a'*a.
	ab_e, u=la.eig(ab)
	#retain only real part
	u=u.real
	ab_e=ab_e.real

	#sort it in descending order.
	idx=ab_e.argsort()[::-1]
	ab_e=ab_e[idx]
	u=u[:,idx]


	ba_e, v=la.eig(ba)
	#retain only real part
	v=v.real
	ba_e=ba_e.real

	#sort in descending order.i
	idx = ba_e.argsort()[::-1]   
	ba_e = ba_e[idx]
	v=v[:,idx]
	print u,ba_e,v'''

	#the matric s in svd is squre root of eigen values of a*a' or a'*a(both are equal).
	s=[math.sqrt(i) for i in ba_e]
	
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
	for i in a:
		count=0
		for j in i:
			if j!=0:
				count+=1
	
	#get svd of the matrix.
	U,S,V=SVD(a)

	#also we're gonna need a' for reconstruction.
	Vt=V.transpose()

	#Now take a user_id and reconstruct the rating matrix using the Decomposition.
	uid=raw_input("UID: ")
	while(uid!=0):
		row=a[users[uid]]
		j=np.dot(row,V)
		uid_rating=np.dot(j,Vt)
		er=0
		count=0
		#print users[uid]
		g=a[users[uid]]

		#Calculating Root Mean Square Error for the user.
		for i in range(len(g)):
			if g[i]!=0:
				er=er+((g[i]-uid_rating[i])**2)
				count+=1

		er=er/count

		er=math.sqrt(er)
		print er
		uid=raw_input("UID: ")

main()

