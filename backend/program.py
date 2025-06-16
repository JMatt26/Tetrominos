# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part B: Game Playing Agent

from game import PlayerColor, Action, PlaceAction, Coord

import numpy as np
import copy
import time

class Shape:
    """
    This is the superclass that represents the basic tetris shape objects
    """

    def __init__(self, shapes, position=Coord(0, 0), rotation_index=0):
        self.shapes = shapes
        self.position = position
        self.rotation_index = rotation_index

    def get_place_action(self) -> PlaceAction:
        """
        Generates a PlaceAction based on the shape's current position and rotation.
        
        Returns:
            PlaceAction: A PlaceAction object representing the shape's placement
        """
        # Get the coordinates for the current rotation
        relative_coords = self.shapes[self.rotation_index]
        
        # Convert relative coordinates to absolute coordinates
        absolute_coords = [
            self.position + coord
            for coord in relative_coords
        ]
        
        # Create and return the PlaceAction
        return PlaceAction(*absolute_coords)


class IShape(Shape):
    """
    I shape and its rotations, with a relative position at (0,0)
    """

    def __init__(self, position=Coord(0, 0), rotation_index=0):
        shapes = [
            [Coord(0, 0), Coord(0, 1), Coord(0, 2), Coord(0, 3)],  # horizontal state
            [Coord(0, 0), Coord(1, 0), Coord(2, 0), Coord(3, 0)]   # vertical state
        ]
        super().__init__(shapes, position, rotation_index)


class OShape(Shape):
    """
    O shape and its rotations, with a relative position at (0,0)
    """

    def __init__(self, position=Coord(0, 0), rotation_index=0):
        shapes = [
            [Coord(0, 0), Coord(0, 1), Coord(1, 0), Coord(1, 1)]
        ]
        super().__init__(shapes, position, rotation_index)


class TShape(Shape):
    """
    T shape and its rotations, with a relative position at (0,0)
    """

    def __init__(self, position=Coord(0, 0), rotation_index=0):
        shapes = [
            [Coord(0, 0), Coord(0, 1), Coord(0, 2), Coord(1, 1)],   # Pointing Down
            [Coord(0, 0), Coord(1, 0), Coord(2, 0), Coord(1, 10)],  # Pointing Left
            [Coord(0, 0), Coord(0, 10), Coord(0, 9), Coord(10, 10)], # Pointing Up
            [Coord(0, 0), Coord(10, 0), Coord(9, 0), Coord(10, 1)]   # Pointing Right
        ]
        super().__init__(shapes, position, rotation_index)


class JShape(Shape):
    """
    J shape and its rotations, with a relative position at (0,0)
    """

    def __init__(self, position=Coord(0, 0), rotation_index=0):
        shapes = [
            [Coord(0, 0), Coord(0, 1), Coord(10, 1), Coord(9, 1)], # Pointing Up
            [Coord(0, 0), Coord(1, 0), Coord(1, 1), Coord(1, 2)],  # Pointing Right
            [Coord(0, 0), Coord(0, 10), Coord(1, 10), Coord(2, 10)],  # Pointing Down
            [Coord(0, 0), Coord(10, 0), Coord(10, 10), Coord(10, 9)]   # Pointing Left
        ]
        super().__init__(shapes, position, rotation_index)


class LShape(Shape):
    """
    L shape and its rotations, with a relative position at (0,0)
    """

    def __init__(self, position=Coord(0, 0), rotation_index=0):
        shapes = [
            [Coord(0, 0), Coord(0, 10), Coord(10, 10), Coord(9, 10)],   # Pointing Up
            [Coord(0, 0), Coord(10, 0), Coord(10, 1), Coord(10, 2)],    # Pointing Right
            [Coord(0, 0), Coord(0, 1), Coord(1, 1), Coord(2, 1)],       # Pointing Down
            [Coord(0, 0), Coord(1, 0), Coord(1, 10), Coord(1, 9)]       # Pointing Left
        ]
        super().__init__(shapes, position, rotation_index)


class ZShape(Shape):
    """
    Z shape and its rotations, with a relative position at (0,0)
    """

    def __init__(self, position=Coord(0, 0), rotation_index=0):
        shapes = [
            [Coord(0, 0), Coord(1, 0), Coord(1, 1), Coord(0, 10)],
            [Coord(0, 0), Coord(0, 10), Coord(1, 10), Coord(10, 0)]
        ]
        super().__init__(shapes, position, rotation_index)


class SShape(Shape):
    """
    S shape and its rotations, with a relative position at (0,0)
    """

    def __init__(self, position=Coord(0, 0), rotation_index=0):
        shapes = [
            [Coord(0, 0), Coord(1, 0), Coord(1, 10), Coord(0, 1)],
            [Coord(0, 0), Coord(1, 0), Coord(0, 10), Coord(10, 10)]
        ]
        super().__init__(shapes, position, rotation_index)

class GameState:
    """
    This class is the core environment abstraction that holds the board state
    and functions

    Args:
            board: A dictionary mapping Coord objects to PlayerColor, representing the occupied cells.
            current_player: The player whose turn it is (PlayerColor.RED or PlayerColor.BLUE).
    """
    
    def __init__(self, board: dict[Coord, PlayerColor] = None, current_player : PlayerColor = None, turn_count: int = 0):
        self.board = board
        self.current_player = current_player
        self.turn_count = turn_count
    
    def is_line_full(self, action : PlaceAction) -> tuple[list[int], list[int]]:
        """
        This method returns a tuple containing two lists, each 
        holding the row and columns that are full

        Args:
                action: The last move that was made by an agent before updating the board
        """
        rows_to_check = set()
        cols_to_check = set()
        for coord in action.coords:
            rows_to_check.add(coord.r)
            cols_to_check.add(coord.c)

        full_rows = []
        full_cols = []
        
        for target_row in rows_to_check:
            is_row_full = True
            for c in range(0,11):
                if not self.board.get(Coord(target_row, c)):
                    is_row_full = False
                    break
            if is_row_full:
                full_rows.append(target_row)
                
        for target_col in cols_to_check:
            is_col_full = True
            for r in range(0,11):
                if not self.board.get(Coord(r, target_col)):
                    is_col_full = False
                    break
            if is_col_full:
                full_cols.append(target_col)
                
        return full_rows, full_cols
    
    def clear_lines(self, rows, cols):
        """
        Method responsible for clearing a line that is full

        Args:
                rows: List of rows that need to be cleared
                cols: List of columns that need to be cleared
        """

        if rows:
            for row in rows:
                for c in range(0,11):
                    if Coord(row, c) in self.board:
                        self.board.pop(Coord(row, c), None)
        
        if cols:
            for col in cols:
                for r in range(0,11):
                    if Coord(r, col) in self.board:
                        self.board.pop(Coord(r, col), None)

    def _clearance_score(self, shape: Shape) -> float:
        """
        Heuristic score that rewards moves which bring rows/cols closer to full.
        """
        temp_board = copy.deepcopy(self.board)
        action = shape.get_place_action()

        for coord in action.coords:
            temp_board[coord] = self.current_player

        # Count filled cells in affected rows and cols
        rows = {coord.r for coord in action.coords}
        cols = {coord.c for coord in action.coords}

        score = 0

        for r in rows:
            filled = sum(1 for c in range(11) if Coord(r, c) in temp_board)
            score += filled / 11  # Normalize row fill level

        for c in cols:
            filled = sum(1 for r in range(11) if Coord(r, c) in temp_board)
            score += filled / 11  # Normalize col fill level

        return score

    
    def _find_valid_coords(self, color: PlayerColor) -> set:
        """
        Finds all viable coordinates, after the first move, where a player can potentially lay a piece

        Args: 
            color: Player's color

        Returns:
            Set of valid adjacent coords for a token to be placed
        """

        # Get all board pieces of the agents color
        same_colour_pieces = {coord for coord, piece_color in self.board.items() if piece_color == color}

        valid_surrounding_spaces = set()
        for coord in same_colour_pieces:
            valid_surrounding_spaces = self._find_adjacent_coords(coord, valid_surrounding_spaces)
        
        return valid_surrounding_spaces
    
    def _find_adjacent_coords(self, coord: Coord, surrounding_spaces : set) -> set:
        """
        Helper method to find valid adjacent coords next to a coord of its own color

        Args:
            coord: coordinate to check surroundings of
            surrounding_spaces: set of coordinates to append valid tokens to

        Returns:
            Updated set of valid surrounding spaces
        """

        directions = [coord.up(), coord.left(), coord.right(), coord.down()]
        for direction in directions:
            if direction not in self.board:
                surrounding_spaces.add(direction)
        
        return surrounding_spaces
    
    def _first_turn_valid_coords(self) -> set:
        valid_coords = set()
        for r in range(11):
            for c in  range(11):
                valid_coords.add(Coord(r,c))
        
        return valid_coords

    def find_all_valid_moves(self, color: PlayerColor) -> list[tuple[Shape, Coord]]:
        """
        Finds all valid moves for every shape and rotation at each valid coordinate.
        A move is considered valid

        Args:
            color: The color of the player making the move

        Returns:
            A list of tuples containing (Shape, Coord) pairs representing valid moves
        """
        valid_moves = []
        
        # Check if this is the player's first turn (no pieces of their color on the board)
        player_pieces = {coord for coord, piece_color in self.board.items() if piece_color == color}
        if not player_pieces:
            valid_coords = self._first_turn_valid_coords()
        else:
            valid_coords = self._find_valid_coords(color)
        
        # Define all possible shapes
        shapes = [
            IShape(position=Coord(0, 0)),
            OShape(position=Coord(0, 0)),
            TShape(position=Coord(0, 0)),
            JShape(position=Coord(0, 0)),
            LShape(position=Coord(0, 0)),
            ZShape(position=Coord(0, 0)),
            SShape(position=Coord(0, 0))
        ]
        
        # For each valid coordinate
        for valid_coord in valid_coords:
            # For each shape type
            for shape in shapes:
                # For each possible rotation
                for rotation in range(len(shape.shapes)):
                    # Get the relative coordinates for this rotation
                    relative_coords = shape.shapes[rotation]
                    
                    # For each coordinate in the shape
                    for rel_coord in relative_coords:
                        # Calculate the position that would place this coordinate at the valid position
                        # This is: valid_coord - rel_coord
                        base_position = valid_coord - rel_coord
                        
                        # Create a new shape at the calculated base position
                        test_shape = type(shape)(position=base_position, rotation_index=rotation)
                        
                        # Get the coordinates this shape would occupy
                        place_action = test_shape.get_place_action()
                        shape_coords = set(place_action.coords)
                        
                        # Check if any coordinates overlap with existing pieces
                        if not any(coord in self.board for coord in shape_coords):
                            valid_moves.append((test_shape, valid_coord))

        np.random.shuffle(valid_moves)  # Ensure's fair tie breaking for before applying heuristic

        valid_moves.sort(
            key=lambda move: self._clearance_score(move[0]),
            reverse=True
        )
        
        return valid_moves
    
    def has_won(self, color : PlayerColor):
        """
        Returns:
            True if game is over
            False if moves can be made
        """
        opponent_color = PlayerColor.BLUE if color == PlayerColor.RED else PlayerColor.RED
        valid_moves = self.find_all_valid_moves(opponent_color)
        if not valid_moves: 
            return True
        return False
    
class MCTS_Node:
    """
    This class is responsible for the structure and implementation
    of the Monte Carlo Tree Search Algorithm.
    """

    def __init__(self, state: GameState, parent_node: 'MCTS_Node' = None, previous_action: PlaceAction = None):
        self.state = state                          # GameState this node represents
        self.parent_node = parent_node            # Parent Game State
        self.previous_action = previous_action      # Action taken to get here from parent state
        self.children: list[MCTS_Node] = []         # List of child nodes

        self.visits = 0                             
        self.total_wins = 0
        self.untried_actions = state.find_all_valid_moves(state.current_player)

    def expand(self) -> 'MCTS_Node':
        """
        Expands the current node by creating a child node for an untried action.
        
        Returns:
            MCTS_Node: The newly created child node
        """
        if not self.untried_actions:
            return None
            
        # Get the next untried action
        shape, coord = self.untried_actions.pop()
        action = shape.get_place_action()
        
        # Create a new game state for the child
        new_board = copy.deepcopy(self.state.board)
        new_state = GameState(
            board=new_board,
            current_player=self.state.current_player,
            turn_count=self.state.turn_count + 1
        )
        
        # Apply the action to the new state
        for coord in action.coords:
            new_board[coord] = self.state.current_player
            
        # Switch the current player
        new_state.current_player = PlayerColor.RED if self.state.current_player == PlayerColor.BLUE else PlayerColor.BLUE
        
        # Create the child node
        child = MCTS_Node(
            state=new_state,
            parent_node=self,
            previous_action=action
        )
        
        # Add the child to the children list
        self.children.append(child)
        
        return child

    def select_child(self, exploration_constant: float = 1.41) -> 'MCTS_Node':
        """
        Selects the best child node using the UCB1 formula.
        
        Args:
            exploration_constant: The exploration parameter (default is sqrt(2))
            
        Returns:
            MCTS_Node: The selected child node
        """
        if not self.children:
            return None
            
        # Calculate UCB1 value for each child
        ucb_values = []
        for child in self.children:
            if child.visits == 0:
                # If child hasn't been visited, give it maximum value
                ucb_values.append(float('inf'))
            else:
                # UCB1 formula: exploitation + exploration
                exploitation = child.total_wins / child.visits
                exploration = exploration_constant * np.sqrt(np.log(self.visits) / child.visits)
                ucb_values.append(exploitation + exploration)
        
        # Return the child with the highest UCB1 value
        return self.children[np.argmax(ucb_values)]

    def simulate(self) -> bool:
        """
        Simulates a random playout from the current state until reaching a terminal state.
        
        Returns:
            bool: True if the original player (from this node) wins, False otherwise
        """
        current_state = copy.deepcopy(self.state)
        original_player = current_state.current_player
        
        # Limit simulation depth to prevent too long simulations
        max_depth = 10
        depth = 0
        
        while depth < max_depth:
            # Get all valid moves for the current player
            valid_moves = current_state.find_all_valid_moves(current_state.current_player)
            
            if not valid_moves:
                # If no valid moves, the current player loses
                winner = PlayerColor.RED if current_state.current_player == PlayerColor.BLUE else PlayerColor.BLUE
                return winner == original_player
                
            # Randomly select a move
            move_index = np.random.randint(0, len(valid_moves))
            shape, coord = valid_moves[move_index]
            action = shape.get_place_action()
            
            # Apply the move
            for coord in action.coords:
                current_state.board[coord] = current_state.current_player
            
            # Check for and clear any completed lines
            full_rows, full_cols = current_state.is_line_full(action)
            current_state.clear_lines(full_rows, full_cols)
                
            # Switch players
            current_state.current_player = PlayerColor.RED if current_state.current_player == PlayerColor.BLUE else PlayerColor.BLUE
            
            depth += 1
            
        # If we reach max depth, consider it a draw
        return False

    def backpropagate(self, result: bool, original_player: PlayerColor):
        """
        Updates the statistics of this node and all its ancestors based on the simulation result.

        Args:
            result: True if the original player won, False otherwise
            original_player: The player who started the simulation
        """
        self.visits += 1

        # Reward is from the original player's perspective
        if self.state.current_player != original_player:
            self.total_wins += 1 if result else 0

        if self.parent_node is not None:
            self.parent_node.backpropagate(result, original_player)


class Agent:
    """
    This class is the "entry point" for your agent, providing an interface to
    respond to various Tetress game events.
    """

    def __init__(self, color: PlayerColor, iterations: int, **referee: dict):
        """
        This constructor method runs when the referee instantiates the agent.
        Any setup and/or precomputation should be done here.
        """

        self.game_state: dict[Coord, PlayerColor] = {}  # board represented by a dictionary
        self.turn_count = 0

        self.iterations = iterations

        self._color = color
        match color:
            case PlayerColor.RED:
                print("Testing: I am playing as RED")
            case PlayerColor.BLUE:
                print("Testing: I am playing as BLUE")

    def action(self, **referee: dict) -> Action:
        """
        This method is called by the referee each time it is the agent's turn
        to take an action. It must always return an action object.
        """
        # Create a GameState object from our current state
        current_state = GameState(
            board=self.game_state,
            current_player=self._color,
            turn_count=self.turn_count
        )
        
        # Create root node for MCTS
        root = MCTS_Node(current_state)
        
        # Time limit for MCTS (in seconds)
        time_limit = 170  # Leave 10 seconds buffer
        start_time = time.time()
        
        # Run MCTS iterations until time limit
        iterations = 0
        while time.time() - start_time < time_limit:
            # Selection
            node = root
            while node.untried_actions == [] and node.children != []:
                node = node.select_child()
            
            # Expansion
            if node.untried_actions:
                node = node.expand()
            
            # Simulation
            result = node.simulate()
            
            # Backpropagation
            node.backpropagate(result, self._color)
            
            iterations += 1
            
            # Early exit if we've done enough iterations
            if iterations >= self.iterations:
                break
        
        # Select the best child of the root node
        if root.children:
            # Select the child with the most visits
            best_child = max(root.children, key=lambda child: child.visits)
            return best_child.previous_action
        else:
            # If no children were created (shouldn't happen if there are valid moves),
            # select a random valid move
            valid_moves = current_state.find_all_valid_moves(self._color)
            if valid_moves:
                move_index = np.random.randint(0, len(valid_moves))
                shape, coord = valid_moves[move_index]
                return shape.get_place_action()
            else:
                # This should never happen as the referee should handle game over
                raise Exception("No valid moves available")

    def update(self, color: PlayerColor, action: Action, **referee: dict):
        """
        This method is called by the referee after an agent has taken their
        turn. You should use it to update the agent's internal game state.
        """
        # There is only one action type, PlaceAction
        place_action: PlaceAction = action
        c1, c2, c3, c4 = place_action.coords

        # Update the board with the new piece
        self.game_state[c1] = color
        self.game_state[c2] = color
        self.game_state[c3] = color
        self.game_state[c4] = color

        # Create a temporary GameState to check for and clear lines
        temp_state = GameState(
            board=self.game_state,
            current_player=color,
            turn_count=self.turn_count
        )

        # Check for and clear any completed lines
        full_rows, full_cols = temp_state.is_line_full(place_action)
        temp_state.clear_lines(full_rows, full_cols)

        # Update our game state with the cleared lines
        self.game_state = temp_state.board

        self.turn_count += 1

        # print(f"{color} played PLACE action: {c1}, {c2}, {c3}, {c4}")

