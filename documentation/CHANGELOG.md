# Aliases
This is a codenames spoof which I am going to program so I can experiment with different gameplay styles and try to code Algorithms which can play against eachother

# Changelog

## v0.5 - 2/24/2025
This update sets the foundation for more advanced multiplayer interactions, AI enhancements, and overall gameplay improvements.

---

### Added:
- **Single-User Multiplayer**: Enabled seamless switching between teams for a solo player, allowing full game simulation without requiring multiple participants.
- **Dynamic HTML Scripting & Display**: Implemented real-time updates to the game board and UI using JavaScript, improving responsiveness and reducing the need for page reloads.
- **Clue Robot Validation & Evaluation**: Introduced basic logic to assess the validity and quality of bot-generated clues, paving the way for more sophisticated AI-assisted gameplay.

--- 

### Fixed:

- **Integrated Database for Grid Storage**: Moved away from Redis, implementing a structured database-backed approach for efficient indexing and retrieval of the 5x5 game grid.
- **Game Flow Refinements**: Improved turn logic to prevent unnecessary state conflicts, ensuring a smoother user experience.
- **Performance Optimizations**: Reduced redundant data processing and improved rendering speed for faster game state updates.
- **Codebase Cleanup & Modularization**: Refactored core components to improve maintainability and facilitate future expansions.

## v0.4 - 11/21/24

This release marks a significant milestone in the development of the game. The singleplayer game is now fully functional, with a robust backend powered by Flask and Redis for efficient state management. Key bugs have been addressed, making the gameplay smooth and reliable.

---

### Added
- **Redis Integration**: Successfully integrated Redis to manage game state across player interactions. The server now efficiently handles updates to the grid and tracks player turns.
- **Persistent Game State**: Implemented serialization and deserialization for `Tile` and `Grid` classes to ensure the game state is reliably saved and retrieved.
- **Dynamic Gameplay**: Players' actions now dynamically update the UI and backend:
  - Clicking on tiles changes their state based on the team and tile type.
  - Background color dynamically reflects the active player's turn.

---

### Fixed
- **Fixed `Tile` Deserialization**: Resolved the issue where `Tile` objects were incorrectly reconstructed from JSON, ensuring seamless grid updates.
- **Server Response Errors**: Addressed errors causing `500 INTERNAL SERVER ERROR` responses, particularly those stemming from incorrect handling of JSON data.
- **Click Logic**: Fixed issues where tiles could be clicked multiple times or passed incorrect data to the server.
- **Connection Refusals**: Ensured Redis is correctly configured and running to prevent connection errors during gameplay.

---

### Changes
- Enhanced error handling in the frontend to gracefully manage server communication failures.
- Improved code readability and modularity, making future feature additions easier.

---

### Known Issues
- Occasional delays when loading the initial board. Further optimization of Redis interactions is planned.
- The statistics page is still under development and will be included in the next release.

---

### Plans for Future Versions
#### v0.5 - AI Bots and Enhancements
- **Bot Players**: Implement intelligent AI bots that can:
  - Generate clues.
  - Select tiles dynamically based on game state.
  
- **Dynamic Difficulty**: Introduce adjustable bot difficulty levels for a more tailored gaming experience.

#### Surprises in Development
- **Themed Boards**: Special themed word grids for holidays and events.
  
- **Power-Ups**: Add special tiles with unique effects to spice up gameplay.

- **Statistics Page**: Provide comprehensive game statistics at the end of each match.


## [0.03] - 2024-11-18

### Added
- **Tile Click Behavior**: Implemented logic to prevent interactions with already-used tiles by checking the `used` value before processing clicks.
- **Backend Integration**: Enhanced the grid's interactivity by sending tile updates to the backend via a POST request.
- **Dynamic Turn-Based Styling**: Background color of the game adjusts dynamically based on the current player's turn (red or blue).
- **JSON Conversion**: Added `| tojson` filter to ensure correct boolean values are passed from the backend to the front-end.

### Fixed
- **Boolean Handling**: Resolved a `ReferenceError` where `False` was improperly passed in the template. Corrected it to `false` for compatibility with JavaScript.
- **Empty Grid Display**: Fixed a rendering issue where tiles in the game grid did not display words correctly. Updated the template to use `tile.word` instead of `word`.

### Changed
- **Grid Styling**: Adjusted CSS for grid tiles to improve responsiveness and appearance.
- **HTML Template**: Modified the `onclick` handler in the grid template for better integration with game logic and error handling.

### Known Issues
- **Backend Updates**: Occasionally, POST requests may fail if the server connection is interrupted. Error handling for failed POST requests is minimal.
- **Tile Reset**: No mechanism yet for resetting tiles once clicked; must reload the game to start fresh.

## [0.1] - Initial Release
- Set up basic game structure and UI
- Added a 5x5 word grid with clickable boxes
- Implemented team-based coloring for the word grid
- Added functionality to prevent clicking on already clicked boxes
- Introduced clue and number input fields below the grid
- Fixed color assignment after clicks