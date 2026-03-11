#Actual Parameters
N=5         #Number of balls
R=1       #Radius

#Assumptions
Fix=True        #Balls get fixed in their stable position.
Stable=True    #Ball drops only when all the balls got stable.
Infinite=True  #Wedge is Infinite
Rotate=False    #Ball Rotates
Local=False      #Ball reaches only the nearest local energy minima upon touching other balls
Dynamic=False   #Drop Area depends on existing shape
Gaussian=False   #Ball Drop is normalized over drop area
Hypothetic=True    #Probability of getting a shape is directly proportional to the square of the number of ways to approach it.

#Assumed Parameters
A=2*(N-1)*R*2**0.5   #Drop Area (effects only when Dynamic=False) (Suggested Value = 2*(N-1)*R*2**0.5)
H=(2+N*2**0.5)*R   #Drop Height (effects only when Dynamic=False) (Suggested Value = (2+N*2**0.5)*R)
T=0.1   #Time Interval at which ball will fall (effects only when Stable=False)
W=4     #Height of Wedge (effects only when Infinite=False)
g=9.81  #Acceleration due to Gravity
M=1     #Mass
Ew=0    #Coefficient of Restitution between Wedge and Ball
Eb=0    #Coefficient of Restitution between Balls
Fw=0    #Coefficient of Friction between Wedge and Ball
Fb=0    #Coefficient of Friction between Balls

#Simulation Parameters
dt=1/100             #Time Interval at which positions are updated
dv=0.1              #Maximum Velocity for stability (Suggested Value = 0.5*R**0.5)
dF=M*dv*dt          #Maximum Force for stability
st=2                #Time taken in account to confirm stability
Animation=True      #Shows Animation or direct result
Scale=50           #Number of pixels making up one metre
Time=True          #Shows Time
Text=True          #Prints status(Turning it off with Animation=False might test your patience)
Seed=None           #Turn in value to reproduce result

#Modules
import pymunk as phy
import random as r
import Simulation as s
from Tools import *
import math
from functools import partial
from Data import *
from scipy.stats import truncnorm
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
        if n.val != N:
            n += 1
            if not Rotate: self.body = phy.Body(M,math.inf)
            else: self.body = phy.Body(M)
            if Hypothetic:
                self.body.position = C.P(next(P)+(r.random()*2.8-1.4)*R, H)
            elif Gaussian:
                self.body.position = C.P(truncnorm(-2, 2, loc=0, scale=(Ar-Al)/4).rvs(), H)
            else: self.body.position = C.P(r.random() * (Ar-Al) + Al, H) 
            shape = phy.Circle(self.body, C.metre(R))  
            shape.friction = Fb
            shape.elasticity = Eb
            shape.collision_type = 1
            S.add(self.body, shape)
            balls.append(self)
            self.s=[self.stability() for i in range(int(st/dt))]
            for i,s in enumerate(self.s):
                for j in range(i): next(s)
            self.id=n.val
            if Text: print(f"{c.time()} : Added Ball #{self.id}")

    def stability(self):
        while True:
            s=self.body.velocity.length < C.metre(dv) and self.body.force.length < C.metre(dF)
            for i in range(len(self.s)): yield s


    def isStable(self):
        if self.body.body_type is phy.Body.STATIC: return True
        if self.body.position[1]<C.P(y=H)+5: return False
        s= all(list(map(next,self.s)))
        for i in range(len(self.s)-1): map(next,self.s)
        if Fix:
            if s:
                self.pos=C.revert(*self.body.position)
                if Text: print(f"{c.time()} : Ball #{self.id} stabilized at {self.pos}")
                self.body.body_type=phy.Body.STATIC
        return s

    def inBoundary(self):
        if self.body.body_type is phy.Body.STATIC: return True
        pos=self.body.position
        pos=C.revert(*pos)
        b = pos[1]>=pos[0]
        if (not b) and Text: print(f"{c.time()} : Ball #{self.id} fell off from the wedge.")
        return b

    def position(self):
        if self.body.body_type is phy.Body.STATIC: return self.pos
        return C.revert(*self.body.position)

#Some Sorcery
def shady_stuff():
    global Fb,Eb,Fw,Ew,file,Seed,img,A,H,Al,Ar,left,right,P
    if Hypothetic: P=prm.tableau(N,R)
    if Dynamic: #
        A=Al=Ar=0
        left = 1
        right = -1
    else:
        Al=-A/2
        Ar=A/2
    code,kw=encrypt(N=N, R=R, A=A,
                    Fix=Fix, Stable=Stable, Infinite=Infinite, Rotate=Rotate, Local=Local,Dynamic=Dynamic,
                    Gaussian=Gaussian,H=H, T=T, W=W, g=g, M=M, Ew=Ew, Eb=Eb, Fw=Fw, Fb=Fb)
    if Seed is None:
        Seed = r.randrange(sys.maxsize)
        r.seed(Seed)
        file = Data(code,kw)
    else:
        r.seed(Seed)
        file="Data/dump"
    img=code+str(Seed)
    save(file)
    with open(file,'a') as f:
        f.write("\n--- BALL POSITIONS ---\n")
    if Fb==0: Fb=10**-10
    else: Fb=math.sqrt(Fb)
    Fw/=Fb
    if Eb == 0: Eb = 10 ** -10
    else: Eb=math.sqrt(Eb)
    Ew/=Eb
    s.Simulation.dt=dt

def wedge():
    if Infinite: l=N*H
    else: l=W
    line1=phy.Segment(S.static_body,C.P(-l,l),C.P(0,0),1)
    line1.color=(0,0,0,255)
    line2=phy.Segment(S.static_body,C.P(0,0),C.P(l,l),1)
    line2.color = (0, 0, 0,255)
    line1.elasticity=line2.elasticity=Ew
    line1.friction=line2.friction=Fw
    S.add(line1,line2)

def touche():
    global Running
    c.tick()
    if Fix:
        if Stable:
            sf=balls[-1].isStable()
            ib=balls[-1].inBoundary()
        else:
            sf = all([balls[i].isStable() for i in range(n.val)])
            ib = all([balls[i].inBoundary() for i in range(n.val)])
    else:
        if Stable: sf=all([balls[i].isStable() for i in range(n.val)])
        ib=all([balls[i].inBoundary() for i in range(n.val)])
    if Animation and Time: sim.display(next(t)) #+f"\nStable:{sf}")
    else: next(t)
    if Stable:
        if sf:
            if n.val<N: ball()
            else: Running=False
    elif n.val<N:
        if 0<= c.t.val-T*n.val < dt:ball()
    elif Fix:
        if sf: Running=False
    elif all([balls[i].isStable() for i in range(n.val)]): Running =False
    if not ib:
        regret()

def hellyeah():
    return Running

def regret():
    sim.show()
    sys.exit(sim.hold(text="Time: " + c.time()))

def local(vel=None,change=None,**kwargs):
    global left,right,Al,Ar,H #
    arbiter=kwargs['arbiter']
    if vel:
        for b in arbiter.bodies:
            if b.body_type != phy.Body.STATIC: b.velocity=(0,0)
    if change:
        for s in arbiter.shapes:
            if s.body.body_type != phy.Body.STATIC: s.collision_type = 2
    if not (vel or change): #
        for b in arbiter.bodies:
            if b.body_type != phy.Body.STATIC:
                pos=C.revert(*b.position)[0]
                if left>pos:
                    left=pos
                    Al=left-R*2**0.5
                if right<pos:
                    right = pos
                    Ar = right + R * 2 ** 0.5

#Real Code
shady_stuff()
wedge()
ball()
if Local:
    S.on_collision(1, 2,    #Ball and dropped Ball
                   begin=partial(sim.handle,event=partial(local,vel=True,change=True)))
    S.on_collision(1, 0,    #Ball and Wedge
                   begin=partial(sim.handle, event=partial(local, vel=False, change=True)))
    S.on_collision(2, 2,    #Dropped Balls
                   begin=partial(sim.handle, event=partial(local, vel=True, change=False)))
    S.on_collision(2,0,     #Dropped Ball and Wedge
                   begin=partial(sim.handle, event=partial(local, vel=True, change=False)))

if Dynamic:
    S.on_collision(1, 0,    #Ball and Wedge
                   begin=partial(sim.handle, event=partial(local, vel=False, change=False)))

c.reset()
if Animation:
    sim.show()
    sim.simulate(touche, hellyeah)
else:
    sim.blind(touche, hellyeah)
    sim.show()
saveShape(balls,file)
with open(file, 'a') as f:
    f.write(f"\nSeed : {Seed}\n")
if Time: sim.hold(text="Time: " + c.time(),filename=img)

else: sim.hold(filename=img)



