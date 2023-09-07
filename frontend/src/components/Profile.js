import * as React from "react";
import { styled, useTheme } from "@mui/material/styles";
import Box from "@mui/material/Box";
import ProfileCard from "../components/ProfileCard";
import Post from "../components/Post";
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

export default function Profile({open, setCurrentComponent, profileId}) {
  const fetched_user_id = localStorage.getItem("user_id");
  const request_data = {user_id:fetched_user_id};
  const [data, setData] = React.useState([]);
  const [profilePosts, setProfilePosts] = React.useState([]);
  const [isLoading, setIsLoading] = React.useState(true);
  const buttonStyle = {
    width: '400px',  // Adjust the width as needed
    height: '50px', // Adjust the height as needed
  };

  React.useEffect(() => {
    
    axios
      .post("http://localhost:8000/api/get_user_profile/", request_data, {
        headers: {
          "Content-Type": "application/json",
        },
      }).then (response => {
        setData(response.data);
        setIsLoading(false);
      })
  }, []);

  React.useEffect(() => {
    
    axios
      .post("http://localhost:8000/api/home/", request_data, {
        headers: {
          "Content-Type": "application/json",
        },
      }).then (response => {
        setProfilePosts(response.data);
        setIsLoading(false);
      })
  }, []);

  return (
    <Box sx={{ display: "flex" }}>
      <Main open={open}>
        <DrawerHeader />
        {isLoading ? (
          <></>
        ) : 
            (
              <>
              {/* <ProfileCard postData={data} /> */}
              {
                profilePosts.map((postData, index) => (
                  <Post key={index} postData={postData} />
                ))
              }
              </>
            
            
            )
        }
      </Main>
    </Box>
  );
};







// import React from 'react';
// import { Avatar, Card, CardContent, CardHeader, Typography } from '@mui/material';
// import axios from "axios";
// import { styled, useTheme } from "@mui/material/styles";

// const drawerWidth = 240;

// const Main = styled("main", { shouldForwardProp: (prop) => prop !== "open" })(
//   ({ theme, open }) => ({
//     flexGrow: 1,
//     padding: theme.spacing(3),
//     transition: theme.transitions.create("margin", {
//       easing: theme.transitions.easing.sharp,
//       duration: theme.transitions.duration.leavingScreen,
//     }),
//     marginLeft: `-${drawerWidth}px`,
//     ...(open && {
//       transition: theme.transitions.create("margin", {
//         easing: theme.transitions.easing.easeOut,
//         duration: theme.transitions.duration.enteringScreen,
//       }),
//       marginLeft: 0,
//     }),
//   })
// );

// const DrawerHeader = styled("div")(({ theme }) => ({
//   display: "flex",
//   alignItems: "center",
//   padding: theme.spacing(0, 1),
//   // necessary for content to be below app bar
//   ...theme.mixins.toolbar,
//   justifyContent: "flex-end",
// }));

// export default function UserProfile ({ open, setCurrentComponent }) {

//   const fetched_user_id = localStorage.getItem("user_id");
//   const request_data = { user_id: fetched_user_id, group_type: "page" };
//   const [data, setData] = React.useState([]);
//   const [isLoading, setIsLoading] = React.useState(true);
//   React.useEffect(() => {
//     axios
//       .post("http://localhost:8000/api/get_user_profile/", request_data, {
//         headers: {
//           "Content-Type": "application/json",
//         },
//       })
//       .then((response) => {
//         setData(response.data);
//         console.log(response.data.profile_pic[0])
//         setIsLoading(false);
//       });
//   }, []);

//   return (
//     <Card>
//       <Main open={open}>
//         <DrawerHeader />
//         <CardHeader
//         avatar={<Avatar aria-label="post">
//         <img
//           src={data.profile_pic}
//           alt="R"
//           style={{ width: "100%", height: "100%", objectFit: "cover" }}
//         ></img>
//       </Avatar>}
//         title={data.user_name}
//         subheader={`Friends: ${data.friend_count}`}
//       />
//       <img src={data.cover_photo} alt="Cover" style={{ width: '100%', maxHeight: '400px' }} />
//       <CardContent>
//         <Typography variant="body1">Additional profile information goes here.</Typography>
//       </CardContent>
//       </Main>
      
//     </Card>
//   );
// };



