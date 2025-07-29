## -*- coding: utf-8 -*-
## (C) 2013 Muthiah Annamalai,
## Licensed under GPL Version 3

import turtle

class TamilTurtle:
    """ TamilTurtle class implements a singleton for famed Turtle module.
        Unfortunately turtle class does not take str arguments.    """
    instance = None
    
    @staticmethod
    def getInstance( ):
        if not TamilTurtle.instance:
            TamilTurtle.instance = turtle.Pen();
        return TamilTurtle.instance
    
    @staticmethod
    def functionAttributes():
        attrib = {0:['ht','home','showturtle','hideturtle','reset','penup','up','down','pendown','clear','isvisible',],
                  1:['rt','lt','left','right','forward','fd','bd','backward','color','fill','speed','pencolor','dot'],
                  2:['goto'],
                  -1:['circle','setworldcoordinates'] } #-1 => indicates varargs
        return attrib
    
    # 0-arg functions
    @staticmethod
    def home():
        TamilTurtle.getInstance().home(*[])

    @staticmethod
    def clear():
        TamilTurtle.getInstance().clear(*[])

    @staticmethod
    def showturtle( ):
        TamilTurtle.getInstance().showturtle(*[])

    @staticmethod
    def hideturtle():
        TamilTurtle.getInstance().hideturtle(*[])
    
    @staticmethod
    def penup():
        TamilTurtle.getInstance().penup(*[])
    up = penup;

    @staticmethod
    def pendown():
        TamilTurtle.getInstance().pendown(*[])
        
    @staticmethod
    def down():
        TamilTurtle.pendown()
    
    # 1-arg functions
    @staticmethod
    def rt(x):
        TamilTurtle.getInstance().rt(*[x])

    @staticmethod
    def right(x):
        TamilTurtle.rt(x)
    
    @staticmethod
    def lt(x):
        TamilTurtle.getInstance().lt(*[x])
    
    @staticmethod
    def left(x):
        TamilTurtle.lt(x)
        
    @staticmethod
    def forward(x):
        TamilTurtle.getInstance().forward(*[x])

    @staticmethod
    def fd(x):
        TamilTurtle.forward(x)
            
    @staticmethod
    def backward(x):
        TamilTurtle.getInstance().backward(*[x])

    @staticmethod
    def bd(x):
        TamilTurtle.backward(x)
    
    @staticmethod
    def back(x):
        TamilTurtle.getInstance().back(*[x])

    @staticmethod
    def bk(x):
        TamilTurtle.getInstance().bk(*[x])
    
    @staticmethod
    def setworldcoordinates(*x): #polymorphic invocation supported here
        turtle.setworldcoordinates(*x)
    
    @staticmethod
    def circle(*x): #polymorphic invocation supported here
        TamilTurtle.getInstance().circle(*x)

    @staticmethod
    def clearstamp(x):
        TamilTurtle.getInstance().clearstamp(*[x])

    @staticmethod
    def clearstamps(x):
        TamilTurtle.getInstance().clearstamps(*[x])

    @staticmethod
    def clone(x):
        TamilTurtle.getInstance().clone(*[x])

    @staticmethod
    def color(x):        
        TamilTurtle.getInstance().color(*[str(x)])
    
    @staticmethod
    def degrees(x):
        TamilTurtle.getInstance().degrees(*[x])

    @staticmethod
    def distance(x):
        TamilTurtle.getInstance().distance(*[x])

    @staticmethod
    def dot(x):
        TamilTurtle.getInstance().dot(*[x])

    @staticmethod
    def fill(x):
        TamilTurtle.getInstance().fill(*[x])

    @staticmethod
    def fillcolor(x):
        TamilTurtle.getInstance().fillcolor(*[x])

    @staticmethod
    def getpen(x):
        TamilTurtle.getInstance().getpen(*[x])

    @staticmethod
    def getscreen(x):
        TamilTurtle.getInstance().getscreen(*[x])

    @staticmethod
    def getturtle(x):
        TamilTurtle.getInstance().getturtle(*[x])

    @staticmethod
    def goto(x,y):
        TamilTurtle.getInstance().goto(*[x,y])

    @staticmethod
    def heading(x):
        TamilTurtle.getInstance().heading(*[x])

    @staticmethod
    def ht():
        TamilTurtle.getInstance().ht(*[])

    @staticmethod
    def isdown(x):
        TamilTurtle.getInstance().isdown(*[x])

    @staticmethod
    def isvisible():
        TamilTurtle.getInstance().isvisible(*[])

    @staticmethod
    def ondrag(x):
        TamilTurtle.getInstance().ondrag(*[x])

    @staticmethod
    def onrelease(x):
        TamilTurtle.getInstance().onrelease(*[x])

    @staticmethod
    def pd(x):
        TamilTurtle.getInstance().pd(*[x])

    @staticmethod
    def pen(x):
        TamilTurtle.getInstance().pen(*[x])

    @staticmethod
    def pencolor(x):
        TamilTurtle.getInstance().pencolor(*[str(x)])

    @staticmethod
    def pensize(x):
        TamilTurtle.getInstance().pensize(*[x])

    @staticmethod
    def pos(x):
        TamilTurtle.getInstance().pos(*[x])
    
    @staticmethod
    def position(x):
        TamilTurtle.getInstance().position(*[x])

    @staticmethod
    def pu(x):
        TamilTurtle.getInstance().pu(*[x])

    @staticmethod
    def radians(x):
        TamilTurtle.getInstance().radians(*[x])

    @staticmethod
    def reset():
        TamilTurtle.getInstance().reset()
    
    @staticmethod
    def resizemode(x):
        TamilTurtle.getInstance().resizemode(*[x])

    @staticmethod
    def seth(x):
        TamilTurtle.getInstance().seth(*[x])

    @staticmethod
    def setpos(x):
        TamilTurtle.getInstance().setpos(*[x])

    @staticmethod
    def setposition(x):
        TamilTurtle.getInstance().setposition(*[x])

    @staticmethod
    def settiltangle(x):
        TamilTurtle.getInstance().settiltangle(*[x])

    @staticmethod
    def setundobuffer(x):
        TamilTurtle.getInstance().setundobuffer(*[x])

    @staticmethod
    def setx(x):
        TamilTurtle.getInstance().setx(*[x])

    @staticmethod
    def sety(x):
        TamilTurtle.getInstance().sety(*[x])

    @staticmethod
    def shape(x):
        TamilTurtle.getInstance().shape(*[x])

    @staticmethod
    def shapesize(x):
        TamilTurtle.getInstance().shapesize(*[x])

    @staticmethod
    def speed(x):
        TamilTurtle.getInstance().speed(*[x])

    @staticmethod
    def st(x):
        TamilTurtle.getInstance().st(*[x])

    @staticmethod
    def stamp(x):
        TamilTurtle.getInstance().stamp(*[x])

    @staticmethod
    def tilt(x):
        TamilTurtle.getInstance().tilt(*[x])

    @staticmethod
    def tiltangle(x):
        TamilTurtle.getInstance().tiltangle(*[x])

    @staticmethod
    def towards(x):
        TamilTurtle.getInstance().towards(*[x])

    @staticmethod
    def tracer(x):
        TamilTurtle.getInstance().tracer(*[x])

    @staticmethod
    def turtlesize(x):
        TamilTurtle.getInstance().turtlesize(*[x])

    @staticmethod
    def undo(x):
        TamilTurtle.getInstance().undo(*[x])

    @staticmethod
    def undobufferentries(x):
        TamilTurtle.getInstance().undobufferentries(*[x])

    @staticmethod
    def width(x):
        TamilTurtle.getInstance().width(*[x])

    @staticmethod
    def write(x):
        TamilTurtle.getInstance().write(*[x])

    @staticmethod
    def xcor(x):
        TamilTurtle.getInstance().xcor(*[x])

    @staticmethod
    def ycor(x):
        TamilTurtle.getInstance().ycor(*[x])
