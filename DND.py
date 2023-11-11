import pygame
import sys

################################ NEW! #################################

import pandas as pd
import random

##monsters

##use pandas to read in the excel file and choose a random monster

pd.set_option('display.max_columns', None)
df = pd.read_excel('Monster Spreadsheet (D&D5e).xlsx')

def random_monster():
    selection = random.choice(df["Name"])
    return df.loc[df['Name'] == selection]
#print(random_monster())

########################################################################

class DndMainGame:
    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    
    background_image = pygame.image.load("map.jpg")
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
        
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("DND")
        
        self.camera_x = (self.background_rect.width - self.WIDTH) // 2
        self.camera_y = (self.background_rect.height - self.HEIGHT) // 2
        
        print(self.camera_x)
        print(self.camera_y)
        
        self.camera_speed = camera_speed
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.moving_left = True
                elif event.key == pygame.K_RIGHT:
                    self.moving_right = True
                elif event.key == pygame.K_UP:
                    self.moving_up = True
                elif event.key == pygame.K_DOWN:
                    self.moving_down = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.moving_left = False
                elif event.key == pygame.K_RIGHT:
                    self.moving_right = False
                elif event.key == pygame.K_UP:
                    self.moving_up = False
                elif event.key == pygame.K_DOWN:
                    self.moving_down = False
            elif event.type == pygame.MOUSEMOTION: # Get Mouse Hover position (0,0) is the top left
                self.mouse_x, self.mouse_y = event.pos
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
         # Clear the screen
        self.screen.fill(self.WHITE)
        
        # Draw the background image at its position
        self.screen.blit(self.background_image, (-self.camera_x, -self.camera_y))

        
        ##### FAILED CODE BELOW ###
        # Scale the image to the zoom/scroll level and mouse position
        #if self.scrolling:
            #scale_factor_x = abs(self.mouse_x-self.WIDTH/2)/self.WIDTH 
            #scale_factor_y = abs(self.mouse_y-self.HEIGHT/2)/self.HEIGHT
            
            #print(abs(self.mouse_x-self.WIDTH/2)/self.WIDTH )
        #else:
            #scale_factor_x = scale_factor_y = 1
        #scaled_image = pygame.transform.scale_by(self.background_image, (self.scroll_scale, 1))
        #self.background_rect = scaled_image.get_rect()
        #print(self.background_rect)
        # This gets new centre
        # Old centre - new centre = correct scalig
        # new centre
        #temp = ((self.background_rect.width - self.WIDTH) // 2) 
        #print(self.scroll_scale)
        
        # Draw the background image at its position
        # x and y where the top_left of the soruce will be placed
        # Current image placed -600 -325 out of camera
        #print(self.change_x)
        #self.screen.blit(scaled_image, (-self.camera_x*self.scroll_scale+(600-temp) , -self.camera_y))
        # Get the center of the window
        #window_center = self.screen.get_rect().center
        # Scale the image by the difference
        #scaled_image = pygame.transform.scale(self.background_image, (int(self.background_image.get_width() - difference[0]), int(self.background_image.get_height() - difference[1])))
        
         # Blit the scaled image to the screen
        #self.screen.blit(scaled_image, (0, 0))
        # Calculate the new center of the screen considering the camera position
        # Calculate the new center of the screen considering the camera position
        # Calculate the new center of the screen considering the camera position
        #screen_center = (self.WIDTH // 2, self.HEIGHT // 2)
        #camera_center = (self.camera_x + self.WIDTH // 2, self.camera_y + self.HEIGHT // 2)

        # Calculate the difference between these two centers
        #difference = (camera_center[0] - screen_center[0], camera_center[1] - screen_center[1])

        # Scale the image based on the zoom/scroll level
        #scaled_image = pygame.transform.scale(self.background_image, (int(self.background_rect.width * self.scroll_scale), int(self.background_rect.height * self.scroll_scale)))

        # Calculate the position to blit the scaled image, ensuring it is centered on the screen
        #blit_position = (screen_center[0] - scaled_image.get_width() // 2 + difference[0], screen_center[1] - scaled_image.get_height() // 2 + difference[1])

        # Adjust the blit position based on the camera position
        #blit_position = (blit_position[0] - self.camera_x, blit_position[1] - self.camera_y)

        # Blit the scaled image to the screen at the adjusted position
        #self.screen.blit(scaled_image, blit_position)
        
        #screen_center = (self.WIDTH // 2, self.HEIGHT // 2)

        # Calculate the scaled size of the background image.
        #scaled_width = int(self.scroll_scale * self.background_image.get_width())
        #scaled_height = int(self.scroll_scale * self.background_image.get_height())

        # Create a new surface for the scaled background image.
        #scaled_background_image = pygame.Surface((scaled_width, scaled_height))

        # Scale the background image onto the new surface.
        #pygame.transform.scale(self.background_image, scaled_background_image.get_size(), scaled_background_image)

        # Calculate the offset of the scaled background image from the center of the screen.
        #offset_x = (scaled_width - self.WIDTH) // 2 - self.camera_x
        #offset_y = (scaled_height - self.HEIGHT) // 2 - self.camera_y

        # Blit the scaled background image onto the screen, offset by the calculated amount.
        #screen.blit(scaled_background_image, (screen_center[0] - offset_x, screen_center[1] - offset_y))
        
    def main(self):
        # Initialize Pygame
        pygame.init()
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            # Update the display
            pygame.display.flip()

            # Cap the frame rate
            self.clock.tick(self.FPS)
        pygame.quit()
        sys.exit()
   
# Needs to be remade right now is bad   
class MenuBox():
    def __init__(self, x_cord, y_cord, height, width, font, screen):
        self.x = x_cord
        self.y = y_cord
        self.h = height
        self.w = width
        self.font = font
        self.screen = screen
        
    def show_menu(self, mouse_x, mouse_y, spawn_pos_x, spawn_pos_y):
        if (mouse_x >= self.x and mouse_x <= self.x + self.w) and (mouse_y >= self.y and mouse_y <= self.y + self.h):
            print(f"X Pos: {mouse_x}, Y: POS: {mouse_y}")
            pygame.draw.rect(self.screen, BLACK, (self.x-spawn_pos_x, self.y-spawn_pos_y, self.h, self.w))
            pygame.draw.rect(screen, WHITE, (self.x+5-spawn_pos_x, self.y+5-spawn_pos_y, self.h-10, self.w-10))
            item1_text = self.font.render("Menu Item 1", True, BLACK)
            item2_text = self.font.render("Menu Item 2", True, BLACK)
            self.screen.blit(item1_text, (self.x-spawn_pos_x + 10, self.y-spawn_pos_y + 10))
            self.screen.blit(item2_text, (self.x-spawn_pos_x + 10, self.y-spawn_pos_y + 60))

if __name__ == "__main__":
    print(random_monster())
    # Width, Height, Frame rate, Camera Speed
    game = DndMainGame(400, 400, 60, 5) 
    game.main()