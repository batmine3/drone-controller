from random import randint
from dronekit import connect, VehicleMode, LocationGlobal
import time, json
from math import sin, cos, sqrt, atan2, radians



def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command
    #  after Vehicle.simple_takeoff will execute immediately).
    while True:
        print(f" Altitude: {vehicle.location.global_relative_frame.alt}")
        #Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.99:
            print("Reached target altitude")
            break
        time.sleep(1)

def distance_to_point(lat, long, currentLat, currentLong):
    R = 6373.0
    lat1 = radians(lat)
    lon1 = radians(long)
    lat2 = radians(currentLat)
    lon2 = radians(currentLong)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    print(f"Distance restante : {format(distance, '.3f')} km", end="\r")

def go_to_point(lat, long, alt):
    point = LocationGlobal(lat, long, alt)
    vehicle.simple_goto(point)
    while True:
        currentLat = vehicle.location.global_frame.lat
        currentLong = vehicle.location.global_frame.lon
        currentAlt = vehicle.location.global_frame.alt
        if (
            (currentAlt >= 0.99 * alt and currentAlt <= 1.01 * alt) and
            (currentLat >= 0.99 * lat and currentLat <= 1.01 * lat) and
            (abs(currentLong) >= abs(0.99 * long) and abs(currentLong) <= abs(1.01 * long))
        ) or (vehicle.armed == False):
            return
        else:
            # print("=======================")
            # print(
            #     f"Alt(min: {alt * 0.99}, current: {currentAlt}, max: {alt * 1.01}) : {currentAlt >= 0.99 * alt and currentAlt <= 1.01 * alt}")
            # print(
            #     f"Lat(min: {lat * 0.99}, current: {currentLat}, max: {lat * 1.01}) : {currentLat >= 0.99 * lat and currentLat <= 1.01 * lat}")
            # print(
            #     f"Lng(min: {long * 0.99}, current: {currentLong}, max: {long * 1.01}) : {abs(currentLong) >= abs(0.99 * long) and abs(currentLong) <= abs(1.01 * long)}")
            # print("=======================")

            distance_to_point(lat, long, vehicle.location.global_frame.lat, vehicle.location.global_frame.lon)
            time.sleep(2)

def reset_battery(lat, long):
    print("\nOn se pose")
    go_to_point(lat, long, 0)
    print("=== Evenements ===")
    reportEvent()
    print("=== Fin Evenements ===")
    print("\nOn change de batterie")
    arm_and_takeoff(60)
    print("\nOn redécolle")

def reportEvent():
    events = [
        "Un malandrin a été surpris en train de voler la casquette d'une vieille dame.",
        "Bizarre, des hommes ont été aperçu en train de décharger de la farine colombienne.",
        "Un homme a volé la pelle d'un enfant. Que fait-on ? Rien c'est la vie et elle est dure !",
        "Intriguant, des crabes ont lancé une partie de poker contre les mouettes.",
        "Suprenant, le bus des Girondins de Bordeaux a été aperçu au font de l'eau, pas étonnant que le club coule !",
        "Il y a gavé monde sur la plage, flemme de surveiller.",
        "Un leviator sauvage apparait, que faire ??"
    ]
    for i in range (2):
        print(events[randint(0, 6)])


vehicle = connect("127.0.0.1:14550", wait_ready=True)


# on décolle
arm_and_takeoff(60)

print("Début de la surveillance du port !!")

# on charge les points de surveillance
with open('locations.json') as file:
    data = json.load(file)

# vehicle.simple_goto(embarcadere)

for counter in range (2):
    print("Je vais à l'embarcadère")
    go_to_point(data["embarcadere"]["lat"], data["embarcadere"]["long"], 60)
    reset_battery(data["embarcadere"]["lat"], data["embarcadere"]["long"])
    print("Je vais au phare")
    go_to_point(data["phare"]["lat"], data["phare"]["long"], 60)
    reset_battery(data["phare"]["lat"], data["phare"]["long"])


    
print("Fin de la surveillance du port")


vehicle.close()
