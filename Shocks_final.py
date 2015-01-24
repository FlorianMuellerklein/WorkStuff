import time
import random
import pygame
import serial
import numpy as np

# get subject number
#
subject = raw_input('Enter participant id ... ')

# initialize data files
#
open(('ShocksTiming' + '/' + str(subject) + '_shocks.txt'), 'a').close()
open(('ShocksTiming' + '/' + str(subject) + '_shockstim.txt'), 'a').close()
open(('ShocksTiming' + '/' + str(subject) + '_noshocks.txt'), 'a').close()
open(('ShocksTiming' + '/' + str(subject) + '_fixation.txt'), 'a').close()

# initialize pygame window
#
pygame.init()
w = 800
h = 600
size = (w,h)
screen = pygame.display.set_mode((size))#, pygame.FULLSCREEN)
pygame.mouse.set_visible(False)

def wait_4_scanner():
    task_trig = serial.Serial(3)
    print 'wait for scanner ... '
    while True:
        if task_trig.read() > 0:
            break
            
def trigger_shock():
    shock_trig = serial.Serial(4)
    shock_trig.write(str(1))
    shock_trig.close()
    print 'shock'
    
def fixation(starttime):
    print 'fixation'
    #
    # get the timing of fixation onset
    #
    timing = time.time() - starttime
    #
    # write the fixation onset time to file
    #
    with open(('ShocksTiming' + '/' + str(subject) + "_fixation.txt"), "a") as myfile:
        myfile.write(str(timing) + '\n')
    
    #
    # loop until the current time is the same as predefined stop time
    #
    stop = time.time() + 20
    while time.time() < stop:
        img = pygame.image.load('/Volumes/CRUZER/Python/Shocks/cross.bmp')
        screen.blit(img, (100,0))
        pygame.display.flip()
        
    
def safe(starttime):
    print 'safe'
    #
    # write safe stim onset time to file
    #
    timing = time.time() - starttime
    with open(('ShocksTiming' + '/' + str(subject) + "_fixation.txt"), "a") as myfile:
        myfile.write(str(timing) + '\n')
    #
    # loop until stop time is met
    #
    stop = time.time() + 40
    while time.time() < stop:
            img2 = pygame.image.load('/Volumes/CRUZER/Python/Shocks/safe.jpg')
            screen.blit(img2, (100,0))
            pygame.display.flip()
    
    fixation(starttime)
            
def shocks(starttime):
    print 'shocks'
    #
    # generate 4 random times to administer shocks
    #
    shocktimes = []
    for i in range(0,4):
        stop = time.time() + np.around(random.randint(1, 50))
        shocktimes.append(stop)
        
    print shocktimes
    print time.time()
    
    # 
    # writing timing of onset of shock stim to file
    #
    timing = time.time() - starttime
    with open(('ShocksTiming' + '/' + str(subject) + "_shockstim.txt"), "a") as myfile:
        myfile.write(str(timing) + '\n')
        
    #
    # put up shock stim
    #
    img = pygame.image.load('/Volumes/CRUZER/Python/Shocks/danger.jpg')
    screen.blit(img, (100,0))
    pygame.display.flip()
        
    #
    # continuously loop until stop time is met
    #
    stop = time.time() + 40
    while time.time() < stop :

            if time.time() in shocktimes:
                    trigger_shock()
                    timing = time.time() - starttime
                    with open(('ShocksTiming' + '/' + str(subject) + "_shocks.txt"), "a") as myfile:
                        myfile.write(str(timing) + '\n')

    fixation(starttime)
    
def main():
    #
    # wait for scanner
    #
    wait_4_scanner()
    
    # get start time
    #
    starttime = time.time()

    fixation(starttime)
    
    #
    # loop through task 10 times
    #
    for i in range(1,11):
    
        # 
        # generate random number between 1 and 10 in order to choose with part we run
        #
        choose = np.around(random.randint(1,10))
        
        # if we choose an even number do shocks else do safe
        if choose % 2 == 0:
            shocks(starttime)
        else:
            safe(starttime)

    pygame.display.quit()
            
if __name__ == '__main__':
    main()
