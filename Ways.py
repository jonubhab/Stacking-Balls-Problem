import math
A=[7,7,7,7,7,7,7,6]
n=len(A)    #4
A.append(0)
print(sum(A))
P=math.factorial(sum(A))

#for k in range(1,n+1): #4 times
for k in range(1,n+1):
    for j in range(k,n+1): #4 3 2 1
        for i in range(A[j]+1,A[j-1]+1):
            t=(A[k-1]-k+j-i+1)**2
            P/=t

print(P*100)