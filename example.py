import pygame

pygame.init()

screen = pygame.display.set_mode((640, 640))
clock = pygame.time.Clock()

delta_time = 0.1 # used to scale motion to whatever fps not just one set fps

# image
# img = pygame.image.load('img.png').convert() or .convert_alpha() if png
# img = pygame.transform.scale(img, img.get_width() * 2, same with height)
# img.set_colorkey((0, 0, 0)) to get rid of color like black background

# blit surfaces # then you can render. might be faster ?
# images = pygame.Surface((64, 64), pygame.SRCALPHA) # makes surface you can put images on
# images.blit(img, (0, 0))

# sound
# sound = pygame.mixer.Sound('sound.wav')

# sound.play()

font = pygame.font.Font(None, size=30) # gets game font

running = True
y = 0
MOVE = 50
moving = False

while running:
    screen.fill((255, 255, 255))
    # screen.blit(img, (x, 30))
    # x += 1 * delta_time 
    # set alpha sets transperency
    
    
    text = font.render('Hello World', True, (0,0,0))
    hitbox = pygame.Rect(y, 100, text.get_width(), text.get_height())
    
    mpos = pygame.mouse.get_pos()
    
    target = pygame.Rect(300, 0, 160, 280)
    collision = hitbox.colliderect(target)
    m_collision = hitbox.collidepoint(mpos)
    pygame.draw.rect(screen, (255 * collision, 255, 0), target)
    
    screen.blit(text, (y, 100))
    if collision:
        MOVE *= -1
    elif m_collision:
        MOVE *= -1
  
    if moving:
        y += MOVE * delta_time
    

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                moving = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                moving = False
            
    pygame.display.flip() # display images when rendered
    
    delta_time = clock.tick(60) / 1000 # fps to display
    delta_time = max(0.001, min(0.1, delta_time))
    
pygame.quit()

class PongGame:
    def __init__():
        pass