import React, { useState } from 'react';
import { useSpring, animated } from 'react-spring';
//import './ReactionButtons.css'; // Import your CSS file

const  ReactionButton = ({ onReaction }) => {
  const [reactions, setReactions] = useState({
    like: 0,
    love: 0,
    wow: 0,
  });

  const handleReaction = (reaction) => {
    setReactions((prevReactions) => ({
      ...prevReactions,
      [reaction]: prevReactions[reaction] + 1,
    }));
    onReaction(reaction);
  };

  const buttonScale = useSpring({ scale: 1, config: { tension: 200, friction: 10 } });

  return (
    <div className="reaction-buttons">
      <animated.button
        className="reaction-button like"
        onClick={() => {
          handleReaction('like');
          buttonScale.scale.set(1.1);
        }}
        style={{ transform: buttonScale.scale.interpolate((scale) => `scale(${scale})`) }}
      >
        Like ({reactions.like})
      </animated.button>
      <animated.button
        className="reaction-button love"
        onClick={() => {
          handleReaction('love');
          buttonScale.scale.set(1.1);
        }}
        style={{ transform: buttonScale.scale.interpolate((scale) => `scale(${scale})`) }}
      >
        Love ({reactions.love})
      </animated.button>
      <animated.button
        className="reaction-button wow"
        onClick={() => {
          handleReaction('wow');
          buttonScale.scale.set(1.1);
        }}
        style={{ transform: buttonScale.scale.interpolate((scale) => `scale(${scale})`) }}
      >
        Wow ({reactions.wow})
      </animated.button>
    </div>
  );
};
export default ReactionButton;

// const App = () => {
//   const handleReaction = (reaction) => {
//     // Here, you can handle what happens when a reaction is clicked, e.g., send data to a server.
//     console.log(`User reacted with ${reaction}`);
//   };

//   return (
//     <div>
//       <h1>Post Title</h1>
//       <p>Post content goes here.</p>
//       <ReactionButton onReaction={handleReaction} />
//     </div>
//   );
// };

// export default App;
