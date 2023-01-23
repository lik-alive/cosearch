import { createBrowserRouter, RouterProvider } from "react-router-dom";

import Layout from "./layouts/Layout";
import Index from "./routes/Index";
import Login from "./routes/Login";
import Scopus from "./routes/Scopus";
import ErrorPage from "./ErrorPage";

export default function Routes() {
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
        {
          path: "scopus",
          element: <Scopus />,
        },
      ],
    },
    {
      path: "/login",
      element: <Login />,
      errorElement: <ErrorPage />,
    },
  ]);

  return <RouterProvider router={router} />;
}
