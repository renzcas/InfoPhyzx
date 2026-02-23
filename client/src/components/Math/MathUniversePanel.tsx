import { useEffect, useState } from "react";
import { useTime } from "../context/TimeContext";

export default function MathUniversePanel() {
  const { t } = useTime();

  const [primes, setPrimes] = useState({});
  const [hilbert, setHilbert] = useState({ field: [], energy: 0 });
  const [riemann, setRiemann] = useState({ field: [], energy: 0 });

  // Fetch prime pulses
  useEffect(() => {
    fetch("/api/math/primes", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ t, N: 50 })
    })
      .then(res => res.json())
      .then(data => setPrimes(data.pulses || {}));
  }, [t]);

  // Fetch Hilbert modes
  useEffect(() => {
    fetch("/api/math/hilbert", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ t, N: 50 })
    })
      .then(res => res.json())
      .then(data => setHilbert({ field: data.field || [], energy: data.energy || 0 }));
  }, [t]);

  // Fetch Riemann modes
  useEffect(() => {
    fetch("/api/math/riemann", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ t, L: 200 })
    })
      .then(res => res.json())
      .then(data => setRiemann({ field: data.field || [], energy: data.energy || 0 }));
  }, [t]);

  return (
    <div style={{ padding: "20px", color: "#eee" }}>
      <h2>Math Universe Panel</h2>
      <p>t = {t.toFixed(2)}</p>

      <section style={{ marginTop: "20px" }}>
        <h3>Prime Pulses</h3>
        <pre style={{ background: "#111", padding: "10px" }}>
          {JSON.stringify(primes, null, 2)}
        </pre>
      </section>

      <section style={{ marginTop: "20px" }}>
        <h3>Hilbert Modes</h3>
        <p>Energy: {hilbert.energy.toFixed(4)}</p>
        <pre style={{ background: "#111", padding: "10px" }}>
          {JSON.stringify(hilbert.field.slice(0, 20), null, 2)}...
        </pre>
      </section>

      <section style={{ marginTop: "20px" }}>
        <h3>Riemann Spectral Modes</h3>
        <p>Energy: {riemann.energy.toFixed(4)}</p>
        <pre style={{ background: "#111", padding: "10px" }}>
          {JSON.stringify(riemann.field.slice(0, 20), null, 2)}...
        </pre>
      </section>
    </div>
  );
}