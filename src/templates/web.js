const fs = require('fs');
const path = require('path');

function generate(projectPath, options) {
  const { name, description, author } = options;

  // Create index.html
  const indexHtml = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${name}</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>Welcome to ${name}</h1>
            <p>${description}</p>
        </header>
        <main>
            <section>
                <h2>Getting Started</h2>
                <p>This is a static website template. Start editing to make it your own!</p>
            </section>
        </main>
        <footer>
            <p>Created by ${author || 'Your Name'}</p>
        </footer>
    </div>
    <script src="script.js"></script>
</body>
</html>
`;

  fs.writeFileSync(path.join(projectPath, 'index.html'), indexHtml);

  // Create styles.css
  const stylesCss = `* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #333;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}

.container {
    background: white;
    border-radius: 10px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    padding: 2rem;
    max-width: 800px;
    margin: 2rem;
}

header {
    text-align: center;
    margin-bottom: 2rem;
}

h1 {
    color: #667eea;
    margin-bottom: 0.5rem;
}

h2 {
    color: #764ba2;
    margin-bottom: 1rem;
}

main {
    margin: 2rem 0;
}

section {
    margin-bottom: 1.5rem;
}

footer {
    text-align: center;
    margin-top: 2rem;
    padding-top: 1rem;
    border-top: 1px solid #eee;
    color: #666;
}
`;

  fs.writeFileSync(path.join(projectPath, 'styles.css'), stylesCss);

  // Create script.js
  const scriptJs = `// Add your JavaScript code here
console.log('Welcome to ${name}!');

document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM loaded');
});
`;

  fs.writeFileSync(path.join(projectPath, 'script.js'), scriptJs);

  // Create .gitignore
  const gitignore = `.DS_Store
*.log
`;

  fs.writeFileSync(path.join(projectPath, '.gitignore'), gitignore);

  // Create README.md
  const readme = `# ${name}

${description}

## Getting Started

Simply open \`index.html\` in your browser to view the website.

## Project Structure

- \`index.html\` - Main HTML file
- \`styles.css\` - CSS styles
- \`script.js\` - JavaScript code

## Author

${author || 'Your Name'}

## License

ISC
`;

  fs.writeFileSync(path.join(projectPath, 'README.md'), readme);
}

module.exports = { generate };
