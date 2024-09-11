import pygame

# Update the Resource class to handle capacity
class Resource:
    def __init__(self, name, capacity=1, cooldown_time=0, position=(0, 0)):
        self.name = name
        self.capacity = capacity
        self.in_use = 0
        self.cooldown_time = cooldown_time
        self.last_used_time = 0
        self.position = position

    def is_available(self, current_time):
        if self.in_use >= self.capacity:
            print(f"Debug: Resource {self.name} is at full capacity ({self.in_use}/{self.capacity})")
            return False
        if current_time - self.last_used_time < self.cooldown_time:
            print(f"Debug: Resource {self.name} is in cooldown (last used: {self.last_used_time}, current time: {current_time})")
            return False
        return True

    def use(self, current_time):
        if self.in_use < self.capacity:
            self.in_use += 1
            self.last_used_time = current_time
            print(f"Debug: Resource {self.name} used (now in use: {self.in_use}/{self.capacity})")
            return True
        print(f"Debug: Failed to use resource {self.name} (in use: {self.in_use}/{self.capacity})")
        return False

    def release(self, current_time):
        if self.in_use > 0:
            self.in_use -= 1
            self.last_used_time = current_time
            print(f"Debug: Resource {self.name} released (now in use: {self.in_use}/{self.capacity})")
            return True
        print(f"Debug: Failed to release resource {self.name} (already at 0 use)")
        return False