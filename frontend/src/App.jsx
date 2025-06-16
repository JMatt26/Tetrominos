import { useState } from "react";
import GameBoard from "./GameBoard";
import { startGame, sendHumanMove, sendAgentMove } from "./api";
import { SHAPES } from "./constants";

function App() {
  const [board, setBoard] = useState(Array(11).fill(Array(11).fill(null)));
  const [selectedShape, setSelectedShape] = useState("I");
  const [rotation, setRotation] = useState(0);
  const [agentThinking, setAgentThinking] = useState(false);
  const [iterations, setIterations] = useState(1);


  const handleStart = async () => {
    const res = await startGame(iterations);
    setBoard(res.board);
  };

  const handleCellClick = async (baseRow, baseCol) => {
    if (agentThinking) return;

    const relativeCoords = SHAPES[selectedShape][rotation];
    const coords = relativeCoords.map(({ r, c }) => ({
      row: (baseRow + r) % 11,
      col: (baseCol + c) % 11,
    }));
  
    try {
      const res = await sendHumanMove(coords);
  
      // Force React to re-render by making a deep copy of the board
      const newBoard = res.board.map(row => [...row]);
      console.log("Board received from backend:", res.board);
      setBoard(newBoard);

      if (res.winner === "Human (Red)") {
        alert("You Win!");
        return;
      }

      setAgentThinking(true);
      console.log("Agent is thinking...");
      const agentRes = await sendAgentMove();
      const updatedBoard = agentRes.board.map(row => [...row]);
      console.log("Board received from backend:", agentRes.board);
      setBoard(updatedBoard);

      if (res.winner === "Agent (Blue)") {
        alert("Agent Wins!");
        return;
      }
    } catch (err) {
      console.error("Move failed", err);
    } finally {
      setAgentThinking(false);
      console.log("Agent move completed");
    }
  };

  return (
    <div style={{ textAlign: "center", color: "white", background: "#111", minHeight: "100vh" }}>
      <h1>Tetress: Human vs Agent</h1>
      <div>
        <label>Iterations (1-20): </label>
        <select value={iterations} onChange={(e) => setIterations(Number(e.target.value))}>
          {Array.from({ length: 20 }, (_, i) => i + 1).map(val => (
            <option key={val} value={val}>{val}</option>
          ))}
        </select>
        <p style={{ fontSize: "0.9rem", color: "#ccc", marginTop: 4 }}>
          More iterations = smarter AI but slower performance. (Select once before start of game)
        </p>
      </div>
      <button onClick={handleStart}>Start Game</button>
      <div style={{ marginTop: 10 }}>
        <label>Select Shape: </label>
        <select value={selectedShape} onChange={(e) => { setSelectedShape(e.target.value); setRotation(0); }}>
          {Object.keys(SHAPES).map(shape => (
            <option key={shape} value={shape}>{shape}</option>
          ))}
        </select>
        <button onClick={() => setRotation((rotation + 1) % SHAPES[selectedShape].length)}>Rotate</button>
      </div>
      <GameBoard
        board={board}
        onCellClick={handleCellClick}
        selectedShape={selectedShape}
        rotation={rotation}
      />
      {agentThinking && (
        <div style={{ marginTop: 10, fontStyle: "italic", color: "lightgray" }}>
          Agent is making a move...
        </div>
      )}
    </div>
  );
}

export default App;
