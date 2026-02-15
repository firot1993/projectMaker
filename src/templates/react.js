const fs = require('fs');
const path = require('path');

function generate(projectPath, options) {
  const { name, description, author } = options;

  // Create package.json
  const packageJson = {
    name: name,
    version: '0.1.0',
    description: description,
    private: true,
    dependencies: {
      react: '^18.2.0',
      'react-dom': '^18.2.0',
      'react-scripts': '^5.0.1',
    },
    scripts: {
      start: 'react-scripts start',
      build: 'react-scripts build',
      test: 'react-scripts test',
      eject: 'react-scripts eject',
    },
    eslintConfig: {
      extends: ['react-app'],
    },
    browserslist: {
      production: ['>0.2%', 'not dead', 'not op_mini all'],
      development: ['last 1 chrome version', 'last 1 firefox version', 'last 1 safari version'],
    },
  };

  fs.writeFileSync(
    path.join(projectPath, 'package.json'),
    JSON.stringify(packageJson, null, 2)
  );

  // Create public directory
  fs.mkdirSync(path.join(projectPath, 'public'), { recursive: true });

  // Create public/index.html
  const indexHtml = `<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="description" content="${description}" />
    <title>${name}</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>
`;

  fs.writeFileSync(path.join(projectPath, 'public', 'index.html'), indexHtml);

  // Create src directory
  fs.mkdirSync(path.join(projectPath, 'src'), { recursive: true });

  // Create src/index.js
  const indexJs = `import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
`;

  fs.writeFileSync(path.join(projectPath, 'src', 'index.js'), indexJs);

  // Create src/App.js
  const appJs = `import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Welcome to ${name}</h1>
        <p>${description}</p>
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
      </header>
    </div>
  );
}

export default App;
`;

  fs.writeFileSync(path.join(projectPath, 'src', 'App.js'), appJs);

  // Create src/App.css
  const appCss = `.App {
  text-align: center;
}

.App-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-size: calc(10px + 2vmin);
  color: white;
}

.App-header h1 {
  margin-bottom: 1rem;
}

.App-header p {
  max-width: 600px;
  margin: 0.5rem auto;
}

code {
  background-color: rgba(255, 255, 255, 0.1);
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
}
`;

  fs.writeFileSync(path.join(projectPath, 'src', 'App.css'), appCss);

  // Create src/index.css
  const indexCss = `body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

code {
  font-family: source-code-pro, Menlo, Monaco, Consolas, 'Courier New',
    monospace;
}

* {
  box-sizing: border-box;
}
`;

  fs.writeFileSync(path.join(projectPath, 'src', 'index.css'), indexCss);

  // Create .gitignore
  const gitignore = `# dependencies
/node_modules
/.pnp
.pnp.js

# testing
/coverage

# production
/build

# misc
.DS_Store
.env.local
.env.development.local
.env.test.local
.env.production.local

npm-debug.log*
yarn-debug.log*
yarn-error.log*
`;

  fs.writeFileSync(path.join(projectPath, '.gitignore'), gitignore);

  // Create README.md
  const readme = `# ${name}

${description}

## Getting Started

### Installation

\`\`\`bash
npm install
\`\`\`

### Running the application

\`\`\`bash
npm start
\`\`\`

Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

### Building for production

\`\`\`bash
npm run build
\`\`\`

### Running tests

\`\`\`bash
npm test
\`\`\`

## Learn More

This project was bootstrapped with Create React App.

## Author

${author || 'Your Name'}

## License

ISC
`;

  fs.writeFileSync(path.join(projectPath, 'README.md'), readme);
}

module.exports = { generate };
