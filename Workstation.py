import pygame
from gui.Colors import*

class Workstation:
    def __init__(self, name, position, window, time, capacity=1):
        self.name = name
        self.position = position
        self.capacity = capacity
        self.occupied = 0
        self.queue = []
        self.current_unit = None
        self.total_processing_time = 0
        self.units_processed = 0
        self.last_entry_time = {}
        self.cycle_times = {}
        self.time = time
        self.window = window

    def record_entry(self, station_name, current_time):
        if station_name in self.last_entry_time:
            cycle_time = current_time - self.last_entry_time[station_name]
            if station_name not in self.cycle_times:
                self.cycle_times[station_name] = []
            self.cycle_times[station_name].append(cycle_time)
        self.last_entry_time[station_name] = current_time

    def get_average_cycle_time(self, station_name):
        if station_name in self.cycle_times and self.cycle_times[station_name]:
            return sum(self.cycle_times[station_name]) / len(self.cycle_times[station_name])
        return 0

    #Compares the amount of units occupying the workstation to its stated capacity
    #If less than capacity, then capacity then return true
    def is_available(self):
        is_available = self.occupied < self.capacity 
        return is_available
    
    def add_to_queue(self, unit):
        self.queue.append(unit)

    def remove_from_queue(self):
        if self.queue:
            return self.queue.pop(0)
        return None
    
    #If the current workstation is not not available
    def start_processing(self, unit):
        self.occupied += 1
        self.current_unit = unit
        self.current_unit.processing_start_time = self.time.get_simulation_time()
        return True

    def finish_processing(self):
        if self.current_unit:
            if self.occupied > 0:
                processing_time = self.time.get_simulation_time() - self.current_unit.processing_start_time
                self.total_processing_time += processing_time
                self.units_processed += 1
                self.occupied -= 1
                finished_unit = self.current_unit
                self.current_unit = None
                return finished_unit
        return None

    def get_average_processing_time(self):
        if self.units_processed > 0:
            return self.total_processing_time / self.units_processed
        return 0

    def update(self):
        if not self.current_unit and self.queue:
            next_unit = self.remove_from_queue()
            if next_unit:
                self.start_processing(next_unit)


    def draw_info(self):
        font = pygame.font.Font(None, 24)
        
        # Draw workstation name
        name_text = font.render(self.name, True, BLACK)
        name_rect = name_text.get_rect(center=(self.position[0] + 5, self.position[1] - 40))
        self.window.screen.blit(name_text, name_rect)
        
        # Draw average processing time
        avg_time = self.get_average_processing_time()
        time_text = font.render(f"Avg: {self.format_time_ms(avg_time)}", True, BLACK)
        time_rect = time_text.get_rect(center=(self.position[0] - 10, self.position[1] + 90))
        self.window.screen.blit(time_text, time_rect)

        # Draw average cycle time
        avg_cycle_time = self.get_average_cycle_time(self.name)
        cycle_text = font.render(f"Cycle: {self.format_time_ms(avg_cycle_time)}", True, BLACK)
        cycle_rect = cycle_text.get_rect(center=(self.position[0] - 10, self.position[1] + 110))
        self.window.screen.blit(cycle_text, cycle_rect)
        
        # Draw queue length
        queue_text = font.render(f"Queue: {len(self.queue)}", True, BLACK)
        queue_rect = queue_text.get_rect(center=(self.position[0] - 10, self.position[1] + 130))
        self.window.screen.blit(queue_text, queue_rect)
   
    @staticmethod
    def format_time_ms(seconds):
        minutes, seconds = divmod(int(seconds), 60)
        return f"{minutes:02d}:{seconds:02d}"