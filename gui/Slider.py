import pygame
import sys

class Slider:
    def __init__(self, min_value, max_value, initial_value, width, x, y):
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value
        self.previous_value = initial_value
        self.width = width
        self.x = x
        self.y = y
        self.dragging = False
        self.value_changed = False
        self.height = 10  # Adjust this value as needed
        self.rect = pygame.Rect(self.x, self.y - self.height // 2, self.width, self.height)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
            #if self.is_over(event.pos):
                self.dragging = True
                self.update_value(event.pos[0])
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.update_value(event.pos[0])

    def is_over(self, pos):
        return self.x <= pos[0] <= self.x + self.width and self.y - 5 <= pos[1] <= self.y + 5

    def update_value(self, x):
        self.value = ((x - self.x) / self.width) * (self.max_value - self.min_value) + self.min_value
        self.value = max(self.min_value, min(self.max_value, self.value))
        new_value = ((x - self.x) / self.width) * (self.max_value - self.min_value) + self.min_value
        new_value = max(self.min_value, min(self.max_value, new_value))
        if new_value != self.value:
            self.previous_value = self.value
            self.value = new_value
            self.value_changed = True

    def get_value(self):
        print(f"Slider value: {self.value}")
        return self.value
    
    def check_value_changed(self):
        if self.value_changed:
            self.value_changed = False
            return True
        return False

    def draw(self, surface):
        pygame.draw.line(surface, (200, 200, 200), (self.x, self.y), (self.x + self.width, self.y), 2)
        button_x = self.x + (self.value - self.min_value) / (self.max_value - self.min_value) * self.width
        pygame.draw.circle(surface, (100, 100, 100), (int(button_x), self.y), 10)
        font = pygame.font.Font(None, 24)
        text = font.render(f"Time Scale: {self.value:.1f}", True, (0, 0, 0))
        surface.blit(text, (self.x, self.y - 30))