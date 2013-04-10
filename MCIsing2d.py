#!/usr/bin/env python
from __future__ import division
import numpy as np
import pylab
from numpy.random import random #import only one function from somewhere
from numpy.random import randint
from numpy import mod, exp
import scipy
import matplotlib.cm as cm
from time import sleep
import sys

def initialize(size):
    """
    Initialize a random array where our spins are all up or down.
    """
    return np.random.choice([-1, 1], size=(size, size)).tolist()

#@profile
def deltaU(s,i,j,size):
    """
    Compute delta U of flipping a given dipole at i,j
    Note periodic boundary conditions, which is why we need to know the size.

    This function returns deltaU/2
    """
    above = s[(i+1) % size][j]
    below = s[(i-1) % size][j]
    right = s[i][(j+1) % size]
    left =  s[i][(j-1) % size]

    return s[i][j]*(above+below+left+right)

def deltaUtest(s,i,j,size):
    return s[i][j]*(s[(i+1) % size][j] + s[(i-1) % size][j] +
                    s[i][(j+1) % size] + s[i][(j-1) % size])

def colorsquare(s,fig):
    fig.clear()
    pylab.imshow(s,interpolation='nearest',cmap=cm.Greys_r)
    fig.canvas.draw()
    #ax.set_title("Trial %s of %s"%(trial,numtrials))
    pylab.draw()


def shouldshow(iteration,size,showevery):
    if showevery is 1:
        return True
    if showevery == -1:
        return False
    if showevery is None:
        #if size <= 10:
        #    showevery = 1
        #    delay = 5
        if size < 100:
            showevery = int(size*size/2)
        else:
            showevery = size*size
        return divmod(iteration,showevery)[1] == 0

@profile
def simulate(size, T, showevery=None, graphics=True):
    """
    
    Arguments:
    - `size`: lattice length
    - `T`: in units of epsilon/k
    - `showevery`: how often to update the display. If None, a heuristic will be used.
    """
    # Some magic to set up plotting
    #pylab.ion() # You need this if running standalone
    import time
    start = time.time()

    if graphics:
        fig = pylab.figure()
        ax = fig.add_subplot(111)

    s = initialize(size)

    if graphics:
        colorsquare(s,fig)
        pylab.show()
    
    numtrials = 100*size**2
    print "numtrials",numtrials

    """b_factor pre-calculates the Boltzmann factors for our 4 possible
    positive energies. delatU returns an int -4 <= dU <= 4. b_factor is
    of length 5 to save a subtraction, i.e. we want b_factor[4]. b_factor[0]
    is never used but is retained for convenience.
    """
    b_factor = [exp(-2*i/T) for i in xrange(5)]
    rands = random(numtrials)
    for trial in xrange(numtrials):
        i = randint(size) # choose random row
        j = randint(size) # and random column
        ediff = deltaUtest(s,i,j,size)
        if ediff <= 0: # flipping reduces the energy
            s[i][j] *= -1
        else:
            if rands[trial] < b_factor[ediff]:
                s[i][j] *= -1
        if graphics and shouldshow(trial,size,showevery):
            print "Showing iteration",trial
            colorsquare(s,fig)
    if graphics: colorsquare(s,fig)
    stop = time.time()
    print "That took",stop-start,"seconds, or",numtrials/(stop-start),"trials per second"
    
if __name__ == '__main__':
    #raw_input()  # you need this.
    if len(sys.argv) == 1:
        simulate(50, 1, graphics=False)
    else:
        simulate(int(sys.argv[1]), 1, graphics=False)
