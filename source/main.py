#!/usr/bin/env python
# coding: utf-8

# In[303]:


# organise directories
import os as os
import shutil
homedir = os.getcwd() + '\\..\\'

def HideHome(path, home=homedir):
    newPath = path.split(home)[1]
    return 'home\\'+ newPath

sourcedir = homedir + 'source\\'
outputdir = homedir + 'output\\'
oldoutputdir = outputdir + 'old\\'
savedir = homedir + 'save\\'

#copies files from cwd
def CopyFile(fileName, destinationPath, overwrite = True, savecopy = False):
    if savecopy:
        print('duplicate of ',end='')
        CopyFile(fileName, savedir, False, False)
    if (not overwrite ) and os.path.exists(destinationPath + fileName):
        print(fileName+ ' exists aleady')
        return
    try:
        #overwrite or create contents
        shutil.copyfile(path+'\\'+fileName, destinationPath)
        print(fileName + " copied to:", HideHome(destinationPath + fileName))
    except shutil.SameFileError:
        print("Source represents the same file as Destination.")

#moves from the cwd (assumes dir ends with \\)
def MoveFile(fileName, destinationPath=outputdir[:-1], overwrite = True, savecopy = False):
    if savecopy:
        print('duplicate of ',end='')
        CopyFile(fileName, savedir, False, False)
    if (not overwrite ) and os.path.exists(destinationPath  +'\\'+ fileName):
        print(fileName+ ' exists aleady')
        return
    if (overwrite and (os.path.exists(destinationPath  +'\\'+ fileName))):
        shutil.copy(destinationPath +'\\'+ fileName,oldoutputdir)
        os.remove(destinationPath +'\\'+ fileName)
        print('old files in destination folder moved to ouput\old\\')
    try:
        #overwrite or create contents
        shutil.move(sourcedir+fileName, destinationPath)
        print(fileName +' moved to: ' + HideHome(destinationPath + '\\' + fileName))
    except shutil.SameFileError:
        print("Source represents the same file as Destination.")


def viewgrid(SquaresX,SquaresY):
    totalSquares = SquaresX * SquaresY
    dimensions = "(" + str(SquaresX) +"," + str(SquaresY)+ ")"
    print("totalsquares: ",dimensions, ": ", totalSquares)
    for cursory in range(SquaresY):
        print(cursory, ": ", end="")
        for cursorx in range(SquaresX):
            print("[ ]",sep=" ", end="")
        print()

G_CanvasWidth = 210
#A4: width: 210mm no idea how its translated to ints
G_CanvasHeight = 297
#A4 heigth: 297mm

G_SquaresX = 4
G_SquaresY = 4
G_SquareWidth = 25

#main draw logic
from svg_turtle import SvgTurtle
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
import webbrowser as chrome
import turtle as Turtle
import math as mt

def drawturle(t, size):
    t.pensize(2+size)
    t.dot()
    t.pensize(size)
    t.forward(10+size)
    t.pensize(1)
    t.back(10+size)

def draw_board(t, backgroundcolor = 'white', SquaresX = G_SquaresX, SquaresY = G_SquaresY, SquareWidth = G_SquareWidth):
    t.fillcolor(backgroundcolor)
    # t.begin_fill()
    #draw the board
    for CurrentSreenDirection in (['right', 'up', 'left', 'down']):
        t.forward(SquaresX*SquareWidth)
        t.left(90)
    # t.end_fill()

    # t.pensize(1)
    for CurrentSreenDirection in (['right', 'up', 'left', 'down']):
        #TODO draw a line for each x
        for positionX in range(SquaresX):
            t.forward(SquareWidth)
            t.left(90)
            t.forward(SquareWidth)
            t.back(SquareWidth)
            t.left(270)
        t.left(90)


#fills the outer SquaresX squares with lines stretching inside from the border
def draw_lines_for_squares(t, SquaresX = G_SquaresX, SquaresY= G_SquaresY, SquareWidth = G_SquareWidth):
    for CurrentSreenDirection in (['right', 'up', 'left', 'down']):
        #TODO draw a line for each x
        for positionX in range(SquaresX):
            t.forward(SquareWidth)
            t.left(90)
            t.forward(SquareWidth)
            t.back(SquareWidth)
            t.left(270)
        t.left(90)
    # t.right(90)

#fills the outer SquaresX squares with numbers going left to right bottom up
def draw_numbers_for_squares(t, SquaresX = G_SquaresX, SquaresY= G_SquaresY, SquareWidth = G_SquareWidth):
    # for CurrentSreenDirection in (['right', 'up', 'left', 'down']):
    for positionY in range(SquaresY):
        #TODO draw a number for each x
        for positionX in range(SquaresX):
            draw_digit(1,t,digitwidth=1)
            t.pensize(0)
            t.forward(SquareWidth)
        #move back and unto the next line of Ysquares
        t.back(SquaresX*SquareWidth)
        t.left(90)
        t.forward(SquareWidth)
        t.right(90)
    #move back down
    t.right(90)
    t.forward(SquaresY*SquareWidth)
    t.left(90)
    t.pensize(1)

def move_to_inner_square(t,SquareWidth = G_SquareWidth):
    t.pensize(0)
    t.forward(SquareWidth)
    t.left(90)
    t.forward(SquareWidth)
    t.right(90)
    t.pensize(1)

def move_to_outer_square(t,SquareWidth = G_SquareWidth):
    t.pensize(0)
    t.back(SquareWidth)
    t.right(90)
    t.forward(SquareWidth)
    t.left(90)
    t.pensize(1)

#leaves the turtle in the middle of the square looking up
def center_in_square(t, skiptop=1,SquareWidth=22):
    #center in square
    t.pensize(0)
    t.forward(SquareWidth/2)
    t.left(90)
    t.forward(skiptop)
    t.pensize(1)

def move_back_to_start_of_square(t, SquareWidth=22):
    #move back to start of square from middle top
    t.left(180)
    t.forward(SquareWidth)
    t.left(90)
    t.back(SquareWidth/2)

#santa could not do it in time
#draws a digit with lines and start back at beginning
def draw_digit(digit,t,skiptop=4, digitcolor = 'black', digitwidth=3, SquareWidth=22):
     
    # oldpensize = t.pensize
    # oldpencolor = t.pencolor
    t.pensize(digitwidth)
    t.pencolor(digitcolor)
    r_drawsquare = SquareWidth/2 - skiptop
    match digit:
        case 1:
            center_in_square(t,skiptop,SquareWidth)
            t.pensize(digitwidth)
            t.forward(SquareWidth-2*skiptop)
            t.left(180-45)
            t.forward(4)
            t.back(4)
            t.left(180+45)
            t.pensize(0)
            t.forward(skiptop)

            move_back_to_start_of_square(t,SquareWidth)

        case _:
            # print("error")
            pass
    t.pensize(1)


#starts and ends looking right in bottomleft corner
def draw_square_board(t, backgroundcolor = 'white', SquaresX = 4, SquaresY = 4, SquareWidth = 22):
    t.fillcolor(backgroundcolor)
    # t.begin_fill()
    #draw the board
    for CurrentSreenDirection in (['right', 'up', 'left', 'down']):
        t.forward(SquaresX*SquareWidth)
        t.left(90)
    # t.end_fill()

    # t.right(90)
    # drawturle(t,5)
    draw_lines_for_squares(t,4,4,SquareWidth)

    # drawturle(t,3) #these are facing the same direction now which is logical
    #then get in pos and draw inner
    move_to_inner_square(t,SquareWidth)
    draw_lines_for_squares(t,2,2,SquareWidth)
    move_to_outer_square(t,SquareWidth)
    # drawturle(t,3) #these are facing the same direction now which is logical
    draw_numbers_for_squares(t,4,4,SquareWidth)

def draw_4_squares(t, SquaresXY = G_SquaresX, SquareWidth = G_SquareWidth):
    SquaresX = SquaresY = SquaresXY
    #initial positioning
    t.pensize(0)
    t.back(5)
    t.left(90)
    t.forward(25)
    t.left(270)
    t.pensize(1)

    for SquareLocation in ['topright', 'topleft', 'bottomleft', 'bottomright']:
        t.pensize(0)
        t.forward(11)
        if SquareLocation == ('topright'):
            t.left(90)
            t.forward(25)
            t.left(270)
        elif SquareLocation == ('bottomleft'):
            t.left(90)
            t.forward(25)
            t.left(270)
        t.pensize(1)
        draw_square_board(t)
        # t.pencilup()
        #back at start
        t.left(180)
        #rotate for next board
        t.left(90)

    # t.pensize(0)
    # t.forward(11)
    # t.pensize(1)




def write_file(draw_func, filename, width = G_CanvasWidth, height = G_CanvasHeight):
    t = SvgTurtle(width, height)
    draw_func(t)
    t.save_as(filename)
    #TODO fix clip path error code

def apply_draw_to_t(t,draw_func):
    draw_func(t)

def GenerateNewFiles(Name):
    match Name:
        case 'SmallBoard':
            draw_func = draw_small_square
        case 'MainBoard':
            #this is for the two medium ones
            draw_func = draw_2_medium_squares
            # draw_func = draw_square_board
        case 'LargeBoard':
            #final
            draw_func = draw_large_board
        case _:
            draw_func = draw_4_squares
    #new svg
    write_file(draw_func=draw_func, filename=(Name+'.svg'))
    drawing = svg2rlg((Name + '.svg'))
    MoveFile(Name+'.svg')
    
    #new pdf
    renderPDF.drawToFile(drawing, (Name + '.pdf'))
    MoveFile(Name+'.pdf')
    chrome.open_new(outputdir + Name + '.pdf')

    #clear the garbage
    print(chr(27) + "[2J")

def GenerateNewPDFFromOldFile(Name):
    match Name:
        case _:
            pass
    drawing = svg2rlg((Name + '.svg'))
    renderPDF.drawToFile(drawing, (Name + '.pdf'))


#main game logic

def solution_menu(solutionstring, solution):
    while(1):
        print("please type the solution for "+solutionstring+": ")
        digits = input()
        if digits == "q":
            exit()
        if digits == solution:
            print("well done!")
            time.sleep(3)
            return 0
        elif digits.__len__() > 4:
            print("WRONG lol!!! no but seriously, just "+solutionstring+" please..")
            time.sleep(5)
        else:
            print("incorrect")
            time.sleep(3)
            print(chr(27) + "[2J")


def open_first_puzzle():
    # GenerateNewFiles("SmallBoard")
    
    chrome.open_new(outputdir + "klein" + '.pdf')
    solution_menu("the bottom 4 digits",  "3451")
    print("Let's see if you can do these two as well!")
    time.sleep(3)
    print("Are you ready?")
    return


def open_second_puzzle():
    
    chrome.open_new(outputdir + "middel" + '.pdf')
    # GenerateNewFiles("MainBoard")
    # GenerateNewFiles("leftmiddleBoard")
    
    solution_menu("the digits in the red field",  "531")

def open_third_puzzle():
    # GenerateNewFiles("rightmiddleBoard")
    solution_menu("the digits in the green field",  "345")
    print("Well well well, you are good at this")
    time.sleep(3)
    print("But the real test only begins now!")
    time.sleep(3)
    print("Can you solve the last puzzle? It's BIG!")
    

def open_fourth_puzzle():
    chrome.open_new(outputdir + "groot" + '.pdf')
    # GenerateNewFiles("LargeBoard")
    solution_menu("the digit in the gold field",  "1")
    print("WELL DONE. YOU ARE THE GREATEST!!")
    time.sleep(2)
    print("Time to open your presents!!!!!!")
    exit()

    
def allpuzzles():
    open_first_puzzle()
                
    open_second_puzzle()
                
    open_third_puzzle()
                
    open_fourth_puzzle()

def secret_santa_menu():
    print("Santa wanted to make a tectonic puzzle generator...")
    time.sleep(3)
    print("but he wasn't smart enough to figure out the logic")
    time.sleep(3)
    print("You just might have what it takes to complete his work!")
    time.sleep(3)
    print("Will you help save christmas?")
    time.sleep(3)
    t = Turtle.Turtle()
    apply_draw_to_t(t,draw_4_squares)
    
    exit()


# In[308]:


#michellegame

import time as time
def michellegame():
    while(1):
        print("Please write your name: ")
        name = input()
        if (name != ""):
            print("Welcome "+ name+ ", this is your digital chrismas present")
            time.sleep(3)
            if (name == "michelle" or name == "michelle Kingma" or name == "Michelle" or name == "Michelle Kingma" or name == "mies"  or name == "Mies" or name == "m" or name == "M"):
                print("This christmas, you have to solve 4 tectonics in order to prove yourself")
                time.sleep(3)
                print("Though the first one is easy, this challenge is not to be taken lightly")
                time.sleep(3)
                print("Can you unlock the secret?")
                time.sleep(3)

                open_first_puzzle()
                
                open_second_puzzle()
                
                open_third_puzzle()
                
                open_fourth_puzzle()
            elif name == "Lucas" or name == "lucas" or name =="L" or name == "l":
                print("You have unlocked the secret santa menu")
                time.sleep(3)
                secret_santa_menu()
                print("cya")
            elif name == "lskip":
                allpuzzles()
                print("gg")
            elif name == "santa":
                secret_santa_menu()
            else:
                print(" Just kidding, this present is for someone else.")
            break
    print("done")


michellegame()