from pygamehelper import *
from pygame import *
from pygame.locals import *
from vec2d import *
from math import e, pi, cos, sin, sqrt
from random import uniform

class Point:
    def __init__(self, pos, speed, w, h):
        self.pos = pos
        self.size = int(uniform(10, 25))
        self.color = [0, int(50 + ((self.size - 10) * 10)), 0]
        self.speed = speed
        self.speed.length /= 4
        self.w, self.h = w, h
        self.alive = True
        
    def update(self, others, gravity, magnets, box, merge):
        if self.speed.length < 255:
            self.color[0] = self.speed.length
        else:
            self.color[0] = 255
        for point in others:
            if point is not self and point.alive:
                dir = point.pos - self.pos
                if dir.length < (self.size + point.size):
                    impact_energy = point.speed
                    if impact_energy.length > 0:
                        impact_energy.length = int(impact_energy.length * (point.size / self.size) * 0.6)
                    
                    impact_speed = dir
                    impact_speed.length = 0 - (((self.size + point.size) - dir.length) / 2)
                    
                    self.pos += impact_speed
                    self.speed += impact_speed
                    self.speed += impact_energy
                    #self.speed = vec2d(int((self.speed[0] * 4) / 5), int((self.speed[1] * 4) / 5))
                    if merge:
                        self.size = int(sqrt(point.size * point.size + self.size * self.size))
                        point.alive = False
                    
                elif magnets:
                    if dir.length < 20 * self.size:
                        dir.length = int((dir.length / 20 ) * (self.size / point.size) * 0.02)
                        print(self.size , "ima leng : ", dir.length)
                        point.speed -= dir
                    
        if gravity:
            self.speed += vec2d(0, 2)
        
        if box:
            if self.pos[1] > self.h - self.size:
                self.speed = vec2d(self.speed[0], - int((self.speed[1] * 4) / 5) )
                self.pos[1] = self.h - self.size
            elif self.pos[1] < 0 + self.size:
                self.speed = vec2d(self.speed[0], - int((self.speed[1] * 4) / 5) )
                self.pos[1] = 0 + self.size
             
             
            if self.pos[0] > self.w - self.size:
                self.pos[0] = self.w - self.size
                self.speed = vec2d(- int((self.speed[0] * 3) / 5), self.speed[1])
            elif self.pos[0] < 0 + self.size:
                self.pos[0] = 0 + self.size
                self.speed = vec2d(- int((self.speed[0] * 3) / 5), self.speed[1])
                
        self.pos += self.speed
        
    def draw(self, screen, zoom, offset):
        pygame.draw.circle(screen, self.color, (int(self.pos[0] * zoom) + offset[0], int(self.pos[1] * zoom) + offset[1]), int(self.size * zoom))
        if self.speed.length > 30:
            self.draw_vector(screen, zoom, offset)
    
    def draw_vector(self, screen, zoom, offset):
        pygame.draw.line(screen, (0, 0, 0), self.pos * zoom + offset, (self.pos + self.speed) * zoom  + offset)

class Starter(PygameHelper):
    def __init__(self):
        self.w, self.h = 1200, 700
        PygameHelper.__init__(self, size=(self.w, self.h), fill=((255,255,255)))
        
        self.points = []
        self.mouse_gravity = False
        self.mouse_gravity_point = vec2d(0, 0)
        self.gravity = True
        self.clear_screen = True
        self.magnetisum = False
        self.box = True
        self.merge = False
        self.offset = vec2d(0, 0)
        self.motion = vec2d(0, 0)
        self.pos = vec2d(0, 0)
        self.zoom = 1
        self.cleaner = pygame.image.load("cleaner.png")
        
    def update(self):
        for point in self.points:
            if point.alive:
                point.update(self.points, self.gravity, self.magnetisum, self.box, self.merge)
        if self.mouse_gravity:
            for point in self.points:
                rel_pos = self.mouse_gravity_point - point.pos
                rel_pos.length = 3
                point.speed += rel_pos
        
    def keyUp(self, key):
        if key == 100:
            self.mouse_gravity = not self.mouse_gravity
            print("Mouse Gravity is : ", self.mouse_gravity)
            self.mouse_gravity_point = self.pos
        if key == 97:
            self.gravity = not self.gravity
            print("Normal Gravity is : ", self.gravity)
        if key == 115:
            self.clear_screen = not self.clear_screen
            print("Clear screen is : ", self.clear_screen)
            if self.clear_screen: pygame.image.save(self.screen, 'capture.bmp')
        if key == 119:
            self.magnetisum = not self.magnetisum
            print("Ball atraction is : ", self.magnetisum)
        if key == 113:
            self.box = not self.box
            print("Borders are : ", self.box)
        if key == 101:
            self.merge = not self.merge
            print("Ball merge is : ", self.merge)
        if key == 269:
            self.zoom *= 0.5
        if key == 270:
            self.zoom *= 2
        if key == 273:
            self.offset[1] -= 10
        if key == 274:
            self.offset[1] += 10
        if key == 275:
            self.offset[0] += 10
        if key == 276:
            self.offset[0] -= 10
        
    def mouseUp(self, button, pos):
        temp = Point(pos * self.zoom + self.offset, self.motion, self.w, self.h)
        self.points.append(temp)
        
        
    def mouseMotion(self, buttons, pos, rel):
        self.motion = vec2d(rel) * self.zoom + self.offset
        self.pos = vec2d(pos)  * self.zoom + self.offset
        
        
    def draw(self):
        if self.clear_screen:
            self.screen.fill((255, 255, 255))
        for point in self.points:
            if point.alive:
                #if point.pos[0] > 0 and point.pos[0] < self.w and point.pos[1] > 0 and point.pos[1] < self.h:
                point.draw(self.screen, self.zoom, self.offset)
        
s = Starter()
s.mainLoop(40)
