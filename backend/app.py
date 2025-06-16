from flask import Flask, request, jsonify
from flask_cors import CORS
from program import Agent, GameState
from game import PlayerColor, PlaceAction, Coord
import os

app = Flask(__name__)
CORS(app)  # Allow React frontend to access backend

# Global game and agent state
game_state = None
agent = None

@app.route("/start_game", methods=["POST"])
def start_game():
    global game_state, agent

    data = request.get_json()
    iterations = data.get("iterations", 1)
    agent = Agent(PlayerColor.BLUE, iterations)
    game_state = agent.game_state

    return jsonify({"board": serialize_board(game_state)})

@app.route("/human_move", methods=["POST"])
def human_move():
    global game_state, agent

    data = request.get_json()
    coords = data.get("coords", [])

    if len(coords) != 4:
        return jsonify({"error": "Exactly 4 coordinates required."}), 400

    try:
        coord_objs = [Coord(coord["row"], coord["col"]) for coord in coords]
        action = PlaceAction(*coord_objs)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
    # Check for overlap before applying move
    for coord in coord_objs:
        if game_state.get(coord) is not None:
            return jsonify({"error": "Invalid move: cell already occupied."}), 400
        
    # Adjacency check unless it's the first move
    red_exists = any(color == PlayerColor.RED for color in game_state.values())
    if red_exists:
        if not any(is_adjacent_to_red(coord, game_state) for coord in coord_objs):
            return jsonify({"error": "Move must be adjacent to an existing red piece."}), 400

    # Apply human move only
    agent.update(PlayerColor.RED, action)
    game_state = agent.game_state

    current_state = GameState(board=game_state, current_player=PlayerColor.RED)
    if current_state.has_won(PlayerColor.RED):
        serialized_board = serialize_board(game_state)
        print("Human has won")
        return jsonify({
            "board": serialized_board,
            "winner": "Human (Red)"
        })


    # Print and return updated board
    serialized_board = serialize_board(game_state)

    return jsonify({"board": serialized_board})

@app.route("/agent_move", methods=["POST"])
def agent_move():
    global agent, game_state

    ai_action = agent.action()
    agent.update(PlayerColor.BLUE, ai_action)
    game_state = agent.game_state

    current_state = GameState(board=game_state, current_player=PlayerColor.BLUE)
    if current_state.has_won(PlayerColor.RED):
        serialized_board = serialize_board(game_state)
        print("Agent has won")
        return jsonify({
            "board": serialized_board,
            "winner": "Agent (Blue)"
        })
    
    serialized_board = serialize_board(game_state)

    return jsonify({"board": serialize_board(game_state)})


def serialize_board(board_dict):
    grid = [[None for _ in range(11)] for _ in range(11)]
    for coord, color in board_dict.items():
        if color == PlayerColor.RED:
            grid[coord.r][coord.c] = "R"
        elif color == PlayerColor.BLUE:
            grid[coord.r][coord.c] = "B"
    return grid

def is_adjacent_to_red(coord: Coord, board):
    directions = [coord.up(), coord.left(), coord.right(), coord.down()]
    # for r, c in directions:
        # neighbor = Coord((coord.r + r) % 11, (coord.c + c) % 11)  # wrap around
    for neighbor in directions:
        if board.get(neighbor) == PlayerColor.RED:
            return True
    return False

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(debug=False, host="0.0.0.0", port=port)
