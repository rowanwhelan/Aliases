# Aliases
This is a codenames spoof which I am going to program so I can experiment with different gameplay styles and try to code Algorithms which can play against eachother

# Changelog

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