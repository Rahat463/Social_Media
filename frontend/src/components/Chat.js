import * as React from "react";
import { styled, useTheme } from "@mui/material/styles";
import Box from "@mui/material/Box";
import ChatCard from "../components/ChatCard";
import axios from "axios";
import Button from "@mui/material/Button";
import Grid from "@mui/material/Grid";
import TextField from "@mui/material/TextField";
import SendIcon from "@mui/icons-material/Send";

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

export default function Chat({open, setCurrentComponent, friend_id, setUpdatePostId}) {
  console.log(friend_id)
  const fetched_user_id = localStorage.getItem("user_id");
  const request_data = {user_id:fetched_user_id, friend_id:friend_id};
  const [data, setData] = React.useState([]);
  const [isLoading, setIsLoading] = React.useState(true);
  const [description, setDescription] = React.useState("");
  const [media, setMedia] = React.useState(null);
 
  React.useEffect(() => {
    
    const response = axios
      .post("http://localhost:8000/api/get_messages/", request_data, {
        headers: {
          "Content-Type": "application/json",
        },
      }).then (response => {
        setData(response.data);
        setIsLoading(false);
        console.log(response.data)
      })
  }, []);

  const handleInputChange = (event) => {
    const input = event.target.value;
    setDescription(input);
  }

  const handleMediaChange = (e) => {
    const file = e.target.files[0];
    setMedia(file);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    try{
      const user_id = localStorage.getItem('user_id')
      const request_data = new FormData();
      request_data.append("description", description);
      request_data.append("user_id", user_id);
      request_data.append("friend_id", friend_id);
      request_data.append("media", media);
      // request_data.append("cover_photo", coverPhoto);
      const response = await axios
        .post("http://localhost:8000/api/set_message/", request_data, {
          headers: {
            "Content-Type": "multipart/form-data",
            // "X-CSRFToken": csrfToken,
          },
        })
        if ('error' in response.data){console.log(response.data.error);}
        // else {navigate("/routes/SignIn");}
      } catch (error) {console.log(error);}
    };

  return (
    <Box sx={{ display: "flex" }}>
      <Main open={open}>
        <DrawerHeader />
        {isLoading ? (
          <></>
        ) : (
          data.map((messageData, index) => (
            <ChatCard key={index} messageData={messageData} open={open} setCurrentComponent = {setCurrentComponent} setUpdatePostId={setUpdatePostId}/>
          ))
        )}
        <Grid  container direction="row" justifyContent="center" alignItems="stretch">
          <Grid item xs={12}>
            <TextField
              id="outlined-multiline-flexible"
              label="Multiline"
              multiline
              maxRows={4}
              fullWidth
              onChange={handleInputChange}
            />
          </Grid>
          <Grid item xs={8}>
          <input
                  type="file"
                  accept="image/*"
                  onChange={handleMediaChange}
                  style={{ marginBottom: "10px" }}
                />
          </Grid>
          <Grid item xs={4} >
            <Button variant="contained" endIcon={<SendIcon />} style={{ height: '100%' }} onClick={handleSubmit}>
              Send
            </Button>
          </Grid>
        </Grid>
        <Grid item xs={12}>
        {media && (
                  <div>
                    <img
                      src={URL.createObjectURL(media)}
                      alt="Selected"
                      // {...URL.createObjectURL(profilePic)}
                      style={{ maxWidth: "100%", marginBottom: "10px" }}
                    />
                  </div>
                )}
        </Grid>
      </Main>
    </Box>
  );
};
