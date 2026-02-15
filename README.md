# projectMaker

A simple and powerful CLI tool to scaffold new projects with pre-configured templates.

## Features

- 🚀 Quick project scaffolding
- 📦 Multiple project templates (Node.js, Python, React, Static Web)
- 🎨 Interactive CLI with beautiful prompts
- 📝 Auto-generated README and configuration files
- ⚡ Zero configuration required

## Installation

### Global Installation

```bash
npm install -g projectmaker
```

### Local Usage (without installation)

```bash
npx projectmaker create my-project
```

## Usage

### Create a new project

```bash
projectmaker create
```

You'll be prompted to enter:
- Project name
- Project type (Node.js, Python, React, or Static Website)
- Project description
- Author name

### Create a project with a specific name

```bash
projectmaker create my-awesome-project
```

### List available templates

```bash
projectmaker list
```

## Available Templates

### 1. Node.js (Express API)

A Node.js project with Express.js framework for building REST APIs.

**Includes:**
- Express server setup
- Basic API endpoints
- Package.json with scripts
- .gitignore

**Getting started:**
```bash
projectmaker create my-api
# Select "Node.js (Express API)"
cd my-api
npm install
npm start
```

### 2. Python (Flask)

A Python project with Flask framework for building web applications and APIs.

**Includes:**
- Flask application setup
- Basic API endpoints
- requirements.txt
- .gitignore

**Getting started:**
```bash
projectmaker create my-python-app
# Select "Python (Flask)"
cd my-python-app
pip install -r requirements.txt
python app.py
```

### 3. Static Website (HTML/CSS/JS)

A simple static website with HTML, CSS, and JavaScript.

**Includes:**
- index.html with basic structure
- styles.css with modern styling
- script.js for JavaScript code
- .gitignore

**Getting started:**
```bash
projectmaker create my-website
# Select "Static Website (HTML/CSS/JS)"
cd my-website
# Open index.html in your browser
```

### 4. React Application

A React application with modern setup.

**Includes:**
- React 18 setup
- React Scripts for development
- Basic component structure
- Modern styling
- .gitignore

**Getting started:**
```bash
projectmaker create my-react-app
# Select "React Application"
cd my-react-app
npm install
npm start
```

## Examples

### Creating a Node.js API

```bash
$ projectmaker create
? What is your project name? my-api
? What type of project do you want to create? Node.js (Express API)
? Project description: My awesome API
? Author name: John Doe

🚀 Creating your project...

✨ Project "my-api" created successfully!

Next steps:
  cd my-api
  npm install
  npm start
```

## Development

### Clone the repository

```bash
git clone https://github.com/firot1993/projectMaker.git
cd projectMaker
```

### Install dependencies

```bash
npm install
```

### Test locally

```bash
npm link
projectmaker create test-project
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

ISC

## Author

Created with ❤️ by the projectMaker team
