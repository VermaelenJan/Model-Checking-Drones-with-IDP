import math
from random import randint

Curr_Height = []
Time = 0
DistanceBetween = {}
Home = (0, 0)
Inspection_Z = 0
Insp = []
Locations3D = {}
Curr_DistanceToTarget = []
Curr_DistanceToHome = []
Curr_DistanceToRA = []
Drone_Pos = []
Target = {}
plan = []
Height_lower = 0
Height_higher = 0
NonDetMove = []
Battery = []


def make_list(string, time, cast2int=True):
    result = []
    for i in range(time+1):
        val = (((string.split(str(i) + "->"))[1]).split(" "))[0]
        if cast2int:
            if not val[-1].isdigit():
                val = val[0:-1]
            result.append(int(val))
        else:
            if val[-1].__contains__(";"):
                val = val[0:-1]
            result.append(val)
    return result


def parse(file):
    with open(file) as f:
        content = f.readlines()

    for line in content:
        if line.__contains__(" Time = "):
            global Time
            Time = (int((((line.split("{ ")[1]).split(" }")[0]).split(".."))[1]))

        if line.__contains__(" Inspection = "):
            global Insp
            Insp = (((line.split("{ ")[1]).split(" }")[0]).split("; "))

        if line.__contains__(" DistanceBetween = "):
            values = (line.split("{")[1]).split(" }")[0]
            split = values.split(";")
            for val in split:
                value = val[1:]
                mapping = value.split("->")
                locations = (mapping[0]).split(",")
                from_location = locations[0]
                to_location = locations[1]
                value = mapping[1]
                global DistanceBetween
                DistanceBetween[(from_location, to_location)] = int(value)

        if line.__contains__(" Curr_Height = "):
            values = (line.split("{ ")[1]).split(" }")[0]
            global Curr_Height
            Curr_Height = make_list(values, Time)

        if line.__contains__(" InspectionHeight = "):
            lower_bound = (int((((line.split("{ ")[1]).split(" }")[0]).split(".."))[0]))
            upper_bound = (int((((line.split("{ ")[1]).split(" }")[0]).split(".."))[1]))
            global Inspection_Z
            Inspection_Z = (lower_bound + upper_bound)/2.0

        if line.__contains__(" Curr_DistanceToTarget = "):
            values = (line.split("{ ")[1]).split(" }")[0]
            global Curr_DistanceToTarget
            Curr_DistanceToTarget = make_list(values, Time)

        if line.__contains__(" Target = "):
            values = (line.split("{ ")[1]).split(" }")[0]
            global Target
            Target = make_list(values, Time, cast2int=False)

        if line.__contains__(" Plan = "):
            values = (line.split("{ ")[1]).split(" }")[0]
            global Plan
            Plan = make_list(values, Time, cast2int=False)

        if line.__contains__(" Height = "):
            global Height_lower
            Height_lower = (int((((line.split("{ ")[1]).split(" }")[0]).split(".."))[0]))
            global Height_higher
            Height_higher = (int((((line.split("{ ")[1]).split(" }")[0]).split(".."))[1]))

        if line.__contains__(" Curr_DistanceToHome = "):
            values = (line.split("{ ")[1]).split(" }")[0]
            global Curr_DistanceToHome
            Curr_DistanceToHome = make_list(values, Time)

        if line.__contains__(" NonDetMove = "):
            values = (line.split("{ ")[1]).split(" }")[0]
            values = values.split("; ")
            global NonDetMove
            NonDetMove = [int(val) for val in values]

        if line.__contains__(" Curr_DistanceToRA = "):
            values = (line.split("{ ")[1]).split(" }")[0]
            global Curr_DistanceToRA
            Curr_DistanceToRA = make_list(values, Time)

        if line.__contains__(" Battery = "):
            values = (line.split("{ ")[1]).split(" }")[0]
            global Battery
            Battery = make_list(values, Time)


def point_direction_distance(point, direction, distance):
    (x, y) = point
    new_x = math.cos(math.degrees(direction))*float(distance) + x
    new_y = math.sin(math.degrees(direction))*float(distance) + y
    return new_x, new_y


def generate_locations():
    Locations3D['Home'] = (0, 0)

    random_direction = randint(0, 359)
    insp1_3d = point_direction_distance(Home, random_direction, DistanceBetween[('Home', 'Insp1')])
    Locations3D['Insp1'] = insp1_3d

    x0 = Home[0]
    y0 = Home[1]
    x1 = insp1_3d[0]
    y1 = insp1_3d[1]
    r0 = DistanceBetween[('Home', 'Insp2')]
    r1 = DistanceBetween[('Insp1', 'Insp2')]

    d = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
    a = (r0 ** 2 - r1 ** 2 + d ** 2) / (2 * d)
    h = math.sqrt(r0 ** 2 - a ** 2)
    x2 = x0 + a * (x1 - x0) / d
    y2 = y0 + a * (y1 - y0) / d
    x3 = x2 + h * (y1 - y0) / d
    #  x3 = x2 - h * (y1 - y0) / d
    y3 = y2 - h * (x1 - x0) / d
    #  y3 = y2 + h * (x1 - x0) / d
    Locations3D['Insp2'] = (x3, y3)


def calculate_drone_pos():
    Drone_Pos.append(Home)
    for i in range(1, Time+1):
        if (Curr_DistanceToTarget[i] == Curr_DistanceToTarget[i-1]) & (Target[i] == Target[i-1]):
            Drone_Pos.append(Drone_Pos[i-1])

        elif Target[i] != Target[i-1]:
            if Curr_DistanceToTarget[i-1] == 0:
                Drone_Pos.append(Drone_Pos[i - 1])
            else:
                start_point = (Drone_Pos[i - 1][0], Drone_Pos[i - 1][1])
                if Target[i] == "Home":
                    step_size = 1
                    step_size /= Curr_DistanceToHome[i-1]
                    step_size *= math.hypot(Drone_Pos[i-1][0], Drone_Pos[i-1][1])
                    Drone_Pos.append(point_direction_distance(start_point,
                                                              math.radians(math.atan2(
                                                                  Locations3D[Target[i - 1]][1] - Drone_Pos[i - 1][1],
                                                                  Locations3D[Target[i - 1]][0] - Drone_Pos[i - 1][0])),
                                                              step_size))
                else:
                    print("Debug")

        elif (Curr_DistanceToTarget[i] < Curr_DistanceToTarget[i-1]) & (Target[i] == Target[i-1]):
            start_point = (Drone_Pos[i-1][0], Drone_Pos[i-1][1])
            step_size = 1
            step_size /= Curr_DistanceToTarget[i-1]
            step_size *= math.hypot(Locations3D[Target[i-1]][0] - Drone_Pos[i-1][0],
                                    Locations3D[Target[i-1]][1] - Drone_Pos[i-1][1])
            Drone_Pos.append(point_direction_distance(start_point,
                                                      math.radians(math.atan2(
                                                          Locations3D[Target[i-1]][1] - Drone_Pos[i-1][1],
                                                          Locations3D[Target[i-1]][0] - Drone_Pos[i-1][0])),
                                                      step_size))

        elif (Curr_DistanceToTarget[i] > Curr_DistanceToTarget[i - 1]) & (Target[i] == Target[i - 1]):
            start_point = (Drone_Pos[i - 1][0], Drone_Pos[i - 1][1])
            step_size = 1
            step_size /= Curr_DistanceToTarget[i - 1]
            step_size *= math.hypot(Locations3D[Target[i - 1]][0] - Drone_Pos[i - 1][0],
                                    Locations3D[Target[i - 1]][1] - Drone_Pos[i - 1][1])
            Drone_Pos.append(point_direction_distance(start_point,
                                                      math.radians(math.atan2(
                                                          Locations3D[Target[i - 1]][1] - Drone_Pos[i - 1][1],
                                                          Locations3D[Target[i - 1]][0] - Drone_Pos[i - 1][0])),
                                                      -step_size))
        else:
            print("debug!")


def generate_state(file):
    parse(file)
    generate_locations()
    calculate_drone_pos()

    state = []
    for i in range(Time+1):
        state.append(
            (
                (Home[0], Home[1], 0),
                (Drone_Pos[i][0], Drone_Pos[i][1], Curr_Height[i]),
                [(ix, iy, Inspection_Z) for name, (ix, iy) in Locations3D.items() if name != 'Home'],
                Plan[i],
                (Height_lower, Height_higher),
                i in NonDetMove,
                Battery[i],
                Target[i],
                Curr_DistanceToTarget[i],
                Curr_DistanceToHome[i],
                Curr_DistanceToRA[i]
            )
        )
    return state

