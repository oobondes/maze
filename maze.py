import os
import random
import numpy as np
import colorama as color
import os
import pygame
import time
import platform
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

clear = 'cls' if platform.system() == 'Windows' else 'clear'
win = \
    r"""    ____     __   ,-----.      ___    _         .--.      .--..-./`) ,---.   .--. 
   \   \   /  /.'  .-,  '.  .'   |  | |        |  |_     |  |\ .-.')|    \  |  | 
    \  _. /  '/ ,-.|  \ _ \ |   .'  | |        | _( )_   |  |/ `-' \|  ,  \ |  | 
     _( )_ .';  \  '_ /  | :.'  '_  | |        |(_ o _)  |  | `-'`"`|  |\_ \|  | 
 ___(_ o _)' |  _`,/ \ _/  |'   ( \.-.|        | (_,_) \ |  | .---. |  _( )_\  | 
|   |(_,_)'  : (  '\_/ \   ;' (`. _` /|        |  |/    \|  | |   | | (_ o _)  | 
|   `-'  /    \ `"/  \  ) / | (_ (_) _)        |  '  /\  `  | |   | |  (_,_)\  | 
 \      /      '. \_/``".'   \ /  . \ /        |    /  \    | |   | |  |    |  | 
  `-..-'         '-----'      ``-'`-''         `---'    `---` '---' '--'    '--' 
                                                                                 """
color.init(autoreset=True)

class maze:
    wall = 2
    space = 3
    def __init__(self, size, ysize = None, wall = '#', space = ' '):
        self.wall = wall
        self.space = space
        self.ysize = ysize if ysize else size
        self.size = size
        self.mz = np.zeros((self.size+2,self.size+2), np.int8)
        self.mz[0] = np.ones((self.size+2), np.int8)
        self.mz[-1] = np.ones((self.size+2), np.int8)
        for i in range(1, self.size+1):
            self.mz[i][0] = 1
            self.mz[i][-1] = 1
        self.genMaze()
        #self.divide(0,0,self.size,self.size)
        #self.mz = [['#' for x in range(self.size)] for y in range(self.size)]
        #self.genMaze()

    #might be useless and worth gettign rid of========================================================
    def horizontal(l, h):
        if l==h:
            return [True,False][random.randint(0,1)]
        return h>l

    def neighbors(self,x,y, shuf = True):
        n = list()
        for i,j in [[x+1,y],[x-1,y],[x,y+1],[x,y-1]]:
            if 0<=i<self.size and 0<=j<self.ysize:
                n.append([i,j])
        if shuf:random.shuffle(n)
        return n

    def spaces(self, x, y):
        s = list()
        for i,j in [[x+1,y],[x-1,y],[x,y+1],[x,y-1]]:
            if 0<=i<self.size and 0<=j<self.ysize:
                s.append([i,j])
            else:
                s.append([])
        return s

    def iswall(self,x,y):
        n = self.neighbors(x,y)
        count = 0
        if self.mz[y][x] == self.space:return False
        for i,j in n:
            if self.mz[j][i] == self.space:
                count += 1
        return count>1

#this code was copy and pasted and does not work yet
#FIX THIS HERE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def solve(self):
        prev = dict()
        dst = dict()
        q = list()
        for y in range(len(self.mz)):
            for x in range(len(self.mz[0])):
                if self.mz[y][x] == self.space:
                    prev[f'{x},{y}'] = ''
                    dst[f'{x},{y}'] = 99999
                    q.append(f'{x},{y}')
        dst[f'{self.curs[0]},{self.curs[1]}'] = 0
        next = [f'{self.curs[0]},{self.curs[1]}']
        while q:
            u = next.pop(0)
            del q[q.index(u)]
            x,y = [int(i) for i in u.split(',')]
            for pt in [[x+1,y],[x,y+1],[x-1,y],[x,y-1]]:
                if 0<=pt[0]<=self.size and 0<=pt[1]<=self.ysize and f'{pt[0]},{pt[1]}' in q:
                    alt = dst[u] + 1
                    v=f'{pt[0]},{pt[1]}'
                    if alt < dst[v]:
                        dst[v] = alt
                        prev[v] = u
                        next.append(v)
            next.sort(key=lambda x: dst[x])
            if u == f'{self.goal[0]},{self.goal[1]}':
                break
        route = []
        pointer = f'{self.goal[0]},{self.goal[1]}'
        
        while True:
            if pointer == '':break
            tmp = prev[pointer]
            route.insert(0,tmp)
            pointer = tmp
            if tmp == f'{self.curs[0]},{self.curs[1]}':
                break 
        for pt in route:
            self.curs = [int(i) for i in pt.split(',')]
            self.printMaze()
            time.sleep(.15)


    def genMaze(self):

        self.mz = np.zeros((self.ysize,self.size),dtype=str)
        
        unvisited = list()
        for x in range(self.size):
            for y in range(self.ysize):
                unvisited.append([x,y])
        random.shuffle(unvisited)
        next = [unvisited[0]]
        v = len(unvisited)

        ord = list()
        while unvisited and next:
            u = next[0]
            ord.append(u)
            del next[0]
            try:
                unvisited.remove(u)
            except:
                pass
            x, y = u[0],u[1]
            if self.mz[y][x] != 0:pass
            if self.mz[y][x] != 0:
                pass
            self.mz[y][x] = self.space
            neighb = self.neighbors(x,y)
            for i,j in neighb:
                if [i,j] in unvisited:
                    if self.iswall(i,j):
                        self.mz[j][i]=self.wall
                        try:
                            unvisited.remove([i,j])
                        except:
                            pass
                        try:
                            next.remove([i,j])
                        except:
                            pass
                    else:
                        if [i,j] not in next:
                            next.insert(0,[i,j])   #append([i,j])
            #self.printMaze()
            #breakpoint()
        #print(ord)
        #print(f'len:{len(ord)}\origLen:{v}')
        for i in range(len(self.mz)):
            for j in range(len(self.mz[0])):
                if self.mz[i][j] == '0':
                    self.mz[i][j] = self.wall
        self.curs=[np.where(self.mz[0] == self.space)[0][0],0]
        self.goal=[np.where(self.mz[0] == self.space)[0][-1],self.ysize-1]


    



    def genMaze2(self):
        self.mz = np.ones((self.size+2,self.size+2), np.dtype.str)
        q = [f'{x}-{y}' for x in range(1,self.size+1) for y in range(1,self.size+1)]
        nxt = [q[0]]

        while nxt:
            self.printMaze()
            u = nxt[0]
            del nxt[0]
            q.remove(u)

            x,y = [int(i) for i in u.split('-')]
            self.mz[y][x] = 0
            for pt in [[x+1,y+1],[x-1,y+1],[x-1,y+1],[x-1,y-1]]:
                if 0<=pt[0]<=self.size and 0<=pt[1]<=self.size and f'{pt[0]}-{pt[1]}' in q:
                    #if not (f'{pt[0]+1}-{pt[1]}' in q and f'{pt[0]-1}-{pt[1]}' in q) or not (f'{pt[0]}-{pt[1]+1}' in q and f'{pt[0]}-{pt[1]-1}' in q):
                    if self.mz[pt[1]][pt[0]+1] ==  self.mz[pt[1]+1][pt[0]+1] == self.mz[pt[1]+1][pt[0]] == 0:
                        q.remove(f'{pt[0]}-{pt[1]}')
            for pt in [[x+1,y],[x,y+1],[x-1,y],[x,y-1]]:
                if 0<=pt[0]<=self.size and 0<=pt[1]<=self.size and f'{pt[0]}-{pt[1]}' in q:
                    nxt.append(f'{pt[0]}-{pt[1]}')
            #random.shuffle(nxt)


    

    def printMaze(self):
        mz_s = ''
        #print(''.join([color.Back.GREEN+'=' for x in range(2+len(self.mz[0]))]))
        mz_s+= color.Back.GREEN + '='*(2+len(self.mz[0])) + color.Back.RESET + '\n'
        for i, line in enumerate(self.mz):
            #print(color.Back.GREEN +'|',end='')
            mz_s += color.Back.GREEN +'|'

            for j, c in enumerate(line):
                if i==self.curs[1] and j==self.curs[0]:
                    #print(color.Back.BLUE+' ',end='')
                    mz_s+= color.Back.BLUE+' '
                    continue
                if i==self.goal[1] and j==self.goal[0]:
                    #print(color.Back.BLUE+' ',end='')
                    mz_s+= color.Back.RED+' '
                    continue
                if c==self.wall:
                    #print(color.Back.GREEN +'*',end='')
                    mz_s+= color.Back.GREEN+' '
                elif c==self.space:
                   #print(color.Back.BLACK + self.space,end='')
                    mz_s+= color.Back.YELLOW +' '
                else: 
                    #print(color.Back.RED+c,end='')
                    mz_s+= color.Back.YELLOW+' '
            #print(color.Back.GREEN +'|')
            mz_s+= color.Back.GREEN+'|' + color.Back.RESET + '\n'
        #print(''.join([color.Back.GREEN+'=' for x in range(2+len(self.mz[0]))]))
        mz_s+= color.Back.GREEN + '='*(2+len(self.mz[0])) +color.Back.RESET +   '\n'
        print ('\n')
        os.system(clear)
        print(mz_s)

    def left(self):
        x,y = self.curs
        if x-1 >= 0:
            if self.mz[y][x-1] == self.space:
                self.curs=[x-1,y]
        return

    def right(self):
        x,y = self.curs
        if x-1 <= self.size:
            if self.mz[y][x+1] == self.space:
                self.curs=[x+1,y]
        return

    def up(self):
        x,y = self.curs
        if y-1 >= 0:
            if self.mz[y-1][x] == self.space:
                self.curs=[x,y-1]
        return

    def down(self):
        x,y = self.curs
        if y+1 <= self.ysize:
            if self.mz[y+1][x] == self.space:
                self.curs=[x,y+1]
        return

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        running = True
        while running:
            if self.curs == self.goal:
                print(win)
                return
            # Look at every event in the queue
            for event in pygame.event.get():
                # Did the user hit a key?
                if event.type == KEYDOWN:
                    # Was it the Escape key? If so, stop the loop.
                    if event.key == K_ESCAPE:
                        self.solve()
                        #running = False
                    if event.key == K_DOWN:
                        self.down()
                    if event.key == K_UP:
                        self.up()
                    if event.key == K_LEFT:
                        self.left()
                    if event.key == K_RIGHT:
                        self.right()
                   # if even.key == pygame.locals.K_LCTRL:
                   #     self.solve()
                    self.printMaze()

                    # Did the user click the window close button? If so, stop the loop.
                    if event.key == K_ESCAPE:
                        running = False
            



if __name__ == '__main__':
    size = os.get_terminal_size()
    m = maze(size.columns-3,size.lines-3)
    m.printMaze()
    m.run()