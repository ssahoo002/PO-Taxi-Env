import gtpyhop
import test_harness as th
import ast
import math
from heapq import heappop, heappush
import random
the_domain = gtpyhop.Domain(__package__)

print('-----------------------------------------------------------------------')

drive_amt = 0

# states and rigid relations
# there are 3 passengers, 3 dropoffs , 1 taxi
# instantiate bushes with coordinates
rigid = gtpyhop.State('rigid relations')
bush0 = []
bush1 = [(4,3),(4,2), (5,3), (5,2)]
bush2 = [(4,3),(4,2), (5,3), (5,2), (7,7), (7,8), (6,7), (6,8)]
bush3 = [(4,3),(4,2), (5,3), (5,2), (7,7), (7,8), (6,7), (6,8), (6,6), (6,5), (7,5), (7,6)]
bush4 = [(4,3),(4,2), (5,3), (5,2), (7,7), (7,8), (6,7), (6,8), (6,6), (6,5), (7,5), (7,6), (6,3), (6,2), (7,3), (7,2)]
bush5 = [(4,3),(4,2), (5,3), (5,2), (7,7), (7,8), (6,7), (6,8), (6,6), (6,5), (7,5), (7,6), (6,3), (6,2), (7,3), (7,2), (8,4), (8,5), (9,4), (9,5)]

rigid.types = {
    'taxi': ['t1'],
    'person': ['p1', 'p2', 'p3'],
    'dropoff_area': ['d1', 'd2', 'd3'],
    'bush': bush0
}


# the locations of the taxi, passengers, and dropoff locations
state = gtpyhop.State('state')
state.loc = {'t1': (4,5), 
                'p1': (8,7), 'p2': (2,3), 'p3': (5,9), 
                'd1': (3,3), 'd2': (8,6), 'd3': (5,1),
                'bushes': []
}

###############################################################################

# helper functions

def is_a(variable,type):
    return variable in rigid.types[type]

# def determine_order_of_moves():


###############################################################################

# Actions:
# drive
# preconditions: taxi must be 1 space away from target location and the target location cannot be a bush space
# effect: taxi is in desired location
def drive(state, taxi, to):
    x, y = to
    if is_a(taxi, 'taxi'):
        if to in state.loc['bushes']:
            print(f"Cannot move to bush space")
            return False
        if x in range(0,10) and y in range(0,10):
            delta_x = abs(state.loc[taxi][0] - x)
            delta_y = abs(state.loc[taxi][1] - y)
            if delta_x + delta_y == 1:
                state.loc[taxi] = (x, y)
                return state
            elif delta_x + delta_y == 0:
                print("Taxi is already in this position")
                return False
            print(f"Failed to execute drive to {to}")
            return False
    print(f"{taxi} is not a taxi")
    return False

# pickup
# precondition: taxi and passenger are in same move space
# effect: passenger location is taxi
def pickup(state, taxi, passenger):
    if is_a(taxi, 'taxi') and is_a(passenger, 'person'):
        if state.loc[taxi] == state.loc[passenger]:
            state.loc[passenger] = taxi
            return state
        else:
            print("Taxi and passenger are not in the same space")
            return False
    print(f"{taxi} is not a taxi or {passenger} is not a person")
    return False

# precondition: passenger must be in the taxi and taxi must be at dropoff location
# effect: passenger location is the dropoff location
def dropoff(state, taxi, passenger, dropoff_area):
    if is_a(taxi, 'taxi') and is_a(passenger, 'person') and is_a(dropoff_area, 'dropoff_area'):
        if state.loc[taxi] == state.loc[dropoff_area]:
            state.loc[passenger] = dropoff_area
            return state
        else:
            print("Taxi is not a dropoff location")
    print(f"{taxi} is not a taxi or {passenger} is not a person or {dropoff_area} is not a dropoff area")
    return False
        
gtpyhop.declare_actions(drive, pickup, dropoff)

###############################################################################

# Navigate helper functions
# This is the naive navigate approach, given taxi and location, it will move toward that point
# Note: Only works when there are no bushes
def naive_navigate(state, taxi, l):
    movements = []
    if(is_a(l, 'person')):
        l = state.loc[l]
    
    if is_a(taxi, 'taxi') and l[0] in range(0,10) and l[1] in range(0,10):
        x,y = state.loc[taxi]
        while (x,y) != l:
            if x < l[0]:
                x += 1
                movements.append(('drive', taxi, (x,y)))
            elif x > l[0]:
                x -= 1
                movements.append(('drive', taxi, (x,y)))
            elif y < l[1]:
                y += 1
                movements.append(('drive', taxi, (x,y)))
            elif y > l[1]:
                y -= 1
                movements.append(('drive', taxi, (x,y)))
            else:
                print("NAVIGATE FAILED")
                break   
    else:
        print("NAVIGATE FAIL") 
    if movements:     
        return movements
    
# AStar navigation
def astar_navigate(state, taxi, l):
    movements = []
    if(is_a(l, 'person')):
        l = state.loc[l]
    
    if is_a(taxi, 'taxi') and l[0] in range(0,10) and l[1] in range(0,10):
        x, y = state.loc[taxi]

    start = state.loc[taxi]
    goal = l
    directions = {
        "up": (-1, 0),
        "down": (1, 0),
        "left": (0, -1),
        "right": (0, 1)
    }

    open_set = []
    heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: calc_dist(start, goal)}

    while open_set:
        _, current = heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                prev = came_from[current]
                path.insert(0, current)
                current = prev

            x, y = start
            for (nx, ny) in path:
                movements.append(('drive', taxi, (nx, ny)))
                x, y = nx, ny
            return movements

        for move, (dx, dy) in directions.items():
            neighbor = (current[0] + dx, current[1] + dy)
            if not (0 <= neighbor[0] < 10 and 0 <= neighbor[1] < 10):
                continue
            if neighbor in state.loc['bushes']: 
                continue

            tentative_g_score = g_score[current] + 1
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + calc_dist(neighbor, goal)
                heappush(open_set, (f_score[neighbor], neighbor))

    return

# MCTS naviation
def mcts_navigate(state, taxi, l):
    movements = []
    if(is_a(l, 'person')):
        l = state.loc[l]
    
    if is_a(taxi, 'taxi') and l[0] in range(0,10) and l[1] in range(0,10):
        x, y = state.loc[taxi]

    directions = {
        "up": (-1, 0),
        "down": (1, 0),
        "left": (0, -1),
        "right": (0, 1)
    }

    def heuristic(current, goal):
        # manhattan distance heuristic
        return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

    def simulate_path(bushes, start, goal):
        path = []
        current = start
        while current != goal:
            # random exploration
            move = random.choice(list(directions.items()))
            dx, dy = move[1]
            next_position = (current[0] + dx, current[1] + dy)
            # moved off grid or into bush
            if not (0 <= next_position[0] < 10 and 0 <= next_position[1] < 10) or next_position in bushes:
                return
            path.append(next_position)
            current = next_position
        return path

    # mcts variables
    # num of iterations
    iterations = 100000
    best_path = None
    best_path_value = float('-inf')

    for _ in range(iterations):
        # simulate path
        path = simulate_path(state.loc['bushes'], state.loc[taxi], l)
        
        if path:
            path_value = len(path) - heuristic(path[-1], l)
        else:
            path_value = float('-inf')
        
        # if best path yet
        if path_value > best_path_value:
            best_path_value = path_value
            best_path = path

    # return movements from best path found
    if best_path:
        x, y = state.loc[taxi]
        for (nx, ny) in best_path:
            movements.append(('drive', taxi, (nx, ny)))
            x, y = nx, ny

    return movements

###############################################################################

# Methods
# if the passenger is already in the taxi, no pickup necessary
def no_pickup(state, taxi, passenger, navigate):
    if state.loc[passenger] == taxi:
        return []

# if the passenger is in the same move space as the taxi, just pickup
def only_pickup(state, taxi, passenger, navigate):
    l = state.loc[passenger]
    if is_a(taxi, 'taxi') and l[0] in range(0,10) and l[1] in range(0,10) and is_a(passenger, 'person'):
        if l == state.loc[taxi]:
            return [('pickup', taxi, passenger)]

# if the taxi must navigate to the passneger's space, then pickup    
def move_and_pickup(state, taxi, passenger, navigate):
    l = state.loc[passenger]
    plan = []
    if is_a(taxi, 'taxi') and l[0] in range(0,10) and l[1] in range(0,10) and is_a(passenger, 'person'):
        x = navigate(state, taxi, l)
        if x:
            plan.extend(x)
        plan.append(('pickup', taxi, passenger))
        return plan

# if the passenger is already at their designated dropoff location, do nothing
def no_dropoff(state, taxi, passenger, l, navigate):
    if state.loc[passenger] == l:
        return []
    
# if the passenger is in the taxi and the taxi is at dropoff location, just dropoff    
def only_dropoff(state, taxi, passenger, l, navigate):
    l = state.loc[l]
    if is_a(taxi, 'taxi') and l[0] in range(0,10) and l[1] in range(0,10) and is_a(passenger, 'person'):
        return [('dropoff', taxi, passenger, l)]

# if the passenger is in the taxi, but taxi is not at dropoff location, taxi navigates to it, then drops off passenger
def move_and_dropoff(state, taxi, passenger, d, navigate):
    l = state.loc[d]
    plan = []
    if is_a(taxi, 'taxi') and l[0] in range(0,10) and l[1] in range(0,10) and is_a(passenger, 'person'):
        x = navigate(state, taxi, l)
        if x:
            plan.extend(navigate(state, taxi, l))
        plan.append(('dropoff', taxi, passenger, d))
        return plan


gtpyhop.declare_task_methods('passenger_pickup', no_pickup, only_pickup, move_and_pickup)
gtpyhop.declare_task_methods('passenger_dropoff', no_dropoff, only_dropoff, move_and_dropoff)


###############################################################################

# Commands
def c_drive(state, taxi, to):
    global drive_amt
    x, y = to
    if is_a(taxi, 'taxi'):
        if to in rigid.types['bush']:
            state.loc['bushes'].append(to)            
            print(state.loc['bushes'])
            print(f"Cannot move to bush space!")
            return state
        if x in range(0,10) and y in range(0,10):
            delta_x = abs(state.loc[taxi][0] - x)
            delta_y = abs(state.loc[taxi][1] - y)
            if delta_x + delta_y == 1:
                state.loc[taxi] = (x, y)
                drive_amt += 1
                return state
            elif delta_x + delta_y == 0:
                print("Taxi is already in this position")
                return False
            print(f"Failed to execute drive to {to}")
            return False
    print(f"{taxi} is not a taxi")
    return False

def c_pickup(state, taxi, passenger):
    if is_a(taxi, 'taxi') and is_a(passenger, 'person'):
        if state.loc[taxi] == state.loc[passenger]:
            state.loc[passenger] = taxi
            return state
        else:
            print("Taxi and passenger are not in the same space")
            return False
    print(f"{taxi} is not a taxi or {passenger} is not a person")
    return False

def c_dropoff(state, taxi, passenger, dropoff_area):
    if is_a(taxi, 'taxi') and is_a(passenger, 'person') and is_a(dropoff_area, 'dropoff_area'):
        if state.loc[taxi] == state.loc[dropoff_area]:
            state.loc[passenger] = dropoff_area
            return state
        else:
            print("Taxi is not a dropoff location")
    print(f"{taxi} is not a taxi or {passenger} is not a person or {dropoff_area} is not a dropoff area")
    return False

gtpyhop.declare_commands(c_drive, c_pickup, c_dropoff)


###############################################################################
# Order of Moves function
# this is designed to decide which passenger to pick up first. 
# Then, it will determine if it should dropoff that passenger or pickup the next closest passenger. 
# It will repeat until all passengers are moved to their dropoff locations.
def calc_dist(c1, c2):
    return abs((c1[0] - c2[0]) + abs(c1[1] - c2[1]))

def order_of_operations(state, navigate):
    passengers = {
        'p1': state.loc['p1'],
        'p2': state.loc['p2'],
        'p3': state.loc['p3']
    }
    dropoffs = {
        'p1': state.loc['d1'],
        'p2': state.loc['d2'],
        'p3': state.loc['d3']
    }
    taxi = state.loc['t1']

    picked_up = set()
    delivered = set()
    
    # stores sequence of actions
    operations = []
    
    while len(delivered) < 3:
        # finds closest passenger to pick up
        closest_passenger = None
        closest_distance = float('inf')
        
        for p, location in passengers.items():
            if p not in picked_up:
                dist = calc_dist(taxi, location)
                if dist < closest_distance:
                    closest_passenger = p
                    closest_distance = dist
        
        # pick up passenger if found
        if closest_passenger:
            taxi = passengers[closest_passenger]
            picked_up.add(closest_passenger)
            operations.append(('passenger_pickup', 't1', closest_passenger, navigate))
        
        # check if dropoff
        closest_dropoff = None
        closest_dropoff_distance = float('inf')
        
        for p in picked_up:
            if p not in delivered:
                dist = calc_dist(taxi, dropoffs[p])
                if dist < closest_dropoff_distance:
                    closest_dropoff = p
                    closest_dropoff_distance = dist
        
        if closest_dropoff:
            taxi = dropoffs[closest_dropoff]
            delivered.add(closest_dropoff)
            _dropoff = 'd' + closest_dropoff[1]
            operations.append(('passenger_dropoff', 't1', closest_dropoff, _dropoff, navigate))
    
    return operations
    
def check_goal_state(state):
    if state.loc['p1'] == 'd1' and state.loc['p2'] == 'd2' and state.loc['p3'] == 'd3':
        return True
    return False



###############################################################################

print('-----------------------------------------------------------------------')
# print(f"Created the domain '{domain_name}'. To run the examples, type this:")
# print(f"{domain_name}.main()")

def main(do_pauses=True):
    """
    Run various examples.
    main() will pause occasionally to let you examine the output.
    main(False) will run straight through to the end, without stopping.
    """

    # If we've changed to some other domain, this will change us back.
    gtpyhop.current_domain = the_domain
    gtpyhop.print_domain()

    _state = state.copy()

    state.display(heading='\nInitial state is')

    th.pause(do_pauses)

    gtpyhop.verbose = 3
    # order = order_of_operations(state, astar_navigate)
    # new_state = gtpyhop.run_lazy_lookahead(state1, order)
    # th.pause(do_pauses)
    # plan = gtpyhop.find_plan(new_state,[('travel','alice','park')])

    # order = order_of_operations(state, astar_navigate)
    order = order_of_operations(_state, astar_navigate)
    # state = state.copy()
    # steps
    for action in order:
        print(action)
        # execution action
        print(f"Executing action: {action}")
        _state = gtpyhop.run_lazy_lookahead(_state, [action])
        
        # checks goal state after actions
        if check_goal_state(_state):
            print("# Drives:", drive_amt)
            print("Goal state reached!")
            break
        else:
            print("Goal state not reached yet.")
            th.pause(do_pauses)


if __name__ == "__main__":
    main()