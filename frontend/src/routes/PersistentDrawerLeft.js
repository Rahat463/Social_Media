import * as React from "react";
import Box from "@mui/material/Box";
import Navbar from "../components/Navbar";
import RightSidebar from "../components/RightSidebar";
import Feed from "../components/Feed";
import CreatePost from "../components/CreatePost";
import Friends from "../components/Friends";
import FriendReq from "../components/FriendReq";
import Groups from "../components/Groups";
import CreateGroup from "../components/CreateGroup";
import Pages from "../components/Pages";
import CreatePage from "../components/CreatePage";
import ChatHome from "../components/ChatHome";
import Events from "../components/Events";
import CreateEvent from "../components/CreateEvent";
import MarketPlace from "../components/MarketPlace";
import CreateMarketPlace from "../components/CreateMarketPlace";
import Profile from "../components/Profile";
import SearchPage from "../components/SearchPage";
import UpdatePost from "../components/UpdatePost";
import Chat from "../components/Chat";


export default function PersistentDrawerLeft() {
  const [profileId, setProfileId] = React.useState([]);
  const [searchData, setSearchData] = React.useState([]);
  const [updatePostId, setUpdatePostId] = React.useState([]);
  const [isSidebarOpen, setIsSidebarOpen] = React.useState(false);
  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  const [currentComponent, setCurrentComponent] = React.useState("feed");

  return (
    <Box sx={{ display: "flex" }}>
      <Navbar isOpen={isSidebarOpen} toggleSidebar={toggleSidebar} setCurrentComponent = {setCurrentComponent} setSearchData = {setSearchData} setProfileId={setProfileId} />
      { currentComponent.toLowerCase() === "feed" && < Feed open={isSidebarOpen} setCurrentComponent = {setCurrentComponent} setUpdatePostId={setUpdatePostId}/>}
      { currentComponent === "createpost" && < CreatePost open={isSidebarOpen} setCurrentComponent = {setCurrentComponent} />}
      { currentComponent === "Groups" && < Groups open={isSidebarOpen} setCurrentComponent = {setCurrentComponent} />}
      { currentComponent === "Pages" && < Pages open={isSidebarOpen} setCurrentComponent = {setCurrentComponent} />}
      { currentComponent === "Friends" && < Friends open={isSidebarOpen} setCurrentComponent = {setCurrentComponent} setProfileId={setProfileId}/>}
      { currentComponent === "Requests" && < FriendReq open={isSidebarOpen} setCurrentComponent = {setCurrentComponent} setProfileId={setProfileId}/>}
      { currentComponent === "creategroup" && < CreateGroup open={isSidebarOpen} setCurrentComponent = {setCurrentComponent} />}
      { currentComponent === "createpage" && < CreatePage open={isSidebarOpen} setCurrentComponent = {setCurrentComponent} />}
      { currentComponent === "Messages" && < ChatHome open={isSidebarOpen} setCurrentComponent = {setCurrentComponent} setProfileId={setProfileId} />}
      { currentComponent === "Events" && < Events open={isSidebarOpen} setCurrentComponent = {setCurrentComponent} />}
      { currentComponent === "createevent" && < CreateEvent open={isSidebarOpen} setCurrentComponent = {setCurrentComponent} />}
      { currentComponent === "MarketPlace" && < MarketPlace open={isSidebarOpen} setCurrentComponent = {setCurrentComponent} />}
      { currentComponent === "createmarketplace" && < CreateMarketPlace open={isSidebarOpen} setCurrentComponent = {setCurrentComponent} />}
      { currentComponent === "Profile" && < Profile open={isSidebarOpen} setCurrentComponent = {setCurrentComponent} profileId = {profileId} />}
      { currentComponent === "search" && < SearchPage open={isSidebarOpen} setCurrentComponent = {setCurrentComponent} searchData = {searchData} setProfileId={setProfileId} />}
      { currentComponent === "editpost" && < UpdatePost open={isSidebarOpen} setCurrentComponent = {setCurrentComponent} post_id = {updatePostId} />}
      { currentComponent === "Chat" && < Chat open={isSidebarOpen} setCurrentComponent = {setCurrentComponent} friend_id = {profileId} />}
      <RightSidebar/>
    </Box>
  );
}
