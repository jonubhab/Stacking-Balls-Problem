import random as r
import numpy as np

def permute(N):
    L=[i for i in range(1,N+1)]
    r.shuffle(L)
    return L



def tableau(N,R):
    L=permute(N)
    P=[[] for i in range(N)]
    for n in L:
        for i in range(N):
            if len(P[i])==0 or P[i][-1]<n:
                P[i].append(n)
                x=np.array([(2*i+1)*R,(2*len(P[i])-1)*R])
                s=1/2**0.5
                X=np.array([[s,-s],[s,s]])@x
                yield X[0]
                yield X[1]
                break
            else:
                P[i],n=bump(n,P[i])


def bump(n,seq):
    i=0
    while n>seq[i]: i+=1
    v=seq[i]
    seq[i]=n
    return seq,v
