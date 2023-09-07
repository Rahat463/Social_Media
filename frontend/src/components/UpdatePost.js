import { useState } from "react";
import * as React from "react";
import Avatar from "@mui/material/Avatar";
import CssBaseline from "@mui/material/CssBaseline";
import TextField from "@mui/material/TextField";
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import LockOutlinedIcon from "@mui/icons-material/LockOutlined";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import axios from "axios";
import { styled, useTheme } from "@mui/material/styles";
import Button from "@mui/material/Button";


const defaultTheme = createTheme();

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

export default function UpdatePost({open, setCurrentComponent, post_id}) {
  const [media, setMedia] = useState(null);

  const handleMediaChange = (e) => {
    const file = e.target.files[0];
    setMedia(file);
  };

  const [description, setDescription] = useState("");
  const handleInputChange = (event) => {
    const { value } = event.target;
    setDescription(value)
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    try{
      const user_id = localStorage.getItem("user_id");
      const request_data = new FormData();
      request_data.append("description", description)
      request_data.append("media", media);
      request_data.append("post_id", post_id)
      const response = await axios
        .post("http://localhost:8000/api/update_user_post/", request_data, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        if ('error' in response.data){console.log(response.data.error);}
        else {setCurrentComponent('feed')}
      } catch (error) {console.log(error);}
    };

  return (
    <ThemeProvider theme={defaultTheme}>
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <Box
          sx={{
            marginTop: 8,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
          }}
        >
          <Avatar sx={{ m: 1, bgcolor: "secondary.main" }}>
            <LockOutlinedIcon />
          </Avatar>
          <Typography component="h1" variant="h5">
            Create Post
          </Typography>
          <Main open={open}>
          <Box
            component="form"
            noValidate
            onSubmit={handleSubmit}
            sx={{ mt: 3 }}
          >
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <label htmlFor="media-input">Image :</label>
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleMediaChange}
                  style={{ marginBottom: "10px" }}
                />
                {media && (
                  <div>
                    <p>Selected Image: {media.name}</p>
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
                <TextField
                  margin="normal"
                  required
                  fullWidth
                  id="description"
                  label="Description"
                  name="description"
                  value={description}
                  autoComplete="description"
                  onChange={handleInputChange}
                  autoFocus
                />
              </Grid>
            </Grid>
            <Button
                  type="submit"
                  fullWidth
                  variant="contained"
                  sx={{ mt: 3, mb: 2 }}
                >
                    Create Post
                </Button>
          </Box>
          </Main>
        </Box>
      </Container>
    </ThemeProvider>
  );
}
