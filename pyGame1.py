import pygame
from personaje import Cubo
from enemigo import Enemigo
from bala import Bala
from item import Item
import random
import time


pygame.init()
pygame.mixer.init()

ANCHO = 1000
ALTO = 800
VENTANA = pygame.display.set_mode([ANCHO, ALTO])
FPS = 60
FUENTE = pygame.font.SysFont("Comic Sans", 40)
SONIDO_DISPARO = pygame.mixer.Sound('media/laser2.mp3')
SONIDO_MUERTE_ENEMIGO = pygame.mixer.Sound('media/enemy_destroy.mp3')
SONIDO_FIN = pygame.mixer.Sound('media/nave_destroy.mp3')

jugando = True
reloj = pygame.time.Clock()
vida =5
puntos = 0
tiempo_pasado = 0
tiempo_entre_enemigos = 500  
tiempo_entre_enemigos_base = 1000
cubo = Cubo(ANCHO/2, ALTO-75)
enemigos = []
balas = []
items = []
tiempo_entre_items = 15000
tiempo_pasado_2 = 0
ultima_bala = 0 
tiempo_entre_balas = 100
enemigos.append(Enemigo(ANCHO/2,100))

def crear_bala():
    global ultima_bala
    if pygame.time.get_ticks() - ultima_bala > tiempo_entre_balas:
        balas.append(Bala(cubo.rect.centerx,cubo.rect.centery))
        ultima_bala = pygame.time.get_ticks()
        SONIDO_DISPARO.play()

def gestionar_teclas(teclas):
    # if teclas[pygame.K_w]:
        # cubo.y -= cubo.velocidad
    if teclas[pygame.K_a]:
        if cubo.x >= 0:
            cubo.x -= cubo.velocidad
    # if teclas[pygame.K_s]:
    #     cubo.y += cubo.velocidad
    if teclas[pygame.K_d]:
        if cubo.x + cubo.ancho <= ANCHO:
            cubo.x += cubo.velocidad
    if teclas[pygame.K_SPACE]:
        crear_bala()


while jugando and  vida > 0:

    tiempo_pasado += reloj.tick(FPS)
    tiempo_pasado_2 += reloj.tick(FPS)
    if tiempo_pasado > tiempo_entre_enemigos:
        enemigos.append(Enemigo(random.randint(0, ANCHO),-100))
        tiempo_pasado = 0 
        tiempo_entre_enemigos = random.randint(50, tiempo_entre_enemigos_base)
        if tiempo_entre_enemigos_base > 80:
            tiempo_entre_enemigos_base -= 20

    if tiempo_pasado_2 > tiempo_entre_items:
        items.append(Item(random.randint(0, ANCHO),-100)) 
        tiempo_pasado_2 = 0 


   
    eventos = pygame.event.get()
    teclas = pygame.key.get_pressed()
    texto_vida = FUENTE.render(f"Vida: {vida}", True, "white")
    texto_puntos = FUENTE.render(f"puntos: {puntos}", True, "white")
    gestionar_teclas(teclas)
    

    for evento in eventos: 
        if evento.type == pygame.QUIT:
            jugando = False

    VENTANA.fill("black")
    cubo.dibujar(VENTANA)

    for enemigo in enemigos: 
        enemigo.dibujar(VENTANA)
        enemigo.movimiento()
        if pygame.Rect.colliderect(cubo.rect, enemigo.rect):
            print("tocadito")
            vida -= 1
            print(f"te quedan {vida} vidas")
            enemigos.remove(enemigo)
        if enemigo.y > ALTO:
            puntos +=1
            enemigos.remove(enemigo)
        for bala in balas:
            if pygame.Rect.colliderect(bala.rect, enemigo.rect):
                enemigo.vida -= 1
                balas.remove(bala)
                
        if enemigo.vida <= 0:
            enemigos.remove(enemigo)
            puntos += 5
            SONIDO_MUERTE_ENEMIGO.play()


    for bala in balas:
         bala.dibujar(VENTANA)
         bala.movimiento()
         if bala.y < 0:
             balas.remove(bala)

    for item in items: 
        item.dibujar(VENTANA)
        item.movimiento()
        if pygame.Rect.colliderect(item.rect, cubo.rect):
            items.remove(item)
            if item.tipo ==1:
                if tiempo_entre_balas > 200:
                    tiempo_entre_balas /=2
            elif item.tipo == 2:
                cubo.velocidad *=2
        if item.y > ALTO:
            items.remove(item)


    VENTANA.blit(texto_vida, (20,20))
    VENTANA.blit(texto_puntos, (20,70))

    pygame.display.update()
SONIDO_FIN.play()
time.sleep(0.3)
pygame.quit()
nombre = input("introduce tu nombre: ")
with open('puntuaciones.txt', 'a') as archivo:
    archivo.write(f"{nombre}- {puntos}\n")

quit()