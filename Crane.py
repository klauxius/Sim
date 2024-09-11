import pygame
from gui.Colors import*
import sys

class Crane:
    def __init__(self, name, initial_position, window, time):
        self.name = name
        self.position = initial_position
        self.target_position = initial_position
        self.in_use = False
        self.current_user = None
        self.time = time
        self.speed = 200  # pixels per second
        self.window = window
        self.operation_timer = 0
        self.operation_duration = 0

    def move_to(self, target_position):
        self.target_position = target_position
        print(f"Time: {self.time.format_time()} - Crane {self.name} moved to {target_position}")

    def use(self, unit, operation_time):
        if not self.in_use:
            self.in_use = True
            self.current_user = unit
            self.operation_timer = 0
            self.operation_duration = operation_time
            self.move_to(unit.pos)
            print(f"Time: {self.time.format_time()} - Crane {self.name} is now being used by {unit} for {operation_time} seconds")
            return True
        return False
    
    def update(self, delta_time):
        if self.position != self.target_position:
            dx = self.target_position[0] - self.position[0]
            dy = self.target_position[1] - self.position[1]
            distance = (dx**2 + dy**2)**0.5
            
            move_distance = self.speed * delta_time
            if move_distance >= distance:
                self.position = self.target_position
            else:
                move_x = (dx / distance) * move_distance
                move_y = (dy / distance) * move_distance
                self.position = (self.position[0] + move_x, self.position[1] + move_y)
        
        if self.in_use:
            self.operation_timer += delta_time
            if self.operation_timer >= self.operation_duration:
                self.release()

    def release(self):
        if self.in_use:
            self.in_use = False
            print(f"Time: {self.time.format_time()} - Crane {self.name} has been released by {self.current_user}")
            self.current_user = None
            self.operation_timer = 0
            self.operation_duration = 0
            return True
        return False
    
    def draw(self):
        scaled_pos = self.window.scale_pos(self.position)
        pygame.draw.circle(self.window.screen, BLUE, scaled_pos, 10)
        pygame.draw.line(self.window.screen, BLACK, (scaled_pos[0], 100), scaled_pos, 2)
