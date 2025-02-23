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

    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        
        if keys[pygame.K_a] and playr_x > 0:
            player_rect = pygame.Rect(playr_x - playr_speed, playr_y, playr_width, playr_height)
            if not wall1.collide(player_rect):
                playr_x -= playr_speed

        
        if keys[pygame.K_d] and playr_x < WIDTH - playr_width:
            player_rect = pygame.Rect(playr_x + playr_speed, playr_y, playr_width, playr_height)
            if not wall1.collide(player_rect):
                playr_x += playr_speed

        
        if keys[pygame.K_SPACE] and not jump:
            jump = True
            start_jump = jump_streng

        if jump:
            playr_y += start_jump
            start_jump += gravity

            if playr_y >= grond_y:
                playr_y = grond_y
                jump = False
                start_jump = 0

        
        player_rect = pygame.Rect(playr_x, playr_y, playr_width, playr_height)
        if wall1.collide(player_rect):
            if playr_y + playr_height > wall1.y:  
                playr_y = wall1.y - playr_height
                jump = False
                start_jump = 0

        screen.blit(background, (0, 0))

        pygame.draw.rect(screen, playr_color, (playr_x, playr_y, playr_width, playr_height))
        wall1.draw()

        pygame.display.flip()
        pygame.time.Clock().tick(FPS)

pygame.quit()
