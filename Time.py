import pygame
from gui.Colors import*
from gui.Window import Window



class Time:
    def __init__(self, time_scale=80, start_hour=7, start_minute=30):
        self.time_scale = time_scale
        self.simulation_time = (start_hour * 3600 + start_minute * 60)  # Start time in seconds
        self.real_time = 0  # in seconds
        self.shift_start = 7.5  # 7:30 AM
        self.shift_end = 24  # 3:30 PM
        self.paused = False
        self.breaks = {
            "Morning Break": {"start": "9:55", "end": "10:20"},
            "Lunch Break": {"start": "12:20", "end": "13:05"},
            "Afternoon Break": {"start": "15:20", "end": "15:40"}
        }
        self.last_update_time = pygame.time.get_ticks() / 1000.0
        self.start_time = self.simulation_time

    def run_time(self):
        total_seconds = int(self.simulation_time - self.start_time)
        days, remainder = divmod(total_seconds, 86400)  # 86400 seconds in a day
        hours, remainder = divmod(remainder, 3600)
        minutes, _ = divmod(remainder, 60)
        
        if days > 0:
            return f"{days}d {hours:02d}h {minutes:02d}m"
        else:
            return f"{hours:02d}h {minutes:02d}m"


    def update(self):
        if not self.paused:
            current_time = pygame.time.get_ticks() / 1000.0  # Convert to seconds
            delta_time = current_time - self.last_update_time
            self.real_time += delta_time
            self.simulation_time += delta_time * self.time_scale
            self.last_update_time = current_time

    def toggle_pause(self):
        self.paused = not self.paused
        if not self.paused:
            self.last_update_time = pygame.time.get_ticks() / 1000.0  # Reset last update time when unpausing

    def is_paused(self):
        return self.paused


    def get_simulation_time(self):
        return self.simulation_time

    def format_time(self):
        total_seconds = int(self.simulation_time)
        hours = (total_seconds // 3600) % 24
        minutes = (total_seconds % 3600) // 60
        return f"{hours:02d}:{minutes:02d}"

    def is_within_shift_time(self):
        hours = (self.simulation_time // 3600) % 24
        minutes = (self.simulation_time % 3600) // 60
        current_time = hours + minutes / 60
        return self.shift_start <= current_time < self.shift_end

    def is_break_time(self):
        current_time = self.format_time()
        for break_info in self.breaks.values():
            if break_info["start"] <= current_time < break_info["end"]:
                return True
        return False
    
    def draw_clock(self,window, x, y):
        font = pygame.font.Font(None, 36)
        time_str = self.format_time()
        text = font.render(time_str, True, BLACK)
        window.screen.blit(text, (x, y))

    def get_time_scale(self):
        return self.time_scale

    def set_time_scale(self, new_scale):
        self.time_scale = new_scale

    def get_runtime_string(self):
        run_time_text = self.run_time()
        return f"Run Time: {run_time_text}"
        