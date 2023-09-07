import * as React from 'react';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import Post from './Post';
import ImgMediaCard from './FriendReq';
import "../static/css/background.css";
import FriendReq from './FriendReq';

export default function SimpleContainer() {
  
  return (
    <React.Fragment>
      <CssBaseline />
      <Container maxWidth="lg">
        <Box sx={{ bgcolor: '#cfe8fc', height: '100vh' }}>
        <FriendReq/>
        
        </Box>
      </Container>
    </React.Fragment>
  );
}