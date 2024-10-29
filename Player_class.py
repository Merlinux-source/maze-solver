from Cell_class import Cell


class Player:
    def __init__(self, maze, initial_position: tuple[int, int]) -> None:
        self.Maze = maze
        self.position = initial_position  # tuple of X coordinate and y Coordinate

    def get_current_cell(self) -> Cell:
        """Get the current cell the player is in."""
        x, y = self.position
        return self.Maze.grid[y][x]

    def get_current_cell(self) -> Cell:
        """Get the current cell the player is in."""
        x, y = self.position
        return self.Maze.grid[y][x]

    def get_possible_moves(self, allow_visited: bool = False) -> list[Cell]:
        """Get all possible cells the player can move to from the current position.
        
        Parameters:
        allow_visited (bool): If False, exclude cells that have already been visited.
        
        Returns:
        list[Cell]: A list of valid cells the player can move to.
        """
        x, y = self.position
        possible_moves = []

        # Define potential moves with directions
        directions = {
            'up': (x, y - 1),
            'down': (x, y + 1),
            'left': (x - 1, y),
            'right': (x + 1, y)
        }

        # Check each direction for wall constraints and boundaries
        for direction, (nx, ny) in directions.items():
            # Ensure we don't go out of bounds
            if 0 <= nx < self.Maze.width and 0 <= ny < self.Maze.height:
                current_cell = self.Maze.grid[y][x]
                new_cell = self.Maze.grid[ny][nx]

                # Check for walls and visited status if required
                if direction == 'up' and not current_cell.has_top_wall and not new_cell.has_bottom_wall:
                    if allow_visited or not new_cell.visited:
                        possible_moves.append(new_cell)
                elif direction == 'down' and not current_cell.has_bottom_wall and not new_cell.has_top_wall:
                    if allow_visited or not new_cell.visited:
                        possible_moves.append(new_cell)
                elif direction == 'left' and not current_cell.has_left_wall and not new_cell.has_right_wall:
                    if allow_visited or not new_cell.visited:
                        possible_moves.append(new_cell)
                elif direction == 'right' and not current_cell.has_right_wall and not new_cell.has_left_wall:
                    if allow_visited or not new_cell.visited:
                        possible_moves.append(new_cell)

        return possible_moves

    def move_to(self, cell: Cell, undo=False) -> None:
        """Move the player to the specified cell if it's adjacent and accessible."""
        if cell in self.get_possible_moves():
            self.get_current_cell().draw_move(cell, undo=undo)
            self.position = (cell.grid_coordinate_x, cell.grid_coordinate_y)
            cell.visited = True  # Mark the new cell as visited upon moving
            
            return
        raise Exception("Impossible move for the player object.")