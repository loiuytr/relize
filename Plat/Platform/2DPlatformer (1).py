import pygame
from pygame import image, transform

BACKGROUND_COLOR = (0, 0, 0)

WIDTH = 1200
HEIGHT = 600

FPS = 60

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer")

playr_color = (0, 128, 255)
playr_x = 0
playr_width = 50
playr_height = 50
playr_y = HEIGHT - playr_height
playr_speed = 5

jump = False

gravity = 1
jump_streng = -15

start_jump = 0
grond_y = HEIGHT - playr_height

running = True

background = transform.scale(image.load("Fon.png"), (WIDTH, HEIGHT))
player_skin = transform.scale(image.load("1234.png"), (playr_width, playr_height))
def reset_player():
    global playr_x, playr_y, jump, start_jump
    playr_x = 0  
    playr_y = HEIGHT - playr_height  
    jump = False
    start_jump = 0

def draw_menu():
    font = pygame.font.Font(None, 74)
    text_start = font.render("Start", True, (255, 255, 255))
    text_exit = font.render("Exit", True, (255, 255, 255))

    start_rect = text_start.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    exit_rect = text_exit.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    screen.fill((0, 0, 0))  
    screen.blit(text_start, start_rect)
    screen.blit(text_exit, exit_rect)

    pygame.display.flip()

    return start_rect, exit_rect

def draw_level():
    font = pygame.font.Font(None, 74)
    text_level1 = font.render('Level 1', True, (255, 255, 255))

    Level_1 = text_level1.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    
    screen.fill((0, 0, 0))  
    screen.blit(text_level1, Level_1)
    
    pygame.display.flip()

    return Level_1


class Barriel:
    def __init__(self, color, x, y, width, height):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def collide(self, player_rect):
        return pygame.Rect(self.x, self.y, self.width, self.height).colliderect(player_rect)


def menu():
    global running
    menu_active = True
    
    start_rect, exit_rect = draw_menu()

    while menu_active:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                menu_active = False
                running = False
            if e.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_rect.collidepoint(mouse_pos):
                    menu_active = False
                    level_active = True
                    while level_active:
                        for e in pygame.event.get():
                            if e.type == pygame.QUIT:
                                level_active = False
                                running = False
                        Level_1 = draw_level()
                        if e.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = pygame.mouse.get_pos()
                            if Level_1.collidepoint(mouse_pos):
                                level_active = False
                elif exit_rect.collidepoint(mouse_pos):
                    menu_active = False
                    running = False


while running:
    menu()  

    playr_x = 0  
    playr_y = HEIGHT - playr_height  
    jump = False

    wall1 = Barriel((255, 255, 255), 500, 550, 150, 50)
    wall2 = Barriel((0,0,0),500,550,5,50)
    wall3 = Barriel((0,0,0),645,550,5,50)
    wall4 = Barriel((0,0,0),500,550,150,5)
    enemy = Barriel((0,0,0),800,550,20,50)
    enemy1 = Barriel((0,0,0),900,550,20,50)
    enemy2 = Barriel((0,0,0),620,500,20,50)
    wall5 = Barriel((255,255,255),1000,550,100,50)
    wall6 = Barriel((0,0,0),1000,550,5,50)
    wall7 = Barriel((0,0,0),1100,550,5,50)
    wall8 = Barriel((0,0,0),1000,550,100,5)

    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        player_rect = pygame.Rect(playr_x, playr_y, playr_width, playr_height)
        wall1_rect = pygame.Rect(wall1.x, wall1.y, wall1.width, wall1.height)
        enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
        enemy1_rect = pygame.Rect(enemy1.x, enemy1.y, enemy1.width, enemy1.height)
        enemy2_rect = pygame.Rect(enemy2.x, enemy2.y, enemy2.width, enemy2.height)
        wall5_rect = pygame.Rect(wall5.x, wall5.y, wall5.width, wall5.height)

        if keys[pygame.K_a] and playr_x > 0:
            new_rect = player_rect.move(-playr_speed, 0)
            if not wall1_rect.colliderect(new_rect) and not wall5_rect.colliderect(new_rect):
                playr_x -= playr_speed

        if keys[pygame.K_d] and playr_x < WIDTH - playr_width:
            new_rect = player_rect.move(playr_speed, 0)
            if not wall1_rect.colliderect(new_rect) and not wall5_rect.colliderect(new_rect):
                playr_x += playr_speed

        if keys[pygame.K_SPACE] and not jump:
            jump = True
            start_jump = jump_streng

        if jump:
            playr_y += start_jump
            start_jump += gravity

            if player_rect.colliderect(wall1_rect) and start_jump < 0: 
                playr_y = wall1.y - playr_height  
                jump = False
                start_jump = 0
            if player_rect.colliderect(wall5_rect) and start_jump < 0: 
                playr_y = wall5.y - playr_height  
                jump = False
                start_jump = 0               

            if playr_y >= grond_y:
                playr_y = grond_y
                jump = False
                start_jump = 0

        if not jump and playr_y < grond_y:
            playr_y = grond_y

        if player_rect.colliderect(wall1_rect):
            if playr_y + playr_height > wall1.y:  
                playr_y = wall1.y - playr_height  
                jump = False
                start_jump = 0
        if player_rect.colliderect(wall5_rect):
            if playr_y + playr_height > wall5.y:  
                playr_y = wall5.y - playr_height  
                jump = False
                start_jump = 0
        if player_rect.colliderect(enemy_rect) :
            font = pygame.font.Font(None, 74)
            lose_text = font.render('You Lose', True, (255, 255, 255))
            screen.fill((0, 0, 0))
            screen.blit(lose_text, lose_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
            pygame.display.flip()
            pygame.time.delay(2000)
            menu()
            reset_player()
        if player_rect.colliderect(enemy1_rect):
            font = pygame.font.Font(None, 74)
            lose_text = font.render('You Lose', True, (255, 255, 255))
            screen.fill((0, 0, 0))
            screen.blit(lose_text, lose_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
            pygame.display.flip()
            pygame.time.delay(2000)
            menu()
            reset_player()
        if player_rect.colliderect(enemy2_rect):
            font = pygame.font.Font(None, 74)
            lose_text = font.render('You Lose', True, (255, 255, 255))
            screen.fill((0, 0, 0))
            screen.blit(lose_text, lose_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
            pygame.display.flip()
            pygame.time.delay(2000)
            menu()
            reset_player()

        screen.blit(background, (0, 0))
        
        
        screen.blit(player_skin, (playr_x, playr_y))
        
        wall1.draw()
        wall2.draw()
        wall3.draw()
        wall4.draw()
        enemy.draw()
        enemy1.draw()
        enemy2.draw()
        wall5.draw()
        wall6.draw()
        wall7.draw()
        wall8.draw()

        pygame.display.flip()
        pygame.time.Clock().tick(FPS)

pygame.quit()
