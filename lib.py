def if_cont(cell_height, a_height, a_is_burning):
    """Returns a non-zero float representing the ignition factor contribution
    that an adjacent cell with height a_height provides to a cell with
    height cell_height if it is burning, or 0.0 if it is not burning"""
    
    if not a_is_burning:
        return 0.0
    
    # no modifier for relatively flat cells
    if cell_height == a_height:
        return 1.0
    # fire spreads slower downhill
    if a_height > cell_height:
        return 0.5
    # fire spreads faster uphill
    if cell_height > a_height:
        return 2.0
    
def get_neighbours(i, j, dim):
    """Returns a list of pairs representing the coordinates of cells that are
    immediate neighbours of the cell at position (i, j)"""
    
    neighbours = []
    
    # iterate through cells in a 3x3 grid, centered at (i, j) and filter for
    # those who are within a dim x dim grid
    for y in range(-1, 2):
        for x in range(-1, 2):
            n_i, n_j = i + y, j + x
            if 0 <= n_i < dim and 0 <= n_j < dim and not (x == y == 0):
                neighbours.append((n_i, n_j))
    return neighbours
    
def get_wind_adjacent(i, j, dim, w_direction):
    """Returns a list of pairs representing the coordinates of cells that can
    affect the cell at position (i, j) based on the wind rule"""
    
    if not w_direction:
        return []
    
    pos_modifiers = {
        'N': [(-2, -1), (-2, 0), (-2, 1)],
        'NE': [(-2, 1), (-2, 2), (-1, 2)],
        'E': [(-1, 2), (0, 2), (1, 2)],
        'SE': [(1, 2), (2, 2), (2, 1)],
        'S': [(2, 1), (2, 0), (2, -1)],
        'SW': [(2, -1), (2, -2), (1, -2)],
        'W': [(1, -2), (0, -2), (-1, -2)],
        'NW': [(-1, -2), (-2, -2), (-2, -1)]
    }[w_direction]
    
    wind_adjacent = []
    
    # iterate through possible cells and filter those within a dim x dim grid
    for y, x in pos_modifiers:
        n_i, n_j = i + y, j + x
        if 0 <= n_i < dim and 0 <= n_j < dim:
            wind_adjacent.append((n_i, n_j))
    return wind_adjacent

def check_ignition(b_grid, f_grid, h_grid, i_threshold, w_direction, i, j):
    """Returns a boolean indicating whether or not the cell at position (i, j)
    will start burning on the next unit time frame, based on the current
    model of the situation."""
    
    # a cell that is already burning or has no fuel cannot burn
    if b_grid[i][j] or f_grid[i][j] == 0:
        return False
        
    dim = len(b_grid)
    cell_height = h_grid[i][j]
    i_factor = 0
    
    # construct list of immediate neighbour cells
    neighbour_cells = get_neighbours(i, j, dim)
    
    # construct a list of 'wind-adjacent' cells
    wind_adjacent_cells = get_wind_adjacent(i, j, dim, w_direction)
    
    # iterate over all adjacent cells
    for a_i, a_j in (neighbour_cells + wind_adjacent_cells):
        i_factor += if_cont(cell_height, h_grid[a_i][a_j], b_grid[a_i][a_j])
        
    return i_factor >= i_threshold


def run_model(f_grid, h_grid, i_threshold, w_direction, burn_seeds):
    """Returns a list containing a list of the states of the
    landscape and the total number of cells that have been burnt
    at each time frame as a tuple, playing out the scenario given by the model."""

    dim = len(f_grid)

    states = []
    
    def run_model_r(f_grid, burning_cells, burn_count):
        """Recursive helper function for run_model"""
        
        start_b_grid = [[True if (i, j) in burn_seeds and f_grid[i][j] else False for j in range(dim)] for i in range(dim)] 
        new_burn_count = burn_count
        states.append((f_grid, start_b_grid, new_burn_count))
        
        f_grid = [r[::] for r in f_grid]
        
        # construct b_grid to be used with check_ignition
        b_grid = [[False for _ in range(dim)] for _ in range(dim)]

        # use a copy of burning_cells to avoid mutability issues
        for (i, j) in burning_cells[::]:
            # remove cells that have finished burning
            if f_grid[i][j] == 0:
                burning_cells.remove((i, j))
            else:
                # decrement fuel load for burning cells
                f_grid[i][j] -= 1
                b_grid[i][j] = True
        
        # construct coordinates for all cells in the grid
        coords = [(i, j) for i in range(dim) for j in range(dim)]
        
        # iterate over the entire grid to check if each cell will start to burn
        for (i, j) in coords:
            if (i, j) not in burning_cells:    
                if check_ignition(b_grid, f_grid, h_grid,
                                  i_threshold, w_direction, i, j):
                    burning_cells.append((i, j))
                    new_burn_count += 1
                
        # base case is when there are no burning cells
        if burning_cells:
            # recursive call to simulate the next unit time frame
            run_model_r(f_grid, burning_cells, new_burn_count)
    
    run_model_r(f_grid, burn_seeds, len(burn_seeds))

    return states
