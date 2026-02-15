const fs = require('fs');
const path = require('path');

const templates = {
  nodejs: require('./templates/nodejs'),
  python: require('./templates/python'),
  web: require('./templates/web'),
  react: require('./templates/react'),
};

function generateProject(options) {
  const { name, type, description, author } = options;
  const projectPath = path.join(process.cwd(), name);

  // Check if directory already exists
  if (fs.existsSync(projectPath)) {
    throw new Error(`Directory "${name}" already exists`);
  }

  // Create project directory
  fs.mkdirSync(projectPath, { recursive: true });

  // Generate template files
  const template = templates[type];
  if (!template) {
    throw new Error(`Template "${type}" not found`);
  }

  template.generate(projectPath, { name, description, author });
}

module.exports = { generateProject };
