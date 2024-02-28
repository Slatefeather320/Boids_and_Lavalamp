import pygame, math
width = 1000; height = 600
window = pygame.display.set_mode((width, height)) 
pygame.display.set_caption('Boids')

##########################################
#USER SETTINGS
bounce = False #Set to true if you want boids to bounce off of window edge
allignInfluence = 0.1
seperateInfluence = 0.005
cohesionInfluence = 0.001
allignRadius = 100
seperateRadius = 20  
cohesionRadius = 100
##########################################

class Boids:
    def __init__(self, index, vel, pos):
        self.index = index
        self.pos = pos
        self.vel = vel

instances = []

def makeNewBoid(index, vel=pygame.Vector2(0,0), pos=pygame.Vector2(width/2,height/2)):
    instances.append(Boids(index, vel, pos))

def asc(boid, allignInfluence=0.1,seperateInfluence=0.005, cohesionInfluence=0.001, allignRadius=100,seperateRadius=20,  cohesionRadius=100):
    allignDir = pygame.Vector2()
    seperateDir = pygame.Vector2()
    cohesianAverage = pygame.Vector2(0,0)
    count = 0
    for otherBoid in instances:
        if otherBoid != boid:
            dist = (otherBoid.pos - boid.pos).magnitude()
            if dist < allignRadius:
                allignDir = allignDir + otherBoid.vel
            if dist < seperateRadius:
                seperateDir = seperateDir + (boid.pos - otherBoid.pos)
            if dist < cohesionRadius:
                cohesianAverage = cohesianAverage + otherBoid.pos
                count+=1
    if cohesianAverage.magnitude()>0:
        cohesianAverage /= count
    if allignDir.magnitude() > 0:
        boid.vel = ((allignDir.normalize()*allignInfluence)+ (seperateDir*seperateInfluence) + ((cohesianAverage-boid.pos)*cohesionInfluence) + boid.vel.normalize()).normalize()*boid.vel.magnitude()
    

def moveBoids():
    for boid in instances:
        boid.pos = boid.pos + boid.vel
        if boid.pos.x > width:
            if bounce:
                boid.vel.x = abs(boid.vel.x)*-1
            else:
                boid.pos.x = 0
        if boid.pos.x < 0:
            if bounce:
                boid.vel.x = abs(boid.vel.x)
            else:
                boid.pos.x = width
        if boid.pos.y > height:
            if bounce:
                boid.vel.y = abs(boid.vel.y)*-1
            else:
                boid.pos.y = 0
        if boid.pos.y < 0:
            if bounce:
                boid.vel.y = abs(boid.vel.y)
            else:
                boid.pos.y = height
        asc(boid,allignInfluence,seperateInfluence,cohesionInfluence,allignRadius,seperateRadius,cohesionRadius)

def renderBoids():
    for Boid in instances:
        pygame.draw.circle(window, (10,10,60), Boid.pos, 15)

def splat(x=100):
    for i in range(0,x):
        theta = 2 * math.pi * i/x
        mag = 5
        xcomp = mag*math.sin(theta)
        ycomp = mag*math.cos(theta)
        makeNewBoid(i, pygame.Vector2(xcomp,ycomp),pygame.Vector2((width/2)+xcomp*25,(height/2)+ycomp*25))

splat(100)

running = True
while running:
    window.fill((255,255,255))
    moveBoids()
    renderBoids()
    pygame.display.update()
    pygame.time.Clock().tick(60)
    for event in pygame.event.get():   
        if event.type == pygame.QUIT: 
            running = False