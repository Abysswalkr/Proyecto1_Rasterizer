import pygame
from pygame.locals import *
from gl import *
from model import Model
from shaders import *

width = 940
height = 540

screen = pygame.display.set_mode((width, height), pygame.SCALED)
clock = pygame.time.Clock()

rend = Renderer(screen)
rend.glLoadBackground('textures/tren.bmp')

modelo1 = Model('models/cat.obj')
modelo1.loadTexture('textures/cat.bmp')
modelo1.vertexShader = vertexShader
modelo1.fragmentShader = dissolveShader
modelo1.translate[2] = -5
modelo1.translate[1] = -1.5
modelo1.translate[0] = -2
modelo1.scale[0] = 1.5
modelo1.scale[1] = 1
modelo1.scale[2] = 1.5

modelo2 = Model('models/jake.obj')
modelo2.loadTexture('textures/jake.bmp')
modelo2.vertexShader = vertexShader
modelo2.fragmentShader = blueRedStripesShader
modelo2.translate[2] = -16
modelo2.translate[0] = 0
modelo2.translate[1] = -1.5
modelo2.scale[0] = 1.5
modelo2.scale[1] = 1.1
modelo2.scale[2] = 1.5


modelo3 = Model('models/Coach.obj')
modelo3.loadTexture('textures/Coach.bmp')
modelo3.vertexShader = vertexShader
modelo3.fragmentShader = fireAndSmokeShader
modelo3.translate[2] = -5
modelo3.translate[0] = 2
modelo3.translate[1] = -1.5
modelo3.scale[0] = 1.5
modelo3.scale[1] = 1.5
modelo3.scale[2] = 1.5
modelo3.rotate[1] -= 90

modelo4 = Model('models/viejo.obj')
modelo4.loadTexture('textures/viejo.bmp')
modelo4.vertexShader = vertexShader
modelo4.fragmentShader = rgbLightShader
modelo4.translate[2] = -8
modelo4.translate[0] = -6
modelo4.translate[1] = -1.5
modelo4.scale[0] = 1.5
modelo4.scale[1] = 1.6
modelo4.scale[2] = 1.5
modelo4.rotate[1] -= 300


rend.models.append(modelo1)
rend.models.append(modelo2)
rend.models.append(modelo3)
rend.models.append(modelo4)


isRunning = True
while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False

            elif event.key == pygame.K_1:
                rend.primitiveType = POINTS

            elif event.key == pygame.K_2:
                rend.primitiveType = LINES

            elif event.key == pygame.K_3:
                rend.primitiveType = TRIANGLES

            elif event.key == pygame.K_4:
                modelo1.rotate[0] += 5
            elif event.key == pygame.K_5:
                modelo1.rotate[1] += 5
            elif event.key == pygame.K_6:
                modelo1.rotate[2] += 5


            elif event.key == pygame.K_RIGHT:
                rend.camera.translate[0] += 1
            elif event.key == pygame.K_LEFT:
                rend.camera.translate[0] -= 1
            elif event.key == pygame.K_UP:
                rend.camera.translate[1] += 1
            elif event.key == pygame.K_DOWN:
                rend.camera.translate[1] -= 1

    rend.glClear()
    rend.glClearBackground()

    rend.glRender()
    # rend.glTriangle(puntoA, puntoB, puntoC)

    pygame.display.flip()
    clock.tick(60)

rend.glGenerateFrameBuffer("output.bmp")

pygame.quit()
