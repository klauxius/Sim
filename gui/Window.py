import pygame

class Window:
    def __init__(self, width = 1080, height=720, title="Network Transformer Simulation"):
        self.width = width
        self.height = height
        self.title = title
        self.original_size = (1920, 1080)  # Original design size
        self.scale = 1
        self.offset = (0, 0)
        self.is_fullscreen = False
    
    def init_display(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)

    def resize(self, new_width, new_height):
        self.width = new_width
        self.height = new_height
        if self.is_fullscreen:
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((self.width, self.height))
    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((self.width, self.height))
        self.on_resize()

    def set_background_color(self, color):
        self.background_color = color

    def clear(self):
        self.screen.fill(self.background_color)

    def update(self):
        pygame.display.flip()

    def get_size(self):
        return self.width, self.height

    def set_title(self, new_title):
        self.title = new_title
        pygame.display.set_caption(self.title)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.VIDEORESIZE:
                self.resize(event.w, event.h)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:  # Press 'f' to toggle fullscreen
                    self.toggle_fullscreen()
                
        return True
    
    # Add a new method to adjust mouse positions
    def adjust_mouse_pos(self, pos):
        return self.unscale_pos(pos)

    def scale_pos(self, pos):
        if pos is None:
            return (0, 0)  # Return a default position if None is passed
        return (int(pos[0] * self.scale + self.offset[0]), 
                int(pos[1] * self.scale + self.offset[1]))

    def unscale_pos(self, pos):
        return (int((pos[0] - self.offset[0]) / self.scale),
                int((pos[1] - self.offset[1]) / self.scale))
    
    def quit(self):
        pygame.quit()

    # Call this method when the window is resized
    def on_resize(self):
        self.scale_screen()
    
    def draw_text(self, text, position, font_size=36, color=(0, 0, 0)):
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, position)

    def get_surface(self):
        return self.screen


    def scale_screen(self):
        current_window_size = self.get_size()

        # Calculate scaling factors
        scale_x = current_window_size[0] / self.original_size[0]
        scale_y = current_window_size[1] / self.original_size[1]
        
        # Choose the smaller scaling factor to maintain aspect ratio
        self.scale = min(scale_x, scale_y)
        
        # Calculate new size while maintaining aspect ratio
        new_width = int(self.original_size[0] * self.scale)
        new_height = int(self.original_size[1] * self.scale)
        
        # Center the scaled content
        self.offset = (
            (current_window_size[0] - new_width) // 2,
            (current_window_size[1] - new_height) // 2
        )
        
        # Create a scaling matrix
        scaling_matrix = pygame.transform.scale(self.screen, (new_width, new_height))
        
        # Clear the screen
        self.screen.fill((0, 0, 0))  # Fill with black color
        
        # Draw the scaled content
        self.screen.blit(scaling_matrix, self.offset)
        
        # Update the display
        pygame.display.flip()
