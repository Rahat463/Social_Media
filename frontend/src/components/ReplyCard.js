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
import axios from "axios";

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
  // maxWidth: 500, // Set the maximum width to make it moderately larger
  border: "2px solid #ccc",
  borderRadius: "10px",
};

const mediaStyles = {
  flex: "1",
  objectFit: "cover",
};

export default function ReplyCard({replyData, open, setCurrentComponent}) {
  const [expanded, setExpanded] = React.useState(false);

  const handleExpandClick = async () => {
    setExpanded(!expanded);
  };

  return (
    <Card sx={cardStyles}>
      <CardHeader
        avatar={
          <Avatar sx={{ bgcolor: red[500] }} aria-label="post">
            <img
              src={replyData.profile_pic[0]}
              alt="R"
              style={{ width: "100%", height: "100%", objectFit: "cover" }}
            ></img>
          </Avatar>
        }
        action={
          <IconButton aria-label="settings">
            <MoreVertIcon />
          </IconButton>
        }
        title={replyData.user_name}
        subheader={replyData.init_time}
      />
      <CardMedia
        component="img"
        image={replyData.media[0]}
        alt="Paella dish"
        sx={mediaStyles}
      />
      <CardContent>
        <Typography variant="body2" color="text.secondary">
          {replyData.description}
        </Typography>
      </CardContent>
      <CardActions disableSpacing>
        <IconButton aria-label="add to favorites">
          <FavoriteIcon />
        </IconButton>
        <IconButton aria-label="share">
          <ShareIcon />
        </IconButton>
      </CardActions>
    </Card>
  );
}
