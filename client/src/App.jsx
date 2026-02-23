import React from "react";
import { TimeProvider } from "./context/TimeContext";

import ControlPanel from "./components/ControlPanel";
import MathUniversePanel from "./components/MathUniversePanel";
import CosmosGraphPanel from "./components/CosmosGraphPanel";

export default function App() {
  return (
    <TimeProvider>
      <div style={{
        display: "grid",
        gridTemplateColumns: "1fr 1fr",
        gridTemplateRows: "auto auto",
        gap: "20px",
        padding: "20px",
        background: "#000",
        minHeight: "100vh",
        color: "#eee"
      }}>
        
        {/* Top-left: Controls */}
        <div style={{ border: "1px solid #333", padding: "20px" }}>
          <ControlPanel />
        </div>

        {/* Top-right: Math Universe */}
        <div style={{ border: "1px solid #333", padding: "20px" }}>
          <MathUniversePanel />
        </div>

        {/* Bottom: Cosmos Graph */}
        <div style={{
          gridColumn: "1 / span 2",
          border: "1px solid #333",
          padding: "20px"
        }}>
          <CosmosGraphPanel />
        </div>

      </div>
    </TimeProvider>
  );
}