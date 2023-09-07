import * as React from "react";
import { styled, useTheme } from "@mui/material/styles";
import Box from "@mui/material/Box";
import Post from "./Post";
import axios from "axios";
import Button from "@mui/material/Button";
import EventCard from "./EventCard";
import DeleteIcon from "@mui/icons-material/Delete";
import SendIcon from "@mui/icons-material/Send";
import Stack from "@mui/material/Stack";

const drawerWidth = 240;

const Main = styled("main", { shouldForwardProp: (prop) => prop !== "open" })(
  ({ theme, open }) => ({
    flexGrow: 1,
    padding: theme.spacing(3),
    transition: theme.transitions.create("margin", {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
    marginLeft: `-${drawerWidth}px`,
    ...(open && {
      transition: theme.transitions.create("margin", {
        easing: theme.transitions.easing.easeOut,
        duration: theme.transitions.duration.enteringScreen,
      }),
      marginLeft: 0,
    }),
  })
);

const DrawerHeader = styled("div")(({ theme }) => ({
  display: "flex",
  alignItems: "center",
  padding: theme.spacing(0, 1),
  // necessary for content to be below app bar
  ...theme.mixins.toolbar,
  justifyContent: "flex-end",
}));

export default function Events({ open, setCurrentComponent }) {
  const fetched_user_id = localStorage.getItem("user_id");
  const request_data = { user_id: fetched_user_id };
  const [data, setData] = React.useState([]);
  const [isLoading, setIsLoading] = React.useState(true);
  React.useEffect(() => {
    const response = axios
      .post("http://localhost:8000/api/get_events/", request_data, {
        headers: {
          "Content-Type": "application/json",
        },
      })
      .then((response) => {
        setData(response.data);
        setIsLoading(false);
      });
  }, []);
  const handleButtonClick = () => {
    setCurrentComponent("createevent");
  };

  return (
    <Box sx={{ position: "relative", display: "flex" }}>
      <Button
        variant="contained"
        endIcon={<SendIcon />}
        style={{
          position: "fixed",
          bottom: "16px", // Adjust this value as needed
          right: "430px", // Adjust this value as needed
          zIndex: 100,
        }}
        onClick={handleButtonClick}
      >
        Send
      </Button>
      <Main open={open}>
        <DrawerHeader />
        {isLoading ? (
          <></>
        ) : (
          data.map((postData, index) => (
            <EventCard key={index} postData={postData} />
          ))
        )}
        <div className="dropdown">
          <button
            className="btn btn-secondary dropdown-toggle"
            type="button"
            data-bs-toggle="dropdown"
            aria-expanded="false"
          >
            Dropdown button
          </button>
          <ul className="dropdown-menu">
            <li>
              <a className="dropdown-item" href="#">
                Action
              </a>
            </li>
            <li>
              <a className="dropdown-item" href="#">
                Another action
              </a>
            </li>
            <li>
              <a className="dropdown-item" href="#">
                Something else here
              </a>
            </li>
          </ul>
        </div>
      </Main>
    </Box>
  );
}
