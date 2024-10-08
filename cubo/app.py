import numpy as np
import pygame
import math


def aps4():
    def transform(verts, theta_x, theta_y, theta_z, dif_x, dif_y, dif_z, scale):

        scaling = np.array([[scale, 0, 0, 0],
                            [0, scale, 0, 0],
                            [0, 0, scale, 0],
                            [0, 0, 0, 1]])
        
        x_rotation = np.array([[1,0,0,0],
                            [0,math.cos(theta_x),-math.sin(theta_x),0],
                            [0,math.sin(theta_x),math.cos(theta_x),0],
                            [0,0,0,1]])
        
        y_rotation = np.array([[math.cos(theta_y),0,math.sin(theta_y),0],
                            [0,1,0,0],
                            [-math.sin(theta_y),0,math.cos(theta_y),0],
                            [0,0,0,1]])
        
        z_rotation = np.array([[math.cos(theta_z),-math.sin(theta_z),0,0],
                            [math.sin(theta_z),math.cos(theta_z),0,0],
                            [0,0,1,0],
                            [0,0,0,1]])
        
        translation = np.array([[1,0,0,dif_x],[0,1,0,dif_y],[0,0,1,dif_z],[0,0,0,1]])
        
        vertices = verts.T
        new_m = np.vstack((vertices, np.ones(vertices.shape[1])))

        A = translation @ x_rotation @ y_rotation @ z_rotation @ scaling @ new_m

        return A[:-1].T



    def lower_dim(x, y, z, d=200):
        # Matriz de projeção fornecida
        P = np.array([
            [0, 0, -d, 0],
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, -1/d, 0]
        ])

        ponto_homogeneo = np.array([x,y,z, 1]).T
        ponto_projetado = P @ ponto_homogeneo
        ponto_projetado = ponto_projetado/ponto_projetado[3]    

        return [int(x), int(y)]


    vertices = {
        "cubo": np.array([
        [-1, -1, -1],
        [ 1, -1, -1],
        [ 1,  1, -1],
        [-1,  1, -1],
        [-1, -1,  1],
        [ 1, -1,  1],
        [ 1,  1,  1],
        [-1,  1,  1]    
    ])*200,
        "diamante": np.array([
        [0, 0, -1],  
        [1, 0, 0], 
        [0, 1, 0],
        [-1, 0, 0],
        [0, -1, 0],
        [0, 0, 1]

    ]) * 200}


    arestas = { 

    "cubo": [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7)
    ],
    "diamante": [
        (0, 1), (0, 2), (0, 3), (0, 4),
        (5, 1), (5, 2), (5, 3), (5, 4),
        (1, 2), (2, 3), (3, 4), (4, 1)
    ]}

    pygame.init()
    screen = pygame.display.set_mode((1200,800))
    clock = pygame.time.Clock()
    running = True

    obj = "cubo"

    transformation_args = [-0.31999999999999995, -0.33999999999999997, 0, 580, 380, 0, 1]

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_LEFT]:
            transformation_args[1] -= 0.02
        if teclas[pygame.K_RIGHT]:
            transformation_args[1] += 0.02
        if teclas[pygame.K_UP]:
            transformation_args[0] += 0.02
        if teclas[pygame.K_DOWN]:
            transformation_args[0] -= 0.02

        if teclas[pygame.K_a]:
            transformation_args[3] -= 10
        if teclas[pygame.K_d]:
            transformation_args[3] += 10
        if teclas[pygame.K_w]:
            transformation_args[4] -= 10
        if teclas[pygame.K_s]:
            transformation_args[4] += 10
        if teclas[pygame.K_w]:
            transformation_args[4] -= 10
        if teclas[pygame.K_s]:
            transformation_args[4] += 10

        if teclas[pygame.K_p]:
            transformation_args[6] -= 0.02
        if teclas[pygame.K_o]:
            transformation_args[6] += 0.02

        if teclas[pygame.K_r]:
            transformation_args = [-0.31999999999999995, -0.33999999999999997, 0, 580, 380, 0, 1]

        if teclas[pygame.K_f]:
            if obj == "cubo":
                obj = "diamante"
            else:
                obj = "cubo"

        screen.fill("black")

        # RENDER YOUR GAME HERE
        # cubo.draw_cube(screen)
        # pygame.draw.line(screen, "white", (50,50),(100,100))

        vertices_rotacionados = transform(vertices[obj],*transformation_args)
        projected_points = [lower_dim(*vert) for vert in vertices_rotacionados]

            # Desenhando as arestas
        for aresta in arestas[obj]:
            pygame.draw.line(screen, "white", projected_points[aresta[0]], projected_points[aresta[1]], 2)

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()