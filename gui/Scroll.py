import pygame


class Scroll:
    def __init__(self, window, content_size):
        self.window = window
        self.content_size = content_size
        self.view_rect = pygame.Rect(0, 0, window.width, window.height)
        self.scroll_speed = 5

    def update(self, keys):
        # Handle keyboard input for scrolling
        if keys[pygame.K_LEFT]:
            self.scroll_horizontal(-self.scroll_speed)
        if keys[pygame.K_RIGHT]:
            self.scroll_horizontal(self.scroll_speed)
        if keys[pygame.K_UP]:
            self.scroll_vertical(-self.scroll_speed)
        if keys[pygame.K_DOWN]:
            self.scroll_vertical(self.scroll_speed)

    def scroll_horizontal(self, dx):
        self.view_rect.x += dx
        self.view_rect.x = max(0, min(self.view_rect.x, self.content_size[0] - self.window.width))

    def scroll_vertical(self, dy):
        self.view_rect.y += dy
        self.view_rect.y = max(0, min(self.view_rect.y, self.content_size[1] - self.window.height))

    def get_visible_rect(self):
        return self.view_rect

    def adjust_position(self, pos):
        # Adjust a global position to the current view
        return (pos[0] - self.view_rect.x, pos[1] - self.view_rect.y)

    def global_to_local(self, pos):
        # Convert a global position to local (screen) coordinates
        return (pos[0] - self.view_rect.x, pos[1] - self.view_rect.y)

    def local_to_global(self, pos):
        # Convert local (screen) coordinates to global position
        return (pos[0] + self.view_rect.x, pos[1] + self.view_rect.y)

    def is_visible(self, rect):
        # Check if a given rect is visible in the current view
        return self.view_rect.colliderect(rect)

    def handle_window_resize(self, new_size):
        # Adjust view_rect when window is resized
        self.view_rect.width, self.view_rect.height = new_size
        self.scroll_horizontal(0)  # Ensure we're still within bounds
        self.scroll_vertical(0)

    def zoom(self, factor, center):
        # Implement zooming functionality
        old_size = self.view_rect.size
        new_width = int(self.view_rect.width / factor)
        new_height = int(self.view_rect.height / factor)
        
        # Ensure we don't zoom out beyond the content size
        new_width = min(new_width, self.content_size[0])
        new_height = min(new_height, self.content_size[1])
        
        # Calculate new position to keep the center point stable
        dx = (new_width - old_size[0]) * ((center[0] - self.view_rect.x) / old_size[0])
        dy = (new_height - old_size[1]) * ((center[1] - self.view_rect.y) / old_size[1])
        
        self.view_rect.width = new_width
        self.view_rect.height = new_height
        self.scroll_horizontal(-dx)
        self.scroll_vertical(-dy)
        
        