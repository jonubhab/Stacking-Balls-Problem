#Actual Parameters
N=10         #Number of balls
R=0.5       #Radius

#Assumed Parameters
H=2*R   #Drop Height (effects only when Dynamic=False) (Suggested Value = (2+N*2**0.5)*R)
g=9.81  #Acceleration due to Gravity
T=(2.1*H/g)**0.5   #Time Interval at which ball will fall (effects only when Stable=False)

#Simulation Parameters
dt=1/100
Animation=False      #Shows Animation or direct result
Scale=100           #Number of pixels making up one metre
Time=True          #Shows Time
Text=True          #Prints status(Turning it off with Animation=False might test your patience)

#Modules
import pymunk as phy
import Simulation as s
from Tools import *
import math
from Data import *
import 04_Permute as prm


#Initializing Simulation
S=phy.Space()
sim=s.Simulation(S)
C=Cartesian(metre=Scale)
S.gravity = (0.0, C.metre(g))
c=Timer()
t=c.lap()
n=Counter()
balls=[]
Running=True



#Defining your balls
class ball():

    def __init__(self):
        global n
        if n.val>0:
            balls[n.val-1].body.body_type = phy.Body.STATIC
        if n.val != N:
            n += 1
            self.body = phy.Body(1,math.inf)
            self.body.position = C.P(next(P), next(P)+H)
            shape = phy.Circle(self.body, C.metre(R))  
            shape.friction=0.1
            shape.elasticity=0
            S.add(self.body, shape)
            balls.append(self)
            self.id=n.val
            if Text: print(f"{c.time()} : Added Ball #{self.id}")

    def position(self):
        return C.revert(*self.body.position)

#Some Sorcery
def shady_stuff():
    global file,img,H,P
    P=prm.tableau(N,R)
    code,kw=encrypt(N=N, R=R, H=H, T=T, g=g)
    file = Data(code,kw)
    img=code
    save(file)
    with open(file,'a') as f:
        f.write("\n--- BALL POSITIONS ---\n")
    s.Simulation.dt=dt

def wedge():
    l=N*H
    line1=phy.Segment(S.static_body,C.P(-l,l),C.P(0,0),1)
    line1.color=(0,0,0,255)
    line2=phy.Segment(S.static_body,C.P(0,0),C.P(l,l),1)
    line2.color = (0, 0, 0,255)
    line1.friction=line2.friction=1
    S.add(line1,line2)

def touche():
    global Running
    c.tick()
    if Animation and Time: sim.display(next(t))
    else: next(t)
    if n.val<N:
        if 0<= c.t.val-T*n.val < dt:ball()
    elif c.t.val>(N+1)*T:
        balls[-1].body.body_type = phy.Body.STATIC
        Running=False

def hellyeah():
    return Running

#Real Code
shady_stuff()
wedge()
ball()



c.reset()
if Animation:
    sim.show()
    sim.simulate(touche, hellyeah)
else:
    sim.blind(touche, hellyeah)
    sim.show()
saveShape(balls,file)
if Time: sim.hold(text="Time: " + c.time(),filename=img)

else: sim.hold(filename=img)

