import * as React from "react";
import { styled, useTheme } from "@mui/material/styles";
import Box from "@mui/material/Box";
import Grid from "@mui/material/Grid";
import SendIcon from "@mui/icons-material/Send";
import TextField from "@mui/material/TextField";
import CommentCard from "../components/CommentCard";
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

export default function Comments({ open, setCurrentComponent, post_id }) {
  const [data, setData] = React.useState([]);
  const [isLoading, setIsLoading] = React.useState(true);
  const [description, setDescription] = React.useState("");
  const [media, setMedia] = React.useState(null);
  const buttonStyle = {
    width: "400px", // Adjust the width as needed
    height: "50px", // Adjust the height as needed
  };

  React.useEffect(() => {
    const response = axios
      .post(
        "http://localhost:8000/api/get_comment_info/",
        { post_id: post_id },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      )
      .then((response) => {
        setData(response.data);
        console.log(response.data);
        setIsLoading(false);
      });
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
      request_data.append("post_id", post_id);
      request_data.append("media", media);
      // request_data.append("cover_photo", coverPhoto);
      const response = await axios
        .post("http://localhost:8000/api/set_post_comment/", request_data, {
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
      {/* <Main open={open}> */}
      <DrawerHeader />
      <Grid >
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
        <Grid item xs={12}>
          {isLoading ? (
            <></>
          ) : (
            data.map((postData, index) => (
              <CommentCard
                key={index}
                commentData={postData}
                open={open}
                setCurrentComponent={setCurrentComponent}
              />
            ))
          )}
        </Grid>
      </Grid>
      {/* </Main> */}
    </Box>
  );
}
