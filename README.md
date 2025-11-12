# T-Rex Game

A classic Chrome Dinosaur-style game built with Python and Tkinter.

## Description

This is a complete rewrite of the T-Rex jumping game where you control a dinosaur that must jump over obstacles. The game features:

- **Smooth Jump Physics**: Realistic gravity-based jumping mechanics
- **Progressive Difficulty**: Game speed increases as you score more points
- **Score Tracking**: Real-time score display with persistent high score
- **Proper Collision Detection**: Accurate rectangle-based collision system
- **Game Over & Restart**: Clean game state management with restart functionality

## How to Play

1. Run the game: `python3 trexgame.py`
2. Press **SPACE** to make the T-Rex jump
3. Avoid the brown obstacles
4. Press **R** to restart after game over

## Controls

- `SPACE` - Jump
- `R` - Restart game (when game over)

## Features

### Fixed Issues from Original Version:
- ✅ Non-blocking jump animation (original used blocking loops)
- ✅ Proper obstacle spawning with correct coordinates
- ✅ Accurate collision detection
- ✅ Score increments only when passing obstacles (not every frame)
- ✅ Game properly stops on collision
- ✅ Score and high score displayed on screen
- ✅ Working restart functionality
- ✅ Difficulty progression system

### Game Mechanics:
- **Jump Physics**: Velocity-based jumping with gravity
- **Obstacles**: Randomly sized and spaced obstacles
- **Scoring**: Earn points by successfully passing obstacles
- **Speed Increase**: Game gets faster every 10 points
- **High Score**: Best score is saved to `high_score.txt`

## Requirements

- Python 3.x
- tkinter (usually included with Python)

## Technical Details

The game is built using object-oriented programming with a main `TRexGame` class that handles:
- Game state management
- Physics calculations
- Collision detection
- Score tracking and persistence
- Event handling
- Game loop with proper timing (50 FPS)
