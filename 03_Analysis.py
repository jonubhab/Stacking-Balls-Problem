import pymunk as phy
import Simulation as s
from Tools import Cartesian

file_path = f"Data/{input("File Name : ")}"


with open(file_path,'r') as f:
    for i,l in enumerate(f):
        if i==1: N=int(l[11:])
        if i==2:
            R=float(l[11:])
            break

def data():
    with open(file_path, 'r') as f:
        Data = []
        Read = False
        for l in f:
            l = l.strip()
            if Read: Data.append(l)
            if l == "--- BALL POSITIONS ---":
                Data=[]
                Read = True
            if l == "--- TRANSCRIPT ---":
                Data = Data[:-2]
                e = []
                for j in Data:
                    e.append(list(map(float, j[1:-1].strip().split(','))))
                yield e
                Data = []
                Read = False



n=1
d=data()

class Shape:
    def __init__(self,s):
        self.s=s
        self.n=1
        self.seq=[Sequence([i for i in range(N)])]#,self.ex)]

    def isSame(self,s):
        l,b= compare(self.s,s)
        if b :
            self.add(l)
        return b


    def add(self,l):
        self.n+=1
        f = True
        for j in self.seq:
            if j.isSame(l):
                f = False
                next(d)
                break
        if f: self.seq.append(Sequence(l))

    def display(self):
        print(self.s)
        print(f"Frequency: {self.n}")
        print(f"Probability: {self.n/n*100}%")
        print(f"No. of Sequences: {len(self.seq)}")
        if len(self.seq)>1:
            for k,i in enumerate(self.seq,1):
                print(f"\nSequence #{k}:",end=' ')
                i.display()



class Sequence:
    def __init__(self,l):
        self.l=l
        self.n=1

    def isSame(self,l):
        b=all([self.l[i]==l[i] for i in range(N)])
        if b: self.add()
        return b

    def add(self):
        self.n+=1

    def display(self):
        print(self.l)
        print(f"Frequency: {self.n}")


def compare(s1,s2,seq=False):
    l=[-1]*len(s1)
    for j,p1 in enumerate(s1):
        for k,p2 in enumerate(s2):
            if equal(p1,p2): l[j]=k
    if seq: return all(a <= b for a, b in zip(l[:-1], l[1:]))
    else: return l,all(-1 < b for b in l)

def equal(p1,p2):
    return ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**0.5 < 0.2*R




shape=[Shape(next(d))]
for i in d:
    if len(i) > 0:
        f = True
        for j in shape:
            if j.isSame(i):
                f = False
                break
        if f: shape.append(Shape(i))
        n += 1

print(f"No. of Shapes: {len(shape)}")
print("_"*50)
for k, i in enumerate(shape, 1):
    print(f"\nShape #{k}:", end=' ')
    i.display()
    print("_" * 50)



def ball(pos,S,C):
    body = phy.Body()
    body.position = C.P(*pos)  # 2
    shape = phy.Circle(body, C.metre(R))
    S.add(body, shape)
    body.body_type = phy.Body.STATIC

def wedge(S,C):
    l=2*N*R
    line1=phy.Segment(S.static_body,C.P(-l,l),C.P(0,0),1)
    line1.color=(0,0,0,255)
    line2=phy.Segment(S.static_body,C.P(0,0),C.P(l,l),1)
    line2.color = (0, 0, 0,255)
    S.add(line1,line2)

while True:
    i=int(input("Enter shape to view (0-Exit) : "))
    if i==0: break
    S = phy.Space()
    sim = s.Simulation(S)
    C = Cartesian()
    wedge(S,C)
    for pos in shape[i-1].s:
        ball(pos,S,C)
    sim.show()
    sim.hold()

