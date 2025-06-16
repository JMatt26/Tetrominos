import { useState } from "react";
import { SHAPES } from "./constants";

const CELL_SIZE = 50;
const ROWS = 11;
const COLS = 11;

function GameBoard({ board, onCellClick, selectedShape, rotation }) {
  const [hoverCell, setHoverCell] = useState(null);

  const getHoveredCoords = () => {
    if (!hoverCell) return [];
    const shape = SHAPES[selectedShape][rotation];
    return shape.map(({ r, c }) => ({
      row: (hoverCell.row + r) % ROWS,
      col: (hoverCell.col + c) % COLS,
    }));
  };

  const isHovered = (r, c) => {
    return getHoveredCoords().some(coord => coord.row === r && coord.col === c);
  };

  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: `repeat(${COLS}, ${CELL_SIZE}px)`,
        justifyContent: "center",
        marginTop: 20,
      }}
    >
      {board.flatMap((row, rIdx) =>
        row.map((cell, cIdx) => {
          const hovered = isHovered(rIdx, cIdx);
          return (
            <div
              key={`${rIdx}-${cIdx}`}
              onClick={() => onCellClick(rIdx, cIdx)}
              onMouseEnter={() => setHoverCell({ row: rIdx, col: cIdx })}
              onMouseLeave={() => setHoverCell(null)}
              style={{
                width: CELL_SIZE,
                height: CELL_SIZE,
                backgroundColor: cell === "R"
                  ? "red"
                  : cell === "B"
                  ? "blue"
                  : hovered
                  ? "#888" // preview color
                  : "#333",
                border: "1px solid #555",
                cursor: "pointer",
              }}
            />
          );
        })
      )}
    </div>
  );
}

export default GameBoard;
