import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# ==============================================================================
# CONFIGURAÇÕES E CORES
# ==============================================================================
DISPLAY_SIZE = (1024, 768)
COLOR_SKY     = (0.4, 0.6, 0.9, 1.0)
COLOR_GRASS_1 = (0.1, 0.45, 0.1)     
COLOR_GRASS_2 = (0.15, 0.55, 0.15)   
COLOR_ASPHALT = (0.2, 0.2, 0.23)     
COLOR_LINE    = (0.9, 0.9, 0.9)      
COLOR_SAND    = (0.76, 0.7, 0.5)     
COLOR_KERB_R  = (0.8, 0.1, 0.1)      
COLOR_KERB_W  = (0.9, 0.9, 0.9)      

# Cores Renault R25
RENAULT_BLUE_BASE = (0.0, 0.3, 0.7)
RENAULT_YELLOW_BASE = (1.0, 0.85, 0.0)
CARBON_BLACK_BASE = (0.15, 0.15, 0.15)
TIRE_GREY_BASE    = (0.2, 0.2, 0.2)
RIMS_SILVER_BASE  = (0.7, 0.7, 0.7)
GLOW_RED          = (1.0, 0.1, 0.1) 

# ==============================================================================
# HELPERS DE MODELAGEM
# ==============================================================================
def get_shaded_colors(base_color):
    top = [min(1.0, c * 1.3) for c in base_color]
    side = base_color
    bottom = [c * 0.7 for c in base_color]
    return top, side, bottom

def draw_cube_shaded(sx, sy, sz, base_color):
    color_top, color_side, color_bottom = get_shaded_colors(base_color)
    glPushMatrix()
    glScalef(sx, sy, sz)
    glBegin(GL_QUADS)
    glColor3f(*color_top); glNormal3f(0,1,0); glVertex3f(-0.5,0.5,0.5); glVertex3f(0.5,0.5,0.5); glVertex3f(0.5,0.5,-0.5); glVertex3f(-0.5,0.5,-0.5)
    glColor3f(*color_side)
    # Lados simplificados para performance
    glNormal3f(0,0,1); glVertex3f(-0.5,-0.5,0.5); glVertex3f(0.5,-0.5,0.5); glVertex3f(0.5,0.5,0.5); glVertex3f(-0.5,0.5,0.5)
    glNormal3f(0,0,-1); glVertex3f(-0.5,0.5,-0.5); glVertex3f(0.5,0.5,-0.5); glVertex3f(0.5,-0.5,-0.5); glVertex3f(-0.5,-0.5,-0.5)
    glNormal3f(-1,0,0); glVertex3f(-0.5,-0.5,-0.5); glVertex3f(-0.5,-0.5,0.5); glVertex3f(-0.5,0.5,0.5); glVertex3f(-0.5,0.5,-0.5)
    glNormal3f(1,0,0); glVertex3f(0.5,-0.5,0.5); glVertex3f(0.5,-0.5,-0.5); glVertex3f(0.5,0.5,-0.5); glVertex3f(0.5,0.5,0.5)
    glColor3f(*color_bottom); glNormal3f(0,-1,0); glVertex3f(-0.5,-0.5,-0.5); glVertex3f(0.5,-0.5,-0.5); glVertex3f(0.5,-0.5,0.5); glVertex3f(-0.5,-0.5,0.5)
    glEnd()
    glPopMatrix()

def draw_cylinder(radius, height, segments, base_color):
    quadric = gluNewQuadric()
    color_top, color_side, color_bottom = get_shaded_colors(base_color)
    glPushMatrix()
    glTranslatef(0, -height/2, 0) 
    glRotatef(-90, 1, 0, 0) 
    glColor3f(*color_bottom); gluDisk(quadric, 0, radius, segments, 1)
    glColor3f(*color_side); gluCylinder(quadric, radius, radius, height, segments, 1)
    glTranslatef(0, 0, height); glColor3f(*color_top); gluDisk(quadric, 0, radius, segments, 1)
    glPopMatrix()
    gluDeleteQuadric(quadric)

def draw_sphere(radius, segments, base_color):
    quadric = gluNewQuadric()
    glColor3f(*get_shaded_colors(base_color)[1]) 
    gluSphere(quadric, radius, segments, segments)
    gluDeleteQuadric(quadric)

def draw_wheel_ultra_detailed(radius, width, steer_angle=0, brake_glow=False):
    glPushMatrix()
    glRotatef(steer_angle, 0, 1, 0)
    quadric = gluNewQuadric()
    tire_top, tire_side, tire_bot = get_shaded_colors(TIRE_GREY_BASE)
    glColor3f(*tire_side)
    glPushMatrix()
    glTranslatef(0, 0, -width/2) 
    gluCylinder(quadric, radius, radius, width, 24, 1)
    glColor3f(*tire_bot); gluDisk(quadric, 0, radius, 24, 1)
    glPushMatrix()
    glTranslatef(0, 0, width/2)
    glColor3f(*CARBON_BLACK_BASE)
    gluDisk(quadric, radius * 0.4, radius * 0.8, 16, 1)
    if brake_glow:
        glColor3f(*GLOW_RED)
        glLineWidth(2)
        glBegin(GL_LINES)
        for i in range(12):
            angle = (i/12) * 2 * math.pi
            glVertex3f(math.cos(angle)*radius*0.5, math.sin(angle)*radius*0.5, 0)
            glVertex3f(math.cos(angle)*radius*0.7, math.sin(angle)*radius*0.7, 0)
        glEnd()
    glPopMatrix()
    glTranslatef(0, 0, width)
    glColor3f(*get_shaded_colors(CARBON_BLACK_BASE)[0])
    gluDisk(quadric, 0, radius, 24, 1)
    glColor3f(*get_shaded_colors(RIMS_SILVER_BASE)[0])
    gluDisk(quadric, 0, radius*0.7, 20, 1)
    glPushMatrix()
    glColor3f(0.05, 0.05, 0.05)
    gluSphere(quadric, radius*0.15, 8, 8)
    glPopMatrix()
    glPopMatrix()
    gluDeleteQuadric(quadric)
    glPopMatrix()

def draw_renault_car_ultimate_realism(steering):
    glTranslatef(0, 0.35, 0)
    # Chassi
    glPushMatrix(); glTranslatef(0, 0.2, -0.1); draw_cube_shaded(0.5, 0.4, 1.8, RENAULT_YELLOW_BASE); glPopMatrix()
    # Bico
    glPushMatrix(); glTranslatef(0, 0.05, 1.6); glRotatef(4, 1, 0, 0); draw_cube_shaded(0.3, 0.15, 1.2, RENAULT_BLUE_BASE)
    glPushMatrix(); glTranslatef(0, -0.1, 0.3); draw_cube_shaded(0.5, 0.1, 0.8, RENAULT_BLUE_BASE); glPopMatrix()
    glPushMatrix(); glTranslatef(0, 0.05, 0.8); draw_sphere(0.15, 12, RENAULT_BLUE_BASE); glPopMatrix()
    glPopMatrix()
    # Sidepods
    for side in [-1, 1]:
        glPushMatrix()
        glTranslatef(side * 0.5, 0.15, -0.1)
        draw_cube_shaded(0.45, 0.4, 0.8, RENAULT_BLUE_BASE)
        glPushMatrix(); glTranslatef(0,0,-0.7); glScalef(0.7, 1, 1.2); draw_cube_shaded(0.45, 0.4, 0.8, RENAULT_BLUE_BASE); glPopMatrix()
        glPushMatrix(); glTranslatef(side*0.3, 0.15, 0.2); glScalef(0.1, 0.2, 0.1); draw_cube_shaded(1,1,1, CARBON_BLACK_BASE); glPopMatrix()
        glPopMatrix()
    # Airbox
    glPushMatrix(); glTranslatef(0, 0.4, -0.5); draw_cube_shaded(0.3, 0.4, 0.8, RENAULT_YELLOW_BASE)
    glPushMatrix(); glTranslatef(0, 0.3, 0.0); glScalef(0.2, 0.1, 0.2); draw_cube_shaded(1,1,1, CARBON_BLACK_BASE); glPopMatrix()
    glPopMatrix()
    # Cockpit
    glPushMatrix(); glTranslatef(0, 0.4, 0.05); draw_cube_shaded(0.4, 0.3, 0.5, CARBON_BLACK_BASE)
    glPushMatrix(); glTranslatef(0, 0.3, -0.1); glScalef(0.08, 0.55, 0.08); draw_cube_shaded(1,1,1, CARBON_BLACK_BASE); glPopMatrix()
    glPushMatrix(); glTranslatef(0, 0.58, -0.1); glScalef(0.45, 0.08, 0.08); draw_cube_shaded(1,1,1, CARBON_BLACK_BASE); glPopMatrix()
    glPopMatrix()
    # Piloto
    glPushMatrix(); glTranslatef(0, 0.6, -0.1); draw_sphere(0.17, 16, RENAULT_BLUE_BASE)
    glPushMatrix(); glTranslatef(0, 0, 0.17); glRotatef(90, 1, 0, 0); draw_cylinder(0.15, 0.05, 10, CARBON_BLACK_BASE); glPopMatrix()
    glPopMatrix()
    # Asas
    glPushMatrix(); glTranslatef(0, -0.1, 2.1); glScalef(1.5, 0.03, 0.4); draw_cube_shaded(1,1,1, CARBON_BLACK_BASE); glPopMatrix()
    for side in [-1, 1]:
        glPushMatrix(); glTranslatef(side*0.75, -0.1, 2.1); glScalef(0.1, 0.25, 0.4); draw_cube_shaded(1,1,1, CARBON_BLACK_BASE); glPopMatrix()
    glPushMatrix(); glTranslatef(0, 0.6, -1.6); draw_cube_shaded(1.3, 0.25, 0.4, CARBON_BLACK_BASE); glPopMatrix()
    for side in [-1, 1]:
        glPushMatrix(); glTranslatef(side*0.65, 0.6, -1.6); glScalef(0.1, 0.4, 0.4); draw_cube_shaded(1,1,1, CARBON_BLACK_BASE); glPopMatrix()
    # Rodas
    glPushMatrix(); glTranslatef(-0.9, 0, 1.4); draw_wheel_ultra_detailed(0.32, 0.35, steering); glPopMatrix()
    glPushMatrix(); glTranslatef( 0.9, 0, 1.4); draw_wheel_ultra_detailed(0.32, 0.35, steering); glPopMatrix()
    glPushMatrix(); glTranslatef(-0.95, 0, -1.1); draw_wheel_ultra_detailed(0.35, 0.45, 0, brake_glow=True); glPopMatrix()
    glPushMatrix(); glTranslatef( 0.95, 0, -1.1); draw_wheel_ultra_detailed(0.35, 0.45, 0, brake_glow=True); glPopMatrix()

# ==============================================================================
# PISTA REFORMULADA (SEM BUGS)
# ==============================================================================
def generate_track_geometry():
    """ 
    Gera todos os vértices da pista antecipadamente.
    Isso evita 'buracos' nas curvas conectando os segmentos perfeitamente.
    """
    center_points = []
    steps = 300
    scale_x = 90
    scale_z = 60
    
    # Gerar linha central
    for i in range(steps):
        angle = (i / steps) * 2 * math.pi
        x = math.cos(angle) * scale_x
        z = math.sin(angle) * scale_z
        # Deformação suave
        if z < 0: z += math.sin(x*0.1) * 12
        if x > 50: z += math.cos(z*0.2) * 5
        center_points.append((x, z))
    
    # Fechar o loop duplicando os primeiros pontos no final
    center_points.append(center_points[0])
    center_points.append(center_points[1]) # Necessário para cálculo de tangente suave no fim
    
    track_width = 14.0
    
    left_points = []
    right_points = []
    
    # Gerar bordas baseadas na tangente
    # Ignoramos o último ponto auxiliar no loop de desenho
    for i in range(len(center_points) - 1):
        p_curr = center_points[i]
        p_next = center_points[i+1]
        
        dx = p_next[0] - p_curr[0]
        dz = p_next[1] - p_curr[1]
        length = math.sqrt(dx*dx + dz*dz)
        if length == 0: length = 1 # Evitar div por zero
        
        # Vetor Normal (Perpendicular)
        nx = -dz / length
        nz = dx / length
        
        # Cria vértices da esquerda e direita
        l_x = p_curr[0] + nx * track_width / 2
        l_z = p_curr[1] + nz * track_width / 2
        
        r_x = p_curr[0] - nx * track_width / 2
        r_z = p_curr[1] - nz * track_width / 2
        
        left_points.append((l_x, l_z))
        right_points.append((r_x, r_z))
        
    return center_points, left_points, right_points

def draw_environment(center_pts, left_pts, right_pts):
    # GRAMA (Chão)
    tileSize = 20.0
    mapRadius = 10
    glBegin(GL_QUADS)
    glNormal3f(0, 1, 0)
    for i in range(-mapRadius, mapRadius):
        for j in range(-mapRadius, mapRadius):
            if (i + j) % 2 == 0: glColor3f(*COLOR_GRASS_1)
            else:                glColor3f(*COLOR_GRASS_2)
            x0, z0 = i * tileSize, j * tileSize
            glVertex3f(x0, -0.5, z0); glVertex3f(x0 + tileSize, -0.5, z0)
            glVertex3f(x0 + tileSize, -0.5, z0 + tileSize); glVertex3f(x0, -0.5, z0 + tileSize)
    glEnd()

    # PISTA (Sem sobreposição/Z-Fighting)
    # Camadas de altura para evitar bugs visuais
    Y_SAND = -0.45
    Y_ASPHALT = -0.40
    Y_LINES = -0.38
    Y_KERB = -0.35 # Mais alto = Zebra 3D
    
    num_segs = len(center_pts) - 2 # -2 pois adicionamos pontos extras
    
    for i in range(num_segs):
        # Indices
        curr = i
        next_i = i + 1
        
        # Coordenadas
        l1x, l1z = left_pts[curr]
        r1x, r1z = right_pts[curr]
        l2x, l2z = left_pts[next_i]
        r2x, r2z = right_pts[next_i]
        
        # Vetores para cálculos de largura extra (Zebra/Brita)
        # Aproximação simples usando a diferença dos pontos
        dx = l1x - r1x
        dz = l1z - r1z
        len_w = math.sqrt(dx*dx + dz*dz)
        nx, nz = dx/len_w, dz/len_w # Vetor apontando para esquerda

        kerb_w = 2.0
        sand_w = 4.0
        
        # AREA DE ESCAPE (BRITA) - Camada mais baixa
        glColor3f(*COLOR_SAND)
        glBegin(GL_QUADS)
        # Esq
        glVertex3f(l1x, Y_SAND, l1z); glVertex3f(l2x, Y_SAND, l2z)
        glVertex3f(l2x + nx*(kerb_w+sand_w), Y_SAND, l2z + nz*(kerb_w+sand_w))
        glVertex3f(l1x + nx*(kerb_w+sand_w), Y_SAND, l1z + nz*(kerb_w+sand_w))
        # Dir
        glVertex3f(r1x, Y_SAND, r1z); glVertex3f(r2x, Y_SAND, r2z)
        glVertex3f(r2x - nx*(kerb_w+sand_w), Y_SAND, r2z - nz*(kerb_w+sand_w))
        glVertex3f(r1x - nx*(kerb_w+sand_w), Y_SAND, r1z - nz*(kerb_w+sand_w))
        glEnd()

        # ASFALTO - Camada Base
        glColor3f(*COLOR_ASPHALT)
        glBegin(GL_QUADS)
        glVertex3f(l1x, Y_ASPHALT, l1z); glVertex3f(l2x, Y_ASPHALT, l2z)
        glVertex3f(r2x, Y_ASPHALT, r2z); glVertex3f(r1x, Y_ASPHALT, r1z)
        glEnd()
        
        # LINHAS BRANCAS
        glColor3f(*COLOR_LINE)
        lw = 0.4 # Largura da linha
        glBegin(GL_QUADS)
        # Esq
        glVertex3f(l1x, Y_LINES, l1z); glVertex3f(l2x, Y_LINES, l2z)
        glVertex3f(l2x - nx*lw, Y_LINES, l2z - nz*lw); glVertex3f(l1x - nx*lw, Y_LINES, l1z - nz*lw)
        # Dir
        glVertex3f(r1x, Y_LINES, r1z); glVertex3f(r2x, Y_LINES, r2z)
        glVertex3f(r2x + nx*lw, Y_LINES, r2z + nz*lw); glVertex3f(r1x + nx*lw, Y_LINES, r1z + nz*lw)
        glEnd()
        
        # ZEBRAS 3D (RAMPA)
        is_red = (i // 4) % 2 == 0
        glColor3f(*COLOR_KERB_R) if is_red else glColor3f(*COLOR_KERB_W)
        
        glBegin(GL_QUADS)
        # Esq (Sobe do asfalto para fora)
        glVertex3f(l1x, Y_ASPHALT, l1z); glVertex3f(l2x, Y_ASPHALT, l2z)
        glVertex3f(l2x + nx*kerb_w, Y_KERB, l2z + nz*kerb_w)
        glVertex3f(l1x + nx*kerb_w, Y_KERB, l1z + nz*kerb_w)
        # Dir
        glVertex3f(r1x, Y_ASPHALT, r1z); glVertex3f(r2x, Y_ASPHALT, r2z)
        glVertex3f(r2x - nx*kerb_w, Y_KERB, r2z - nz*kerb_w)
        glVertex3f(r1x - nx*kerb_w, Y_KERB, r1z - nz*kerb_w)
        glEnd()

# ==============================================================================
# MAIN LOOP
# ==============================================================================
def main():
    pygame.init()
    pygame.display.set_mode(DISPLAY_SIZE, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("F1 Fixed Track - Sem Bugs, Sem Piscar")

    glMatrixMode(GL_PROJECTION); glLoadIdentity()
    gluPerspective(60, (DISPLAY_SIZE[0] / DISPLAY_SIZE[1]), 0.1, 400.0)
    glMatrixMode(GL_MODELVIEW); glLoadIdentity()
    glEnable(GL_DEPTH_TEST)
    glClearColor(*COLOR_SKY)

    # Gera a geometria UMA VEZ
    center_pts, left_pts, right_pts = generate_track_geometry()
    
    # Carro
    car_x, car_z = center_pts[0]
    car_angle = 90.0
    car_speed = 0.0
    steering_vis = 0.0
    camera_orbit_angle = 0.0
    clock = pygame.time.Clock()

    while True:
        dt = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); return
            if event.type == KEYDOWN and event.key == K_ESCAPE: pygame.quit(); return

        keys = pygame.key.get_pressed()
        if keys[K_UP]:    car_speed += 30.0 * dt
        elif keys[K_DOWN]: car_speed -= 30.0 * dt
        else:             car_speed *= 0.97
        car_speed = max(min(car_speed, 90.0), -20.0)

        turn_amount = 100.0 * dt * (abs(car_speed) / 90.0)
        if keys[K_LEFT]: car_angle += turn_amount * (1 if car_speed >= 0 else -1); steering_vis = 25
        elif keys[K_RIGHT]: car_angle -= turn_amount * (1 if car_speed >= 0 else -1); steering_vis = -25
        else: steering_vis = 0
            
        if keys[K_q]: camera_orbit_angle -= 120.0 * dt
        if keys[K_e]: camera_orbit_angle += 120.0 * dt

        rad_angle = math.radians(car_angle)
        car_x -= math.sin(rad_angle) * car_speed * dt
        car_z -= math.cos(rad_angle) * car_speed * dt

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT); glLoadIdentity()

        total_cam_angle = rad_angle + math.radians(camera_orbit_angle)
        cam_dist = 11.0 + (abs(car_speed) / 20.0)
        cam_height = 3.5 + (abs(car_speed) / 30.0)
        cam_x = car_x + math.sin(total_cam_angle) * cam_dist
        cam_z = car_z + math.cos(total_cam_angle) * cam_dist
        
        gluLookAt(cam_x, cam_height, cam_z, car_x, 1.0, car_z, 0, 1, 0)

        # Desenha a pista corrigida
        draw_environment(center_pts, left_pts, right_pts)

        glPushMatrix()
        glTranslatef(car_x, 0, car_z)
        glRotatef(car_angle + 180, 0, 1, 0)
        draw_renault_car_ultimate_realism(steering_vis)
        glPopMatrix()

        pygame.display.flip()

if __name__ == "__main__":
    main()