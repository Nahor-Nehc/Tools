import pygame

class Button:
  def __init__(self):
    self.buttons = []
    self.visible = []
    self.hidden = []
    
    self.attrs = {
      "rect" : 0,
      "colour" : 1,
      "event" : 2,
      "outlineWidth" : 3,
      "outlineColour" : 4,
      "text" : 5,
      "font" : 6,
      "textColour" : 7,
    }
    
  def create(self, rect, colour, event, outlineWidth = 0, outlineColour = (0, 0, 0), visible = True, text = "", font = None, textColour = (0, 0, 0)):
    temp = [rect, colour, event, outlineWidth, outlineColour, text, font, textColour]
    if visible == True:
      self.visible.append(temp)
    else:
      self.hidden.append(temp)
    self.buttons.append(temp)

  def draw(self, window):
    for button in self.visible:
      pygame.draw.rect(window, button[self.attrs["colour"]], button[self.attrs["rect"]])
      if button[self.attrs["outlineWidth"]] != 0:
        pygame.draw.rect(window, button[self.attrs["outlineColour"]], button[self.attrs["rect"]], button[self.attrs["outlineWidth"]])
      if button[self.attrs["font"]] != None:
        txt = button[self.attrs["font"]].render(button[self.attrs["text"]], 1, button[self.attrs["textColour"]])
        window.blit(txt, (button[self.attrs["rect"]].centerx - txt.get_width()/2, button[self.attrs["rect"]].centery - txt.get_height()/2))
      
  def check(self, mouse):
    for button in self.visible:
      if button[self.attrs["rect"]].collidepoint(mouse):
        pygame.event.post(pygame.event.Event(button[self.attrs["event"]]))
        
  def toggleVis(self, rect):
    edited = False
    for button in self.visible:
      if button[self.attrs["rect"]] == rect:
        self.visible.remove(button)
        self.hidden.append(button)
        edited = True
        
    if edited == False:
      for button in self.hidden:
        if button[self.attrs["rect"]] == rect:
          self.hidden.remove(button)
          self.visible.append(button)
      
  def changeAttr(self, rect, attr, newVal):
    if attr in self.attrs.keys():
      for button in self.buttons:
        if button[self.attrs["rect"]] == rect:
          button[self.attrs[attr]] = newVal
    else:
      raise ValueError("Attribute does not exist: " + str(attr))
    
  def remove(self, rect):
    for button in self.buttons:
      if button[self.attrs["rect"]] == rect:
        self.buttons.remove(button)
        try:
          self.hidden.remove(button)
        except:
          self.visible.remove(button)


class Scroll:
  def __init__(self, x, y, width, height, maxHeight, scrollbarWidth, colour):
    self.buffer = 2
    
    self.currentY = 0
    
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.total = maxHeight
    self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    self.surface = pygame.Surface((self.width, self.height))
    self.colour = colour
    
    self.surface.fill(self.colour)
    
    self.scrollClickY = 0
    
    self.scrollBar = [self.width - scrollbarWidth - self.buffer, self.height*(self.currentY/self.total) + self.buffer, scrollbarWidth, (self.height/self.total)*self.height - self.buffer*2]
    self.scrollBarRect = pygame.Rect(*self.scrollBar)
    self.down = False
    
    self.items = []
    
  def draw(self, window):
    window.blit(self.surface, (self.x, self.y))
    pygame.draw.rect(self.surface, self.colour, pygame.Rect(0, 0, self.width, self.height))
    for item in self.items:
      if item["shape"] == "rect":
        pygame.draw.rect(self.surface, item["colour"], pygame.Rect(item["x"], item["y"]-self.currentY, item["width"], item["height"]))
        if item["borderWidth"] != None and item["borderColour"] != None:
          pygame.draw.rect(self.surface, item["borderColour"], pygame.Rect(item["x"], item["y"]-self.currentY, item["width"], item["height"]), item["borderWidth"])
          
      elif item["shape"] == "line":
        pygame.draw.aaline(self.surface, item["colour"], (item["start"][0], item["start"][1]-self.currentY), (item["end"][0], item["end"][1]-self.currentY), item["width"])
        
      elif item["shape"] == "circle":
        pygame.draw.circle(self.surface, item["colour"], (item["centerx"], item["centery"] - self.currentY), item["radius"])
        if item["borderWidth"] != None and item["borderColour"] != None:
          pygame.draw.circle(self.surface, item["borderColour"], (item["centerx"], item["centery"] - self.currentY), item["radius"], item["borderWidth"])
          
    
    pygame.draw.rect(self.surface, (211, 211, 211), self.scrollBarRect)

  def draw_rect(self, colour, x, y, width, height, borderWidth=None, borderColour=None):
    dictionary = {
      "shape" : "rect",
      "colour" : colour,
      "x" : x,
      "y" : y,
      "width" : width,
      "height" : height,
      "borderWidth" : borderWidth,
      "borderColour" : borderColour
    }
    self.items.append(dictionary)
    
  def draw_line(self, colour, start, end, width):
    dictionary = {
      "shape" : "line",
      "colour" : colour,
      "start" : start,
      "end" : end,
      "width" : width
    }
    self.items.append(dictionary)
    
  def draw_circle(self, colour, centerx, centery, radius, borderWidth = None, borderColour = None):
    dictionary = {
      "shape" : "circle",
      "colour" : colour,
      "centerx" : centerx,
      "centery" : centery,
      "radius" : radius,
      "borderWidth" : borderWidth,
      "borderColour" : borderColour
    }
    self.items.append(dictionary)

  def blit(self, surface, destination):
    pass
  
  def checkMouseDown(self, mouse):
    rect = pygame.Rect(self.scrollBarRect.left + self.x, self.scrollBarRect.top + self.y, self.scrollBarRect.width, self.scrollBarRect.height)
    if rect.collidepoint(mouse):
      self.scrollClickY = mouse[1]
      self.down = True
      self.origin = self.scrollBarRect[1]
      
  def checkMouseMotion(self, mouse):
    if pygame.mouse.get_pressed()[0] and self.down == True:
      self.currentY = self.origin + mouse[1] - self.scrollClickY
      
      if self.currentY < self.buffer:
        self.currentY = self.buffer
        
      elif self.currentY > self.height - self.scrollBarRect.height - self.buffer:
        self.currentY = self.height - self.scrollBarRect.height - self.buffer
      self.scrollBar[1] = self.currentY
      self.scrollBarRect = pygame.Rect(*self.scrollBar)
        
  def checkMouseUp(self, mouse):
    self.scrollClickY = 0
    self.down = False

  def checkScroll(self, event, sensitivity=5):
    self.currentY -= sensitivity*event.y
    if self.currentY < self.buffer:
      self.currentY = self.buffer

    elif self.currentY > self.height - self.scrollBarRect.height - self.buffer:
      self.currentY = self.height - self.scrollBarRect.height - self.buffer
      
    self.scrollBar[1] = self.currentY
    self.scrollBarRect = pygame.Rect(*self.scrollBar)
    
class Menu:
  class header:
    def __init__(self, bgcolour, fgcolour, textcolour, x, y, width, height, headings, font, padding, outlinecolour=(0, 0, 0)):
      self.bgcolour = bgcolour
      self.fgcolour = fgcolour
      self.textcolour = textcolour
      self.outlinecolour = outlinecolour
      self.font = font
      self.padding = padding
      self.x = x
      self.y = y
      self.width = width
      self.height = height
      self.headings = headings
      self.current = 0
      
    def setCurrent(self, current):
      self.current = current
      
    def draw(self, window):
      pygame.draw.rect(window, self.bgcolour, pygame.Rect(self.x, self.y, self.width, self.height))
      pygame.draw.line(window, self.outlinecolour, (0, self.y + self.height), (self.width, self.y + self.height))
      totalLen = self.x + 5
      for heading in self.headings:
        text = self.font.render(heading.upper(), 1, self.textcolour)
        if self.headings.index(heading) == self.current:
          pygame.draw.rect(window, self.outlinecolour, pygame.Rect(totalLen, self.y, text.get_width()+self.padding, self.height-1), 1)
          pygame.draw.rect(window, self.fgcolour, pygame.Rect(totalLen + 1, self.y + 1, text.get_width()+self.padding - 2, self.height-2))
        else:
          pygame.draw.rect(window, self.outlinecolour, pygame.Rect(totalLen, self.y + self.padding/5, text.get_width()+ self.padding, self.y + self.height+1-self.padding/5), 1)
        window.blit(text, (totalLen + self.padding/2, (self.y*2 + self.height-text.get_height())/2))
        totalLen += text.get_width()+self.padding-1

