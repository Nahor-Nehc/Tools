import pygame
import sys
import pygmtls as tools

pygame.init()

WIDTH, HEIGHT = 600, 700

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tester")

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED =   (211,   0,   0)
GREEN = (  0, 150,   0)
DGREEN = ( 0, 100,   0)
BLUE =  (  0,   0, 211)
LBLUE = (137, 207, 240)
GREY =  (201, 201, 201)
LGREY = (231, 231, 231)
LBROWN  = (185, 122, 87)
DBROWN = (159, 100, 64)

DURATION = 200 #ms
PADDING = 20

FONT = pygame.font.SysFont("consolas.ttf", 20)

FPS = 30

surface = pygame.Surface((100, 100))
surface.fill(RED)

TEST = pygame.USEREVENT + 1

def drawWin(buttons, scroll, headings):
  pygame.draw.rect(WIN, BLACK, pygame.Rect(0, 0, WIDTH, HEIGHT))
  buttons.draw(WIN)
  
  # surf = pygame.Surface((50,50))
  # surf.fill(GREEN)
  # surface.blit(surf, (50, 60))
  
  # WIN.blit(surface, (200, 200))
  #scroll.draw(WIN)
  headings.draw(WIN)
  pygame.display.flip()
  


def main():
  
  buttons = tools.Button()
  
  #initiates the clock
  clock = pygame.time.Clock()
  
  rect = pygame.Rect(PADDING, PADDING, 200, 100)
  
  scroll = tools.Scroll(100, 100, 500, 500, 2000, 20, WHITE)
  
  headings = tools.Menu.header(LGREY, WHITE, BLACK, 100, 100, 400, 40, ["1", "2", "oiuytgfdcvbghj", "right"], FONT, 20)

  #initiates game loop
  run = True
  while run:

    #ticks the clock
    clock.tick(FPS)

    #gets mouse position
    mouse = pygame.mouse.get_pos()

    #for everything that the user has inputted ...
    for event in pygame.event.get():
      
      #if the "x" button is pressed ...
      if event.type == pygame.QUIT:
        
        #ends game loop
        run = False
        
        #terminates pygame
        pygame.quit()
        
        #terminates system
        sys.exit()
        
      if event.type == pygame.KEYDOWN:
        scroll.draw_rect(RED, 100, 400, 200, 200, 3, BLACK)
        scroll.draw_circle(GREEN, 100, 200, 50, 10, BLUE)
        
      if event.type == pygame.MOUSEBUTTONUP:
        scroll.checkMouseUp(mouse)
        
      if event.type == pygame.MOUSEBUTTONDOWN:
        scroll.checkMouseDown(mouse)
        
      if event.type == pygame.MOUSEMOTION:
        scroll.checkMouseMotion(mouse)
        
      if event.type == pygame.MOUSEWHEEL:
        scroll.checkScroll(event, 10)

      if event.type == TEST:
        pass
        
    drawWin(buttons, scroll, headings)

main()