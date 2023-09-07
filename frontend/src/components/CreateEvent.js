import { useState } from "react";
import * as React from "react";
import Avatar from "@mui/material/Avatar";
import Button from "@mui/material/Button";
import CssBaseline from "@mui/material/CssBaseline";
import TextField from "@mui/material/TextField";
import FormControlLabel from "@mui/material/FormControlLabel";
import Checkbox from "@mui/material/Checkbox";
import Link from "@mui/material/Link";
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import LockOutlinedIcon from "@mui/icons-material/LockOutlined";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import IconButton from "@mui/material/IconButton";
import Visibility from "@mui/icons-material/Visibility";
import VisibilityOff from "@mui/icons-material/VisibilityOff";
import InputAdornment from "@mui/material/InputAdornment";
import axios from "axios";

const defaultTheme = createTheme();

export default function CreateEvent({open, setCurrentComponent}) {
  const user_id = localStorage.getItem("user_id");
  const [media, setmedia] = useState(null);

  const handleMediaChange = (e) => {
    const file = e.target.files[0];
    setmedia(file);
  };

  const [formData, setFormData] = useState({
    event_name: "",
    description: "",
    start_time: "",
    end_time: "",
    location: "",
  });
  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    try{
      const request_data = new FormData();
      for (const key in formData) {
        request_data.append(key, formData[key]);
      }
      request_data.append("media", media);
      request_data.append("user_id", user_id);
      const response = await axios
        .post("http://localhost:8000/api/set_event/", request_data, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        if ('error' in response.data){console.log(response.data.error);}
        else {setCurrentComponent("Events")}
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
            Sign up
          </Typography>
          <Box
            component="form"
            noValidate
            onSubmit={handleSubmit}
            sx={{ mt: 3 }}
          >
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <TextField
                  autoComplete="event-name"
                  name="event_name"
                  required
                  fullWidth
                  id="event_name"
                  label="Event Name"
                  value={formData.event_name}
                  onChange={handleInputChange}
                  autoFocus
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  required
                  fullWidth
                  id="description"
                  label="Description"
                  name="description"
                  value={formData.description}
                  onChange={handleInputChange}
                  autoComplete="description"
                />
              </Grid>
              <Grid item xs={12}>
                <label htmlFor="media-input">Image</label>
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
                  required
                  fullWidth
                  id="start_time"
                  label="Start Time"
                  name="start_time"
                  type="date"
                  value={formData.start_time}
                  onChange={handleInputChange}
                  InputLabelProps={{
                    shrink: true,
                  }}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  required
                  fullWidth
                  id="end_time"
                  label="End Time"
                  name="end_time"
                  type="date"
                  value={formData.end_time}
                  onChange={handleInputChange}
                  InputLabelProps={{
                    shrink: true,
                  }}
                />
              </Grid>
              <Grid>
                <TextField
                  margin="normal"
                  required
                  fullWidth
                  id="location"
                  label="Location"
                  name="location"
                  value={formData.location}
                  autoComplete="location"
                  onChange={handleInputChange}
                  autoFocus
                />
              </Grid>

              <Grid item xs={12}>
                <FormControlLabel
                  control={
                    <Checkbox value="allowExtraEmails" color="primary" />
                  }
                  label="I want to receive inspiration, marketing promotions and updates via email."
                />
              </Grid>
            </Grid>
            {/* <div> */}
              {/* <a
                href="/routes/SignIn"
                style={{ textDecoration: "none", color: "inherit" }}
              > */}
                <Button
                  type="submit"
                  fullWidth
                  variant="contained"
                  sx={{ mt: 3, mb: 2 }}
                >
                    Sign Up
                </Button>
              {/* </a> */}
            {/* </div> */}
            <Grid container justifyContent="flex-end">
              <Grid item>
                <Link href="/routes/SignIn" variant="body2">
                  Already have an account? Sign in
                </Link>
              </Grid>
            </Grid>
          </Box>
        </Box>
      </Container>
    </ThemeProvider>
  );
}

