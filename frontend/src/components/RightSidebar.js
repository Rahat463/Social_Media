import * as React from "react";
import { styled, useTheme } from "@mui/material/styles";
import Box from "@mui/material/Box";
import Drawer from "@mui/material/Drawer";
import List from "@mui/material/List";
import Divider from "@mui/material/Divider";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemText from "@mui/material/ListItemText";
import { Link } from "react-router-dom";

//start

const drawerWidth = 420;

const DrawerHeader = styled("div")(({ theme }) => ({
  display: "flex",
  alignItems: "center",
  padding: theme.spacing(0, 1),
  // necessary for content to be below app bar
  ...theme.mixins.toolbar,
  justifyContent: "flex-end",
}));

export default function RightSidebar() {
  
  const linksRight = {
    RightItem1: "/right-item-1",
    RightItem2: "/right-item-2",
  };

  return (
    <Box sx={{ display: "flex" }}>
   {/* Right sidebar Start */}
   <Drawer
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          "& .MuiDrawer-paper": {
            width: drawerWidth,
            boxSizing: "border-box",
          },
        }}
        variant="persistent"
        anchor="right"
        open={true} // Set this to true to make the right sidebar always open
      >
        <DrawerHeader>
          {/* You can add a close button if needed */}
        </DrawerHeader>
        <Divider />
        <List>
          {Object.entries(linksRight).map(([text, url]) => (
            <ListItem key={text} disablePadding>
              <Link
                to={url}
                style={{ textDecoration: "none", color: "inherit" }}
              >
                <ListItemButton>
                  <ListItemText primary={text} />
                </ListItemButton>
              </Link>
            </ListItem>
          ))}
        </List>
      </Drawer>
      {/* Right Sidebar End */}
    </Box>
  );
}

