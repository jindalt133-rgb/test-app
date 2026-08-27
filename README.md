# Quiz CLI

![Node.js](https://img.shields.io/badge/Node.js-18%2B-339933?logo=node.js&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![CLI](https://img.shields.io/badge/Type-Command--Line%20App-informational)

`quiz-cli` is an interactive Node.js terminal quiz game designed to help developers practice programming fundamentals. It presents a menu-driven experience with categories, selectable question counts, instant feedback, and a final review of incorrect answers.

## Overview

This application is built as a lightweight, dependency-free CLI that runs entirely on Node.js built-in APIs and ES modules. It loads a structured question bank from `data/questions.json`, lets the user choose a category, then walks through a randomized quiz session with:

- multiple-choice questions
- progress tracking
- immediate correctness feedback
- explanation text for each question
- score summary at the end
- review of missed questions
- replay support

The quiz currently covers:

- JavaScript Basics
- Node.js Fundamentals
- General Programming

## Features

- Interactive terminal UI with colored output
- Category selection and question-count selection
- Randomized question order per quiz session
- Progress bar and per-question progress display
- Immediate correct/incorrect answer feedback
- Explanations shown after each answer
- Final score summary with performance messaging
- Review section for incorrect answers
- Built with ES modules and async/await
- No external npm dependencies

## Project Structure

```text
quiz-cli/
├── data/
│   └── questions.json
├── src/
│   ├── colors.js
│   ├── input.js
│   └── quiz.js
├── index.js
└── package.json
```

### File and folder purpose

- **`index.js`** — Application entry point and main CLI flow. Loads questions, shows the banner, handles category/question count selection, runs the quiz loop, and manages replay/error handling.
- **`src/quiz.js`** — Quiz engine. Shuffles questions, tracks score and answers, renders progress, asks questions, and displays final results plus review for incorrect responses.
- **`src/input.js`** — Readline-based input helpers for prompts, selections, confirmations, and press-enter pauses.
- **`src/colors.js`** — ANSI color utilities used to style terminal output without external libraries.
- **`data/questions.json`** — Question bank organized by category. Each question includes options, a correct answer index, and an explanation.
- **`package.json`** — Project metadata, scripts, module type, and Node engine requirement.

## Prerequisites

- **Node.js 18.0.0 or later**
- **npm** (included with Node.js)

No additional dependencies are required.

## Installation

Clone the repository and move into the project directory:

```bash
git clone <repository-url>
cd test-app
```

Install dependencies:

```bash
npm install
```

> This project currently has no external dependencies, so `npm install` completes quickly. It is still a good way to verify your local Node/npm setup.

## Usage

### Start the quiz

```bash
npm start
```

This runs:

```bash
node index.js
```

### How to play

1. Launch the application.
2. Select a quiz category.
3. Choose how many questions to answer.
4. Enter the number corresponding to your answer choice.
5. Read the immediate result and explanation.
6. Review your final score and missed questions.
7. Choose whether to play again.

### Example flow

```text
Choose a category:
  1. JavaScript Basics
  2. Node.js Fundamentals
  3. General Programming

How many questions?
  1. All questions
  2. 3 questions
  3. 5 questions

Your choice (enter number):
```

### Direct execution

The entry file includes a Node shebang (`#!/usr/bin/env node`), so it is set up for CLI execution. On systems where the file is marked executable, it may be run directly as well.

## Available Scripts

| Script | Command | Description |
| ------ | ------- | ----------- |
| `start` | `npm start` | Runs the quiz application |
| `test` | `npm test` | Executes Node’s built-in test runner (`node --test`) |

## Testing

The project is configured to use Node’s native test runner:

```bash
npm test
```

At the time of inspection, no test files were visible in the repository. If you add tests, place them in a pattern recognized by `node --test` so they are discovered automatically.

## Technologies Used

- **Node.js**
- **JavaScript (ES modules)**
- **Built-in `fs/promises` API**
- **Built-in `readline` API**
- **Built-in `path` / `url` utilities**
- **ANSI terminal escape codes** for colorized output

## Configuration Gaps / Pending Items

The repository currently does **not** include the following:

- environment variables
- `.env` configuration
- build pipeline
- Docker configuration
- CI/CD workflow files
- deployment configuration
- database integration

If you extend the app in the future, document any new runtime requirements or environment variables here.

## Notes for Contributors

- Keep question data structured consistently in `data/questions.json`.
- Preserve the existing menu-driven terminal experience when adding new quiz flows.
- If you add categories or question types, make sure the count-selection logic in `index.js` still behaves correctly.
- Keep terminal output readable; the app relies on concise prompts and color-coded feedback.
- Add tests as the codebase grows, especially for quiz logic and input validation.

## License

MIT
