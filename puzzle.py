#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Puzzle.py
# Luis Lujan 2017

''' Grapical sliding tile puzzle, tiles moves presing on it 
if the empty tile it's close.
Reset button scramble the game and init it
Solve button calls panel_puzzle solver 

filas and columnas are the panel size rows and columns
movimientos is the number of random steps to scramble.
blanco is the empty tile.

To run the game exec this script. 
'''

import tkinter as tk
import random
import time
from panel_puzzle import Tablero

# definicion de constantes
debug = True
norte = 'N'
sur   = 'S'
este  = 'E'
oeste = 'W'
blanco= -1
filas = 4
columnas = 4
movimientos = 50000
txt_moves = "moves"
txt_reset = "Reset"
txt_solve = "Solve"
it_cant_move =  "No se puede mover "
txt_win =    " YOU WIN "
borra_gana = "         "
txt_m_err = "mezclar error "
txt_fin = 'This permutation has bee solved in {0:3.3f}ms with {1} steps with these path:\n'

class Puzzle(tk.Frame):
    '''its the puzzle main board its a tkinter window and also writes to the console
      two panels, one butons and labels oter with tiles
      the tiles are in the class Ficha 
    '''
    def __init__(self, master = None):
        super().__init__(master)

        self.fichas = []
        self.ficha_blanca = []
        self.nro_jugadas = 0
        self.panel = Tablero(filas, columnas)
        self.pack()
        self.panel_info = tk.Frame(self)
        self.panel_juego = tk.Frame(self, bg="red")
        self.panel_info.pack(side="top")
        self.panel_juego.pack(side="bottom")
        self.label_jugadas = tk.Label(self.panel_info, text=txt_moves)
        self.label_numero = tk.Label(self.panel_info, width = 4, text= str(self.nro_jugadas))
        self.label_gana = tk.Label(self.panel_info, width = 10, text= borra_gana)
        self.bt_reset = tk.Button(self.panel_info, text= txt_reset, command= self.reset)
        self.bt_solve = tk.Button(self.panel_info, text= txt_solve, command= self.solve)
        self.label_jugadas.grid(row=0, column= 1)
        self.label_numero.grid(row=0, column= 0)
        self.label_gana.grid(row=0, column= 2)
        self.bt_reset.grid(row= 0, column= 3)
        self.bt_solve.grid(row= 0, column = 4)
        self.crea_fichas()

        
    def crea_fichas(self):
        for r in range(filas):
            for c in range(columnas):
                if r == (filas-1) and c == (columnas -1):
                    self.ficha_blanca = r, c
                    break
                b = Ficha(self.panel_juego,1,3,r,c,r*columnas+c)
                t = str(r*columnas+c)
                if len(t) < 2: t = '0' + t
                b["text"] = t
                indice = len(self.fichas)
                b["command"] = lambda i_lan = indice: self.ficha_pulsada(i_lan)
                b.grid(row=(r), column=(c))
                self.fichas.append(b)
        self.mezclar(movimientos)
        
    def ficha_pulsada(self, indice):   
        r,c = self.fichas[indice].posicion()
        if self.ficha_blanca == (r, c+1):
            self.fichas[indice].muevete(r,c+1)
        elif self.ficha_blanca == (r+1,c):
            self.fichas[indice].muevete(r+1,c)
        elif self.ficha_blanca == (r,c-1):
            self.fichas[indice].muevete(r,c-1)
        elif self.ficha_blanca == (r-1,c):
            self.fichas[indice].muevete(r-1,c)
        else:
            if debug:
                print(it_cant_move, indice, r,c, self.ficha_blanca)
            return False
        self.nro_jugadas += 1
        self.ficha_blanca = r, c
        self.label_numero["text"] = str(self.nro_jugadas)
        self.comprobar()
        return True

    def comprobar(self):
        for i in self.fichas:
            if not i.ok():
                return False
        self.label_gana["text"]=txt_win
        for i in self.fichas:
            i.disable()
        self.label_numero["text"] = str(self.nro_jugadas)
        self.bt_solve["state"] = tk.DISABLED
        return True
        
    
    def mezclar(self, movimientos):
        random.seed()
        panel = []
        for i in range(filas):
            panel.append([])
            for j in range(columnas):
                panel[i].append((i,j))
           
        f = filas -1
        c = columnas -1
        panel[f][c]= blanco
        m = 0
        da = blanco
        while m < movimientos:
            plantilla =""
            if (c+1) < columnas and da != oeste:
                plantilla += este
            if (f+1) < filas and da != norte:
                plantilla += sur
            if (c-1) >= 0 and da != este:
                plantilla += oeste
            if (f-1) >= 0 and da != sur:
                plantilla += norte
            if len(plantilla) == 1:
                destino = plantilla[0]
            else:
                destino = plantilla[random.randint(0,len(plantilla)-1)]

            if destino == este:
                panel[f][c] = panel[f][c+1]
                da = este
                c += 1
                panel[f][c] = blanco
            elif destino == sur:
                panel[f][c] = panel[f+1][c]
                da = sur
                f += 1
                panel[f][c] = blanco
            elif destino == oeste:
                panel[f][c] = panel[f][c-1]
                da = oeste
                c -= 1
                panel[f][c] = blanco
            elif destino == norte:
                panel[f][c] = panel[f-1][c]
                da = norte
                f -= 1
                panel[f][c] = blanco
            elif debug:
                print(txt_m_err, destino, f, c)
            m += 1
            
        while (c+1) < columnas:
            panel[f][c] = panel[f][c+1]
            c += 1
            panel[f][c] = blanco
        while (f+1) < filas:
            panel[f][c] = panel[f+1][c]
            f += 1
            panel[f][c] = blanco
            
        for i in range(filas):
            for j in range(columnas):
                if panel[i][j] != blanco:
                    row,col = panel[i][j]
                    self.fichas[i*columnas+j].muevete(row,col)
                else:
                    self.ficha_blanca = i, j
        self.nro_jugadas = 0
        self.label_numero["text"] = str(self.nro_jugadas)

    def reset(self):
        self.label_gana["text"]= borra_gana
        self.bt_solve["state"] = tk.NORMAL
        self.mezclar(movimientos)
                    
    def solve(self):
        self.tiempo = time.clock()
        panel = Tablero(filas, columnas)
        panel.rellena(self.fichas)
        tiempo = time.clock()
        panel.resuelve()
        tiempo = (time.clock() - tiempo) * 1000.0
        for i in range(filas):
            for j in range(columnas):
                indice = panel.contenido((i,j)) 
                if indice != blanco:
                    self.fichas[indice].muevete(i, j)
                else:
                    self.ficha_blanca = i, j
        
        nr_jugadas = panel.jugadas()
        self.nro_jugadas = nr_jugadas
        if self.comprobar():
            print('\n', panel.permutation)
            print(txt_fin.format(tiempo, nr_jugadas))            
            txt_sol = panel.solucion()
            for i in range(0, len(txt_sol), 40):
                print(txt_sol[i:i+40])
                    
class Ficha(tk.Button):
    def __init__(self, master, h=5, w=10, row=0, col=0, indice=0):
        self.pos = row,col
        self.indice = indice
        super().__init__(master,height=h, width=w)
        self['bg']= '#81f'
        self['bd']= 10
        self['font'] = ('Times', 24, 'bold')

    def muevete(self, row, col):
        super().grid(row=row, column=col)
        self.pos = row,col
        self["state"] = tk.NORMAL

    def posicion(self):
        return self.pos

    def row(self):
        return self.pos[0]

    def col(self):
        return self.pos[1]
                
    def ok(self):
        if self.indice == self.pos[0]*columnas + self.pos[1]:
            return True
        else:
            return False
    def disable(self):
        self["state"] = tk.DISABLED

root =tk.Tk()
app = Puzzle(master = root)
app.mainloop()
