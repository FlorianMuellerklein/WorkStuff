import time
import random
import pygame
import serial
import numpy as np

# get subject number
#
subject = raw_input('Enter participant id ... ')
#

# initialize data files
#
open(('ShocksTiming' + '/' + str(subject) + '_shocks.txt'), 'a').close()
open(('ShocksTiming' + '/' + str(subject) + '_shockstim.txt'), 'a').close()
open(('ShocksTiming' + '/' + str(subject) + '_noshocks.txt'), 'a').close()
open(('ShocksTiming' + '/' + str(subject) + '_fixation.txt'), 'a').close()
#

# set up display pattern
pattern1 = ['safe', 'shock', 'safe', 'safe', 'shock', 'shock', 'shock', 'safe', 'safe', 'shock']
pattern2 = ['safe', 'shock', 'shock', 'safe', 'safe', 'shock', 'safe', 'shock', 'safe', 'shock']

# initialize pygame window
#
pygame.init()
w = 800
h = 600
size = (w,h)
screen = pygame.display.set_mode((size), pygame.FULLSCREEN)
pygame.mouse.set_visible(False)
#

def wait_4_scanner():
    task_trig = serial.Serial(0)
    print 'wait for scanner ... '
    while True:
        if task_trig.read() > 0:
            break
            
def trigger_shock():
    shock_trig = serial.Serial(0)
    shock_trig.write(str(1))
    shock_trig.close()
    
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
    stop = time.time() + 10
    while time.time() < stop:
        img = pygame.image.load('E:\Python\Shocks\cross.bmp')
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
            img2 = pygame.image.load('E:\Python\Shocks\safe.jpg')
            screen.blit(img2, (100,0))
            pygame.display.flip()
    
    fixation(starttime)
            
def shocks(starttime, shock_counter, shocktime1, shocktime2, shocktime3, shocktime4):
    print 'shocks'
    
    # 
    # writing timing of onset of shock stim to file
    #
    timing = time.time() - starttime
    with open(('ShocksTiming' + '/' + str(subject) + "_shockstim.txt"), "a") as myfile:
        myfile.write(str(timing) + '\n')
        
    #
    # put up shock stim
    #
    img = pygame.image.load('E:\Python\Shocks\danger.jpg')
    screen.blit(img, (100,0))
    pygame.display.flip()
        
    #
    # continuously loop until stop time is met
    #
    stop = time.time() + 40
    while time.time() < stop :

            if time.time() == shocktime1 and shock_counter <= 13:
                    print 'shock'
                    trigger_shock()
                    timing = time.time() - starttime
                    with open(('ShocksTiming' + '/' + str(subject) + "_shocks.txt"), "a") as myfile:
                        myfile.write(str(timing) + '\n')
                    shock_counter += 1

            if time.time() == shocktime2 and shock_counter <= 13:
                    print 'shock'
                    trigger_shock()
                    timing = time.time() - starttime
                    with open(('ShocksTiming' + '/' + str(subject) + "_shocks.txt"), "a") as myfile:
                        myfile.write(str(timing) + '\n')
                    shock_counter += 1

            if time.time() == shocktime3 and shock_counter <= 13:
                    print 'shock'
                    trigger_shock()
                    timing = time.time() - starttime
                    with open(('ShocksTiming' + '/' + str(subject) + "_shocks.txt"), "a") as myfile:
                        myfile.write(str(timing) + '\n')
                    shock_counter += 1

            if time.time() == shocktime4 and shock_counter <= 13:
                    print 'shock'
                    trigger_shock()
                    timing = time.time() - starttime
                    with open(('ShocksTiming' + '/' + str(subject) + "_shocks.txt"), "a") as myfile:
                        myfile.write(str(timing) + '\n')
                    shock_counter += 1
    
    fixation(starttime)

    return shock_counter
    
def main():
    #
    # wait for scanner
    #
    #wait_4_scanner()

    # initialize shock counter, each person gets no more than 14
    shock_counter = 0
    
    # get start time
    #
    starttime = time.time()

    fixation(starttime)
    
    #
    # loop through task randomly choosing one of two patterns
    #
    if random.randint(0,10) % 2 == 0:
        task_pattern = pattern1
    else:
        task_pattern = pattern2
    
    for p in task_pattern:
        
        # if we choose an even number do shocks else do safe
        if p == 'shock':
                #
            # generate 4 random times to administer shocks
            #
            randtime1 = np.around(random.randint(1, 60))
            shocktime1 = time.time() + randtime1
            randtime2 = np.around(random.randint(1, 60))
            shocktime2 = time.time() + randtime2
            randtime3 = np.around(random.randint(1, 60))
            shocktime3 = time.time() + randtime3
            randtime4 = np.around(random.randint(1, 60))
            shocktime4 = time.time() + randtime4
            shock_counter = shocks(starttime, shock_counter, shocktime1, shocktime2, shocktime3, shocktime4)
        else:
            safe(starttime)

    pygame.display.quit()
            
if __name__ == '__main__':
    main()
