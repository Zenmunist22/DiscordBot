import React from "react";
import * as ReactDOM from "react-dom/client";
import App from "./App.tsx";
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import Login from "./Login.tsx";
import Register from "./Register.tsx";


const router = createBrowserRouter([
  {
    path: "/",
    element: <App></App>,
    children: [
      {
        path: "/login/",
        element: <Login/>
      },
      {
        path: "/register/",
        element: <Register/>
      }
    ]
  },
]);

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <RouterProvider router = {router}>
      
    </RouterProvider>
  </React.StrictMode>
);
