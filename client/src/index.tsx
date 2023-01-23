import React from "react";
import ReactDOM from "react-dom/client";
import { transitions, positions, Provider as AlertProvider } from "react-alert";
import AlertTemplate from "components/AlertTemplate";

import App from "./App";

// optional configuration
const options = {
  position: positions.TOP_RIGHT,
  timeout: 2000,
  transition: transitions.FADE,
};

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <AlertProvider template={AlertTemplate} {...options}>
      <App />
    </AlertProvider>
  </React.StrictMode>,
);
