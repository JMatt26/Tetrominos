import axios from "axios";
const API = axios.create({ baseURL: process.env.REACT_APP_API_URL });

export const startGame = async (iterations) => {
  const res = await API.post("/start_game", {iterations});
  console.log(process.env.REACT_APP_API_URL)
  return res.data;
};

export const sendHumanMove = async (coords) => {
  const res = await API.post("/human_move", { coords });
  return res.data;
};

export const sendAgentMove = async () => {
    const res = await API.post("/agent_move");
    return res.data;
  };
