import { useEffect, useState } from "react";
import { useTime } from "../context/TimeContext";

export default function CosmosGraphPanel() {
  const { episode } = useTime();

  const [graph, setGraph] = useState({ nodes: [], edges: {} });
  const [curvature, setCurvature] = useState({});
  const [entropy, setEntropy] = useState({});

  // Fetch cosmos state whenever episode changes
  useEffect(() => {
    fetch("/api/cosmos/run", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ steps: episode })
    })
      .then(res => res.json())
      .then(data => {
        const state = data.state || {};
        setGraph(state.graph || { nodes: [], edges: {} });

        // Fetch curvature
        fetch("/api/math/curvature", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ graph: state.graph })
        })
          .then(res => res.json())
          .then(data => setCurvature(data.curvature || {}));

        // Fetch entropy
        fetch("/api/math/entropy", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ graph: state.graph })
        })
          .then(res => res.json())
          .then(data => setEntropy(data.entropy || {}));
      });
  }, [episode]);

  return (
    <div style={{ padding: "20px", color: "#eee" }}>
      <h2>Cosmos Graph Panel</h2>
      <p>Episode = {episode}</p>

      <section style={{ marginTop: "20px" }}>
        <h3>Nodes</h3>
        <pre style={{ background: "#111", padding: "10px" }}>
          {JSON.stringify(graph.nodes, null, 2)}
        </pre>
      </section>

      <section style={{ marginTop: "20px" }}>
        <h3>Edges</h3>
        <pre style={{ background: "#111", padding: "10px" }}>
          {JSON.stringify(graph.edges, null, 2)}
        </pre>
      </section>

      <section style={{ marginTop: "20px" }}>
        <h3>Curvature</h3>
        <pre style={{ background: "#111", padding: "10px" }}>
          {JSON.stringify(curvature, null, 2)}
        </pre>
      </section>

      <section style={{ marginTop: "20px" }}>
        <h3>Entropy</h3>
        <pre style={{ background: "#111", padding: "10px" }}>
          {JSON.stringify(entropy, null, 2)}
        </pre>
      </section>
    </div>
  );
}