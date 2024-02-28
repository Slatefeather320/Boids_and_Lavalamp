import pygame, math
width = 300; height = 600
window = pygame.display.set_mode((width, height)) 
pygame.display.set_caption('Desktop Lavalamp')
lava = (255, 153, 112)
lamp = (46, 2, 38)

class Boids:
    def __init__(self, index, vel, pos):
        self.index = index
        self.pos = pos
        self.vel = vel

instances = []

def makeNewBoid(index, vel=pygame.Vector2(0,0), pos=pygame.Vector2(width/2,height/2)):
    instances.append(Boids(index, vel, pos))

def allign(boid, influence=0.07,radius=80):
    sumDir = pygame.Vector2()
    for otherBoid in instances:
        if otherBoid != boid and (otherBoid.pos - boid.pos).magnitude() < radius:
            sumDir += otherBoid.vel
    if sumDir.magnitude() > 0:
        boid.vel = ((sumDir.normalize()*influence) + boid.vel.normalize()).normalize()*boid.vel.magnitude()
    

def moveBoids():
    for boid in instances:
        boid.pos = boid.pos + boid.vel
        if boid.pos.x > width-20:
            boid.vel.x *= -1
        if boid.pos.x < 20:
            boid.vel.x *= -1
        if boid.pos.y > height-20:
            boid.vel.y *= -1
        if boid.pos.y < 20:
            boid.vel.y *= -1
        allign(boid)

def renderBoids():
    for Boid in instances:
        pygame.draw.circle(window, lava, Boid.pos, 50)

def splat(x=100):
    for i in range(0,x):
        theta = 2 * math.pi * i/x
        mag = 5
        xcomp = mag*math.sin(theta)
        ycomp = mag*math.cos(theta)
        makeNewBoid(i, pygame.Vector2(xcomp,ycomp))

splat(250)

running = True
while running:
    window.fill(lamp)
    moveBoids()
    renderBoids()
    pygame.display.update()
    pygame.time.Clock().tick(60)
    for event in pygame.event.get():   
        if event.type == pygame.QUIT: 
            running = False