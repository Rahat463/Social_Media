import * as React from "react";
import { styled } from "@mui/material/styles";
import Card from "@mui/material/Card";
import CardHeader from "@mui/material/CardHeader";
import CardMedia from "@mui/material/CardMedia";
import CardContent from "@mui/material/CardContent";
import CardActions from "@mui/material/CardActions";
import Collapse from "@mui/material/Collapse";
import Avatar from "@mui/material/Avatar";
import IconButton from "@mui/material/IconButton";
import Typography from "@mui/material/Typography";
import { red } from "@mui/material/colors";
import FavoriteIcon from "@mui/icons-material/Favorite";
import ShareIcon from "@mui/icons-material/Share";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import MoreVertIcon from "@mui/icons-material/MoreVert";
import Comments from "./Comments";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import { useState } from "react";
import axios from "axios";
import PostMenu from "./PostMenu";

const ExpandMore = styled((props) => {
  const { expand, ...other } = props;
  return <IconButton {...other} />;
})(({ theme, expand }) => ({
  transform: !expand ? "rotate(0deg)" : "rotate(180deg)",
  marginLeft: "auto",
  transition: theme.transitions.create("transform", {
    duration: theme.transitions.duration.shortest,
  }),
}));

const cardStyles = {
  display: "flex",
  flexDirection: "column",
  border: "2px solid #ccc",
  borderRadius: "10px",
};

const mediaStyles = {
  flex: "1",
  objectFit: "cover",
};

export default function Post({
  open,
  setCurrentComponent,
  postData,
  setUpdatePostId,
}) {
  const [expanded, setExpanded] = React.useState(false);
  const [commentInfo, setCommentInfo] = React.useState([]);
  const [anchorE2, setAnchorE2] = React.useState(null);
  const [shareMenuOpen, setShareMenuOpen] = React.useState(false);
  const [reactions, setReactions] = React.useState({
    like: "👍",
    love: "❤️",
    fire: "🔥",
  });

  const handleExpandClick = () => {
    setExpanded(!expanded);
  };

  const handleShareMenuClose = () => {
    setAnchorE2(null);
    setShareMenuOpen(false);
  };

  const handleReaction = async (reaction) => {
    try {
      const user_id = localStorage.getItem("user_id");

    //   const request_data = new FormData();
    //   request_data.append("reaction", reaction);
    //   request_data.append("user_id", user_id);
    //   request_data.append("post_id", postData.post_id);
    //  console.log(reaction,user_id,postData.post_id)
    const request_data={reaction:reaction,user_id:user_id,post_id:postData.post_id}
      const response = await axios.post(
        "http://localhost:8000/api/setPostReact/",
        request_data,
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      // Handle the API response as needed
      console.log(`User reacted with ${reaction}`);
      
      // Update the reactions state based on the response
      setReactions((prevReactions) => ({
        ...prevReactions,
        [reaction]: prevReactions[reaction] + 1,
      }));
    } catch (error) {
      console.error("Error reacting to post:", error);
    }
  };

  return (
    <Card sx={cardStyles}>
      <CardHeader
        avatar={
          <Avatar sx={{ bgcolor: red[500] }} aria-label="post">
            {postData?.user_name?.charAt(0) || "U"}
          </Avatar>
        }
        action={
          <>
            <PostMenu
              setCurrentComponent={setCurrentComponent}
              setUpdatePostId={setUpdatePostId}
              post_id={postData.post_id}
            />
          </>
        }
        title={postData?.user_name || "No User Name"}
        subheader={postData?.init_time || "No Init Time"}
      />
      <CardMedia
        component="img"
        image={postData?.media?.[0] || "fallback-image-url-if-media-is-missing"}
        alt="pic"
        sx={mediaStyles}
      />
      <CardContent>
        <Typography variant="body2" color="text.secondary">
          {postData?.description || "No Description"}
        </Typography>
      </CardContent>
      <CardActions disableSpacing>
        <IconButton
          aria-label="add to favorites"
          onClick={() => handleReaction("like")}
        >
          {/* <FavoriteIcon /> */}
          {reactions.like}
        </IconButton>
        <IconButton
          aria-label="love"
          onClick={() => handleReaction("love")}
        >
          {/* <FavoriteIcon /> */}
          {reactions.love}
        </IconButton>
        <IconButton
          aria-label="fire"
          onClick={() => handleReaction("fire")}
        >
          {/* <FavoriteIcon /> */}
          {reactions.fire}
        </IconButton>
        <div className="component-container">
          <IconButton
            aria-label="share"
            onClick={(event) => {
              setAnchorE2(event.currentTarget);
              setShareMenuOpen(true);
            }}
          >
            <ShareIcon />
          </IconButton>
        </div>
        <Menu
          anchorEl={anchorE2}
          open={shareMenuOpen}
          onClose={handleShareMenuClose}
          anchorOrigin={{
            vertical: "top",
            horizontal: "right",
          }}
          transformOrigin={{
            vertical: "top",
            horizontal: "right",
          }}
        >
          <MenuItem onClick={handleShareMenuClose}>Share in Page</MenuItem>
          <MenuItem onClick={handleShareMenuClose}>Share in Group</MenuItem>
          <MenuItem onClick={handleShareMenuClose}>Share in Feed</MenuItem>
          {/* Add more menu items as needed */}
        </Menu>
        <ExpandMore
          expand={expanded}
          onClick={handleExpandClick}
          aria-expanded={expanded}
          aria-label="show more"
        >
          <ExpandMoreIcon />
          Comments
        </ExpandMore>
      </CardActions>
      <Collapse in={expanded} timeout="auto" unmountOnExit>
        <CardContent>
          <Comments
            post_id={postData.post_id}
            open={open}
            setCurrentComponent={setCurrentComponent}
          />
        </CardContent>
      </Collapse>
    </Card>
  );
}
