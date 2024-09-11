import random
import pygame
import sys

class Spawn:
    def __init__(self, x, y, station,station_path, workstation=None, time = None, periodic=True, spawn_interval=180, random_kva=False, kva_list=None, window=None):
        self.x = x
        self.y = y
        self.time = time
        self.station = station
        self.station_position = station.position if station else (x, y)
        self.workstation = workstation
        self.spawn_timer = 0
        self.spawn_interval = spawn_interval 
        self.last_spawn_time = 0
        self.units_spawned = 0
        self.random_kva = random_kva
        self.periodic = periodic
        self.kva_list = kva_list if kva_list is not None else [300, 500, 750, 1000, 1500, 2000, 2500]
        self.kva_index = 0
        self.window = window
        self.Unit = None  # Add this line
        self.stations = None  
        self.station_path = station_path


    def update(self, time, delta_time, window):
        self.time = time # Update the time reference
        if not self.time.is_within_shift_time() or self.time.is_break_time():
            return None
        if self.periodic:
            self.spawn_timer += delta_time * self.time.time_scale
            #Spawn unit only if station has capacity
            if (self.spawn_timer >= self.spawn_interval and self.station):
                available_workstation = self.station.get_available_workstation()
                if available_workstation and self.station.has_capacity():
                    new_unit = self.spawn_unit(window)
                    self.spawn_timer = 0
                    self.units_spawned += 1
                    return new_unit
        return None
    
    def set_unit_class_and_stations(self, Unit, stations):
        self.Unit = Unit
        self.stations = stations
        # Optionally, you can double-check here that self.station is in stations
        if self.station.name not in stations:
            raise ValueError(f"Spawn station {self.station.name} not found in provided stations")

    def spawn_unit(self, window):

        if self.Unit is None or self.stations is None:
            raise ValueError("Unit class and stations dictionary must be set before spawning units")
        
        kva = self.get_kva()
        #spawn unit at spawn point
        new_unit = self.Unit(self.station,self.station_path, kva=kva, time=self.time, pos=(self.x, self.y))
        #Use the station dictionary
        new_unit.stations_dict = self.stations
        
        if self.station:
            available_workstation = self.station.get_available_workstation()
            if available_workstation:
                new_unit.target_pos = available_workstation.position
                new_unit.current_workstation = available_workstation
                available_workstation.start_processing(new_unit)  # Inform the workstation it's now occupied
                new_unit.has_workstation = True
                # Start the first operation
                new_unit.processing = True
            else:
                new_unit.target_pos = self.station.position
        else:
            new_unit.target_pos = (self.x, self.y)
            new_unit.pos = (self.x, self.y)  # Ensure the unit spawns at the spawn position

        new_unit.spawn_time = self.time.format_time()
        new_unit.id = f"{new_unit.kva}kVA-{new_unit.spawn_time}-{self.units_spawned:04d}"
        print(f"Time: {self.time.format_time()} - New unit spawned: {new_unit}")
        #new_unit.update(0)
            
        return new_unit
    
    def get_kva(self):
        if self.random_kva:
            return random.choice(self.kva_list)
        else:
            kva = self.kva_list[self.kva_index]
            self.kva_index = (self.kva_index + 1) % len(self.kva_list)
            return kva

    def set_spawn_interval(self, interval):
        self.spawn_interval = interval

    def set_spawn_position(self, x, y):
        self.x = x
        self.y = y
        self.station = None
        self.workstation = None

    def set_spawn_station(self, station, workstation=None):
        self.station = station
        self.workstation = workstation
        self.x, self.y = station.position

    #Draw circle around spawn point
    def draw(self, window):
        pos = window.scale_pos((self.x, self.y))
        radius = int(5 * window.scale)  # Scale the radius of the circle
        pygame.draw.circle(window.get_surface(), (0, 255, 0), pos, radius)



