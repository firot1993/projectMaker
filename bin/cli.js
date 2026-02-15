#!/usr/bin/env node

const { program } = require('commander');
const inquirer = require('inquirer');
const chalk = require('chalk');
const fs = require('fs');
const path = require('path');
const { generateProject } = require('../src/generator');

program
  .name('projectmaker')
  .description('A CLI tool to scaffold new projects with templates')
  .version('1.0.0');

program
  .command('create')
  .description('Create a new project from a template')
  .argument('[project-name]', 'Name of the project')
  .action(async (projectName) => {
    try {
      const answers = await inquirer.prompt([
        {
          type: 'input',
          name: 'projectName',
          message: 'What is your project name?',
          default: projectName || 'my-project',
          when: !projectName,
        },
        {
          type: 'list',
          name: 'projectType',
          message: 'What type of project do you want to create?',
          choices: [
            { name: 'Node.js (Express API)', value: 'nodejs' },
            { name: 'Python (Flask)', value: 'python' },
            { name: 'Static Website (HTML/CSS/JS)', value: 'web' },
            { name: 'React Application', value: 'react' },
          ],
        },
        {
          type: 'input',
          name: 'description',
          message: 'Project description:',
          default: 'A new project',
        },
        {
          type: 'input',
          name: 'author',
          message: 'Author name:',
          default: '',
        },
      ]);

      const finalProjectName = projectName || answers.projectName;
      
      console.log(chalk.blue('\n🚀 Creating your project...\n'));
      
      await generateProject({
        name: finalProjectName,
        type: answers.projectType,
        description: answers.description,
        author: answers.author,
      });

      console.log(chalk.green(`\n✨ Project "${finalProjectName}" created successfully!\n`));
      console.log(chalk.cyan('Next steps:'));
      console.log(chalk.white(`  cd ${finalProjectName}`));
      
      if (answers.projectType === 'nodejs') {
        console.log(chalk.white('  npm install'));
        console.log(chalk.white('  npm start'));
      } else if (answers.projectType === 'python') {
        console.log(chalk.white('  pip install -r requirements.txt'));
        console.log(chalk.white('  python app.py'));
      } else if (answers.projectType === 'react') {
        console.log(chalk.white('  npm install'));
        console.log(chalk.white('  npm start'));
      } else if (answers.projectType === 'web') {
        console.log(chalk.white('  Open index.html in your browser'));
      }
      
      console.log('');
    } catch (error) {
      console.error(chalk.red('Error creating project:'), error.message);
      process.exit(1);
    }
  });

program
  .command('list')
  .description('List available project templates')
  .action(() => {
    console.log(chalk.blue('\n📋 Available templates:\n'));
    console.log(chalk.white('  • nodejs     - Node.js with Express API'));
    console.log(chalk.white('  • python     - Python with Flask'));
    console.log(chalk.white('  • web        - Static website with HTML/CSS/JS'));
    console.log(chalk.white('  • react      - React application'));
    console.log('');
  });

program.parse();
