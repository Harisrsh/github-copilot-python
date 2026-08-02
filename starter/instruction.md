# Copilot Instructions for this Project

## Code Style
- Use clear, descriptive variable and function names.
- Keep functions small and focused on a single responsibility.
- Add docstrings/comments for any non-obvious logic (e.g., backtracking, solution counting).

## Structure
- Keep game logic (puzzle generation, validation) separate from Flask route handling.
- Frontend logic in main.js should be organized by feature (rendering, timer, hints, leaderboard, etc.), not one giant file.

## Error Handling
- All Flask routes should return clear JSON error messages with appropriate HTTP status codes instead of crashing.
- Frontend fetch calls should handle failures gracefully and show a user-facing message.

## Testing
- Write or update pytest tests for any new backend logic.
- Run the full test suite after every change before committing.

## Style/CSS
- Use CSS custom properties for theming (light/dark mode).
- Prioritize responsive, accessible design — readable text, sufficient contrast, comfortable tap targets on mobile.