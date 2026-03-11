import sys
import pygame as pg
import pymunk.pygame_util
from Tools import *


class Simulation:

    dt=1/500
    def __init__(self,space):
        pg.init()
        pg.display.set_caption("Stacking Balls")
        self.clock = pg.time.Clock()
        self.space=space

    def show(self):
        self.screen = pg.display.set_mode((1280,720))
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)


    def buff(self,*args):
        pass

    def simulate(self,event=None,condition=lambda:True):

        if event is None: event=self.buff

        while condition():
            for i in pg.event.get():
                if i.type == pg.QUIT:
                    sys.exit(0)
                elif i.type == pg.KEYDOWN and i.key == pg.K_ESCAPE:
                    return
                elif i.type == pg.KEYDOWN and i.key == pg.K_p:
                    self.hold()
                elif i.type == pg.KEYDOWN and i.key == pg.K_SPACE:
                    pg.display.quit()
                    self.blind(event,condition)
                    return

            self.space.step(Simulation.dt)
            self.screen.fill((255, 255, 255))

            event()

            self.space.debug_draw(self.draw_options)

            pg.display.flip()
            self.clock.tick(1/Simulation.dt)

    def blind(self, event=None, condition=lambda: True,space=None):

        if event is None: event = self.buff
            
        while condition():
            self.space.step(Simulation.dt)
            event()


    def hold(self,cond=lambda:True,text="",filename="Experiment"):
        self.screen.fill((255, 255, 255))
        self.display(text)
        self.space.debug_draw(self.draw_options)
        pg.display.flip()
        while cond():
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    return
                elif event.type == pg.KEYDOWN and event.key == pg.K_p:
                    return
                elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    pg.image.save(self.screen, f"Shapes/{filename}.png")

    def display(self,text,x=10,y=10):
        font = pg.font.Font(None, 40)
        text_color = (0, 0, 0)
        if str(type(text)) == "<class 'generator'>": text=next(text)
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(topleft=(x, y))
        self.screen.blit(text_surface, text_rect)

    def handle(self,arbiter, space, data,event=None):
        if event is None: event = self.buff
        event(arbiter=arbiter,space=space,data=data)

        return
