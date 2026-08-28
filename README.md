# Quiz CLI

An interactive command-line quiz game for learning JavaScript, Node.js, and general programming concepts.

## Features

- Interactive terminal UI with colored output
- Multiple quiz categories:
  - JavaScript Basics
  - Node.js Fundamentals
  - General Programming
- Choose how many questions to answer
- Randomized question order
- Instant feedback for each answer
- Final score summary with performance messages
- Review of incorrect answers at the end

## Requirements

- Node.js 18 or higher

## Getting Started

### Install dependencies

This project does not use external dependencies, but you can still install the project if you want npm scripts available:

```bash
npm install
```

### Run the quiz

```bash
npm start
```

Or run directly:

```bash
node index.js
```

## How It Works

1. The app loads quiz questions from `data/questions.json`.
2. You choose a category.
3. You choose how many questions to answer.
4. Each question is presented in the terminal with numbered options.
5. Your answers are scored and explained immediately.
6. A results screen shows your final score and any incorrect answers to review.

## Project Structure

```text
.
├── index.js            # Entry point for the CLI app
├── package.json        # Project metadata and npm scripts
├── data/
│   └── questions.json  # Quiz content and categories
└── src/
    ├── colors.js      # ANSI color helpers for terminal output
    ├── input.js       # Readline-based input helpers
    └── quiz.js        # Quiz logic, scoring, and results
```

## Scripts

- `npm start` - Start the quiz application
- `npm test` - Run Node.js tests

## Tech Stack

- ES Modules
- Node.js built-in `readline`
- Node.js built-in file system APIs
- ANSI terminal colors

## Notes

- Questions are currently loaded from a local JSON file.
- The quiz shuffles questions each time you play.
- You can play again after finishing a round.
