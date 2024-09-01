import pygame

class Slider:
    def __init__(self, min_value, max_value, initial_value, width, x, y):
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value
        self.width = width
        self.x = x
        self.y = y
        self.dragging = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_over(event.pos):
                self.dragging = True
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

    def get_value(self):
        return self.value

    def draw(self, surface):
        pygame.draw.line(surface, (200, 200, 200), (self.x, self.y), (self.x + self.width, self.y), 2)
        button_x = self.x + (self.value - self.min_value) / (self.max_value - self.min_value) * self.width
        pygame.draw.circle(surface, (100, 100, 100), (int(button_x), self.y), 10)
        font = pygame.font.Font(None, 24)
        text = font.render(f"Time Scale: {self.value:.1f}", True, (0, 0, 0))
        surface.blit(text, (self.x, self.y - 30))