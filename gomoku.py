import numpy as np
from graphics import *
import time
import pyautogui

x = 15 #棋盘行数
y = 15 #棋盘列数

chessboard = np.zeros((x,y), dtype = int) #初始化棋盘 __=0 ○=-1 ●=1

move = 0

def windows():
    global move,win,piece,newpiece
    
    win=GraphWin("Gomoku",1200,1200) #绘制窗口
    win.setBackground(color_rgb(227,188,116))
    
    linex = liney = 75
    
    while linex < 1126: #绘制棋盘网格
        line = Line(Point(linex,75),Point(linex,1126))
        line.draw(win)
        linex += 75
        
    while liney < 1126:
        line = Line(Point(75,liney),Point(1126,liney))
        line.draw(win)
        liney += 75

    tianyuan = Circle(Point(7 * 75 + 75, 7 * 75 + 75),8) #绘制天元
    tianyuan.setFill("black")
    tianyuan.draw(win)
    
    xingwei = Circle(Point(3 * 75 + 75, 3 * 75 + 75),8) #绘制星位
    xingwei.setFill("black")
    xingwei.draw(win)
    
    xingwei = Circle(Point(3 * 75 + 75, 11 * 75 + 75),8)
    xingwei.setFill("black")
    xingwei.draw(win)
    
    xingwei = Circle(Point(11 * 75 + 75, 3 * 75 + 75),8)
    xingwei.setFill("black")
    xingwei.draw(win)
    
    xingwei = Circle(Point(11 * 75 + 75, 11 * 75 + 75),8)
    xingwei.setFill("black")
    xingwei.draw(win)
    
    for i in range(10000): #下棋
        
        mouse = win.getMouse()
        posx = round(mouse.getX() / 75) - 1
        posy = round(mouse.getY() / 75) - 1
        
        if posx < 0 or posx > 14 or posy < 0 or posy > 14 or \
           chessboard[posx][posy] != 0: #判断是否超出范围或已有棋子
            continue
        
        if move % 2 == 0 and chessboard[posx][posy] == 0: #判断○●和是否有棋子
            chessboard[posx][posy] = 1
            piece = Circle(Point(posx * 75 + 75, posy * 75 + 75),30)
            piece.setFill("black")
            
        if move % 2 == 1 and chessboard[posx][posy] == 0:
            chessboard[posx][posy] = -1
            piece = Circle(Point(posx * 75 + 75, posy * 75 + 75),30)
            piece.setFill("white")
            
        piece.draw(win) #绘制棋子
        move += 1 #手数

        if "newpiece" in globals(): #如果存在,删除上一手棋子高亮
            newpiece.undraw()
        
        newpiece = Polygon(Point(posx * 75 + 75, posy * 75 + 75), \
                           Point(posx * 75 + 75 + 30, posy * 75 + 75), \
                           Point(posx * 75 + 75, posy * 75 + 75 + 30))
        newpiece.setOutline("red")
        newpiece.setFill("red")
        newpiece.draw(win) #绘制上一手棋子高亮
        
        print("评分：",score())
        if bwin == True:
            pyautogui.alert("Black win!", title="Prompt")
            win.getMouse()
            win.close()
            
        if move > 2:
            start=time.time()
            ai(-1)
            print("评分：",score())
            end=time.time()
            print("%0.4f"%(end-start),"s")
            
def lw(chess): #连五判断，●●●●●
    global x,y
    amount = 0
    
    for i in range(x): #横向

        for j in range(y-5+1):
            if chessboard[i][j] == chess and \
               chessboard[i][j+1] == chess and \
               chessboard[i][j+2] == chess and \
               chessboard[i][j+3] == chess and \
               chessboard[i][j+4] == chess:
                amount += 1

    for i in range(x-5+1): #纵向

        for j in range(y):
            if chessboard[i][j] == chess and \
               chessboard[i+1][j] == chess and \
               chessboard[i+2][j] == chess and \
               chessboard[i+3][j] == chess and \
               chessboard[i+4][j] == chess:
                amount += 1

    for i in range(x-5+1): #斜向，左上到右下

        for j in range(y-5+1):
            if chessboard[i][j] == chess and \
               chessboard[i+1][j+1] == chess and \
               chessboard[i+2][j+2] == chess and \
               chessboard[i+3][j+3] == chess and \
               chessboard[i+4][j+4] == chess:
                amount += 1

    for i in range(x-5+1): #斜向，右上到左下

        for j in range(5-1,y):
            if chessboard[i][j] == chess and \
               chessboard[i+1][j-1] == chess and \
               chessboard[i+2][j-2] == chess and \
               chessboard[i+3][j-3] == chess and \
               chessboard[i+4][j-4] == chess:
                amount += 1

    return amount

def hs(chess): #活四判断，__●●●●__
    global x,y
    amount = 0
    
    for i in range(x): #横向

        for j in range(y-6+1):
            if chessboard[i][j] == 0 and \
               chessboard[i][j+1] == chess and \
               chessboard[i][j+2] == chess and \
               chessboard[i][j+3] == chess and \
               chessboard[i][j+4] == chess and \
               chessboard[i][j+5] == 0:
                amount += 1

    for i in range(x-6+1): #纵向

        for j in range(y):
            if chessboard[i][j] == 0 and \
               chessboard[i+1][j] == chess and \
               chessboard[i+2][j] == chess and \
               chessboard[i+3][j] == chess and \
               chessboard[i+4][j] == chess and \
               chessboard[i+5][j] == 0:
                amount += 1

    for i in range(x-6+1): #斜向，左上到右下

        for j in range(y-6+1):
            if chessboard[i][j] == 0 and \
               chessboard[i+1][j+1] == chess and \
               chessboard[i+2][j+2] == chess and \
               chessboard[i+3][j+3] == chess and \
               chessboard[i+4][j+4] == chess and \
               chessboard[i+5][j+5] == 0:
                amount += 1

    for i in range(x-6+1): #斜向，右上到左下

        for j in range(6-1,y):
            if chessboard[i][j] == 0 and \
               chessboard[i+1][j-1] == chess and \
               chessboard[i+2][j-2] == chess and \
               chessboard[i+3][j-3] == chess and \
               chessboard[i+4][j-4] == chess and \
               chessboard[i+5][j-5] == 0:
                amount += 1

    return amount

def ssa(chess): #死四判断A，__●●●●○，不考虑边界
    global x,y
    amount = 0

    for i in range(x): #横向

        for j in range(y-6+1):
            if chessboard[i][j] == 0 and \
               chessboard[i][j+1] == chess and \
               chessboard[i][j+2] == chess and \
               chessboard[i][j+3] == chess and \
               chessboard[i][j+4] == chess and \
               chessboard[i][j+5] == chess*-1:
                amount += 1

    for i in range(x): #横向，反向

        for j in range(y-6+1):
            if chessboard[i][j] == chess*-1 and \
               chessboard[i][j+1] == chess and \
               chessboard[i][j+2] == chess and \
               chessboard[i][j+3] == chess and \
               chessboard[i][j+4] == chess and \
               chessboard[i][j+5] == 0:
                amount += 1

    for i in range(x-6+1): #纵向

        for j in range(y):
            if chessboard[i][j] == 0 and \
               chessboard[i+1][j] == chess and \
               chessboard[i+2][j] == chess and \
               chessboard[i+3][j] == chess and \
               chessboard[i+4][j] == chess and \
               chessboard[i+5][j] == chess*-1:
                amount += 1

    for i in range(x-6+1): #纵向，反向

        for j in range(y):
            if chessboard[i][j] == chess*-1 and \
               chessboard[i+1][j] == chess and \
               chessboard[i+2][j] == chess and \
               chessboard[i+3][j] == chess and \
               chessboard[i+4][j] == chess and \
               chessboard[i+5][j] == 0:
                amount += 1

    for i in range(x-6+1): #斜向，左上到右下

        for j in range(y-6+1):
            if chessboard[i][j] == 0 and \
               chessboard[i+1][j+1] == chess and \
               chessboard[i+2][j+2] == chess and \
               chessboard[i+3][j+3] == chess and \
               chessboard[i+4][j+4] == chess and \
               chessboard[i+5][j+5] == chess*-1:
                amount += 1

    for i in range(x-6+1): #斜向，左上到右下，反向

        for j in range(y-6+1):
            if chessboard[i][j] == chess*-1 and \
               chessboard[i+1][j+1] == chess and \
               chessboard[i+2][j+2] == chess and \
               chessboard[i+3][j+3] == chess and \
               chessboard[i+4][j+4] == chess and \
               chessboard[i+5][j+5] == 0:
                amount += 1

    for i in range(x-6+1): #斜向，右上到左下

        for j in range(6-1,y):
            if chessboard[i][j] == 0 and \
               chessboard[i+1][j-1] == chess and \
               chessboard[i+2][j-2] == chess and \
               chessboard[i+3][j-3] == chess and \
               chessboard[i+4][j-4] == chess and \
               chessboard[i+5][j-5] == chess*-1:
                amount += 1

    for i in range(x-6+1): #斜向，右上到左下，反向

        for j in range(6-1,y):
            if chessboard[i][j] == chess*-1 and \
               chessboard[i+1][j-1] == chess and \
               chessboard[i+2][j-2] == chess and \
               chessboard[i+3][j-3] == chess and \
               chessboard[i+4][j-4] == chess and \
               chessboard[i+5][j-5] == 0:
                amount += 1

    return amount

def ssb(chess): #死四判断B，●__●●●
    global x,y
    amount = 0

    for i in range(x): #横向

        for j in range(y-5+1):
            if chessboard[i][j] == chess and \
               chessboard[i][j+1] == 0 and \
               chessboard[i][j+2] == chess and \
               chessboard[i][j+3] == chess and \
               chessboard[i][j+4] == chess:
                amount += 1

    for i in range(x): #横向，反向

        for j in range(y-5+1):
            if chessboard[i][j] == chess and \
               chessboard[i][j+1] == chess and \
               chessboard[i][j+2] == chess and \
               chessboard[i][j+3] == 0 and \
               chessboard[i][j+4] == chess:
                amount += 1

    for i in range(x-5+1): #纵向

        for j in range(y):
            if chessboard[i][j] == chess and \
               chessboard[i+1][j] == 0 and \
               chessboard[i+2][j] == chess and \
               chessboard[i+3][j] == chess and \
               chessboard[i+4][j] == chess:
                amount += 1

    for i in range(x-5+1): #纵向，反向

        for j in range(y):
            if chessboard[i][j] == chess and \
               chessboard[i+1][j] == chess and \
               chessboard[i+2][j] == chess and \
               chessboard[i+3][j] == 0 and \
               chessboard[i+4][j] == chess:
                amount += 1

    for i in range(x-5+1): #斜向，左上到右下

        for j in range(y-5+1):
            if chessboard[i][j] == chess and \
               chessboard[i+1][j+1] == 0 and \
               chessboard[i+2][j+2] == chess and \
               chessboard[i+3][j+3] == chess and \
               chessboard[i+4][j+4] == chess:
                amount += 1

    for i in range(x-5+1): #斜向，左上到右下，反向

        for j in range(y-5+1):
            if chessboard[i][j] == chess and \
               chessboard[i+1][j+1] == chess and \
               chessboard[i+2][j+2] == chess and \
               chessboard[i+3][j+3] == 0 and \
               chessboard[i+4][j+4] == chess:
                amount += 1

    for i in range(x-5+1): #斜向，右上到左下

        for j in range(5-1,y):
            if chessboard[i][j] == chess and \
               chessboard[i+1][j-1] == 0 and \
               chessboard[i+2][j-2] == chess and \
               chessboard[i+3][j-3] == chess and \
               chessboard[i+4][j-4] == chess:
                amount += 1

    for i in range(x-5+1): #斜向，右上到左下，反向

        for j in range(5-1,y):
            if chessboard[i][j] == chess and \
               chessboard[i+1][j-1] == chess and \
               chessboard[i+2][j-2] == chess and \
               chessboard[i+3][j-3] == 0 and \
               chessboard[i+4][j-4] == chess:
                amount += 1

    return amount

def ssc(chess): #死四判断C，●●__●●
    global x,y
    amount = 0
    
    for i in range(x): #横向

        for j in range(y-5+1):
            if chessboard[i][j] == chess and \
               chessboard[i][j+1] == chess and \
               chessboard[i][j+2] == 0 and \
               chessboard[i][j+3] == chess and \
               chessboard[i][j+4] == chess:
                amount += 1

    for i in range(x-5+1): #纵向

        for j in range(y):
            if chessboard[i][j] == chess and \
               chessboard[i+1][j] == chess and \
               chessboard[i+2][j] == 0 and \
               chessboard[i+3][j] == chess and \
               chessboard[i+4][j] == chess:
                amount += 1

    for i in range(x-5+1): #斜向，左上到右下

        for j in range(y-5+1):
            if chessboard[i][j] == chess and \
               chessboard[i+1][j+1] == chess and \
               chessboard[i+2][j+2] == 0 and \
               chessboard[i+3][j+3] == chess and \
               chessboard[i+4][j+4] == chess:
                amount += 1

    for i in range(x-5+1): #斜向，右上到左下

        for j in range(5-1,y):
            if chessboard[i][j] == chess and \
               chessboard[i+1][j-1] == chess and \
               chessboard[i+2][j-2] == 0 and \
               chessboard[i+3][j-3] == chess and \
               chessboard[i+4][j-4] == chess:
                amount += 1

    return amount

def hsana(chess): #活三判断A，__●●●__
    global x,y
    amount = 0
    
    for i in range(x): #横向

        for j in range(y-5+1):
            if chessboard[i][j] == 0 and \
               chessboard[i][j+1] == chess and \
               chessboard[i][j+2] == chess and \
               chessboard[i][j+3] == chess and \
               chessboard[i][j+4] == 0:
                amount += 1

    for i in range(x-5+1): #纵向

        for j in range(y):
            if chessboard[i][j] == 0 and \
               chessboard[i+1][j] == chess and \
               chessboard[i+2][j] == chess and \
               chessboard[i+3][j] == chess and \
               chessboard[i+4][j] == 0:
                amount += 1

    for i in range(x-5+1): #斜向，左上到右下

        for j in range(y-5+1):
            if chessboard[i][j] == 0 and \
               chessboard[i+1][j+1] == chess and \
               chessboard[i+2][j+2] == chess and \
               chessboard[i+3][j+3] == chess and \
               chessboard[i+4][j+4] == 0:
                amount += 1

    for i in range(x-5+1): #斜向，右上到左下

        for j in range(5-1,y):
            if chessboard[i][j] == 0 and \
               chessboard[i+1][j-1] == chess and \
               chessboard[i+2][j-2] == chess and \
               chessboard[i+3][j-3] == chess and \
               chessboard[i+4][j-4] == 0:
                amount += 1

    return amount

def hsanb(chess): #活三判断B，__●__●●__，不考虑边界
    global x,y
    amount = 0

    for i in range(x): #横向

        for j in range(y-6+1):
            if chessboard[i][j] == 0 and \
               chessboard[i][j+1] == chess and \
               chessboard[i][j+2] == 0 and \
               chessboard[i][j+3] == chess and \
               chessboard[i][j+4] == chess and \
               chessboard[i][j+5] == 0:
                amount += 1

    for i in range(x): #横向，反向

        for j in range(y-6+1):
            if chessboard[i][j] == 0 and \
               chessboard[i][j+1] == chess and \
               chessboard[i][j+2] == chess and \
               chessboard[i][j+3] == 0 and \
               chessboard[i][j+4] == chess and \
               chessboard[i][j+5] == 0:
                amount += 1

    for i in range(x-6+1): #纵向

        for j in range(y):
            if chessboard[i][j] == 0 and \
               chessboard[i+1][j] == chess and \
               chessboard[i+2][j] == 0 and \
               chessboard[i+3][j] == chess and \
               chessboard[i+4][j] == chess and \
               chessboard[i+5][j] == 0:
                amount += 1

    for i in range(x-6+1): #纵向，反向

        for j in range(y):
            if chessboard[i][j] == 0 and \
               chessboard[i+1][j] == chess and \
               chessboard[i+2][j] == chess and \
               chessboard[i+3][j] == 0 and \
               chessboard[i+4][j] == chess and \
               chessboard[i+5][j] == 0:
                amount += 1

    for i in range(x-6+1): #斜向，左上到右下

        for j in range(y-6+1):
            if chessboard[i][j] == 0 and \
               chessboard[i+1][j+1] == chess and \
               chessboard[i+2][j+2] == 0 and \
               chessboard[i+3][j+3] == chess and \
               chessboard[i+4][j+4] == chess and \
               chessboard[i+5][j+5] == 0:
                amount += 1

    for i in range(x-6+1): #斜向，左上到右下，反向

        for j in range(y-6+1):
            if chessboard[i][j] == 0 and \
               chessboard[i+1][j+1] == chess and \
               chessboard[i+2][j+2] == chess and \
               chessboard[i+3][j+3] == 0 and \
               chessboard[i+4][j+4] == chess and \
               chessboard[i+5][j+5] == 0:
                amount += 1

    for i in range(x-6+1): #斜向，右上到左下

        for j in range(6-1,y):
            if chessboard[i][j] == 0 and \
               chessboard[i+1][j-1] == chess and \
               chessboard[i+2][j-2] == 0 and \
               chessboard[i+3][j-3] == chess and \
               chessboard[i+4][j-4] == chess and \
               chessboard[i+5][j-5] == 0:
                amount += 1

    for i in range(x-6+1): #斜向，右上到左下，反向

        for j in range(6-1,y):
            if chessboard[i][j] == 0 and \
               chessboard[i+1][j-1] == chess and \
               chessboard[i+2][j-2] == chess and \
               chessboard[i+3][j-3] == 0 and \
               chessboard[i+4][j-4] == chess and \
               chessboard[i+5][j-5] == 0:
                amount += 1

    return amount

def ssana(chess): #死三判断A，____●●●○，不考虑边界
    global x,y
    amount = 0

    for i in range(x): #横向

        for j in range(y-6+1):
            if chessboard[i][j] == 0 and \
               chessboard[i][j+1] == 0 and \
               chessboard[i][j+2] == chess and \
               chessboard[i][j+3] == chess and \
               chessboard[i][j+4] == chess and \
               chessboard[i][j+5] == chess*-1:
                amount += 1

    for i in range(x): #横向，反向

        for j in range(y-6+1):
            if chessboard[i][j] == chess*-1 and \
               chessboard[i][j+1] == chess and \
               chessboard[i][j+2] == chess and \
               chessboard[i][j+3] == chess and \
               chessboard[i][j+4] == 0 and \
               chessboard[i][j+5] == 0:
                amount += 1

    for i in range(x-6+1): #纵向

        for j in range(y):
            if chessboard[i][j] == 0 and \
               chessboard[i+1][j] == 0 and \
               chessboard[i+2][j] == chess and \
               chessboard[i+3][j] == chess and \
               chessboard[i+4][j] == chess and \
               chessboard[i+5][j] == chess*-1:
                amount += 1

    for i in range(x-6+1): #纵向，反向

        for j in range(y):
            if chessboard[i][j] == chess*-1 and \
               chessboard[i+1][j] == chess and \
               chessboard[i+2][j] == chess and \
               chessboard[i+3][j] == chess and \
               chessboard[i+4][j] == 0 and \
               chessboard[i+5][j] == 0:
                amount += 1

    for i in range(x-6+1): #斜向，左上到右下

        for j in range(y-6+1):
            if chessboard[i][j] == 0 and \
               chessboard[i+1][j+1] == 0 and \
               chessboard[i+2][j+2] == chess and \
               chessboard[i+3][j+3] == chess and \
               chessboard[i+4][j+4] == chess and \
               chessboard[i+5][j+5] == chess*-1:
                amount += 1

    for i in range(x-6+1): #斜向，左上到右下，反向

        for j in range(y-6+1):
            if chessboard[i][j] == chess*-1 and \
               chessboard[i+1][j+1] == chess and \
               chessboard[i+2][j+2] == chess and \
               chessboard[i+3][j+3] == chess and \
               chessboard[i+4][j+4] == 0 and \
               chessboard[i+5][j+5] == 0:
                amount += 1

    for i in range(x-6+1): #斜向，右上到左下

        for j in range(6-1,y):
            if chessboard[i][j] == 0 and \
               chessboard[i+1][j-1] == 0 and \
               chessboard[i+2][j-2] == chess and \
               chessboard[i+3][j-3] == chess and \
               chessboard[i+4][j-4] == chess and \
               chessboard[i+5][j-5] == chess*-1:
                amount += 1

    for i in range(x-6+1): #斜向，右上到左下，反向

        for j in range(6-1,y):
            if chessboard[i][j] == chess*-1 and \
               chessboard[i+1][j-1] == chess and \
               chessboard[i+2][j-2] == chess and \
               chessboard[i+3][j-3] == chess and \
               chessboard[i+4][j-4] == 0 and \
               chessboard[i+5][j-5] == 0:
                amount += 1

    return amount

def ssanb(chess): #死三判断B，__●__●●○，不考虑边界
    global x,y
    amount = 0

    for i in range(x): #横向

        for j in range(y-6+1):
            if chessboard[i][j] == 0 and \
               chessboard[i][j+1] == chess and \
               chessboard[i][j+2] == 0 and \
               chessboard[i][j+3] == chess and \
               chessboard[i][j+4] == chess and \
               chessboard[i][j+5] == chess*-1:
                amount += 1

    for i in range(x): #横向，反向

        for j in range(y-6+1):
            if chessboard[i][j] == chess*-1 and \
               chessboard[i][j+1] == chess and \
               chessboard[i][j+2] == chess and \
               chessboard[i][j+3] == 0 and \
               chessboard[i][j+4] == chess and \
               chessboard[i][j+5] == 0:
                amount += 1

    for i in range(x-6+1): #纵向

        for j in range(y):
            if chessboard[i][j] == 0 and \
               chessboard[i+1][j] == chess and \
               chessboard[i+2][j] == 0 and \
               chessboard[i+3][j] == chess and \
               chessboard[i+4][j] == chess and \
               chessboard[i+5][j] == chess*-1:
                amount += 1

    for i in range(x-6+1): #纵向，反向

        for j in range(y):
            if chessboard[i][j] == chess*-1 and \
               chessboard[i+1][j] == chess and \
               chessboard[i+2][j] == chess and \
               chessboard[i+3][j] == 0 and \
               chessboard[i+4][j] == chess and \
               chessboard[i+5][j] == 0:
                amount += 1

    for i in range(x-6+1): #斜向，左上到右下

        for j in range(y-6+1):
            if chessboard[i][j] == 0 and \
               chessboard[i+1][j+1] == chess and \
               chessboard[i+2][j+2] == 0 and \
               chessboard[i+3][j+3] == chess and \
               chessboard[i+4][j+4] == chess and \
               chessboard[i+5][j+5] == chess*-1:
                amount += 1

    for i in range(x-6+1): #斜向，左上到右下，反向

        for j in range(y-6+1):
            if chessboard[i][j] == chess*-1 and \
               chessboard[i+1][j+1] == chess and \
               chessboard[i+2][j+2] == chess and \
               chessboard[i+3][j+3] == 0 and \
               chessboard[i+4][j+4] == chess and \
               chessboard[i+5][j+5] == 0:
                amount += 1

    for i in range(x-6+1): #斜向，右上到左下

        for j in range(6-1,y):
            if chessboard[i][j] == 0 and \
               chessboard[i+1][j-1] == chess and \
               chessboard[i+2][j-2] == 0 and \
               chessboard[i+3][j-3] == chess and \
               chessboard[i+4][j-4] == chess and \
               chessboard[i+5][j-5] == chess*-1:
                amount += 1

    for i in range(x-6+1): #斜向，右上到左下，反向

        for j in range(6-1,y):
            if chessboard[i][j] == chess*-1 and \
               chessboard[i+1][j-1] == chess and \
               chessboard[i+2][j-2] == chess and \
               chessboard[i+3][j-3] == 0 and \
               chessboard[i+4][j-4] == chess and \
               chessboard[i+5][j-5] == 0:
                amount += 1

    return amount

def ssanc(chess): #死三判断C，__●●__●○，不考虑边界
    global x,y
    amount = 0

    for i in range(x): #横向

        for j in range(y-6+1):
            if chessboard[i][j] == 0 and \
               chessboard[i][j+1] == chess and \
               chessboard[i][j+2] == chess and \
               chessboard[i][j+3] == 0 and \
               chessboard[i][j+4] == chess and \
               chessboard[i][j+5] == chess*-1:
                amount += 1

    for i in range(x): #横向，反向

        for j in range(y-6+1):
            if chessboard[i][j] == chess*-1 and \
               chessboard[i][j+1] == chess and \
               chessboard[i][j+2] == 0 and \
               chessboard[i][j+3] == chess and \
               chessboard[i][j+4] == chess and \
               chessboard[i][j+5] == 0:
                amount += 1

    for i in range(x-6+1): #纵向

        for j in range(y):
            if chessboard[i][j] == 0 and \
               chessboard[i+1][j] == chess and \
               chessboard[i+2][j] == chess and \
               chessboard[i+3][j] == 0 and \
               chessboard[i+4][j] == chess and \
               chessboard[i+5][j] == chess*-1:
                amount += 1

    for i in range(x-6+1): #纵向，反向

        for j in range(y):
            if chessboard[i][j] == chess*-1 and \
               chessboard[i+1][j] == chess and \
               chessboard[i+2][j] == 0 and \
               chessboard[i+3][j] == chess and \
               chessboard[i+4][j] == chess and \
               chessboard[i+5][j] == 0:
                amount += 1

    for i in range(x-6+1): #斜向，左上到右下

        for j in range(y-6+1):
            if chessboard[i][j] == 0 and \
               chessboard[i+1][j+1] == chess and \
               chessboard[i+2][j+2] == chess and \
               chessboard[i+3][j+3] == 0 and \
               chessboard[i+4][j+4] == chess and \
               chessboard[i+5][j+5] == chess*-1:
                amount += 1

    for i in range(x-6+1): #斜向，左上到右下，反向

        for j in range(y-6+1):
            if chessboard[i][j] == chess*-1 and \
               chessboard[i+1][j+1] == chess and \
               chessboard[i+2][j+2] == 0 and \
               chessboard[i+3][j+3] == chess and \
               chessboard[i+4][j+4] == chess and \
               chessboard[i+5][j+5] == 0:
                amount += 1

    for i in range(x-6+1): #斜向，右上到左下

        for j in range(6-1,y):
            if chessboard[i][j] == 0 and \
               chessboard[i+1][j-1] == chess and \
               chessboard[i+2][j-2] == chess and \
               chessboard[i+3][j-3] == 0 and \
               chessboard[i+4][j-4] == chess and \
               chessboard[i+5][j-5] == chess*-1:
                amount += 1

    for i in range(x-6+1): #斜向，右上到左下，反向

        for j in range(6-1,y):
            if chessboard[i][j] == chess*-1 and \
               chessboard[i+1][j-1] == chess and \
               chessboard[i+2][j-2] == 0 and \
               chessboard[i+3][j-3] == chess and \
               chessboard[i+4][j-4] == chess and \
               chessboard[i+5][j-5] == 0:
                amount += 1

    return amount

def ssand(chess): #死三判断D，●____●●
    global x,y
    amount = 0

    for i in range(x): #横向

        for j in range(y-5+1):
            if chessboard[i][j] == chess and \
               chessboard[i][j+1] == 0 and \
               chessboard[i][j+2] == 0 and \
               chessboard[i][j+3] == chess and \
               chessboard[i][j+4] == chess:
                amount += 1

    for i in range(x): #横向，反向

        for j in range(y-5+1):
            if chessboard[i][j] == chess and \
               chessboard[i][j+1] == chess and \
               chessboard[i][j+2] == 0 and \
               chessboard[i][j+3] == 0 and \
               chessboard[i][j+4] == chess:
                amount += 1

    for i in range(x-5+1): #纵向

        for j in range(y):
            if chessboard[i][j] == chess and \
               chessboard[i+1][j] == 0 and \
               chessboard[i+2][j] == 0 and \
               chessboard[i+3][j] == chess and \
               chessboard[i+4][j] == chess:
                amount += 1

    for i in range(x-5+1): #纵向，反向

        for j in range(y):
            if chessboard[i][j] == chess and \
               chessboard[i+1][j] == chess and \
               chessboard[i+2][j] == 0 and \
               chessboard[i+3][j] == 0 and \
               chessboard[i+4][j] == chess:
                amount += 1

    for i in range(x-5+1): #斜向，左上到右下

        for j in range(y-5+1):
            if chessboard[i][j] == chess and \
               chessboard[i+1][j+1] == 0 and \
               chessboard[i+2][j+2] == 0 and \
               chessboard[i+3][j+3] == chess and \
               chessboard[i+4][j+4] == chess:
                amount += 1

    for i in range(x-5+1): #斜向，左上到右下，反向

        for j in range(y-5+1):
            if chessboard[i][j] == chess and \
               chessboard[i+1][j+1] == chess and \
               chessboard[i+2][j+2] == 0 and \
               chessboard[i+3][j+3] == 0 and \
               chessboard[i+4][j+4] == chess:
                amount += 1

    for i in range(x-5+1): #斜向，右上到左下

        for j in range(5-1,y):
            if chessboard[i][j] == chess and \
               chessboard[i+1][j-1] == 0 and \
               chessboard[i+2][j-2] == 0 and \
               chessboard[i+3][j-3] == chess and \
               chessboard[i+4][j-4] == chess:
                amount += 1

    for i in range(x-5+1): #斜向，右上到左下，反向

        for j in range(5-1,y):
            if chessboard[i][j] == chess and \
               chessboard[i+1][j-1] == chess and \
               chessboard[i+2][j-2] == 0 and \
               chessboard[i+3][j-3] == 0 and \
               chessboard[i+4][j-4] == chess:
                amount += 1

    return amount

def ssane(chess): #死三判断E，●__●__●
    global x,y
    amount = 0

    for i in range(x): #横向

        for j in range(y-5+1):
            if chessboard[i][j] == chess and \
               chessboard[i][j+1] == 0 and \
               chessboard[i][j+2] == chess and \
               chessboard[i][j+3] == 0 and \
               chessboard[i][j+4] == chess:
                amount += 1
                
    for i in range(x-5+1): #纵向

        for j in range(y):
            if chessboard[i][j] == chess and \
               chessboard[i+1][j] == 0 and \
               chessboard[i+2][j] == chess and \
               chessboard[i+3][j] == 0 and \
               chessboard[i+4][j] == chess:
                amount += 1
                
    for i in range(x-5+1): #斜向，左上到右下

        for j in range(y-5+1):
            if chessboard[i][j] == chess and \
               chessboard[i+1][j+1] == 0 and \
               chessboard[i+2][j+2] == chess and \
               chessboard[i+3][j+3] == 0 and \
               chessboard[i+4][j+4] == chess:
                amount += 1
                
    for i in range(x-5+1): #斜向，右上到左下

        for j in range(5-1,y):
            if chessboard[i][j] == chess and \
               chessboard[i+1][j-1] == 0 and \
               chessboard[i+2][j-2] == chess and \
               chessboard[i+3][j-3] == 0 and \
               chessboard[i+4][j-4] == chess:
                amount += 1
                
    return amount

def ssanf(chess): #死三判断F，○__●●●__○，不考虑边界
    global x,y
    amount = 0

    for i in range(x): #横向

        for j in range(y-7+1):
            if chessboard[i][j] == chess*-1 and \
               chessboard[i][j+1] == 0 and \
               chessboard[i][j+2] == chess and \
               chessboard[i][j+3] == chess and \
               chessboard[i][j+4] == chess and \
               chessboard[i][j+5] == 0 and \
               chessboard[i][j+6] == chess*-1:
                amount += 1
                
    for i in range(x-7+1): #纵向

        for j in range(y):
            if chessboard[i][j] == chess*-1 and \
               chessboard[i+1][j] == 0 and \
               chessboard[i+2][j] == chess and \
               chessboard[i+3][j] == chess and \
               chessboard[i+4][j] == chess and \
               chessboard[i+5][j] == 0 and \
               chessboard[i+6][j] == chess*-1:
                amount += 1
                
    for i in range(x-7+1): #斜向，左上到右下

        for j in range(y-7+1):
            if chessboard[i][j] == chess*-1 and \
               chessboard[i+1][j+1] == 0 and \
               chessboard[i+2][j+2] == chess and \
               chessboard[i+3][j+3] == chess and \
               chessboard[i+4][j+4] == chess and \
               chessboard[i+5][j+5] == 0 and \
               chessboard[i+6][j+6] == chess*-1:
                amount += 1
                
    for i in range(x-7+1): #斜向，右上到左下

        for j in range(7-1,y):
            if chessboard[i][j] == chess*-1 and \
               chessboard[i+1][j-1] == 0 and \
               chessboard[i+2][j-2] == chess and \
               chessboard[i+3][j-3] == chess and \
               chessboard[i+4][j-4] == chess and \
               chessboard[i+5][j-5] == 0 and \
               chessboard[i+6][j-6] == chess*-1:
                amount += 1
                
    return amount

def hea(chess): #活二判断A，____●●____
    global x,y
    amount = 0
    
    for i in range(x): #横向

        for j in range(y-6+1):
            if chessboard[i][j] == 0 and \
               chessboard[i][j+1] == 0 and \
               chessboard[i][j+2] == chess and \
               chessboard[i][j+3] == chess and \
               chessboard[i][j+4] == 0 and \
               chessboard[i][j+5] == 0:
                amount += 1

    for i in range(x-6+1): #纵向

        for j in range(y):
            if chessboard[i][j] == 0 and \
               chessboard[i+1][j] == 0 and \
               chessboard[i+2][j] == chess and \
               chessboard[i+3][j] == chess and \
               chessboard[i+4][j] == 0 and \
               chessboard[i+5][j] == 0:
                amount += 1

    for i in range(x-6+1): #斜向，左上到右下

        for j in range(y-6+1):
            if chessboard[i][j] == 0 and \
               chessboard[i+1][j+1] == 0 and \
               chessboard[i+2][j+2] == chess and \
               chessboard[i+3][j+3] == chess and \
               chessboard[i+4][j+4] == 0 and \
               chessboard[i+5][j+5] == 0:
                amount += 1

    for i in range(x-6+1): #斜向，右上到左下

        for j in range(6-1,y):
            if chessboard[i][j] == 0 and \
               chessboard[i+1][j-1] == 0 and \
               chessboard[i+2][j-2] == chess and \
               chessboard[i+3][j-3] == chess and \
               chessboard[i+4][j-4] == 0 and \
               chessboard[i+5][j-5] == 0:
                amount += 1

    return amount

def heb(chess): #活二判断B，__●__●__
    global x,y
    amount = 0
    
    for i in range(x): #横向

        for j in range(y-5+1):
            if chessboard[i][j] == 0 and \
               chessboard[i][j+1] == chess and \
               chessboard[i][j+2] == 0 and \
               chessboard[i][j+3] == chess and \
               chessboard[i][j+4] == 0:
                amount += 1

    for i in range(x-5+1): #纵向

        for j in range(y):
            if chessboard[i][j] == 0 and \
               chessboard[i+1][j] == chess and \
               chessboard[i+2][j] == 0 and \
               chessboard[i+3][j] == chess and \
               chessboard[i+4][j] == 0:
                amount += 1

    for i in range(x-5+1): #斜向，左上到右下

        for j in range(y-5+1):
            if chessboard[i][j] == 0 and \
               chessboard[i+1][j+1] == chess and \
               chessboard[i+2][j+2] == 0 and \
               chessboard[i+3][j+3] == chess and \
               chessboard[i+4][j+4] == 0:
                amount += 1

    for i in range(x-5+1): #斜向，右上到左下

        for j in range(5-1,y):
            if chessboard[i][j] == 0 and \
               chessboard[i+1][j-1] == chess and \
               chessboard[i+2][j-2] == 0 and \
               chessboard[i+3][j-3] == chess and \
               chessboard[i+4][j-4] == 0:
                amount += 1

    return amount

def hec(chess): #活二判断C，__●____●__
    global x,y
    amount = 0
    
    for i in range(x): #横向

        for j in range(y-6+1):
            if chessboard[i][j] == 0 and \
               chessboard[i][j+1] == chess and \
               chessboard[i][j+2] == 0 and \
               chessboard[i][j+3] == 0 and \
               chessboard[i][j+4] == chess and \
               chessboard[i][j+5] == 0:
                amount += 1

    for i in range(x-6+1): #纵向

        for j in range(y):
            if chessboard[i][j] == 0 and \
               chessboard[i+1][j] == chess and \
               chessboard[i+2][j] == 0 and \
               chessboard[i+3][j] == 0 and \
               chessboard[i+4][j] == chess and \
               chessboard[i+5][j] == 0:
                amount += 1

    for i in range(x-6+1): #斜向，左上到右下

        for j in range(y-6+1):
            if chessboard[i][j] == 0 and \
               chessboard[i+1][j+1] == chess and \
               chessboard[i+2][j+2] == 0 and \
               chessboard[i+3][j+3] == 0 and \
               chessboard[i+4][j+4] == chess and \
               chessboard[i+5][j+5] == 0:
                amount += 1

    for i in range(x-6+1): #斜向，右上到左下

        for j in range(6-1,y):
            if chessboard[i][j] == 0 and \
               chessboard[i+1][j-1] == chess and \
               chessboard[i+2][j-2] == 0 and \
               chessboard[i+3][j-3] == 0 and \
               chessboard[i+4][j-4] == chess and \
               chessboard[i+5][j-5] == 0:
                amount += 1

    return amount

def sea(chess): #死二判断A，______●●○，不考虑边界
    global x,y
    amount = 0

    for i in range(x): #横向

        for j in range(y-6+1):
            if chessboard[i][j] == 0 and \
               chessboard[i][j+1] == 0 and \
               chessboard[i][j+2] == 0 and \
               chessboard[i][j+3] == chess and \
               chessboard[i][j+4] == chess and \
               chessboard[i][j+5] == chess*-1:
                amount += 1

    for i in range(x): #横向，反向

        for j in range(y-6+1):
            if chessboard[i][j] == chess*-1 and \
               chessboard[i][j+1] == chess and \
               chessboard[i][j+2] == chess and \
               chessboard[i][j+3] == 0 and \
               chessboard[i][j+4] == 0 and \
               chessboard[i][j+5] == 0:
                amount += 1

    for i in range(x-6+1): #纵向

        for j in range(y):
            if chessboard[i][j] == 0 and \
               chessboard[i+1][j] == 0 and \
               chessboard[i+2][j] == 0 and \
               chessboard[i+3][j] == chess and \
               chessboard[i+4][j] == chess and \
               chessboard[i+5][j] == chess*-1:
                amount += 1

    for i in range(x-6+1): #纵向，反向

        for j in range(y):
            if chessboard[i][j] == chess*-1 and \
               chessboard[i+1][j] == chess and \
               chessboard[i+2][j] == chess and \
               chessboard[i+3][j] == 0 and \
               chessboard[i+4][j] == 0 and \
               chessboard[i+5][j] == 0:
                amount += 1

    for i in range(x-6+1): #斜向，左上到右下

        for j in range(y-6+1):
            if chessboard[i][j] == 0 and \
               chessboard[i+1][j+1] == 0 and \
               chessboard[i+2][j+2] == 0 and \
               chessboard[i+3][j+3] == chess and \
               chessboard[i+4][j+4] == chess and \
               chessboard[i+5][j+5] == chess*-1:
                amount += 1

    for i in range(x-6+1): #斜向，左上到右下，反向

        for j in range(y-6+1):
            if chessboard[i][j] == chess*-1 and \
               chessboard[i+1][j+1] == chess and \
               chessboard[i+2][j+2] == chess and \
               chessboard[i+3][j+3] == 0 and \
               chessboard[i+4][j+4] == 0 and \
               chessboard[i+5][j+5] == 0:
                amount += 1

    for i in range(x-6+1): #斜向，右上到左下

        for j in range(6-1,y):
            if chessboard[i][j] == 0 and \
               chessboard[i+1][j-1] == 0 and \
               chessboard[i+2][j-2] == 0 and \
               chessboard[i+3][j-3] == chess and \
               chessboard[i+4][j-4] == chess and \
               chessboard[i+5][j-5] == chess*-1:
                amount += 1

    for i in range(x-6+1): #斜向，右上到左下，反向

        for j in range(6-1,y):
            if chessboard[i][j] == chess*-1 and \
               chessboard[i+1][j-1] == chess and \
               chessboard[i+2][j-2] == chess and \
               chessboard[i+3][j-3] == 0 and \
               chessboard[i+4][j-4] == 0 and \
               chessboard[i+5][j-5] == 0:
                amount += 1

    return amount

def seb(chess): #死二判断B，____●__●○，不考虑边界
    global x,y
    amount = 0

    for i in range(x): #横向

        for j in range(y-6+1):
            if chessboard[i][j] == 0 and \
               chessboard[i][j+1] == 0 and \
               chessboard[i][j+2] == chess and \
               chessboard[i][j+3] == 0 and \
               chessboard[i][j+4] == chess and \
               chessboard[i][j+5] == chess*-1:
                amount += 1

    for i in range(x): #横向，反向

        for j in range(y-6+1):
            if chessboard[i][j] == chess*-1 and \
               chessboard[i][j+1] == chess and \
               chessboard[i][j+2] == 0 and \
               chessboard[i][j+3] == chess and \
               chessboard[i][j+4] == 0 and \
               chessboard[i][j+5] == 0:
                amount += 1

    for i in range(x-6+1): #纵向

        for j in range(y):
            if chessboard[i][j] == 0 and \
               chessboard[i+1][j] == 0 and \
               chessboard[i+2][j] == chess and \
               chessboard[i+3][j] == 0 and \
               chessboard[i+4][j] == chess and \
               chessboard[i+5][j] == chess*-1:
                amount += 1

    for i in range(x-6+1): #纵向，反向

        for j in range(y):
            if chessboard[i][j] == chess*-1 and \
               chessboard[i+1][j] == chess and \
               chessboard[i+2][j] == 0 and \
               chessboard[i+3][j] == chess and \
               chessboard[i+4][j] == 0 and \
               chessboard[i+5][j] == 0:
                amount += 1

    for i in range(x-6+1): #斜向，左上到右下

        for j in range(y-6+1):
            if chessboard[i][j] == 0 and \
               chessboard[i+1][j+1] == 0 and \
               chessboard[i+2][j+2] == chess and \
               chessboard[i+3][j+3] == 0 and \
               chessboard[i+4][j+4] == chess and \
               chessboard[i+5][j+5] == chess*-1:
                amount += 1

    for i in range(x-6+1): #斜向，左上到右下，反向

        for j in range(y-6+1):
            if chessboard[i][j] == chess*-1 and \
               chessboard[i+1][j+1] == chess and \
               chessboard[i+2][j+2] == 0 and \
               chessboard[i+3][j+3] == chess and \
               chessboard[i+4][j+4] == 0 and \
               chessboard[i+5][j+5] == 0:
                amount += 1

    for i in range(x-6+1): #斜向，右上到左下

        for j in range(6-1,y):
            if chessboard[i][j] == 0 and \
               chessboard[i+1][j-1] == 0 and \
               chessboard[i+2][j-2] == chess and \
               chessboard[i+3][j-3] == 0 and \
               chessboard[i+4][j-4] == chess and \
               chessboard[i+5][j-5] == chess*-1:
                amount += 1

    for i in range(x-6+1): #斜向，右上到左下，反向

        for j in range(6-1,y):
            if chessboard[i][j] == chess*-1 and \
               chessboard[i+1][j-1] == chess and \
               chessboard[i+2][j-2] == 0 and \
               chessboard[i+3][j-3] == chess and \
               chessboard[i+4][j-4] == 0 and \
               chessboard[i+5][j-5] == 0:
                amount += 1

    return amount

def sec(chess): #死二判断C，__●____●○，不考虑边界
    global x,y
    amount = 0

    for i in range(x): #横向

        for j in range(y-6+1):
            if chessboard[i][j] == 0 and \
               chessboard[i][j+1] == chess and \
               chessboard[i][j+2] == 0 and \
               chessboard[i][j+3] == 0 and \
               chessboard[i][j+4] == chess and \
               chessboard[i][j+5] == chess*-1:
                amount += 1

    for i in range(x): #横向，反向

        for j in range(y-6+1):
            if chessboard[i][j] == chess*-1 and \
               chessboard[i][j+1] == chess and \
               chessboard[i][j+2] == 0 and \
               chessboard[i][j+3] == 0 and \
               chessboard[i][j+4] == chess and \
               chessboard[i][j+5] == 0:
                amount += 1

    for i in range(x-6+1): #纵向

        for j in range(y):
            if chessboard[i][j] == 0 and \
               chessboard[i+1][j] == chess and \
               chessboard[i+2][j] == 0 and \
               chessboard[i+3][j] == 0 and \
               chessboard[i+4][j] == chess and \
               chessboard[i+5][j] == chess*-1:
                amount += 1

    for i in range(x-6+1): #纵向，反向

        for j in range(y):
            if chessboard[i][j] == chess*-1 and \
               chessboard[i+1][j] == chess and \
               chessboard[i+2][j] == 0 and \
               chessboard[i+3][j] == 0 and \
               chessboard[i+4][j] == chess and \
               chessboard[i+5][j] == 0:
                amount += 1

    for i in range(x-6+1): #斜向，左上到右下

        for j in range(y-6+1):
            if chessboard[i][j] == 0 and \
               chessboard[i+1][j+1] == chess and \
               chessboard[i+2][j+2] == 0 and \
               chessboard[i+3][j+3] == 0 and \
               chessboard[i+4][j+4] == chess and \
               chessboard[i+5][j+5] == chess*-1:
                amount += 1

    for i in range(x-6+1): #斜向，左上到右下，反向

        for j in range(y-6+1):
            if chessboard[i][j] == chess*-1 and \
               chessboard[i+1][j+1] == chess and \
               chessboard[i+2][j+2] == 0 and \
               chessboard[i+3][j+3] == 0 and \
               chessboard[i+4][j+4] == chess and \
               chessboard[i+5][j+5] == 0:
                amount += 1

    for i in range(x-6+1): #斜向，右上到左下

        for j in range(6-1,y):
            if chessboard[i][j] == 0 and \
               chessboard[i+1][j-1] == chess and \
               chessboard[i+2][j-2] == 0 and \
               chessboard[i+3][j-3] == 0 and \
               chessboard[i+4][j-4] == chess and \
               chessboard[i+5][j-5] == chess*-1:
                amount += 1

    for i in range(x-6+1): #斜向，右上到左下，反向

        for j in range(6-1,y):
            if chessboard[i][j] == chess*-1 and \
               chessboard[i+1][j-1] == chess and \
               chessboard[i+2][j-2] == 0 and \
               chessboard[i+3][j-3] == 0 and \
               chessboard[i+4][j-4] == chess and \
               chessboard[i+5][j-5] == 0:
                amount += 1

    return amount

def sed(chess): #死二判断D，●______●
    global x,y
    amount = 0
    
    for i in range(x): #横向

        for j in range(y-5+1):
            if chessboard[i][j] == chess and \
               chessboard[i][j+1] == 0 and \
               chessboard[i][j+2] == 0 and \
               chessboard[i][j+3] == 0 and \
               chessboard[i][j+4] == chess:
                amount += 1

    for i in range(x-5+1): #纵向

        for j in range(y):
            if chessboard[i][j] == chess and \
               chessboard[i+1][j] == 0 and \
               chessboard[i+2][j] == 0 and \
               chessboard[i+3][j] == 0 and \
               chessboard[i+4][j] == chess:
                amount += 1

    for i in range(x-5+1): #斜向，左上到右下

        for j in range(y-5+1):
            if chessboard[i][j] == chess and \
               chessboard[i+1][j+1] == 0 and \
               chessboard[i+2][j+2] == 0 and \
               chessboard[i+3][j+3] == 0 and \
               chessboard[i+4][j+4] == chess:
                amount += 1

    for i in range(x-5+1): #斜向，右上到左下

        for j in range(5-1,y):
            if chessboard[i][j] == chess and \
               chessboard[i+1][j-1] == 0 and \
               chessboard[i+2][j-2] == 0 and \
               chessboard[i+3][j-3] == 0 and \
               chessboard[i+4][j-4] == chess:
                amount += 1

    return amount

def score(): #评估分数
    global bwin,wwin
    
    scoreb = lw(1) * 1000001 + \
            hs(1) * 100001 + \
            ssa(1) * 10001 + \
            ssb(1) * 10001 + \
            ssc(1) * 10001 + \
            hsana(1) * 1001 + \
            hsanb(1) * 1001 + \
            hea(1) * 101 + \
            heb(1) * 101 + \
            hec(1) * 101 + \
            ssana(1) * 71 + \
            ssanb(1) * 71 + \
            ssanc(1) * 71 + \
            ssand(1) * 71 + \
            ssane(1) * 71 + \
            ssanf(1) * 71 + \
            sea(1) * 11 + \
            seb(1) * 11 + \
            sec(1) * 11 + \
            sed(1) * 11 #黑棋分数

    scorew = lw(-1) * 1000000 + \
            hs(-1) * 100000 + \
            ssa(-1) * 10000 + \
            ssb(-1) * 10000 + \
            ssc(-1) * 10000 + \
            hsana(-1) * 1000 + \
            hsanb(-1) * 1000 + \
            hea(-1) * 100 + \
            heb(-1) * 100 + \
            hec(-1) * 100 + \
            ssana(-1) * 70 + \
            ssanb(-1) * 70 + \
            ssanc(-1) * 70 + \
            ssand(-1) * 70 + \
            ssane(-1) * 70 + \
            ssanf(-1) * 70 + \
            sea(-1) * 10 + \
            seb(-1) * 10 + \
            sec(-1) * 10 + \
            sed(-1) * 10 #白棋分数
    

    if lw(1) == 0:
        bwin = False

    if lw(-1) == 0:
        wwin = False
        
    if lw(1) > 0 and wwin == False: #胜利判断
        bwin = True
        
    if lw(-1) > 0 and bwin == False:
        wwin = True
        
    if bwin == True: #对方胜利，进攻价值清零，只防守
        scorew = -10000000
        
    if wwin == True:
        scoreb = -10000000
        
    return scoreb - scorew #总分数

def ai(chess):
    global x,y,move,win,piece,newpiece
    aix = aiy = aim = ain = air = ais = aia = aib = 0
    
    aix2 = np.zeros(9, dtype = int)
    aiy2 = np.zeros(9, dtype = int)
    aim2 = np.zeros(9, dtype = int)
    ain2 = np.zeros(9, dtype = int)

    aix3 = np.zeros(7, dtype = int)
    aiy3 = np.zeros(7, dtype = int)
    aim3 = np.zeros(7, dtype = int)
    ain3 = np.zeros(7, dtype = int)
    aip3 = np.zeros(7, dtype = int)
    aiq3 = np.zeros(7, dtype = int)
    air3 = np.zeros(7, dtype = int)
    ais3 = np.zeros(7, dtype = int)

    aix4 = np.zeros(5, dtype = int)
    aiy4 = np.zeros(5, dtype = int)
    aim4 = np.zeros(5, dtype = int)
    ain4 = np.zeros(5, dtype = int)
    aip4 = np.zeros(5, dtype = int)
    aiq4 = np.zeros(5, dtype = int)
    air4 = np.zeros(5, dtype = int)
    ais4 = np.zeros(5, dtype = int)
    aiu4 = np.zeros(5, dtype = int)
    aiv4 = np.zeros(5, dtype = int)
    aia4 = np.zeros(5, dtype = int)
    aib4 = np.zeros(5, dtype = int)
    
    minscore = 100000000
    maxscore = -100000000
    score1 = 0
    skip = False
    winmove = False
    maxscoremin = np.array([100000000]*9, dtype = int)
    maxscoremin2 = np.array([100000000]*7, dtype = int)
    maxscoremin3 = np.array([100000000]*5, dtype = int)
    maxscoremin4 = 100000000
    
    for i in range(x):
        
        for j in range(y):
            
            score1 = score()
            
            if chessboard[i][j] == 0:
                chessboard[i][j] = chess
                
                score()
                if wwin == True: #下一步胜利
                    winmove = True
                    aix = i
                    aiy = j
                    chessboard[i][j] = 0
                    break
                
                if score() == score1: #该位置分数无变化，剪枝
                    chessboard[i][j] = 0
                    continue
                
                for m in range(x):

                    for n in range(y):
                        
                        if chessboard[m][n] == 0:
                            chessboard[m][n] = chess*-1

                            if score() >= np.max(maxscoremin): #剪枝
                                skip = True
                                chessboard[m][n] = 0
                                break
                            
                            if score() > maxscore: #寻找分数最大位置
                                maxscore = score()
                                aim = m
                                ain = n
                                
                            chessboard[m][n] = 0

                    if skip == True:
                        break
                    
                if skip == False and maxscore < np.min(maxscoremin):
                    aix = i
                    aiy = j
                    
                if skip == False and maxscore < np.max(maxscoremin):
                    aix2[np.argmax(maxscoremin)] = i
                    aiy2[np.argmax(maxscoremin)] = j
                    aim2[np.argmax(maxscoremin)] = aim
                    ain2[np.argmax(maxscoremin)] = ain
                    maxscoremin[np.argmax(maxscoremin)] = maxscore

                skip = False
                maxscore = -100000000
                chessboard[i][j] = 0

        if winmove == True:
            break

    for o in range(9): #对评分前几的点加深搜索
        
        if winmove == True:
            break
        
        chessboard[aix2[o]][aiy2[o]] = chess
        chessboard[aim2[o]][ain2[o]] = chess*-1
        
        for p in range(x):
            
            for q in range(y):

                score1 = score()
            
                if chessboard[p][q] == 0:
                    chessboard[p][q] = chess
                    
                    if score() == score1: #该位置分数无变化，剪枝
                        chessboard[p][q] = 0
                        continue
                    
                    for r in range(x):

                        for s in range(y):
                            
                            if chessboard[r][s] == 0:
                                chessboard[r][s] = chess*-1

                                if score() >= np.max(maxscoremin2): #剪枝
                                    skip = True
                                    chessboard[r][s] = 0
                                    break
                                
                                if score() > maxscore: #寻找分数最大位置
                                    maxscore = score()
                                    air = r
                                    ais = s
                                    
                                chessboard[r][s] = 0

                        if skip == True:
                            break

                    if skip == False and maxscore < np.min(maxscoremin2):
                        aix = aix2[o]
                        aiy = aiy2[o]
                        
                    if skip == False and maxscore < np.max(maxscoremin2):
                        aix3[np.argmax(maxscoremin2)] = aix2[o]
                        aiy3[np.argmax(maxscoremin2)] = aiy2[o]
                        aim3[np.argmax(maxscoremin2)] = aim2[o]
                        ain3[np.argmax(maxscoremin2)] = ain2[o]
                        
                        aip3[np.argmax(maxscoremin2)] = p
                        aiq3[np.argmax(maxscoremin2)] = q
                        air3[np.argmax(maxscoremin2)] = air
                        ais3[np.argmax(maxscoremin2)] = ais
                        maxscoremin2[np.argmax(maxscoremin2)] = maxscore

                    skip = False
                    maxscore = -100000000
                    chessboard[p][q] = 0

        chessboard[aix2[o]][aiy2[o]] = 0
        chessboard[aim2[o]][ain2[o]] = 0

    for t in range(7): #对评分前几的点加深搜索
        
        if winmove == True:
            break
        
        chessboard[aix3[t]][aiy3[t]] = chess
        chessboard[aim3[t]][ain3[t]] = chess*-1
        chessboard[aip3[t]][aiq3[t]] = chess
        chessboard[air3[t]][ais3[t]] = chess*-1
        
        for u in range(x):
            
            for v in range(y):

                score1 = score()
            
                if chessboard[u][v] == 0:
                    chessboard[u][v] = chess
                    
                    if score() == score1: #该位置分数无变化，剪枝
                        chessboard[u][v] = 0
                        continue
                    
                    for a in range(x):

                        for b in range(y):
                            
                            if chessboard[a][b] == 0:
                                chessboard[a][b] = chess*-1

                                if score() >= np.max(maxscoremin3): #剪枝
                                    skip = True
                                    chessboard[a][b] = 0
                                    break
                                
                                if score() > maxscore: #寻找分数最大位置
                                    maxscore = score()
                                    aia = a
                                    aib = b
                                    
                                chessboard[a][b] = 0

                        if skip == True:
                            break

                    if skip == False and maxscore < np.min(maxscoremin3):
                        aix = aix3[t]
                        aiy = aiy3[t]
                        
                    if skip == False and maxscore < np.max(maxscoremin3):
                        aix4[np.argmax(maxscoremin3)] = aix3[t]
                        aiy4[np.argmax(maxscoremin3)] = aiy3[t]
                        aim4[np.argmax(maxscoremin3)] = aim3[t]
                        ain4[np.argmax(maxscoremin3)] = ain3[t]
                        aip4[np.argmax(maxscoremin3)] = aip3[t]
                        aiq4[np.argmax(maxscoremin3)] = aiq3[t]
                        air4[np.argmax(maxscoremin3)] = air3[t]
                        ais4[np.argmax(maxscoremin3)] = ais3[t]
                        
                        aiu4[np.argmax(maxscoremin3)] = u
                        aiv4[np.argmax(maxscoremin3)] = v
                        aia4[np.argmax(maxscoremin3)] = aia
                        aib4[np.argmax(maxscoremin3)] = aib
                        
                        maxscoremin3[np.argmax(maxscoremin3)] = maxscore

                    skip = False
                    maxscore = -100000000
                    chessboard[u][v] = 0
                    
        chessboard[aix3[t]][aiy3[t]] = 0
        chessboard[aim3[t]][ain3[t]] = 0
        chessboard[aip3[t]][aiq3[t]] = 0
        chessboard[air3[t]][ais3[t]] = 0

    for c in range(5): #对评分前几的点加深搜索
        
        if winmove == True:
            break
        
        chessboard[aix4[c]][aiy4[c]] = chess
        chessboard[aim4[c]][ain4[c]] = chess*-1
        chessboard[aip4[c]][aiq4[c]] = chess
        chessboard[air4[c]][ais4[c]] = chess*-1
        chessboard[aiu4[c]][aiv4[c]] = chess
        chessboard[aia4[c]][aib4[c]] = chess*-1
        
        for d in range(x):
            
            for e in range(y):

                score1 = score()
            
                if chessboard[d][e] == 0:
                    chessboard[d][e] = chess
                    
                    if score() == score1: #该位置分数无变化，剪枝
                        chessboard[d][e] = 0
                        continue
                    
                    for f in range(x):

                        for g in range(y):
                            
                            if chessboard[f][g] == 0:
                                chessboard[f][g] = chess*-1

                                if score() >= maxscoremin4: #剪枝
                                    skip = True
                                    chessboard[f][g] = 0
                                    break
                                
                                if score() > maxscore: #寻找分数最大位置
                                    maxscore = score()
                                    
                                chessboard[f][g] = 0

                        if skip == True:
                            break
                        
                    if skip == False and maxscore < maxscoremin4:
                        aix = aix4[c]
                        aiy = aiy4[c]
                        maxscoremin4 = maxscore

                    skip = False
                    maxscore = -100000000
                    chessboard[d][e] = 0
                    
        chessboard[aix4[c]][aiy4[c]] = 0
        chessboard[aim4[c]][ain4[c]] = 0
        chessboard[aip4[c]][aiq4[c]] = 0
        chessboard[air4[c]][ais4[c]] = 0
        chessboard[aiu4[c]][aiv4[c]] = 0
        chessboard[aia4[c]][aib4[c]] = 0
        
    chessboard[aix][aiy] = chess
    piece = Circle(Point(aix * 75 + 75, aiy * 75 + 75),30)
    if chess == 1:
        piece.setFill("black")
    else:
        piece.setFill("white")
    piece.draw(win)
    move += 1
    
    if "newpiece" in globals():
        newpiece.undraw()
            
    newpiece = Polygon(Point(aix * 75 + 75, aiy * 75 + 75), \
                         Point(aix * 75 + 75 + 30, aiy * 75 + 75), \
                         Point(aix * 75 + 75, aiy * 75 + 75 + 30))
    newpiece.setOutline("red")
    newpiece.setFill("red")
    newpiece.draw(win)
    
    print(aix,aiy)
    for i in range(9): #输出log
        print(maxscoremin[i],aix2[i],aiy2[i],aim2[i],ain2[i])
        
    print()
    
    for j in range(7):
        print(maxscoremin2[j],aix3[j],aiy3[j],aim3[j],ain3[j],aip3[j],aiq3[j],air3[j],ais3[j])

    print()
    
    for k in range(5):
        print(maxscoremin3[k],aix4[k],aiy4[k],aim4[k],ain4[k],aip4[k],aiq4[k],air4[k],ais4[k], \
              aiu4[k],aiv4[k],aia4[k],aib4[k])
        
    if winmove == True:
        pyautogui.alert("White win!", title="Prompt")
        win.getMouse()
        win.close()
        
windows()
