import pygame
import time
import random
pygame.font.init()


#screen size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
STAR_WIDTH = 10
STAR_HEIGHT = 10
STAR_SPEED = 5

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Space dodge')

bg = pygame.transform.scale(pygame.image.load('assets/space_image.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))

PLAYER_WIDTH = 60
PLAYER_HEIGHT = 80
MAX_SPEED = 30

FONT = pygame.font.SysFont('comicsans', 30)

class HealthBar():
    def __init__(self, x, y, w, h, max_hp):
        self.x = x 
        self.y = y
        self.w = w
        self.h = h
        self.hp = max_hp
        self.max_hp = max_hp

    def draw(self, surface):
        # calculate health ratio
        ratio = self.hp / self.max_hp
        pygame.draw.rect(surface, 'red', (self.x, self.y, self.w, self.h))
        pygame.draw.rect(surface, 'green', (self.x, self.y, self.w*ratio, self.h))



def draw(player, speed_bar, elapsed_time, stars):
    screen.blit(bg, (0,0))
    
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    screen.blit(time_text, (10, 50))
    
    pygame.draw.rect(screen, 'red', player)
    
    for star in stars:
        pygame.draw.rect(screen, 'white', star)
        
    speed_bar.draw(screen)
    pygame.display.update()

def main():
    run = True
    hit = False
    
    PLAYER_SPEED = 15
    player = pygame.Rect(200, SCREEN_HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    speed_bar = HealthBar(10, 10, 200, 20, MAX_SPEED)
    speed_bar.hp = PLAYER_SPEED
    
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0
    
    star_add_increment = 2000
    star_count = 0
    
    stars = []
    
    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time
        
        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, SCREEN_WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)
            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0
            
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                run = False
                break
            
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_SPEED> 0:
            player.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and player.x + PLAYER_SPEED + PLAYER_WIDTH <= SCREEN_WIDTH:
            player.x += PLAYER_SPEED
        if keys[pygame.K_DOWN] and PLAYER_SPEED > 0:
            speed_bar.hp -= 1
            PLAYER_SPEED -= 1
        
        if keys[pygame.K_UP] and PLAYER_SPEED < MAX_SPEED:
            speed_bar.hp += 1
            PLAYER_SPEED += 1      
        
        for star in stars[:]:
            star.y += STAR_SPEED
            if star.y > SCREEN_HEIGHT:
                stars.remove(star)
            if star.y + STAR_HEIGHT >= player.y and star.colliderect(player):
                # hit = True
                print("hit")  
        
        if hit: 
            lost_text = FONT.render("You lost!", 1, "white")        
            screen.blit(lost_text, (SCREEN_WIDTH/2 - lost_text.get_width()/2, SCREEN_HEIGHT/2 - lost_text.get_height()))  
            pygame.display.update()
            pygame.time.delay(5000)
            break
        
        draw(player, speed_bar, elapsed_time, stars)
    
    pygame.quit()    

if __name__ == "__main__":
    main()