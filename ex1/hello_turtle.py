######################################################################
# FILE: hello_turtle.py
# WRITER: Benjamin Maman, benm, 341145811
# EXERCISE: intro2cs ex1 2017-2018
# DESCRIPTION: Drawing 3 flowers
#######################################################################

import turtle


def draw_petal():
    #This function draws a petal
    turtle.forward(30)
    turtle.right(45)
    turtle.forward(30)
    turtle.right(135)
    turtle.forward(30)
    turtle.right(45)
    turtle.forward(30)
    turtle.right(135)


def draw_flower():
    #This function draws a flower of 4 petals using draw_petal function
    turtle.left(45)
    draw_petal()
    turtle.left(90)
    draw_petal()
    turtle.left(90)
    draw_petal()
    turtle.left(90)
    draw_petal()
    turtle.left(135)
    turtle.forward(150)


def draw_flower_advanced():
    #This function complete the flower and moves the cursor to prepare drawing an other flower
    draw_flower()
    turtle.right(90)
    turtle.up()
    turtle.forward(150)
    turtle.right(90)
    turtle.forward(150)
    turtle.left(90)
    turtle.down()


def draw_flower_bed():
    #This function draws 3 flowers
    turtle.up()
    turtle.forward(200)
    turtle.left(180)
    turtle.down()
    draw_flower_advanced()
    draw_flower_advanced()
    draw_flower_advanced()

#Calling the function and let the window opened
draw_flower_bed()
turtle.done()
