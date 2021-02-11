# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 18:39:44 2020
@author: edgar
"""

import pygame, sys
from pygame.locals import *
import random
import numpy as np

pygame.init()
ventana = pygame.display.set_mode((1000,720))
(w, h) = ventana.get_size()
pygame.display.set_caption("Agente Explorador 2")

nCasillasMarcadas = 10
casillasMarcadas = [0]*nCasillasMarcadas
xRand = np.zeros((10,nCasillasMarcadas))
yRand = np.zeros((10,nCasillasMarcadas))
for k in range(10):
    for j in range(nCasillasMarcadas):
        xRand[k,j] = random.randint(1,9)*w/10
        yRand[k,j] = random.randint(1,9)*h/10

#Colores
blanco = (255,255,255)
rojo = (255,0,0)
negro = (0,0,0)
gris = (200,200,200)
azul = (0,0,255)
verde = (0,255,0)
def colorAleatorio():
    return (random.randint(50,255),random.randint(50,255),random.randint(50,255))

(xInicio, yInicio) = (w/20+w/10*4, h/20+h/10*4) #Inicio
#[0]:N, [1]:S, [2]:E, [3]:O, [4]:C
#Valores: 0: Vacía, 1: Marcada, 2: Pared
entorno1 = [0,0,0,0,0]
#Estrategia aleatoria
def estrategiaAleatoria():
    return [random.randint(0,6) for i in range(243)]

class Agente:
    def __init__(self,ent,estrat,coordX,coordY,col):
        self.puntaje = 0
        self.estrategia = estrat
        self.entorno = ent
        self.entornoEnDecimal = 0
        self.coordX = coordX
        self.coordY = coordY
        self.color = col

    def dibujar(self):
        pygame.draw.circle(ventana,self.color,(self.coordX,self.coordY),12)
        
    def getEntorno(self):
        for i in range(len(self.entorno)):
            self.entorno[i] = 0
        for j in range(len(casillasMarcadas)):
            if casillasMarcadas[j].collidepoint(self.coordX,self.coordY):
                self.entorno[4] = 1
            if casillasMarcadas[j].collidepoint(self.coordX-w/10,self.coordY):
                self.entorno[3] = 1
            if casillasMarcadas[j].collidepoint(self.coordX+w/10,self.coordY):
                self.entorno[2] = 1
            if casillasMarcadas[j].collidepoint(self.coordX,self.coordY-h/10):
                self.entorno[0] = 1
            if casillasMarcadas[j].collidepoint(self.coordX,self.coordY+h/10):
                self.entorno[1] = 1
        if self.coordX-w/10 < 0:
            self.entorno[3] = 2
        if self.coordX+w/10 > w:
            self.entorno[2] = 2
        if self.coordY-h/10 < 0:
            self.entorno[0] = 2
        if self.coordY+h/10 > h:
            self.entorno[1] = 2
        #entorno de sistema base 3 a decimal
        self.entornoEnDecimal = 0
        for i in range(len(self.entorno)):
                self.entornoEnDecimal += self.entorno[i]*(3**i)
        return self.entornoEnDecimal
    
    def cuatro1asEstrategias(self,numEstrategia):
        if numEstrategia == 2:
            self.coordX += w/10
            if self.coordX > w:
                self.puntaje -= 1
                self.coordX = w - w/20
        if numEstrategia == 3:
            self.coordX -= w/10
            if self.coordX < 0:
                self.puntaje -= 1
                self.coordX = w/20
        if numEstrategia == 0:
            self.coordY -= h/10
            if self.coordY < 0:
                self.puntaje -= 1
                self.coordY = h/20
        if numEstrategia == 1:
            self.coordY += h/10
            if self.coordY > h:
                self.puntaje -= 1
                self.coordY = h - h/20
    
    def getPuntaje(self):   #En esta función también se mueve
        nCasillMarcadsnew = nCasillasMarcadas
        for i in range(len(self.estrategia)):
            if i == self.getEntorno():
                self.cuatro1asEstrategias(self.estrategia[i])
                if self.estrategia[i] == 4:
                    levanto = False
                    for j in range(nCasillasMarcadas):
                        if casillasMarcadas[j].collidepoint(self.coordX,
                                                            self.coordY):
                            self.puntaje += 10
                            levanto = True
                            k = j
                    if levanto == True:
                        casillasMarcadas.pop(k)
                        nCasillMarcadsnew -= 1
                    else:
                        self.puntaje -= 3
                if self.estrategia[i] == 5:
                    pass
                if self.estrategia[i] == 6:
                    estrat6 = random.randint(0,3)
                    self.cuatro1asEstrategias(estrat6)
        if self.puntaje > 50:
            self.color = verde
        return nCasillMarcadsnew
                    
class Poblacion:
    def __init__(self):
        self.numAgentes = 100
        self.agentes=[Agente(entorno1,estrategiaAleatoria(),xInicio,yInicio,
                             rojo) for i in range(self.numAgentes)]
        self.puntajes = [0]*self.numAgentes
        self.puntajeMaximo = 0
        self.umbralAgenteMax = 10
        self.agenteMaximo = random.choice(self.agentes)
        self.probabilidadMutacion = 0.1

    def dibujarPoblacion(self):
        for i in range(self.numAgentes):
            self.agentes[i].dibujar()
            
    def evaluar(self):
        for i in range(self.numAgentes):
            self.puntajes[i] = self.agentes[i].puntaje
        self.puntajeMaximo = np.max(self.puntajes)
        indexAgenteMax = np.argmax(self.puntajes)
        self.agenteMaximo = self.agentes[indexAgenteMax]
        
    def seleccionar(self):
        puntajeMin = np.min(self.puntajes)
        intervalo = self.puntajeMaximo - puntajeMin
        if intervalo != 0:
            ptjsNormalizados = np.abs(self.puntajes-puntajeMin)/intervalo
            probabilidades = ptjsNormalizados/sum(ptjsNormalizados)
            print("Puntaje mínimo:",puntajeMin)
            print("Puntaje máximo:",self.puntajeMaximo)
            self.agentes=random.choices(self.agentes,weights=probabilidades,
                                        k=self.numAgentes)
        else:
            print("Puntaje común", self.puntajeMaximo)
            self.agentes = random.choices(self.agentes, k = self.numAgentes)
        if self.puntajeMaximo >= self.umbralAgenteMax:
            indexAgenteMin = np.argmin(self.puntajes)
            self.agentes[indexAgenteMin] = self.agenteMaximo
            self.agentes[indexAgenteMin].color = verde
            print("Agente máximo reintroducido")
            if self.probabilidadMutacion > 0:
                self.probabilidadMutacion -= 0.01
            
    def cruzar(self):
        poblacionAnt = self.agentes
        random.shuffle(poblacionAnt)
        nuevaPoblacion = []
        i = 0
        while(i <= self.numAgentes-2):
            crossPoint = random.randrange(0,243)
            padre = poblacionAnt[i]
            madre = poblacionAnt[i+1]
            n = len(padre.estrategia)
            genotipo1 = np.zeros(243)
            genotipo2 = np.zeros(243)
            genotipo1[0:crossPoint]=padre.estrategia[0:crossPoint]
            genotipo1[crossPoint:n]=madre.estrategia[crossPoint:n]
            genotipo2[0:crossPoint]=madre.estrategia[0:crossPoint]
            genotipo2[crossPoint:n]=padre.estrategia[crossPoint:n]
            hijo1 = Agente(entorno1,genotipo1,xInicio,yInicio,rojo)
            hijo2 = Agente(entorno1,genotipo2,xInicio,yInicio,rojo)
            nuevaPoblacion.append(hijo1)
            nuevaPoblacion.append(hijo2)
            i += 2
        self.agentes = nuevaPoblacion
        
    def mutar(self):
        if self.puntajeMaximo < 1:
            self.probabilidadMutacion = 0.12
        mutaciones = 0
        for i in range(len(self.agentes)):
            if(random.random() < self.probabilidadMutacion):
                idxEstrat = random.randint(0,242)
                if self.puntajeMaximo >= self.umbralAgenteMax:
                    self.agentes[i].estrategia[idxEstrat]=self.agenteMaximo.estrategia[idxEstrat]
                if self.puntajeMaximo < 1:
                    self.agentes[i].estrategia[idxEstrat] = random.randint(0,6)
                mutaciones += 1
        print("Cantidad de mutaciones",mutaciones)

poblacion = Poblacion()
movimientos = 0
start = False
generacion = 1
print("Generación:",generacion)
mundo = 0
while True:
    # Dibuja el mundo
    ventana.fill(negro)
    for i in range(1, 10):
        pygame.draw.line(ventana,blanco,(0,(h/10)*i),(w,(h/10)*i))
    for j in range(1, 10):
        pygame.draw.line(ventana,blanco,((w/10)*j,0),((w/10)*j,h))
    for j in range(nCasillasMarcadas):
        casillasMarcadas[j]=pygame.draw.rect(ventana,gris,
                    (xRand[mundo,j],yRand[mundo,j],w/10,h/10))
    poblacion.dibujarPoblacion()

    if start == True:
        for i in range(poblacion.numAgentes):
            nCasillasMarcadas = poblacion.agentes[i].getPuntaje()
        movimientos += 1
        print(movimientos)
    
    if movimientos == 100:
        poblacion.evaluar()
        poblacion.seleccionar()
        poblacion.cruzar()
        poblacion.mutar()
        movimientos = 0
        generacion += 1
        print("Generación:",generacion)
        mundo += 1
        if mundo > 9:
            mundo = 0
        nCasillasMarcadas = 10
        casillasMarcadas = [0]*nCasillasMarcadas
    
    if generacion == 500:
        start = False
        generacion = 0
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            start = True
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()