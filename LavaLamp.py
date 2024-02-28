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

def allignSeperate(boid, allignInfluence=0.14,seperateInfluence=0.001,allignRadius=100,seperateRadius=40):
    allignDir = pygame.Vector2()
    seperateDir = pygame.Vector2()
    for otherBoid in instances:
        if otherBoid != boid:
            if (otherBoid.pos - boid.pos).magnitude() < allignRadius:
                allignDir = allignDir + otherBoid.vel
            if (otherBoid.pos - boid.pos).magnitude() < seperateRadius:
                seperateDir = seperateDir + (boid.pos - otherBoid.pos)
    if allignDir.magnitude() > 0:
        boid.vel = ((allignDir.normalize()*allignInfluence)+ (seperateDir*seperateInfluence) + boid.vel.normalize()).normalize()*boid.vel.magnitude()
    

def moveBoids():
    hitbox = 35
    for boid in instances:
        boid.pos = boid.pos + boid.vel
        if boid.pos.x > width-hitbox:
            boid.vel.x *= -1
        if boid.pos.x < hitbox:
            boid.vel.x *= -1
        if boid.pos.y > height-hitbox:
            boid.vel.y *= -1
        if boid.pos.y < hitbox:
            boid.vel.y *= -1
        allignSeperate(boid)

def renderBoids():
    for Boid in instances:
        pygame.draw.circle(window, lava, Boid.pos, 40)

def splat(x=100):
    for i in range(0,x):
        theta = 2 * math.pi * i/x
        mag = 2.5
        xcomp = mag*math.sin(theta)
        ycomp = mag*math.cos(theta)
        makeNewBoid(i, pygame.Vector2(xcomp,ycomp))

splat(150)

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
