# Contributing to projectMaker

Thank you for your interest in contributing to projectMaker! This document provides guidelines and instructions for contributing.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR-USERNAME/projectMaker.git`
3. Install dependencies: `npm install`
4. Create a branch: `git checkout -b feature/your-feature-name`

## Development

### Project Structure

```
projectMaker/
├── bin/
│   └── cli.js          # CLI entry point
├── src/
│   ├── generator.js    # Project generator logic
│   └── templates/      # Template modules
│       ├── nodejs.js   # Node.js template
│       ├── python.js   # Python template
│       ├── web.js      # Web template
│       └── react.js    # React template
├── index.js            # Main entry point
├── package.json        # Package configuration
└── README.md           # Documentation
```

### Testing Locally

To test your changes locally:

```bash
# Link the package globally
npm link

# Test the CLI
projectmaker create test-project

# Unlink when done
npm unlink
```

## Adding a New Template

To add a new project template:

1. Create a new file in `src/templates/` (e.g., `mytemplate.js`)

2. Implement the template module:

```javascript
const fs = require('fs');
const path = require('path');

function generate(projectPath, options) {
  const { name, description, author } = options;
  
  // Create your template files here
  // Example:
  fs.writeFileSync(
    path.join(projectPath, 'README.md'),
    `# ${name}\n\n${description}`
  );
  
  // Add more files as needed
}

module.exports = { generate };
```

3. Register the template in `src/generator.js`:

```javascript
const templates = {
  nodejs: require('./templates/nodejs'),
  python: require('./templates/python'),
  web: require('./templates/web'),
  react: require('./templates/react'),
  mytemplate: require('./templates/mytemplate'), // Add your template here
};
```

4. Add the template to the CLI choices in `bin/cli.js`:

```javascript
choices: [
  { name: 'Node.js (Express API)', value: 'nodejs' },
  { name: 'Python (Flask)', value: 'python' },
  { name: 'Static Website (HTML/CSS/JS)', value: 'web' },
  { name: 'React Application', value: 'react' },
  { name: 'My Template', value: 'mytemplate' }, // Add your template here
],
```

5. Update the documentation in README.md and EXAMPLES.md

## Code Style

- Use 2 spaces for indentation
- Use single quotes for strings
- Add comments for complex logic
- Follow existing code patterns

## Submitting Changes

1. Commit your changes: `git commit -am "Add new feature"`
2. Push to your fork: `git push origin feature/your-feature-name`
3. Create a Pull Request on GitHub

### Commit Message Guidelines

- Use clear and descriptive commit messages
- Start with a verb (Add, Fix, Update, etc.)
- Keep the first line under 50 characters
- Add detailed description if needed

Examples:
- `Add Vue.js template`
- `Fix path resolution in Windows`
- `Update README with installation instructions`

## Reporting Issues

When reporting issues, please include:

- Your operating system
- Node.js version (`node --version`)
- npm version (`npm --version`)
- Steps to reproduce the issue
- Expected behavior
- Actual behavior

## Questions?

If you have questions, feel free to:
- Open an issue on GitHub
- Start a discussion in the repository

Thank you for contributing! 🎉
