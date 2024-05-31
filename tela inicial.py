import pygame 

pygame.init() 

width = 1280
height = 720
canvas = pygame.display.set_mode((width, height))

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 130, 0)
blue = (50, 153, 213)

pygame.display.set_caption("test zone") 
exit_game = False
font = pygame.font.SysFont(None, 24)

def title(text, color):
    text = font.render(text, True, color)
    canvas.blit(text, [800, 20])
    
def text_pos(text, color, width, height):
    text = font.render(text, True, color)
    canvas.blit(text, [width, height])
    
def game_title_screen():
    text_pos("Text Game", white, 640, 50)
    text_pos('press enter to start', white, 600, 540)
    text_pos('press esc to quit', white, 1000, 50)
    pygame.display.update()

while not exit_game:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            exit_game = True
    
    canvas.fill(black)
    game_title_screen()
    pygame.display.update()
    
pygame.quit()