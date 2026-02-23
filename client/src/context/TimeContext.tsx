import { createContext, useContext, useState, useCallback } from "react";

const TimeContext = createContext(null);

export function TimeProvider({ children }) {
  const [t, setT] = useState(0);          // continuous time
  const [episode, setEpisode] = useState(0); // discrete episode index

  const advance = useCallback(() => {
    setT(prev => prev + 0.1);
    setEpisode(prev => prev + 1);
  }, []);

  const reset = useCallback(() => {
    setT(0);
    setEpisode(0);
  }, []);

  return (
    <TimeContext.Provider value={{ t, episode, setT, setEpisode, advance, reset }}>
      {children}
    </TimeContext.Provider>
  );
}

export function useTime() {
  const ctx = useContext(TimeContext);
  if (!ctx) {
    throw new Error("useTime must be used inside a TimeProvider");
  }
  return ctx;
}