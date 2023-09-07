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
    product_name: "",
    description: "",
    price: "",
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
        .post("http://localhost:8000/api/set_marketplace/", request_data, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        if ('error' in response.data){console.log(response.data.error);}
        else {setCurrentComponent("MarketPlace")}
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
                  autoComplete="product-name"
                  name="product_name"
                  required
                  fullWidth
                  id="product_name"
                  label="Product Name"
                  value={formData.product_name}
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

              <Grid>
                <TextField
                  margin="normal"
                  required
                  fullWidth
                  id="price"
                  label="price"
                  name="price"
                  value={formData.price}
                  autoComplete="price"
                  onChange={handleInputChange}
                  autoFocus
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
          </Box>
        </Box>
      </Container>
    </ThemeProvider>
  );
}

