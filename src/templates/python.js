const fs = require('fs');
const path = require('path');

function generate(projectPath, options) {
  const { name, description, author } = options;

  // Create app.py
  const appPy = `from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({'message': 'Welcome to ${name} API!'})

@app.route('/api/health')
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
`;

  fs.writeFileSync(path.join(projectPath, 'app.py'), appPy);

  // Create requirements.txt
  const requirements = `Flask==2.3.2
python-dotenv==1.0.0
`;

  fs.writeFileSync(path.join(projectPath, 'requirements.txt'), requirements);

  // Create .gitignore
  const gitignore = `__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
ENV/
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
pip install -r requirements.txt
\`\`\`

### Running the application

\`\`\`bash
python app.py
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
