import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import pandas as pd
from timeit import default_timer as timer

def drawText(x, y, text, font):
    textSurface = font.render(text, True, (255, 255, 66, 255)).convert_alpha()
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glRasterPos2f(x, y)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

def display_letter(letter, z_pos):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    window_width, window_height = pygame.display.get_surface().get_size()
    glOrtho(0, window_width, 0, window_height, -1, 1)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Increase font size as it moves closer
    scale = 1 + (30 + z_pos) * 0.05  # Adjust multiplier for smoother scaling
    font_size = int(50 * scale)
    font = pygame.font.SysFont('arial', font_size)

    # Centering the text
    text_width = font.size(letter)[0]
    text_height = font.size(letter)[1]
    drawText(window_width / 2 - text_width / 2, window_height / 2 - text_height / 2, letter, font)

    pygame.display.flip()

def getting_ready(font):
    ready = False
    while not ready:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                ready = True

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        window_width, window_height = pygame.display.get_surface().get_size()
        glOrtho(0, window_width, 0, window_height, -1, 1)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        text = "READY!"
        text_width = font.size(text)[0]
        text_height = font.size(text)[1]
        drawText(window_width / 2 - text_width / 2, window_height / 2 - text_height / 2, text, font)

        pygame.display.flip()

subject_name = input('Please enter the subject\'s name: ')
filename = subject_name + '.xlsx'
BG_COLOR = pygame.Color(0, 0, 0)

displayedNumbersg = []
targetedClickg = []
realClickg = []

pygame.init()

info = pygame.display.Info()
pygame.display.set_mode((info.current_w, info.current_h), DOUBLEBUF | OPENGL)


pygame.display.set_caption("Go-NoGo")

glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
window_width, window_height = pygame.display.get_surface().get_size()
glOrtho(0, window_width, 0, window_height, -1, 1)

glMatrixMode(GL_MODELVIEW)


font = pygame.font.SysFont('arial', 200)
getting_ready(font)

start = timer()
crash = False

while not crash:
    letters = 'ABCD'
    newLetter = random.choice(letters)
    displayedNumbersg.append(newLetter)
    realClickg.append(0)
    if newLetter == 'C' or newLetter == 'D':
        targetedClickg.append(1)
    else:
        targetedClickg.append(0)
    
    z_pos = -50  # Reset z_pos for each new letter
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    crash = True
                    running = False
                if event.key == pygame.K_a:
                    realClickg[-1] = 1 
        
        display_letter(newLetter, z_pos)
        
        z_pos += 0.5  # Speed
        if z_pos >= 30:
            running = False

        pygame.time.wait(50)

    end = timer()
    elapsedTime = end - start
    if elapsedTime >= 10:
        crash = True

displayedNumbersg.append(-1)
targetedClickg.append(-1)
realClickg.append(-1)

results_gonogo = {
    'Displayed Numbers': displayedNumbersg,
    'Hoped Clicks': targetedClickg,
    'Real Clicks': realClickg
}

df3 = pd.DataFrame(results_gonogo)
print(elapsedTime)
writer = pd.ExcelWriter(filename, engine='xlsxwriter')
df3.to_excel(writer, sheet_name='GoNoGo')
writer.close()

pygame.quit()
exit()
