# projectMaker Examples

This document provides examples of using the projectMaker CLI tool.

## Basic Usage

### Creating a project interactively

```bash
$ projectmaker create

? What is your project name? my-awesome-app
? What type of project do you want to create? Node.js (Express API)
? Project description: My awesome Node.js API
? Author name: John Doe

🚀 Creating your project...

✨ Project "my-awesome-app" created successfully!

Next steps:
  cd my-awesome-app
  npm install
  npm start
```

### Creating a project with a specified name

```bash
$ projectmaker create my-app

? What type of project do you want to create? React Application
? Project description: A React app
? Author name: Jane Smith

🚀 Creating your project...

✨ Project "my-app" created successfully!

Next steps:
  cd my-app
  npm install
  npm start
```

## Template Examples

### Node.js (Express API) Template

Creates a Node.js project with Express.js:

**Generated Files:**
```
my-api/
├── package.json
├── index.js
├── .gitignore
└── README.md
```

**Key Features:**
- Express server setup
- Basic API endpoints (/, /api/health)
- Development scripts with nodemon
- Professional .gitignore

### Python (Flask) Template

Creates a Python project with Flask:

**Generated Files:**
```
my-python-app/
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

**Key Features:**
- Flask application setup
- Basic API endpoints
- Requirements file with Flask and python-dotenv
- Python-specific .gitignore

### Static Website Template

Creates a static website with HTML, CSS, and JavaScript:

**Generated Files:**
```
my-website/
├── index.html
├── styles.css
├── script.js
├── .gitignore
└── README.md
```

**Key Features:**
- Modern HTML5 structure
- Beautiful gradient styling
- Responsive design
- JavaScript ready

### React Application Template

Creates a React application:

**Generated Files:**
```
my-react-app/
├── package.json
├── public/
│   └── index.html
├── src/
│   ├── index.js
│   ├── index.css
│   ├── App.js
│   └── App.css
├── .gitignore
└── README.md
```

**Key Features:**
- React 18 setup
- React Scripts for development
- Modern component structure
- Professional styling

## Command Reference

### Create Command

```bash
projectmaker create [project-name]
```

Creates a new project from a template. If `project-name` is not provided, you will be prompted to enter it.

### List Command

```bash
projectmaker list
```

Lists all available project templates:

```
📋 Available templates:

  • nodejs     - Node.js with Express API
  • python     - Python with Flask
  • web        - Static website with HTML/CSS/JS
  • react      - React application
```

### Help Command

```bash
projectmaker --help
```

Shows help information:

```
Usage: projectmaker [options] [command]

A CLI tool to scaffold new projects with templates

Options:
  -V, --version          output the version number
  -h, --help             display help for command

Commands:
  create [project-name]  Create a new project from a template
  list                   List available project templates
  help [command]         display help for command
```

### Version Command

```bash
projectmaker --version
```

Shows the current version of projectMaker.

## Advanced Usage

### Creating Multiple Projects

You can create multiple projects one after another:

```bash
projectmaker create api-backend
projectmaker create web-frontend
projectmaker create python-service
```

### Using with Different Package Managers

After creating a Node.js or React project, you can use your preferred package manager:

```bash
# Using npm (default)
npm install
npm start

# Using yarn
yarn install
yarn start

# Using pnpm
pnpm install
pnpm start
```

## Tips and Tricks

1. **Keep project names lowercase**: It's a convention to use lowercase names with hyphens for project directories.

2. **Check if directory exists**: The tool will fail if a directory with the same name already exists, preventing accidental overwrites.

3. **Customize after creation**: All generated files are meant to be starting points. Feel free to customize them to fit your needs.

4. **Git initialization**: After creating your project, don't forget to initialize a git repository:
   ```bash
   cd my-project
   git init
   git add .
   git commit -m "Initial commit"
   ```

5. **Environment variables**: For Node.js and Python projects, create a `.env` file for environment-specific configuration.

## Troubleshooting

### Directory already exists

**Error:**
```
Error creating project: Directory "my-project" already exists
```

**Solution:**
Choose a different project name or remove the existing directory.

### Missing dependencies

After creating a project, if you encounter errors, make sure to install dependencies:

**For Node.js/React:**
```bash
npm install
```

**For Python:**
```bash
pip install -r requirements.txt
```

### Permission denied

If you get a permission denied error when running projectmaker globally:

```bash
sudo npm install -g projectmaker
```

Or use npx without installation:

```bash
npx projectmaker create my-project
```
