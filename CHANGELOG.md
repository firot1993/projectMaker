# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-15

### Added

- Initial release of projectMaker CLI tool
- Interactive project scaffolding with `projectmaker create` command
- Node.js (Express API) template with:
  - Express server setup
  - Basic API endpoints
  - Development and production scripts
  - Package.json configuration
- Python (Flask) template with:
  - Flask application setup
  - API endpoints
  - Requirements.txt
  - Python-specific .gitignore
- Static Website (HTML/CSS/JS) template with:
  - Modern HTML5 structure
  - Beautiful gradient styling
  - Responsive CSS design
  - JavaScript ready
- React Application template with:
  - React 18 setup
  - React Scripts for development
  - Modern component structure
  - Professional styling
- `projectmaker list` command to show available templates
- Comprehensive README.md with installation and usage instructions
- EXAMPLES.md with detailed usage examples
- CONTRIBUTING.md with contribution guidelines
- ISC LICENSE file
- Beautiful CLI output with colors (using chalk)
- Interactive prompts (using inquirer)
- Command-line interface (using commander)
- Automatic .gitignore generation for each project type
- Automatic README.md generation for each project

### Security

- No security vulnerabilities detected (CodeQL checked)
- All dependencies are up to date
- Proper error handling for file operations

[1.0.0]: https://github.com/firot1993/projectMaker/releases/tag/v1.0.0
