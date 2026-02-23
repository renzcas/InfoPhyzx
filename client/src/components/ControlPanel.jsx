import { useState } from "react";
import { useTime } from "../context/TimeContext";

export default function ControlPanel() {
  const { advance, reset, episode, setEpisode } = useTime();

  const [steps, setSteps] = useState(10);
  const [surgeryNode, setSurgeryNode] = useState("");
  const [surgeryType, setSurgeryType] = useState("split");

  // Trigger a batch run
  const runBatch = () => {
    setEpisode(episode + steps);
  };

  // Trigger a surgery event by posting to backend
  const triggerSurgery = () => {
    fetch("/api/cosmos/run_with_surgery", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        steps: episode + 1,
        surgery_events: [
          {
            t: episode,
            event: {
              type: surgeryType,
              node: surgeryNode
            }
          }
        ]
      })
    })
      .then(res => res.json())
      .then(() => {
        // After surgery, advance one episode
        advance();
      });
  };

  return (
    <div style={{ padding: "20px", color: "#eee" }}>
      <h2>Control Panel</h2>

      <section style={{ marginTop: "20px" }}>
        <button onClick={advance} style={{ marginRight: "10px" }}>
          Advance Episode
        </button>
        <button onClick={reset}>Reset Universe</button>
      </section>

      <section style={{ marginTop: "20px" }}>
        <h3>Run Batch</h3>
        <input
          type="number"
          value={steps}
          onChange={e => setSteps(parseInt(e.target.value))}
          style={{ width: "80px", marginRight: "10px" }}
        />
        <button onClick={runBatch}>Run</button>
      </section>

      <section style={{ marginTop: "20px" }}>
        <h3>Surgery Event</h3>

        <label>Type:</label>
        <select
          value={surgeryType}
          onChange={e => setSurgeryType(e.target.value)}
          style={{ marginLeft: "10px", marginRight: "20px" }}
        >
          <option value="split">Split Node</option>
          <option value="merge">Merge Nodes</option>
          <option value="collapse_edge">Collapse Edge</option>
          <option value="birth">Birth Node</option>
          <option value="death">Death Node</option>
        </select>

        <label>Node:</label>
        <input
          type="text"
          value={surgeryNode}
          onChange={e => setSurgeryNode(e.target.value)}
          style={{ marginLeft: "10px", marginRight: "10px" }}
        />

        <button onClick={triggerSurgery}>Trigger</button>
      </section>
    </div>
  );
}