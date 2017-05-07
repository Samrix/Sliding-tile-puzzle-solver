#!user/bin/python
# -*- coding: utf-8 -*-
# panel_puzzle.py
# Luis Lujan 2017
'''
 panel_puzzle is a sliding tile puzzle solver.
 It can solve 3x3 and higher puzzles. You can define the size
 with constructor variables filas = rows and columnas = columns
 '''
  
#defines
debug = True
debug_0 = False
blanco = -1
este =  'E'
west =  'W'
norte = 'N'
sur =   'S'
oeste = 'W'
levogiro = True
dextrogiro = False
arbol = 'Tree '

class Tablero():
    '''It is the sliding tile puzzle solver main class''' 
    def __init__(self, filas= 4, columnas= 4):
        self.filas = filas          # panel rows
        self.columnas = columnas    # panel columns
        self.minas = []             # tiles that cann't move
        self.panel = []             # the panel of sliding tiles model
        self.permutation = []       # panel configuration at begining
        self.nro_jugadas = 0        # each time a tile is move increments this variable by 1
        self.lista_jugadas= ''      # list of moves, string of NSWE 
        for i in range(filas):      # creates a empty panel 
            self.panel.append([])
            for j in range(columnas):
                self.panel[i].append(blanco)
    
    def reset(self):
        ''' clear all variables and panel '''
        self.minas.clear()
        for i in range(self.filas):
            for j in range(self.columnas):
                self.panel[i][j] = blanco
        self.nro_jugadas = 0
        self.lista_jugadas= ''
        self.permutation = []

    def contenido(self, pos):
        return self.panel[pos[0]][pos[1]]
    
    def solucion(self):
        return self.lista_jugadas
    
    def jugadas(self):
        return self.nro_jugadas
    
    def rellena(self,fichas):
        ''' interface with graphical panel. 
        fichas it's a list of Ficha class on puzzle.py
        '''
        self.reset()
        for i in range(len(fichas)):
                r,c = fichas[i].posicion()
                self.panel[r][c] = i
        self.permutation = []
        for f in range(self.filas):
            for c in range(self.columnas):
                self.permutation.append(self.panel[f][c])
                
    def inicia(self, lista):
        ''' init with a list of integers, from 0 to filas * columnas and -1 for the blank
        its usefull w
        hen you don't uses the grphical interface '''
        self.reset()
        for i in range(len(lista)):
            self.panel[i//self.columnas][i%self.columnas] = lista[i]
            self.permutation.append(lista[i])
            
    def secuencia(self, seq):
        ''' read a str with N, S, E, W chars and 
        moves the empty tile according to the text'''
        for paso in range(len(seq)):
            bk = self.pos(blanco)
            tile = bk
            si = True
            if   seq[paso] == norte: tile = bk[0] - 1, bk[1]
            elif seq[paso] == sur  : tile = bk[0] + 1, bk[1]
            elif seq[paso] == este : tile = bk[0], bk[1] + 1
            elif seq[paso] == west : tile = bk[0], bk[1] - 1
            else: si = False
            if si:   self.mueve(tile)
            
    def es_ok(self, indice):
        ''' check the panel. panel must beguin at 0 '''
        donde = self.pos(indice)
        if (indice // self.columnas, indice % self.columnas) == donde:
            return True
        else:
            return False

    def pos(self, item):
        ''' look for item in panel and return row and col'''
        f = 0
        while self.panel[f].count(item) == 0 and f < self.filas:
            f += 1
        if f < self.filas:
            c = self.panel[f].index(item)
            return f, c
        else:
            return None        
        
    def resuelve_uno(self, indice, destino = None):
        ''' Try to put a tile on its position, or any destino tile''' 
        origen = self.pos(indice)
        if origen == None: return 1
        if destino == None:
            destino = (indice // self.columnas, indice % self.columnas)
        rutas = {}
        self.arbol(rutas)
        camino = self.camino(origen, destino, rutas)
        if camino == None : return 2
        for i_paso in range(1, len(camino)):
            self.pon_mina(camino[i_paso - 1])
            if not self.pon_blanco_en(camino[i_paso]): return 3
            self.pop_mina()
            if self.mueve(camino[i_paso - 1]) == '': return 4
        self.pon_mina(destino)
        if debug_0: print("Resuelto: ", indice)
        return 0
    
    def resuelve_dos_h(self, indice):
        '''At end of a line you can put only one tile, you must move 
        the last two tiles at the same time''' 
        tile = self.pos(indice)
        if tile == None: return 11 
        tile_propio = (indice // self.columnas, indice % self.columnas)
        tile_aux = tile_propio[0], tile_propio[1]+1
        res_err = self.resuelve_uno(indice, tile_aux)
        if res_err != 0: return res_err
        tile_siguiente = self.pos(indice + 1)
        if tile_siguiente == None: return 12
        p1 = (tile_aux[0]+1, tile_aux[1]-1) == tile_siguiente
        p2 = (tile_aux[0], tile_aux[1]-1)   == tile_siguiente 
        if p1 or p2 :
            self.pop_mina(tile_aux)
            tile_lejos = (tile_aux[0]+2, tile_aux[1])
            res_err = self.resuelve_uno(indice+1, tile_lejos)
            if res_err != 0: return res_err
            res_err = self.resuelve_uno(indice, tile_aux)
            if res_err != 0: return res_err
            self.pop_mina(tile_lejos)
        tile_down = tile_aux[0]+1, tile_aux[1]
        res_err = self.resuelve_uno(indice+1, tile_down)
        if res_err != 0: return res_err
        self.pop_mina(tile_aux)
        res_err = self.resuelve_uno(indice, tile_propio)
        if res_err != 0: return res_err
        self.pop_mina(tile_down)           
        res_err = self.resuelve_uno(indice+1, tile_aux)
        if res_err != 0: return res_err
        return 0
    
    def resuelve_dos_v(self, indice):
        '''At the two last rows you must move two tile at the same time '''
        tile = self.pos(indice)
        if tile == None: return 21 
        tile_propio = (indice // self.columnas, indice % self.columnas)
        tile_aux = tile_propio[0]+1, tile_propio[1]
        res_err = self.resuelve_uno(indice, tile_aux)
        if res_err != 0: return res_err
        tile_siguiente = self.pos(indice + self.columnas)
        if tile_siguiente == None: return 22        
        p1 = (tile_aux[0]-1, tile_aux[1]+1) == tile_siguiente
        p2 = (tile_aux[0]-1, tile_aux[1])   == tile_siguiente
        if p1 or p2 :
            self.pop_mina(tile_aux)
            tile_lejos = (tile_aux[0], tile_aux[1]+2)
            res_err = self.resuelve_uno(indice + self.columnas, tile_lejos)
            if res_err != 0: return res_err
            res_err = self.resuelve_uno(indice, tile_aux)
            if res_err != 0: return res_err
            self.pop_mina(tile_lejos)             
        tile_decho = tile_aux[0], tile_aux[1]+1
        res_err = self.resuelve_uno(indice + self.columnas, tile_decho)
        if res_err != 0: return res_err
        self.pop_mina(tile_aux)
        res_err = self.resuelve_uno(indice, tile_propio)
        if res_err != 0: return res_err
        self.pop_mina(tile_decho)           
        res_err = self.resuelve_uno(indice + self.columnas, tile_aux)
        if res_err != 0: return res_err
        return 0
    
    def resuelve_tres(self):
        ''' The last 3 tiles doesn't permute, only turn 12 positions''' 
        indice = self.filas * self.columnas -2
        tile_ultimo = self.pos(indice)
        bk = self.pos(blanco)
        bk_fin = self.filas -1, self.columnas -1
        if tile_ultimo[1] == self.filas-1: # Giro levojiro
            sentido = levogiro
        else:
            sentido = dextrogiro
        while  not self.es_ok(indice) or bk != bk_fin:
            self.mueve(self.giro(sentido))
            tile_ultimo = self.pos(indice)
            bk = self.pos(blanco)
    
    def resuelve(self):
        ''' Solves the puzzle one by one, row by rov, two last rows 
        column by column and the last 3 tile turnig until end'''
        f = 0
        for f in range(self.filas-2):
            for c in range(self.columnas-2):
                self.resuelve_uno(f*self.columnas+c)
            self.resuelve_dos_h(f*self.columnas+c + 1)
        f += 1
        for c in range(self.columnas - 2):
            self.resuelve_dos_v(f*self.columnas+c)
        self.resuelve_tres()
        
            
    def giro(self, sentido = levogiro ):
        '''At the end left or right must it turn?'''
        bk = self.pos(blanco)
        mgiro = [(0,1),(1,1),(0,0),(1,0)]
        if sentido : mgiro.reverse()
        posicion = (bk[0]-self.filas + 2) * 2 + (bk[1] - self.columnas + 2)
        tile = mgiro[posicion][0] + self.filas -2, mgiro[posicion][1] + self.columnas -2
        return tile
    
    def posibles(self, cc):
        '''From one tile where you can go?, avoiding mines'''
        psb = []
        if cc[0]+1 < self.filas and (cc[0]+1, cc[1]) not in self.minas:
            psb.append((cc[0]+1, cc[1]))
        if cc[1]+1 < self.columnas and (cc[0], cc[1]+1) not in self.minas:
            psb.append((cc[0], cc[1]+1))
        if cc[0]-1 >= 0 and (cc[0]-1, cc[1]) not in self.minas:
            psb.append((cc[0]-1, cc[1]))
        if cc[1]-1 >= 0 and (cc[0], cc[1]-1) not in self.minas:
            psb.append((cc[0], cc[1]-1))
        return psb
    
    def arbol(self, rutas):
        '''You must a tree to make paths, its a dictionary, 
        keys are all tiles in panel, and the definitions are 
        a list with valid coordinates''' 
        for f in range(self.filas):
            for c in range(self.columnas):
                t= self.posibles((f,c))
                rutas[(f,c)] = t
        if debug_0:
            print(arbol)
            for k in rutas:
                print(k, ":", rutas[k])
        return True

    def burbuja(self, origen, destino, rutas):
        '''Is a very quick way of making pathc each steep you 
        chose the tile closer to destination, perhaps it cann`t find 
        the pathc but if it's do it's faster than systematic search'''
        camino = []
        camino.append(origen)
        while destino not in camino:
            ramas  = rutas[camino[-1]]
            distancia2 = []
            indices = []
            for i in range(len(ramas)):
                if ramas[i] not in camino: 
                    distancia2.append((ramas[i][0] - destino[0])**2 + (ramas[i][1] - destino[1])**2)
                    indices.append(i)
            if len(distancia2) > 1:
                i_min = distancia2.index(min(distancia2))
            elif len(distancia2) == 1:
                i_min = 0
            else:
                return None
            camino.append(ramas[indices[i_min]])
        return camino


    def camino(self, origen, destino, rutas):
        '''It is a systematic search of all possible ways, 
        it can take a very long time with lage puzzles.
        Uses the burbuja method always it is possible 
        it's almost ever  i have never seen the message  below'''
        caminos = self.burbuja(origen,destino,rutas)
        if caminos != None:
            return caminos
        if debug: print('Burbuja does not work, searching all possible ways, take a seat', origen, destino)
        caminos=[]
        cam = []
        cam.append(origen)
        caminos.append(cam)
        hay_camino = False
        sigue = True
        if debug_0:
            for i in rutas:
                print('rutas ', i, ':', rutas[i])
        while sigue:
            sigue = False
            for i_sendero in range(len(caminos)):
                ultimo = len(caminos[i_sendero])-1
                if caminos[i_sendero][ultimo] !=  destino and caminos[i_sendero].count(caminos[i_sendero][ultimo]) < 2:
                    cam = []
                    ramas_de_sendero = []
                    for path in caminos[i_sendero]: cam.append(path)
                    for direccion in rutas[caminos[i_sendero][ultimo]]:
                        ramas_de_sendero.append(direccion) 
                    if len(ramas_de_sendero) > 0:
                        sigue = True  
                        caminos[i_sendero].append(ramas_de_sendero.pop())
                    while len(ramas_de_sendero) > 0:
                        rm = ramas_de_sendero.pop()
                        copia_cam  = []
                        for c in cam: copia_cam.append(c)
                        copia_cam.append(rm)
                        caminos.append(copia_cam)
                        if rm == destino: hay_camino = True
            if len(caminos) > (self.filas*self.columnas +10) and hay_camino:
                if debug: print("Camino ", origen, destino, len(caminos))
                sigue = False
        i = 0
        while i < len(caminos):
            if debug_0: print("caminos i:", i, ":", caminos[i])
            if destino not in caminos[i]: 
                caminos.pop(i)
            else: i += 1
        if len(caminos) > 0:
            distancia = caminos[0]
            for i in caminos:
                if debug_0: print("caminos al final", i)
                if len(i) < len(distancia):
                    distancia = i   
            return distancia
        else:
            return None

    def pon_blanco_en(self, pos):
        ''' If you like to move a tile, 
        first you must put the empty tile near it'''
        bk = self.pos(blanco)
        rutas = {}
        self.arbol(rutas)
        cam = self.camino(bk, pos, rutas)
        if cam != None:
            for c in cam:
                if c != bk: self.mueve(c)
            return True
        else: return False

    def mueve(self, tile):
        '''slides a tile ''' 
        bk = self.pos(blanco)
        anterior = ''
        if   bk == (tile[0],   tile[1]+1): anterior = west
        elif bk == (tile[0]+1, tile[1]): anterior = norte
        elif bk == (tile[0],   tile[1]-1): anterior = este
        elif bk == (tile[0]-1, tile[1]): anterior = sur
        else:
            if debug: print("mueve, no se puede", tile, bk)
            return anterior
        self.panel[bk[0]][bk[1]] = self.panel[tile[0]][tile[1]]
        self.panel[tile[0]][tile[1]] = blanco
        self.nro_jugadas += 1
        self.lista_jugadas += anterior
        return anterior        
    
    def pon_mina(self, cc):
        '''protect a tile from been moved '''
        self.minas.append(cc)

    def pop_mina(self, mina = (-1,-1)):
        '''deletes a mine from the list'''
        if mina == (-1,-1):
            return self.minas.pop()
        elif self.minas.count(mina) > 0:
            return self.minas.pop(self.minas.index(mina))
        else:
            return None

    def print(self, txt = None ):
        '''print the panel '''
        if txt != None:
            print(txt)
        else:
            print(self.minas)
        for i in range(self.filas):
            print(" ")
            for j in range(self.columnas):
                if (i,j) not in self.minas:
                    print(self.panel[i][j],  end = "\t")
                else: print(self.panel[i][j],'*', end="\t")
        print(" ")      
        
