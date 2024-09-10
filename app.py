
from re import X
import pygame
from gui.Colors import *
from logger import setup_logger


# Lazy loading of other modules
def load_gui_modules():
    global Button, Window, Slider
    from gui.Button import Button
    from gui.Window import Window
    from gui.Slider import Slider

def load_sim_modules():
    global Workstation, Time, Station, Resource, Crane, Spawn, Unit
    from Workstation import Workstation
    from Time import Time
    from Station import Station
    from Resource import Resource
    from Crane import Crane
    from Spawn import Spawn
    from Unit import Unit



def main():
    pygame.init()

    #Setup logger
    logger = setup_logger()

    load_gui_modules()
    window = Window(width=1920, height=1080)
    window.init_display()

    #Attempt at speeding start up time
    load_sim_modules()

    # Initialize time
    time = Time(time_scale=80, start_hour=7, start_minute=30)

    # Load background
    background = pygame.image.load('new_img.png')
    background = pygame.transform.scale(background, window.get_size())
    
    #time.format_time()
    
    #Define station operations
    station_operations = {
        "Lace and Clamp": [
            {"name": "First coil moved to saddle", "base_time": 300, "req_heads":1, "required_resource": ["crane"]}, #Time in seconds
            {"name": "Leads bent away from window", "base_time": 60, "req_heads":1 },
            {"name": "Second coil moved to saddle", "base_time": 180, "req_heads":1,"required_resource": ["crane"]},
            {"name": "Leads bent away from window", "base_time": 60, "req_heads":1},
            {"name": "Third coil moved to saddle", "base_time": 180, "req_heads":1, "required_resource": ["crane"]},
            {"name": "Leads bent away from window", "base_time": 60, "req_heads":1},
            {"name": "Assemble shields and barriers", "base_time": 420, "req_heads":2},
            {"name": "Adjust saddle height", "base_time": 60, "req_heads":1},
            {"name": "Install sheilds and barriers", "base_time": 210, "req_heads":2},
            {"name": "First core sheets installed", "base_time": 240, "req_heads":1},
            {"name": "First coil laced", "base_time": 1200, "req_heads":1},
            {"name": "Second coil laced", "base_time": 1200, "req_heads":1},
            {"name": "Third coil laced", "base_time": 1200, "req_heads":1},
            {"name": "Picture of laced unit taken", "base_time": 120, "req_heads":1},
            {"name": "Ground straps added", "base_time": 300, "req_heads":1},
            {"name": "First core banded ", "base_time": 460, "req_heads":1},
            {"name": "Second core banded", "base_time": 460, "req_heads":1},
            {"name": "Third core banded", "base_time": 460, "req_heads":1},
            {"name": "All cores banded", "base_time": 240, "req_heads":1},
            {"name": "All cores banded", "base_time": 240, "req_heads":1},
            {"name": "Saddle raised and plate removed", "base_time": 150},
            {"name": "Top and bottom clamps and insulation installed", "base_time": 180, "req_heads":1},
            {"name": "End Clamps and insulation installed", "base_time": 120, "req_heads":1},
            {"name": "Clamp hardware installed", "base_time": 90, "req_heads":1},
            {"name": "Crane moveded over completed interior", "base_time": 120, "req_heads":1, "required_resource": ["crane"]},
            {"name": "Unit moved to flipper", "base_time": 240, "req_heads":1, "required_resource": ["crane", "flipper"]},
            {"name": "Unit flipped", "base_time": 90, "req_heads":1, "required_resource": ["flipper"]},
            {"name": "Unit placed by next station", "base_time": 120, "req_heads":1, "required_resource": ["crane"]}
            
    
        ],
        "FLIP":[{"name": "FLIP 🔁", "base_time": 60, "required_resource":["crane"]}
        ],
        "Lace and Clamp WIP":[{"name": "Move to WIP", "base_time": 60}
        ],
        "Internal Assembly Weld": [
            {"name": "Verify barwork placement", "base_time": 250},
            {"name": "Covering the top of the coil with a blanket", "base_time": 250},
            {"name": "Leads and barwork clamped", "base_time": 250},
            {"name": "Tack welding leads to barwork", "base_time": 250},
            {"name": "Cleaning welds", "base_time": 250},
            {"name": "Clamping X0 lead to barwork", "base_time": 250},
            {"name": "Covering the top of the coil with a blanket", "base_time": 250},
            {"name": "Welding the X0 lead to barwork", "base_time": 250},
            {"name": "Cleaning debris with air hose", "base_time": 250},
            {"name": "Connect leads", "base_time": 250}
        ],
        "Weld Conveyor": [
            {"name": "Advance conveyor", "base_time": 300}
        ],
        "IA HV Conveyor":[
            {"name": "Advance Conveyor", "base_time": 200}
        ],
        "HV Connections": [
            {"name": "Attach HV terminals", "base_time": 250}
        ],
        "HV Connections WIP":[{"name": "Store in WIP", "base_time": 250}
        ],
        "Oven": [
            {"name": "Heat", "base_time": 250}
        ]
    }

   # Create stations with resources
    lace_and_clamp_station = Station("Lace and Clamp", workstations=[
        Workstation("LC1", position=(99, 545),window=window,time=time,capacity=1),
        Workstation("LC2", position=(197, 545),window=window,time=time, capacity=1),
        Workstation("LC3", position=(295, 545),window=window,time=time, capacity=1)
    ], resources=[
        Resource("flipper", capacity=1, cooldown_time=60, position=(541, 387))], position=(40, 460),
        operations=station_operations["Lace and Clamp"],
        wip_capacity=4,
        window=window,time=time,
        wip_positions=[(490, 509), (584, 509), (489, 601), (584, 601)]
    )


    flip = Station("FLIP", 
        workstations=[Workstation("FLIP", position=(541, 387),window=window,time=time, capacity=1)],  # List of workstations
        resources=[Resource("flipper", capacity=1, cooldown_time=0, position=(541, 387))],  # List of resources
        position=(541, 387),
        window=window,time=time,
        operations=station_operations["FLIP"])

    IA_weld_conv = Station("Weld Conveyor", workstations=[
        Workstation("LC3", position=(651, 372), window=window,time=time,capacity=1)],resources=[], position=(651, 372),
        operations=station_operations["Weld Conveyor"],window=window,time=time )

    IA_weld_station = Station("Internal Assembly Weld", workstations=[
        Workstation("Internal Assembly Weld", position=(916, 372),window=window,time=time, capacity=1)
    ],resources=[], position=(916, 372),
        operations=station_operations["Internal Assembly Weld"], window=window,time=time,)

    IA_HV_conv = Station("IA HV Conveyor", workstations=[
        Workstation("LC1", position=(1375, 372), capacity=1,window=window,time=time)],resources=[], position=(1375, 372),
        operations=station_operations["IA HV Conveyor"],
        wip_capacity=3, window=window,time=time,
        wip_positions=[(1375, 372), (1281, 372), (1175, 372)])

    IA_HV_connections = Station("HV Connections", workstations=[
        Workstation("IA_1", position=(1375, 475), window=window,time=time, capacity=1),
        Workstation("IA_2", position=(1175, 475),window=window,time=time, capacity=1)
    ],resources=[],position=(1375, 372), operations=station_operations["HV Connections"],
    wip_capacity=4, window=window,time=time,
        wip_positions=[(1384, 671), (1288, 671), (1205, 671), (1111, 671)])


    oven_station = Station("Oven", workstations=[
        Workstation("Oven A", position=(1848, 437), window=window,time=time, capacity=2),
        Workstation("Oven B", position=(1848, 576), window=window,time=time, capacity=2)],resources=[], position=(1571, 502),
        operations=station_operations["Oven"], window=window,time=time,)

    #Define station dictionary
    stations = {
        "Lace and Clamp": lace_and_clamp_station,
        "FLIP": flip,
        "Weld Conveyor": IA_weld_conv,
        "Internal Assembly Weld": IA_weld_station,
        "IA HV Conveyor": IA_HV_conv,
        "HV Connections": IA_HV_connections,
        "Oven": oven_station
    }


    #Create cranes
    lace_and_clamp_overhead = Crane("Lace and Clamp Overhead Crane", initial_position=(99, 545), window=window,time=time,)


    # Add cranes to stations
    lace_and_clamp_station.cranes["crane"] = lace_and_clamp_overhead
    flip.cranes["crane"] = lace_and_clamp_overhead
    IA_HV_connections.cranes["crane"] = lace_and_clamp_overhead


    #Define flow path
    paths = [
        ("Lace and Clamp", "FLIP"),
        ("FLIP","Weld Conveyor"),
        ("Weld Conveyor", "Internal Assembly Weld"),
        ("Internal Assembly Weld", "IA HV Conveyor"),
        ("IA HV Conveyor", "HV Connections"),
        ("HV Connections", "Oven")
    ]


    #Create spawn point for Lace and Clamp
    lc_spawn = Spawn(40, 460, stations["Lace and Clamp"],paths, time=time, spawn_interval=180, random_kva=True)

    #Custom Spawn
    custom_spawn = Spawn(500, 300, stations["FLIP"],paths, time=time,kva_list=[2500])  # Custom spawn point in

    #List of spawn points
    spawn_points = [lc_spawn]

    # Set Unit class and stations for spawn points
    for spawn in spawn_points:
        spawn.set_unit_class_and_stations(Unit, stations)


    #UI Elements
    # Create pause/play button
    pause_button = Button(10, 10, 100, 50, "Pause", GREEN)

    #Create time scale slider
    time_slider = Slider(80, 400, time.get_time_scale(), 100, 220, 50)

    # Debug: Print all stations
    for name, station in stations.items():
        print(f"Station: {name}, Object: {station}")

    # Main game loop
    running = True

    # Create units
    units = []

    #Start system clock
    clock = pygame.time.Clock()


    #In simulation loop
    while running:

        #Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                adjusted_pos = window.adjust_mouse_pos(event.pos)
                if pause_button.is_clicked(adjusted_pos):
                    time.toggle_pause()
                    pause_button.text = "Play" if time.is_paused() else "Pause"
                    pause_button.color = RED if time.is_paused() else GREEN
                time_slider.handle_event(event)
            elif event.type == pygame.VIDEORESIZE:
                window.on_resize()
                background = pygame.transform.scale(background, window.get_size())
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    time.toggle_pause()
                    pause_button.text = "Play" if time.is_paused() else "Pause"
                    pause_button.color = RED if time.is_paused() else GREEN
                elif event.key == pygame.K_f:
                    window.toggle_fullscreen()

        #When time is not paused
        if not time.is_paused():
            delta_time = time.get_delta_time()
            time.update()
            #if time_slider.check_value_changed():
            time.set_time_scale(time_slider.get_value())
            

            #Update units
            units = [unit for unit in units if not unit.completed]
            for unit in units:
                unit.update(delta_time)

            #Update cranes
            for station in stations.values():
                for crane in station.cranes.values():
                    crane.update(delta_time)

            # Spawn new units
            for spawn in spawn_points:
                new_unit = spawn.update(time,delta_time, window)
                if new_unit:
                    units.append(new_unit)
        # Clear the screen
        window.screen.fill((0, 0, 0))  # Fill with black color
        
        # Draw the background
        scaled_background = pygame.transform.scale(background, (int(window.width * window.scale), int(window.height * window.scale)))
        # Draw background
        window.screen.blit(scaled_background, (0, 0))
        
        # Draw units
        for unit in units:
            unit.draw(window.get_surface(),window)
        
        
        # Draw station information
        for station in stations.values():
            station.draw()
        
        # Draw spawn points
        for spawn in spawn_points:
            spawn.draw(window)

        #load_gui_modules()

        # Draw pause/play button
        pause_button.draw(window.get_surface())

        # Draw clock next to pause button
        time.draw_clock(window, pause_button.rect.right + 10, pause_button.rect.top)

        # Draw runtime
        runtime_string = time.get_runtime_string()
        window.draw_text(runtime_string, (360, 36), font_size=36, color=BLACK)

        # Draw time scale slider
        time_slider.draw(window.get_surface())

        # Handle window events (including resizing)
        #running = window.handle_events()


        #update the display
        window.update()

        # Cap the frame rate
        #clock.tick(60)
    
    #Clean exit if needed 
    window.quit()



if __name__ == "__main__":
    main()
