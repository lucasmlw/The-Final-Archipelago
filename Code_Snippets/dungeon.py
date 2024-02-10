import pygame
import sys
import time

class fonts():
    pygame.font.init()
    default = pygame.font.SysFont(None, 30)
    Arial_20 = pygame.font.SysFont('Arial', 20)
    
    
class h_nav_bar:
    def __init__(self, screen, dark_blue_1, dark_blue_2, white):
        self.display = screen
        self. sidebar_status = "closed"
        self.button_rect = pygame.Rect(0,0,0,0)
        self.sidebar_rect = pygame.Rect(0,0,0,0)
        
        self.db1 = dark_blue_1
        self.db2 = dark_blue_2
        self.w = white
        
    def open_sidebar(self):
        #display.blit(bg, (-xpos, -ypos))
        w, h = pygame.display.get_surface().get_size()
        
        # x pos, y pos, size x, size y
        self.button_rect = pygame.Rect((w/2)-50,h-200,100,20)
        self.sidebar_rect = pygame.Rect(0,h-200,w,200)
        
        pygame.draw.rect(self.display, self.db1, self.sidebar_rect)
        pygame.draw.rect(self.display, self.db2, self.button_rect)
        
        self.display.blit(fonts.default.render('<', True, self.w), (w/2-10, h-200))

    def close_sidebar(self):
        #display.blit(bg, (-xpos, -ypos))
        self.sidebar_rect = pygame.Rect(0,0,0,0)
        w, h = pygame.display.get_surface().get_size()
        
        self.button_rect = pygame.Rect((w/2)-50,h-20,100,20)
        
        pygame.draw.rect(self.display, self.db1, self.button_rect)
        
        self.display.blit(fonts.default.render('^', True, self.w), (w/2-10, h-15))
        
    def detect_collision(self, click_position):
        if (self.button_rect.collidepoint(click_position)):
            if self.sidebar_status == "open":
                self.sidebar_status = "closed"
            elif self.sidebar_status == "closed":
                self.sidebar_status = "open"
        elif (self.sidebar_rect.collidepoint(click_position)):
            print("sidebar click")
            
    def draw(self):
        if self.sidebar_status == "open":
            self.open_sidebar()
        elif self.sidebar_status == "closed":
            self.close_sidebar()


class DungeonView:    
    # The background Image
    background_image = pygame.image.load("coppermine.png")
    background_rect = background_image.get_rect()
    
     # Initialize clock for controlling the frame rate
    clock = pygame.time.Clock()
    
    # Flags to track mouse clicks
    right_mouse_button_pressed = False
    left_mouse_button_pressed = False
    
    #font = pygame.font.Font(None, 36)
    
    running = True
    mouse_x = mouse_y = 0
    
    # Scroll logic, handles how big the erasing zone is
    scroll_direction = 0
    scroll_scale = 1
    scrolling = False
    last_scroll_time = pygame.time.get_ticks()
    scroll_stop_threshold = 50

    fullscreen = True
    
    # This determines if you can erase the black to show the map
    drawing_mode = False
    
    # This determines if the trail when erasing should fill back in
    animation_toggle = False
    pos_buffer = []
    time_buffer = []
    timer = 0.0
    # centre
    centre = 0
    
    pygame.font.init()
    font = pygame.font.Font(None, 36)
    
   # pygame.font.init()
   # font = pygame.font.Font(None, 36)
    
    def __init__(self, w, h, f):  
        self.WIDTH = w
        self.HEIGHT = h
        self.FPS = f
        
        self.init_colours()
        
        pygame.display.set_caption("DND")
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.RESIZABLE)
        
        # Create a black screen the same size as the image to cover the background image
        self.black_screen = pygame.Surface((self.background_rect[2], self.background_rect[3]), pygame.SRCALPHA)
        # 
        self.black_screen.fill(self.BLACK)
        
        # Get the position and dimensions of the window
        self.window_rect = self.screen.get_rect() 
        
        # Quit button
        self.quit_text = self.font.render("Quit", True, (255, 255, 255))
        self.quit_rect = self.quit_text.get_rect(topright=(self.window_rect.right - 10, self.window_rect.top + 10))
        
        # Header menu
        self.header = h_nav_bar(self.screen, self.DARK_BLUE_1, self.DARK_BLUE_2, self.WHITE)
        
        
    def init_colours(self):
        # Colors with alphas
        self.BLACK = (0, 0, 0, 255)
        self.WHITE = (255, 255, 255)
        self.TRANSPARENT = (0, 0, 0, 0)
        
        # Normal Colours
        self.RED = (200,50,50)
        self.GREEN = (50,200,50)
        self.BLUE = (50,50,200)

        self.DARK_BLUE_1 = (50,85,150)
        self.DARK_BLUE_2 = (0,30,100)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: # Check if escape key is pressed
                    self.running = False
                if event.key == pygame.K_RETURN:
                    if self.screen.get_flags() & pygame.FULLSCREEN:
                        self.screen = pygame.display.set_mode((1200, 1000))
                    else:
                        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                if event.key == pygame.K_d:
                    self.drawing_mode = not self.drawing_mode
                if event.key == pygame.K_t:
                    self.animation_toggle = not self.animation_toggle
                        
            elif event.type == pygame.KEYUP:
                pass
            elif event.type == pygame.MOUSEMOTION: # Get Mouse Hover position (0,0) is the top left
                self.mouse_x, self.mouse_y = event.pos
            elif event.type == pygame.MOUSEWHEEL: # Get Scroll Info
                self.scroll_direction = event.y
                self.scrolling = True
                self.last_scroll_time = pygame.time.get_ticks()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    self.right_mouse_button_pressed = True
                if event.button == 1:
                    self.left_mouse_button_pressed = True
                    self.header.detect_collision(event.pos) # Nav Bar collision
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    self.right_mouse_button_pressed = False
                if event.button == 1:
                    self.left_mouse_button_pressed = False
               
        # Check for stop-scrolling
        current_time = pygame.time.get_ticks()
        time_since_last_scroll = current_time - self.last_scroll_time

        if time_since_last_scroll > self.scroll_stop_threshold:
            self.scrolling = False
                
    def update(self):
        # Scale the image based on scroll wheel
        if self.scrolling:
            self.scroll_scale = self.scroll_scale + self.scroll_direction/25
        # Check if the quit button is clicked
        if self.left_mouse_button_pressed and self.quit_rect.collidepoint(pygame.mouse.get_pos()):
            self.running = False
       
    def draw(self):
    
        # Check if the buffer is full
        if len(self.pos_buffer) >= 100:
            self.pos_buffer.pop(0)
            self.time_buffer.pop(0)
            
        if self.drawing_mode:
            # Erase part of the black screen if the right mouse button is pressed
            if self.right_mouse_button_pressed:
                mouse_pos = pygame.mouse.get_pos()
                pygame.draw.circle(self.black_screen, self.TRANSPARENT, (self.mouse_x, self.mouse_y), 25*self.scroll_scale)
            # Fill in part of the screen if the left mouse buttin is clocked 
            if self.left_mouse_button_pressed:
                mouse_pos = pygame.mouse.get_pos()
                pygame.draw.circle(self.black_screen, self.BLACK, (self.mouse_x, self.mouse_y), 25*self.scroll_scale)
                
        elif self.animation_toggle:
            # We want to erase the end of the drawn line
            if self.right_mouse_button_pressed:
                temp = pygame.mouse.get_pos()
                self.pos_buffer.append(temp)
                self.time_buffer.append(round(time.time(), 1))
                pygame.draw.circle(self.black_screen, (0, 0, 0, 0), (self.mouse_x, self.mouse_y), 25*self.scroll_scale)
                

        # Draw the background image and the black screen
        self.screen.blit(self.background_image, (0, 0))
        self.screen.blit(self.black_screen, (0, 0))
        
        # Draw the quit button
        pygame.draw.rect(self.screen, (255, 0, 0), self.quit_rect)  # Red background
        self.screen.blit(self.quit_text, self.quit_rect.topleft)
        
        self.header.draw()
        
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
   


if __name__ == "__main__":
    # Width, Height, Frame rate
    game = DungeonView(1600, 1000, 60) 
    game.main()
