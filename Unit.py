import pygame
import random
from gui.Colors import*
import sys


class Unit:
    def __init__(self,station,station_path, pos=None, kva=None, time=None):
        self.station = station
        self.time = time
        self.pos = pos if pos is not None else (0, 0)  # Default to (0, 0) if no position is provided
        self.current_station = station.name if station else None
        self.has_workstation = None
        self.target_station = station.name
        self.station_operations = station.operations.copy()
        self.speed = 50
        self.timer = 0
        self.processing = False
        self.kva = kva
        self.spawn_time = self.time.format_time()
        self.id = f"{self.kva}kVA-{self.spawn_time}"
        self.size = self.calculate_size()
        self.completed = False
        self.in_wip = False
        self.wip_location = None
        self.completed_operations = 0
        self.total_operations = len(self.station_operations)
        self.moving_to_wip = False
        self.moving_from_wip = False
        self.has_an_operation = None
        self.operation_timer = 0
        self.current_resource = None
        self.flipped = False
        self.current_resources = []
        self.station_resources = []
        self.resource_wait_timers = {}  # New attribute to track wait times for resources
        self.resource_wait_time = 240  # 30 seconds wait time
        self.base_speed = 50
        self.current_resource_position = None
        self.target_pos = None
        self.current_workstation = None
        self.current_resources = []
        self.current_operation = None
        self.station_path = station_path
        self.stations_dict = None
        #target_pos = available_workstation.position
        #self.operation_progress = 0  # Add this line
    
    def process(self, time_increment):
        current_time = self.time.get_simulation_time()
        #print(f"Time: {self.time.format_time()} - Processing {self} at {self.current_station}")
    
        if not self.time.is_within_shift_time() or self.time.is_break_time():
            print(f"Time: {self.time.format_time()} - Not processing {self} due to shift time or break")
            return
        #print(f"Debug: process called for {self} at {self.time.format_time()}")
        if self.target_pos:
            self.move_to_target(time_increment)
        # First, check if we have a workstation
        elif not self.has_workstation:
            available_workstation = self.station.get_available_workstation()
            # if workstation has value,(not empty or none)
            if available_workstation:
                if available_workstation.start_processing(self):
                    self.has_workstation = True
                    self.current_workstation = available_workstation
                    self.target_pos = available_workstation.position
                    print(f"Time: {self.time.format_time()} - {self} assigned to workstation {available_workstation.name}")
                    print(f"Time: {self.time.format_time()} - {self} started processing at {self.current_station}")
            else:
                print(f"Debug: {self} couldn't acquire any workstation")
                return
            
        #if self.target_pos: #if target position has a value, then move to that place
         #   self.move_to_target()

         #If Unit is not processing   
        elif self.processing:
            if not self.time.is_within_shift_time() or self.time.is_break_time():
                self.processing = False
                return  # Pause processing outside shift hours or during break
            
            #If the unit has no current operation
            if not self.current_operation:
                #And the current station has has an operations list 
                if self.station_operations:
                    #Get the next operation in the list
                    next_operation = self.station_operations[0]
                    
                    #Set the current operation to the next operation
                    self.current_operation = next_operation
                    #Get the required resources for the operation
                    required_resources = next_operation.get('required_resource', [])
                    #required_resources = [r for r in required_resources if not r.startswith("workstation")]
                    print(f"Debug: Required resources: {required_resources}")
                    if not self.current_resources:  # Only attempt to acquire resources if we don't have any
                        print(f"Debug: {self} attempting to acquire resources for operation: {next_operation['name']}")
                        if self.acquire_resources(required_resources, current_time):
                            #Remove the operation from the list
                            self.current_operation = self.station_operations.pop(0)
                            print(f"Time: {self.time.format_time()} - {self} started operation: {self.current_operation['name']} at {self.current_station}")
                            self.operation_timer = 0
                        else:
                            #print(f"Time: {self.time.format_time()} - {self} at {self.station.name} starting: {self.has_an_operation['name']} using {', '.join(self.current_resources)}")
                            print(f"Time: {self.time.format_time()} - {self} waiting for resource {self.current_resources} at {self.current_station}")

            #If the unit has an operation   
            if self.current_operation:
                #Calculate the operation time
                operation_time = self.calculate_operation_time(self.current_operation)
                #Increment the operation timer
                self.operation_timer += time_increment
                self.operation_progress = min(self.operation_timer / operation_time, 1)

                if self.operation_timer >= operation_time:
                    print(f"Time: {self.time.format_time()} - {self} at {self.station.name} completed: {self.current_operation['name']}")
                    self.release_resources(current_time)
                    self.has_an_operation = None
                    self.completed_operations += 1
                    self.operation_timer = 0
                
                #If the unit has no operations 
            
            elif self.completed_operations >= self.total_operations:
                self.finish_processing()
                    # No more operations at the current station
                print(f"Time: {self.time.format_time()} - {self} completed all operations at {self.station.name}")
            else:
                print(f"Debug: {self} has no more operations at {self.current_station}, but hasn't completed all operations")

    def update(self, delta_time):
        if not self.time.is_paused():
        # Use delta_time for time-based calculations
            if self.processing:
                self.process(delta_time)
            elif self.target_station and self.target_pos:
                self.move_to_target(delta_time)
            else:
                next_station = self.get_next_station(self.current_station, self.station_path)
                if next_station and self.check_station_capacity(next_station, self.stations_dict):
                    self.set_next_target(next_station, self.stations_dict)

    def acquire_resources(self, required_resources, current_time):
        acquired_resources = []
        for resource_name in required_resources:
            if resource_name.startswith("crane"):
                crane = self.station.get_crane(resource_name)
                operation_time = self.calculate_operation_time(self.current_operation)
                if crane and crane.use(self, operation_time):
                    acquired_resources.append(resource_name)
            elif resource_name in self.station.resources:
                resource = self.station.resources[resource_name]
                if resource.acquire(current_time):
                    acquired_resources.append(resource_name)
        
        if len(acquired_resources) == len(required_resources):
            self.current_resources = acquired_resources
            return True
        else:
            for resource_name in acquired_resources:
                if resource_name.startswith("crane"):
                    crane = self.station.get_crane(resource_name)
                    crane.release()
                else:
                    self.station.resources[resource_name].release(current_time)
            return False

    def are_resources_available(self, resource_names, current_time):
        for resource_name in resource_names:
            if not self.can_attempt_resource_acquisition(resource_name, current_time):
                return False
            if not self.station.resources[resource_name].is_available(current_time):
                self.set_resource_wait_timer(resource_name, current_time)
                return False
        return True #Will return true for all cases outside of the above, resource in timer and can't attmept

    def finish_processing(self):
        if self.has_workstation:
            self.current_workstation.finish_processing()
            self.has_workstation = False
        self.processing = False
        next_station = self.get_next_station(self.current_station, self.station_path)
        #If next station exists and it has available capacity
        if next_station and self.check_station_capacity(next_station):
            self.set_next_target(next_station, self.stations_dict)
        else:
            print(f"Time: {self.time.format_time()} - {self} waiting for capacity at {next_station}")
    
    def release_resources(self, current_time):
        for resource_name in self.current_resources:
            if resource_name.startswith("crane"):
                crane = self.station.get_crane(resource_name)
                if crane:
                    crane.release()
            elif resource_name in self.station.resources:
                self.station.resources[resource_name].release(current_time)
                print(f"Debug: Released resource {resource_name} at {self.station.name}")
        self.current_resources = []

    def can_attempt_resource_acquisition(self, resource_name, current_time):
        if resource_name in self.resource_wait_timers:
            if current_time - self.resource_wait_timers[resource_name] >= self.resource_wait_time:
                del self.resource_wait_timers[resource_name]
                return True
            return False
        return True

    def set_resource_wait_timer(self, resource_name, current_time):
        self.resource_wait_timers[resource_name] = current_time
        print(f"Debug: {self} set wait timer for resource {resource_name}")

    def set_next_target(self, next_station, stations_dict):

        self.current_station = next_station
        self.station = stations_dict[next_station]
        self.station_operations = self.station.operations.copy()
        self.total_operations = len(self.station_operations)
        self.completed_operations = 0
        self.pos = self.station.position
        self.target_pos = None
        self.has_workstation = None

    def __str__(self):
        return f"Unit {self.id}"
    
    def generate_id(self):
        # Generate a unique ID based on KVA, spawn time, and a random number
        random_suffix = ''.join(random.choices('0123456789ABCDEF', k=4))
        return f"{self.kva}kVA-{self.spawn_time}-{random_suffix}"


    def calculate_size(self):
        min_kva, max_kva = 300, 2500
        min_size, max_size = 10, 30
        size = (self.kva - min_kva) / (max_kva - min_kva) * (max_size - min_size) + min_size
        return int(size)
    #Time: 10:37 - Unit 2000kVA-10:32 at Lace and Clamp completed: First coil moved to saddle
    def calculate_operation_time(self, operation):
        if operation is None:
            return 0  # Return 0 if no operation is provided
        base_time = operation.get("base_time", 0)  # Use get() with a default value
        kva_factor = self.kva / 1000  # Normalize KVA to affect time

        #removed kva factor to debug operation time
        real_time = base_time #* (1 + kva_factor * 0.5)  # Adjust factor as needed
        return real_time

    def move(self):
        if self.time.is_break_time():
            return  # Do nothing during break times
        
        # Calculate the time increment based on the time scale
        time_increment = self.time.time_scale / 60  # Assuming 60 FPS
        if self.processing:
            self.process(time_increment)
        elif self.target_station and self.target_pos:  # Check if target_pos is not None
            self.move_to_target(time_increment)
        else:
            # If the unit has completed processing at the current station, move to the next one
            next_station = self.get_next_station(self.current_station, self.station_path)
            if next_station and self.check_station_capacity(next_station, self.station_path):
                self.set_next_target(next_station, self.stations_dict)
            else:
                # If there's no next station or it's at capacity, do nothing
                pass
    
    def move_to_target(self, delta_time):
        #Handle case where there is no target position when move_to_target is called
        if self.target_pos is None:
            print(f"Time: {self.time.format_time()} - Error: {self} has no target position")
            return

        dx = self.target_pos[0] - self.pos[0]
        dy = self.target_pos[1] - self.pos[1]
        distance = (dx**2 + dy**2)**0.5
        
        current_speed = self.base_speed *delta_time  # Assuming 60 FPS

        if distance < current_speed:
            self.pos = self.target_pos
            self.target_pos = None
            self.processing = True
            self.current_station = self.target_station
            #self.target_station = self.get_next_station(self.current_station)
            #self.processing = True
            #self.station = target_station
            
            self.current_resource_position = None  # Reset this when arriving at a new station
            print(f"Time: {self.time.format_time()} - {self} arrived at {self.current_station} at position {self.pos}")
        else:
            move_x = (dx / distance) * current_speed
            move_y = (dy / distance) * current_speed
            self.pos = (self.pos[0] + move_x, self.pos[1] + move_y)
            #print(f"Debug: {self} moving to {self.target_station}. Current position: {self.pos}")
    
    def draw(self,surface, window):
        if not self.in_wip:
            if self.current_resource_position:
                pos = window.scale_pos(self.current_resource_position)
            elif self.pos:
                pos = window.scale_pos(self.pos)
            else:
                pos = window.scale_pos((0, 0))
            pos = window.scale_pos(self.current_resource_position if self.current_resource_position else self.pos)
            rect = pygame.Rect(int(pos[0] - self.size/2), int(pos[1] - self.size/2), self.size, self.size)
            pygame.draw.rect(surface, RED, rect)
            
            if self.processing:
                # Draw overall progress bar
                pygame.draw.rect(surface, GREEN, (int(pos[0] - self.size/2), int(pos[1] - self.size/2) - 5, int(self.size * self.progress), 3))
                # Draw current operation progress bar
                if self.has_an_operation:
                    operation_time = self.calculate_operation_time(self.has_an_operation)
                    operation_progress = self.operation_timer / operation_time
                    pygame.draw.rect(surface, BLUE, (int(pos[0] - self.size/2), int(pos[1] - self.size/2) - 10, int(self.size * operation_progress), 3))

    @staticmethod
    def get_next_station(current_station, paths):
        for start, end in paths:
            if start == current_station:
                return end
        return None  # Return None if there's no next station
    
    #Check if the station has available capacity using the stations_dict
    @staticmethod
    def check_station_capacity(station_name, stations_dict):
        station = stations_dict[station_name]
        return station.get_available_workstation() is not None
    
    @property
    def progress(self):
        return self.completed_operations / self.total_operations if self.total_operations > 0 else 0
    