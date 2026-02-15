const fs = require('fs');
const path = require('path');

function generate(projectPath, options) {
  const { name, description, author } = options;

  // Create package.json
  const packageJson = {
    name: name,
    version: '1.0.0',
    description: description,
    main: 'index.js',
    scripts: {
      start: 'node index.js',
      dev: 'nodemon index.js',
    },
    keywords: [],
    author: author,
    license: 'ISC',
    dependencies: {
      express: '^4.18.2',
    },
    devDependencies: {
      nodemon: '^2.0.22',
    },
  };

  fs.writeFileSync(
    path.join(projectPath, 'package.json'),
    JSON.stringify(packageJson, null, 2)
  );

  // Create index.js
  const indexJs = `const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

app.get('/', (req, res) => {
  res.json({ message: 'Welcome to ${name} API!' });
});

app.get('/api/health', (req, res) => {
  res.json({ status: 'ok' });
});

app.listen(PORT, () => {
  console.log(\`Server is running on port \${PORT}\`);
});
`;

  fs.writeFileSync(path.join(projectPath, 'index.js'), indexJs);

  // Create .gitignore
  const gitignore = `node_modules/
.env
*.log
.DS_Store
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

### Development mode

\`\`\`bash
npm run dev
\`\`\`

## API Endpoints

- \`GET /\` - Welcome message
- \`GET /api/health\` - Health check

## Author

${author || 'Your Name'}

## License

ISC
`;

  fs.writeFileSync(path.join(projectPath, 'README.md'), readme);
}

module.exports = { generate };
