import React from "react";
import ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { transitions, positions, Provider as AlertProvider } from "react-alert";
import AlertTemplate from "components/AlertTemplate";

import "./index.scss";

// Importing the Bootstrap CSS
import "bootstrap/dist/css/bootstrap.min.css";

import Layout from "./layouts/layout";
import Index from "./routes/index";
import ErrorPage from "./error-page";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Layout />,
    errorElement: <ErrorPage />,
    children: [
      {
        index: true,
        element: <Index />,
      },
      // {
      //   path: "contacts/:contactId",
      //   element: <Contact />,
      // },
    ],
  },
]);

// optional configuration
const options = {
  position: positions.TOP_RIGHT,
  timeout: 2000,
  transition: transitions.FADE,
};

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <AlertProvider template={AlertTemplate} {...options}>
      <RouterProvider router={router} />
    </AlertProvider>
  </React.StrictMode>
);
