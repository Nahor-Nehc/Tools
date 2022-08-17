import pygame
import sys
import pygmtls as tools
import os

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

def drawWin(buttons, scroll, headings, explosions):
  pygame.draw.rect(WIN, WHITE, pygame.Rect(0, 0, WIDTH, HEIGHT))
  buttons.draw(WIN)
  
  explosions.play_all(WIN, True)
  
  # scroll.draw(WIN)
  # headings.draw(WIN)
  pygame.display.flip()


def main():
  
  buttons = tools.Button()
  
  #initiates the clock
  clock = pygame.time.Clock()
  
  rect = pygame.Rect(PADDING, PADDING, 200, 100)
  
  scroll = tools.Scroll(0, 100, 500, 500, 2000, 20, WHITE)
  
  explosions = tools.Animation_group()


  explosion1 = tools.Animation(10, 10, frame_type="image")
  
  explosion1.set_frames([pygame.transform.scale(pygame.image.load(os.path.join("Assets", "effects", "explosion", str(x) + ".png")), (50, 50)) for x in range(1, 13)])
  
  explosion1.set_offsets([[0, 0] for i in range(1, 13)])
  
  explosion1.duplicate_frame(3, 5)
  
  explosion2 = tools.Animation(10, 70, frame_type="image")
  
  explosion2.set_frames([pygame.transform.scale(pygame.image.load(os.path.join("Assets", "effects", "explosion", str(x) + ".png")), (50, 50)) for x in range(1, 13)])
  
  explosion2.set_offsets([[0, 0] for i in range(1, 13)])
  
  explosion2.duplicate_all_frames(2)
  
  explosion3 = tools.Animation(10, 130, frame_type="image")
  
  explosion3.set_frames([pygame.transform.scale(pygame.image.load(os.path.join("Assets", "effects", "explosion", str(x) + ".png")), (50, 50)) for x in range(1, 13)])
  
  explosion3.set_offsets([[0, 0] for i in range(1, 13)])
  
  explosion3.duplicate_all_frames(7)
  
  explosions.add_animation(explosion1)
  explosions.add_animation(explosion2)
  explosions.add_animation(explosion3)
  
  headings = tools.Menu.header(LGREY, WHITE, BLACK, 0, 0, WIDTH, 40, ["1", "2", "oiuytgfdcvbghj", "right"], FONT, 20)

  #initiates game loop
  run = True
  while run:

    #ticks the clock
    clock.tick(FPS)

    #gets mouse position
    mouse = pygame.mouse.get_pos()
    
    for i in range(0, scroll.total, 50):
      col = i//7.5
      if col > 255:
        col = 20
    
      scroll.draw_rect((col, col, col), 200, i, 30, 30)


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
        if event.key == pygame.K_RIGHT:
          headings.incrementCurrent()
        if event.key == pygame.K_LEFT:
          headings.decrementCurrent()
          
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
        
    drawWin(buttons, scroll, headings, explosions)

main()