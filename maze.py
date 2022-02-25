import os
import random
import numpy as np
import time
class maze:
    wall = 2
    space = 3
    def __init__(self, size, ysize = None, wall = '#', space = '^'):
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


    def iswall(self,x,y):
        n = self.neighbors(x,y)
        count = 0
        if self.mz[y][x] == self.space:return False
        for i,j in n:
            if self.mz[j][i] == self.space:
                count += 1
        return count>1


    def genMaze(self):

        self.mz = np.zeros((self.ysize,self.size),dtype=np.str)
        
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
            self.printMaze()
            #breakpoint()
        print(ord)
        print(f'len:{len(ord)}\origLen:{v}')


    



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
        print(''.join(['=' for x in range(2+len(self.mz[0]))]))
        for line in self.mz:
            #print(*line,sep='')
            print('|',end='')
            for c in line:
                print(c,end='')#if c==self.wall:print('#',end='')
                #if c==self.space:print('O',end='')
            print('|')
        print(''.join(['=' for x in range(2+len(self.mz[0]))]))
        print ('\n')
        for line in self.mz:
            print(*line, sep='')

if __name__ == '__main__':
    m = maze(8,ysize=20)
    m.printMaze()

