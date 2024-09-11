import pygame
from gui.Colors import*
from Workstation import Workstation
import sys


class Station:
    def __init__(self, name, workstations, resources, position, window, time, operations=None, wip_capacity=0, wip_positions=None, cranes=None):
        self.name = name
        self.workstations = [Workstation(ws.name, ws.position, window, time, ws.capacity) for ws in workstations]
        self.resources = {resource.name: resource for resource in resources}
        self.position = position
        self.operations = operations if operations is not None else []
        self.wip_capacity = wip_capacity
        self.wip_positions = wip_positions if wip_positions is not None else []
        self.wip_units = []
        self.next_wip_position_index = 0
        self.window = window
        self.time = time
        self.cranes = cranes or {}


    def get_available_workstation(self):
        #Loop through all workstions in the list
        for workstation in self.workstations:
            #check if it is available
            if workstation.is_available():
                print(f"Time: {self.time.format_time()} - Available workstation found: {workstation.name}")
                return workstation
            else:
                #For all all not avaiable, print them
                print(f"Time: {self.time.format_time()} - {workstation.name} is NOT available")

        print(f"Time: {self.time.format_time()} - No available workstations at {self.name}")
        return None
    
    def has_capacity(self):
        return any(workstation.is_available() for workstation in self.workstations)
    
    def are_resources_available(self, resource_names, current_time):
        for resource_name in resource_names:
            if not self.resources[resource_name].is_available(current_time):
                print(f"Debug: Resource {resource_name} is not available at {self.name}")
                return False
        return True
    
    def use_resources(self, resource_names, current_time):
        if not resource_names:
            return []  # Return an empty list if no resources are required

        used_resources = []
        for resource_name in resource_names:
            if self.resources[resource_name].use(current_time):
                used_resources.append(resource_name)
                print(f"Debug: Resource {resource_name} acquired at {self.name}")
            else:
                print(f"Debug: Failed to acquire resource {resource_name} at {self.name}")
        
        if len(used_resources) == len(resource_names):
            return used_resources
        else:
            # If we couldn't use all resources, release the ones we did use
            for resource_name in used_resources:
                self.release_resource(resource_name, current_time)
                print(f"Debug: Released resource {resource_name} at {self.name} due to incomplete acquisition")
            return None
        
    def add_to_wip(self, unit):
        if len(self.wip_units) < self.wip_capacity:
            if self.next_wip_position_index < len(self.wip_positions):
                unit.pos = self.wip_positions[self.next_wip_position_index]
                self.next_wip_position_index += 1
            else:
                print(f"Warning: No more defined WIP positions in {self.name}. Using last known position.")
                unit.pos = self.wip_positions[-1]
            
            self.wip_units.append(unit)
            unit.in_wip = True
            unit.wip_location = self.name
            print(f"Time: {self.time.format_time()} - {unit} added to WIP at {self.name} at position {unit.pos}")
            return True
        else:
            print(f"Time: {self.time.format_time()} - WIP at {self.name} is at full capacity. Cannot add {unit}")
            return False
        
    def remove_from_wip(self):
        if self.wip_units:
            unit = self.wip_units.pop(0)
            unit.in_wip = False
            unit.wip_location = None
            self.next_wip_position_index = max(0, self.next_wip_position_index - 1)
            print(f"Time: {self.time.format_time()} - {unit} removed from WIP at {self.name}")
            return unit
        else:
            print(f"Time: {self.time.format_time()} - No units in WIP at {self.name} to remove")
            return None

    def is_wip_full(self):
        return len(self.wip_units) >= self.wip_capacity

    def is_wip_empty(self):
        return len(self.wip_units) == 0

    def get_available_wip_capacity(self):
        return self.wip_capacity - len(self.wip_units)
        
    def release_resource(self, resource_name, current_time):
        if resource_name in self.resources:
            self.resources[resource_name].release(current_time)
            print(f"Debug: Released resource {resource_name} at {self.name}")

    def get_crane(self, crane_name):
        return self.cranes.get(crane_name)
    
    def draw(self):
        # Draw workstation information
        for workstation in self.workstations:
            workstation.draw_info()

        # Draw units in WIP
        for unit in self.wip_units:
            unit.draw(self.window.screen)

        # Draw WIP capacity information
        if self.wip_capacity > 0:
            font = pygame.font.Font(None, 24)
            text = font.render(f"{self.name} WIP: {len(self.wip_units)}/{self.wip_capacity}", True, BLACK)
            self.window.screen.blit(text, self.window.scale_pos((self.wip_positions[0][0], self.wip_positions[0][1] - 30)))
       
        #draw all cranes
        for crane in self.cranes.values():
            crane.draw()


        