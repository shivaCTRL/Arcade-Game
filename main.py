import pygame
import os
pygame.font.init()
pygame.mixer.init()

width, height = 900,500
WIN = pygame.display.set_mode((width, height)) #sets the width and height of the game window
pygame.display.set_caption("Space Arcade!") #display's caption of the game

BORDER = pygame.Rect(width//2-5, 0, 10, height)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets','hitsound.mp3'))
BULLET_FIRE_SOUND =pygame.mixer.Sound(os.path.join('Assets','firesound.mp3'))

HEALTH_FONT =pygame.font.SysFont('ABC',40)
WINNER_FONT =pygame.font.SysFont('ABC',100)



GREY = (230,230,230)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
BULLET_VEL = 7
MAX_BULLETS = 3
FPS = 60
VEL = 5
spaceship_width, spaceship_height = 50, 50

LEFT_HIT = pygame.USEREVENT + 1
RIGHT_HIT = pygame.USEREVENT + 2

left_spaceship_img = pygame.image.load(os.path.join('Assets','left_spaceship.png'))
left_spaceship = pygame.transform.rotate(pygame.transform.scale(left_spaceship_img,(spaceship_width, spaceship_height)), 0)
right_spaceship_img = pygame.image.load(os.path.join('Assets','right_spaceship.png'))
right_spaceship = pygame.transform.rotate(pygame.transform.scale(right_spaceship_img,(spaceship_width, spaceship_height)), 0)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets','space.jpg')),(width, height))

def draw_window(left, right,left_bullets,right_bullets,left_health,right_health):
    #BG color for window
        WIN.fill(GREY)
        WIN.blit(SPACE,(0,0))
        pygame.draw.rect(WIN, BLACK, BORDER)

        left_health_text =HEALTH_FONT.render('Health:'+str(left_health),1,GREY)
        right_health_text =HEALTH_FONT.render('Health:'+str(right_health),1,GREY)
        WIN.blit(left_health_text,(10,10))
        WIN.blit(right_health_text,(width - left_health_text.get_width() - 15,10))



        WIN.blit(left_spaceship, (left.x, left.y))
        WIN.blit(right_spaceship, (right.x, right.y))


        
        for bullet in left_bullets:
                pygame.draw.rect(WIN,YELLOW,bullet)

        for bullet in right_bullets:
                pygame.draw.rect(WIN,RED,bullet)

        

        pygame.display.update() #updates the bg color

        



def handle_left_spaceship_movements(keys_pressed, left):
    if keys_pressed[pygame.K_a] and left.x - VEL > 0: #for LEFT
            left.x -= VEL
    if keys_pressed[pygame.K_d] and left.x + VEL + left.width < BORDER.x :  #for RIGHT
        left.x += VEL
    if keys_pressed[pygame.K_w] and left.y - VEL > 0 : #for up
            left.y -= VEL
    if keys_pressed[pygame.K_s] and left.y + VEL + left.height < height : #for down
            left.y += VEL


def handle_right_spaceship_movements(keys_pressed, right):
    if keys_pressed[pygame.K_LEFT] and right.x - VEL > BORDER.x + BORDER.width : #for LEFT
            right.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and right.x + VEL + right.width < width : #for RIGHT
            right.x += VEL
    if keys_pressed[pygame.K_UP] and right.y - VEL > 0 : #for up
            right.y -= VEL
    if keys_pressed[pygame.K_DOWN] and right.y + VEL + right.height < height : #for down
            right.y += VEL


def handle_bullets(left_bullets, right_bullets, left, right):

        for bullet in left_bullets:
                bullet.x += BULLET_VEL
                if right.colliderect(bullet):
                        pygame.event.post(pygame.event.Event(RIGHT_HIT))
                        left_bullets.remove(bullet)
                elif  bullet.x > width:
                        left_bullets.remove(bullet)       
        
        for bullet in right_bullets:
                bullet.x -= BULLET_VEL
                if left.colliderect(bullet):
                        pygame.event.post(pygame.event.Event(LEFT_HIT))
                        right_bullets.remove(bullet)
                elif  bullet.x < 0 :
                        right_bullets.remove(bullet)       
        
def draw_winner(text):
        draw_text = WINNER_FONT.render(text,1,GREY)
        WIN.blit(draw_text,(width/2 - draw_text.get_width()/2,height/2 - draw_text.get_height()/2))
        pygame.display.update()
        pygame.time.delay(5000)

def main():
    left =pygame.Rect(100, 300, spaceship_width, spaceship_height)
    right =pygame.Rect(700, 300, spaceship_width, spaceship_height)

    left_bullets = []
    right_bullets = []

    left_health = 10
    right_health = 10


    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LCTRL and len(left_bullets) < MAX_BULLETS:    
                        bullet = pygame.Rect(left.x + left.width, left.y + left.height//2 - 2, 10, 5)
                        left_bullets.append(bullet)
                        BULLET_FIRE_SOUND.play()

                    if event.key == pygame.K_RCTRL and len(right_bullets) < MAX_BULLETS :
                        bullet = pygame.Rect(right.x, right.y + right.height//2 - 2, 10, 5)
                        right_bullets.append(bullet) 
                        BULLET_FIRE_SOUND.play()

            if event.type == LEFT_HIT:
                    left_health -= 1
                    BULLET_HIT_SOUND.play()

            if event.type == RIGHT_HIT:    
                    right_health -= 1
                    BULLET_HIT_SOUND.play()

        
        winner_text = ''
        if left_health <= 0 :
                winner_text = 'RIGHT WON!!'

        if right_health <= 0 :
                winner_text = 'LEFT WON!'

        if winner_text != '':
                draw_winner(winner_text)
                break



        
        
        keys_pressed = pygame.key.get_pressed()
        handle_left_spaceship_movements(keys_pressed, left)
        handle_right_spaceship_movements(keys_pressed, right)

        handle_bullets(left_bullets, right_bullets, left, right)

        draw_window(left, right,left_bullets,right_bullets,left_health,right_health) #function call for displaying the window 

    main()    
        
        
        
        

if __name__ =="__main__":
    main()
