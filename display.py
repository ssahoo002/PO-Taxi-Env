import matplotlib.pyplot as plt
import numpy as np

def display_grid_graphically(taxi_pos, passengers, bushes, filename):
    grid_size = 10
    grid = np.zeros((grid_size, grid_size, 3))

    for x in range(grid_size):
        for y in range(grid_size):
            if (x + 1, y + 1) == taxi_pos:
                grid[y, x] = [1, 1, 0]
            elif (x + 1, y + 1) in passengers:
                grid[y, x] = [0, 0, 1]
            elif (x + 1, y + 1) in bushes:
                grid[y, x] = [0, 1, 0]
            elif (x + 1, y + 1) in dropoff_positions:
                grid[y,x] = [0,0,0]
            else:
                grid[y, x] = [1, 1, 1]

    plt.imshow(grid, interpolation='nearest')
    plt.xticks(ticks=np.arange(grid_size), labels=np.arange(1, grid_size + 1))
    plt.yticks(ticks=np.arange(grid_size), labels=np.arange(1, grid_size + 1))
    plt.grid(False)
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()
    

taxi_position = (4, 5)
passenger_positions = [(8,7), (2,3), (5,9)]
dropoff_positions = [(3,3), (8,6), (5,1)]
# bush_positions = [(4,3),(4,2), (5,3), (5,2), (7,7), (7,8), (6,7), (6,8), (6,6), (6,5), (7,5), (7,6), (6,3), (6,2), (7,3), (7,2), (8,4), (8,5), (9,4), (9,5)]
bush0 = []
bush1 = [(4,3),(4,2), (5,3), (5,2)]
bush2 = [(4,3),(4,2), (5,3), (5,2), (7,7), (7,8), (6,7), (6,8)]
bush3 = [(4,3),(4,2), (5,3), (5,2), (7,7), (7,8), (6,7), (6,8), (6,6), (6,5), (7,5), (7,6)]
bush4 = [(4,3),(4,2), (5,3), (5,2), (7,7), (7,8), (6,7), (6,8), (6,6), (6,5), (7,5), (7,6), (6,3), (6,2), (7,3), (7,2)]
bush5 = [(4,3),(4,2), (5,3), (5,2), (7,7), (7,8), (6,7), (6,8), (6,6), (6,5), (7,5), (7,6), (6,3), (6,2), (7,3), (7,2), (8,4), (8,5), (9,4), (9,5)]
filename = 'bush_5.png'
display_grid_graphically(taxi_position, passenger_positions, bush5, filename)