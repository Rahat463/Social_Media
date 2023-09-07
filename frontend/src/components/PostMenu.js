import * as React from 'react';
import Button from '@mui/material/Button';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import MoreVertIcon from "@mui/icons-material/MoreVert";
import DeletePostDialogue from './DeletePostDialogue';


export default function PostMenu({setCurrentComponent, setUpdatePostId, post_id}) {
  const [anchorEl, setAnchorEl] = React.useState(null);
  const open = Boolean(anchorEl);
  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };
  const handleEdit = () => {
    setAnchorEl(null);
     setUpdatePostId(post_id)
    setCurrentComponent('editpost')
  };
  const handleDelete = () => {
    setAnchorEl(null);
  };

  return (
    <div>
      <Button
        id="basic-button"
        aria-controls={open ? 'basic-menu' : undefined}
        aria-haspopup="true"
        aria-expanded={open ? 'true' : undefined}
        onClick={handleClick}
         sx={ { borderRadius: '28px' } }
      >
        <MoreVertIcon />
      </Button>
      <Menu
        id="basic-menu"
        anchorEl={anchorEl}
        open={open}
        onClose={handleClose}
        MenuListProps={{
          'aria-labelledby': 'basic-button',
        }}
      >
        <MenuItem onClick={handleEdit}>Edit Post</MenuItem>
        <DeletePostDialogue onClick={handleDelete} post_id={post_id}>Delete Post</DeletePostDialogue>
        {/* <MenuItem onClick={handleClose}>Logout</MenuItem> */}
      </Menu>
    </div>
  );
}