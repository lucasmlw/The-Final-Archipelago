import pygame
import sys
import wx
import pandas as pd
import random

##initialise pygame
pygame.init()
class system():
    start = 0

##get screen size info
outp = wx.App(False)
width, height = wx.GetDisplaySize()

##monsters

##use pandas to read in the excel file and choose a random monster
pd.set_option('display.max_columns', None)
df = pd.read_excel('Monster Spreadsheet (D&D5e).xlsx')

def random_monster():
    selection = random.choice(list(df["Name"]))
    return df.loc[df['Name'] == selection]

##NEW CLASSES!
class colour():
    black = (0,0,0)
    white = (255,255,255)
    red = (200,50,50)
    green = (50,200,50)
    blue = (50,50,200)

    bg1 = (50,85,150) ##dark blue
    bg2 = (0,30,100) ##darker blue

class font():
    default = pygame.font.SysFont(None, 30)
    Arial_20 = pygame.font.SysFont('Arial', 20)

class screen():
    sidebar_status = "closed"
    button_rect = pygame.Rect(0,0,0,0)
    sidebar_rect = pygame.Rect(0,0,0,0)
    
    def open_sidebar(display, xpos, ypos, bg):
        screen.sidebar_status = "open"
        display.fill(colour.black)
        display.blit(bg, (-ypos, -ypos))
        w, h = pygame.display.get_surface().get_size()
        screen.button_rect = pygame.Rect(w-200,(h/2)-50,20,100)
        screen.sidebar_rect = pygame.Rect(w-200,0,200,h)
        pygame.draw.rect(display, colour.bg2, screen.sidebar_rect)
        pygame.draw.rect(display, colour.bg1, screen.button_rect)
        display.blit(font.default.render('>', True, colour.white), (w-196, (h/2)-12))

    def close_sidebar(display, xpos, ypos, bg):
        screen.sidebar_status = "closed"
        display.fill(colour.black)
        display.blit(bg, (-xpos, -ypos))
        screen.sidebar_rect = pygame.Rect(0,0,0,0)
        w, h = pygame.display.get_surface().get_size()
        screen.button_rect = pygame.Rect(w-20,(h/2)-50,20,100)
        pygame.draw.rect(display, colour.bg1, screen.button_rect)
        display.blit(font.default.render('<', True, colour.white), (w-15, (h/2)-12))

##main game (mainloop)
class DndMainGame:

    ##colours
    BLACK = (0,0,0)
    WHITE = (255,255,255)

    background_image = pygame.image.load("Images/map.jpg")
    background_rect = background_image.get_rect()
    
     # Initialize clock for controlling the frame rate
    clock = pygame.time.Clock()

    # Calculate the initial camera position to start in the center of the image
    camera_x = 0
    camera_y = 0
    change_x =0
    
    # Flags to track keyboard input for camera movement
    moving_left = False
    moving_right = False
    moving_up = False
    moving_down = False
    
    #font = pygame.font.Font(None, 36)
    
    running = True
    mouse_x = mouse_y = 0
    
    scroll_direction = 0
    scroll_scale = 1
    scrolling = False
    last_scroll_time = pygame.time.get_ticks()
    scroll_stop_threshold = 50
    
    # centre
    centre = 0
    
    def __init__(self, w, h, f, camera_speed):
        self.WIDTH = w
        self.HEIGHT = h
        self.FPS = f

        ##create the screen
        self.screen = pygame.display.set_mode((self.WIDTH/1.5, self.HEIGHT/1.5), pygame.RESIZABLE)
        pygame.display.set_caption("DND")

        ##
        self.camera_x = (self.background_rect.width - self.WIDTH) // 2
        self.camera_y = (self.background_rect.height - self.HEIGHT) // 2
        
        self.camera_speed = camera_speed

    def handle_events(self):
        for event in pygame.event.get():

            ##detect button (for opening and closing sidebar) press NEW
            if event.type == pygame.MOUSEBUTTONDOWN and screen.button_rect.collidepoint(event.pos):
                print("button click")
                if screen.sidebar_status == "open":
                    screen.close_sidebar(display=self.screen, xpos=self.camera_x, ypos=self.camera_y, bg=self.background_image)
                elif screen.sidebar_status == "closed":
                    screen.open_sidebar(display=self.screen, xpos=self.camera_x, ypos=self.camera_y, bg=self.background_image)

            elif event.type == pygame.MOUSEBUTTONDOWN and screen.sidebar_rect.collidepoint(event.pos):
                print("sidebar click")
                    
            ##detect mouse click on screen
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print("screen click!")
                    
            ##initialse X button
            if event.type == pygame.QUIT:
                self.running = False

            ##detect key presses
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.moving_left = True
                elif event.key == pygame.K_RIGHT:
                    self.moving_right = True
                elif event.key == pygame.K_UP:
                    self.moving_up = True
                elif event.key == pygame.K_DOWN:
                    self.moving_down = True

            ##detect key releases
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.moving_left = False
                elif event.key == pygame.K_RIGHT:
                    self.moving_right = False
                elif event.key == pygame.K_UP:
                    self.moving_up = False
                elif event.key == pygame.K_DOWN:
                    self.moving_down = False

            ##detect mouse position
            elif event.type == pygame.MOUSEMOTION: # Get Mouse Hover position (0,0) is the top left
                self.mouse_x, self.mouse_y = event.pos

            ##detect mouse scroll
            elif event.type == pygame.MOUSEWHEEL: # Get Scroll Info
               self.scroll_direction = event.y
               self.scrolling = True
               self.last_scroll_time = pygame.time.get_ticks()
               
        # Check for stop-scrolling
        current_time = pygame.time.get_ticks()
        time_since_last_scroll = current_time - self.last_scroll_time

        if time_since_last_scroll > self.scroll_stop_threshold:
            self.scrolling = False

    def update(self):
        # Scale the image based on scroll wheel
        if self.scrolling:
            self.scroll_scale = self.scroll_scale + self.scroll_direction/100
        # Update camera position based on keyboard input
        if self.moving_left:
            self.camera_x -= self.camera_speed
            self.change_x -= self.camera_speed
        if self.moving_right:
            self.camera_x += self.camera_speed
            self.change_x += self.camera_speed
        if self.moving_up:
            self.camera_y -= self.camera_speed
        if self.moving_down:
            self.camera_y += self.camera_speed
        
        # Ensure the camera stays within the bounds of the image
        self.camera_x = max(0, min(self.camera_x, self.background_rect.width - self.WIDTH))
        self.camera_y = max(0, min(self.camera_y, self.background_rect.height - self.HEIGHT))
        
        # Calculate the new center of the screen considering the camera position
        #screen_center = (self.WIDTH // 2, self.HEIGHT // 2)
        #camera_center = (self.camera_x + self.WIDTH // 2, self.camera_y + self.HEIGHT // 2)

        # Calculate the difference between these two centers
        #difference = (camera_center[0] - screen_center[0], camera_center[1] - screen_center[1])

        # Update the camera position to adjust for the scaling around the center
        #self.camera_x -= difference[0] * (self.scroll_scale - 1)
        #self.camera_y -= difference[1] * (self.scroll_scale - 1)        
    def draw(self):

        ##draw these things only once at the start of the program (NEW)
        if system.start == 0:
            system.start = 1

         # Clear the screen
            self.screen.fill(self.WHITE)
        # Draw the background image at its position
            self.screen.blit(self.background_image, (-self.camera_x, -self.camera_y))
        ##create a button NEW
            w, h = pygame.display.get_surface().get_size()
            screen.button_rect = pygame.Rect(w-20,(h/2)-50,20,100)
            pygame.draw.rect(self.screen, colour.bg1, screen.button_rect)
            self.screen.blit(font.default.render('<', True, colour.white), (w-15, (h/2)-12))
        
    def main(self):
        # Initialize Pygame
        pygame.init()
        while self.running:
            self.draw()
            self.handle_events()
            self.update()
            # Update the display
            pygame.display.flip()

            # Cap the frame rate
            self.clock.tick(self.FPS)

        pygame.quit()
        quit()

if __name__ == "__main__":
    #print(random_monster())
    # Width, Height, Frame rate, Camera Speed
    game = DndMainGame(width, height-60, 60, 5) 
    game.main()
