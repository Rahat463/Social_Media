import * as React from "react";
import * as ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import "./index.css";
import Root from "./routes/root";
import SignIn from "./routes/SignIn";
import PersistentDrawerLeft from "./routes/PersistentDrawerLeft";
import SimpleContainer from "./components/container";

import { loader as rootLoader } from "./routes/root";
import ImgMediaCard from "./components/FriendReq";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
  },
  {
    path: "/routes/SignIn",
    element: <SignIn />,
  },
  {
    path: "/routes/PersistentDrawerLeft",
    element: <PersistentDrawerLeft />,
  },
]);

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);
