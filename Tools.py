import pygame as pg
import Simulation


class Cartesian:
    def __init__(self,origin=(640,700),metre=100):
        self.Ox,self.Oy= origin
        self.s=metre

    def P(self,x=None,y=None):
        if x is None:
            Y = self.Oy - y * self.s
            return Y
        if y is None:
            X=self.Ox+x*self.s
            return X
        X = self.Ox + x * self.s
        Y = self.Oy - y * self.s
        return (X,Y)

    def revert(self,x,y):
        X=(x-self.Ox)/self.s
        Y=(self.Oy-y)/self.s
        return (X,Y)


    def metre(self,quantity,dim=1):
        return quantity*self.s**dim

class Counter:

    def __init__(self,v=0):
        self.val=v

    def __add__(self,n):
        self.val+=n
        return self

    def __sub__(self,n):
        self.val -= n
        return self

    def __mul__(self,n):
        self.val *= n
        return self

    def __truediv__(self,n):
        self.val /= n
        return self

    def __floordiv__(self,n):
        self.val //= n
        return self

class Timer:
    def __init__(self):
        self.t=Counter()
        self.start_time=0
        self.current_time_ms = 0
        self.run=True

    def tick(self):
        self.t+=Simulation.Simulation.dt

    def time(self):
        total_seconds = self.current_time_ms
        minutes = int(total_seconds // 60)
        seconds = total_seconds % 60
        return f"{minutes:02d}:{seconds:06.3f}"

    def lap(self):
        while True:
            if self.run: self.current_time_ms = self.t.val - self.start_time
            timer_text = "Time: "+self.time()
            yield timer_text

    def reset(self):
        self.start_time = self.t.val
        self.current_time_ms = 0

    def pause(self):
        self.run=False

    def run(self):
        self.run = True

