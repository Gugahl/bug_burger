import pygame 

pygame.init() 

width = 1800
height = 900
canvas = pygame.display.set_mode((width, height))

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 130, 0)
blue = (50, 153, 213)

pygame.display.set_caption("test zone") 
exit_game = False
font = pygame.font.SysFont(None, 40)

def title(text, color):
    text = font.render(text, True, color)
    canvas.blit(text, [800, 20])
    
def text_pos(text, color, width, height):
    text = font.render(text, True, color)
    canvas.blit(text, [width, height])
    
def game_title_screen():
    title("this is a test message", blue)
    text_pos('press enter to start', red, 100, 450)
    text_pos('press esc to quit', red, 1300, 450)
    pygame.display.update()

while not exit_game:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            exit_game = True
    
    canvas.fill(black)
    game_title_screen()
    pygame.display.update()
    
pygame.quit()