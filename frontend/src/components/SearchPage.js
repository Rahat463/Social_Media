import * as React from "react";
import { styled, useTheme } from "@mui/material/styles";
import Box from "@mui/material/Box";
import SearchCard from "../components/SearchCard";
import axios from "axios";
import Button from "@mui/material/Button";


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

export default function SearchPage({open, setCurrentComponent, searchData}) {

  return (
    <Box sx={{ display: "flex" }}>
      <Main open={open}>
        <DrawerHeader />
        {/* {isLoading ? (
          <></>
        ) : ( */}
          {searchData.map((postData, index) => (
            <SearchCard key={index} postData={postData} />
          ))}
        {/* )} */}
      </Main>
    </Box>
  );
};
