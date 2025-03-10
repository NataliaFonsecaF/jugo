import pygame 
import random

class Item:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ancho = 30
        self.alto = 30
        self.velocidad = 5 
        self.tipo = random.randint(1,2)
        self.color = "orange" if self.tipo == 1 else  "green"
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
       

    def dibujar (self, ventana):
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        pygame.draw.rect(ventana, self.color, self.rect)
        

    def movimiento(self):
        self.y += self.velocidad