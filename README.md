# Quiz CLI

An interactive command-line quiz game for learning JavaScript.

## Features

- Interactive category selection
- Choose how many questions to answer
- Randomized question order
- Immediate feedback for correct/incorrect answers
- Progress bar and final score summary
- Built with Node.js built-in modules only

## Requirements

- Node.js 18 or later

## Getting Started

### Install

```bash
npm install
```

### Run the quiz

```bash
npm start
```

## Scripts

- `npm start` — Run the quiz application
- `npm test` — Run the test suite

## Project Structure

```text
.
├── data/questions.json
├── index.js
├── package.json
└── src/
    ├── colors.js
    ├── input.js
    └── quiz.js
```

## How It Works

1. The app loads quiz questions from `data/questions.json`
2. You choose a category and number of questions
3. Each question is shown with multiple-choice answers
4. Your score is calculated at the end of the quiz

## Technologies Used

- ES Modules
- Async/await
- Node.js `readline`
- File system promises

## License

MIT
