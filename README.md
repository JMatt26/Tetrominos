# Tetromino
## Human vs AI Tetris

### 📚 Table of Contents
- [Project Description](#project-description)
- [Game Rules](#game-rules)
- [How It Works](#how-it-works)
  - [Frontend (React)](#frontend-react)
  - [Backend (Flask)](#backend-flask)
  - [Agent: Monte Carlo Tree Search](#agent-monte-carlo-tree-search)
- [Running with Docker](#running-with-docker)
- [Running Locally (Without Docker)](#running-locally-without-docker)
  - [Backend (Python 312)](#backend-python-312)
  - [Frontend (React)](#frontend-react-1)
- [Future Work](#future-work)
  - [UI Improvements](#ui-improvements)
  - [Agent Enhancements](#agent-enhancements)
- [Disclaimer](#disclaimer)

## Project Description

Tetromino is a two-player adverserial game that is a derivative of the wildly loved game, Tetris. 

Players take turns placing tetris-like pieces on an 11x11 board. This project pits a human player against an AI agent powered by **Monte Carlo Tree Search (MCTS)**. The AI strategically evaluates possible placements by simulating future game states and selecting actions that yield the most promising outcomes based on statistical rollout results.

The project is composed of:
- A Python backend using Flask that manages the game logic and serves API endpoints.
- A React frontend that allows users to interactively play the game.
- A game-playing agent that uses adversarial search (MCTS) to decide moves.
- A Dockerized setup for easy deployment and local testing.

## Game Rules
- First move can be placed anywhere.
- Subsequent moves must be made adjacent to an already placed piece of your colour.
- If a line is full, regardless of the colours comprising it, it is cleared.
- If no more moves can be made on the board, the last player to place a piece is deemed the winner.

## How It Works

### Frontend (React)

- Interactive 11x11 game grid.
- Players can:
  - Select the strength of the AI opponent from a dropdown.
  - Select a tetromino shape from a dropdown.
  - Rotate the shape.
  - Hover over the board to preview placement (includes board wrapping).
  - Click to place the shape and trigger the AI’s response.
- Real-time updates after each human and agent move.

### Backend (Flask)

- Exposes two primary routes:
  - `POST /start_game`: Initializes a new game and empty board.
  - `POST /human_move`: Receives a shape placement from the human, applies it, runs the MCTS agent, and returns the updated board.
- Maintains the game state, validates moves, clears lines, and checks for win conditions.

### Agent: Monte Carlo Tree Search

- The agent implements MCTS for decision-making:
  1. **Selection**: Traverse the tree to find a node with unexplored moves.
  2. **Expansion**: Add new nodes for unexplored valid actions.
  3. **Simulation**: Run heuristic-guided playouts to the end or a fixed depth.
  4. **Backpropagation**: Propagate the simulation results up the tree to inform earlier choices.
- The agent prioritizes moves that maximize future line-clearing potential while balancing exploration and exploitation.

## Running with Docker

### Prerequisites

- Docker installed
- Docker Compose installed

### Steps

```bash
git clone https://github.com/JMatt26/Tetrominos.git
cd Tetrominos
docker-compose up --build
```

Then open your browser at:
```
http://localhost:3000
```

## Running Locally (Without Docker)

### Backend (Python 3.12)

```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend (React)

```bash
cd frontend
npm install
npm start
```

- Ensure that the Flask backend is running on `http://localhost:5001` (as configured in `api.js`).
- The React app should be accessible at `http://localhost:3000`.

## Future Work

### UI Improvements

- Add a move history sidebar for analysis.
- Overall UX improvements

### Agent Enhancements

- Replace heuristic playouts with a neural network:
  - Train a lightweight policy model offline to predict promising moves.
  - Use supervised or reinforcement learning with self-play data.
- Add parallelized simulations to increase strength under time constraints.

## Disclaimer

All files under backend/game belong to the University of Melbourne's COMP30024 Artificial Intelligence course.
