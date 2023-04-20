import os
from os.path import dirname, join, split

SQUARESIZE = 50
NUMROWS = 15
NUMCOLUMNS = 20
SCREENSIZE = WIDTH, HEIGHT = NUMCOLUMNS * SQUARESIZE, NUMROWS * SQUARESIZE

IMAGEFOLDER = join(split(split(split(dirname(__file__))[0])[0])[0], "images")


if __name__ == "__main__":
    print(IMAGEFOLDER)
