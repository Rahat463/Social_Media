import * as React from "react";
import { styled, useTheme } from "@mui/material/styles";
import Box from "@mui/material/Box";
import Post from "./Post";
import axios from "axios";
import Button from "@mui/material/Button";
import FriendReqCard from "./FriendReqCard";

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

export default function FriendReq({open, setCurrentComponent}) {
  const fetched_user_id = localStorage.getItem("user_id");
  const request_data = {user_id:fetched_user_id};
  const [data, setData] = React.useState([]);
  const [isLoading, setIsLoading] = React.useState(true);
  React.useEffect(() => {
    
    const response = axios
      .post("http://localhost:8000/api/get_friend_req_list/", request_data, {
        headers: {
          "Content-Type": "application/json",
        },
      }).then (response => {
        setData(response.data);
        setIsLoading(false);
      })
  }, []);

  return (
    <Box sx={{ display: "flex" }}>
      <Main open={open}>
        <DrawerHeader />
        {isLoading ? (
          <></>
        ) : (
          data.map((postData, index) => (
            <FriendReqCard key={index} postData={postData} />
          ))
        )}
      </Main>
    </Box>
  );
};
