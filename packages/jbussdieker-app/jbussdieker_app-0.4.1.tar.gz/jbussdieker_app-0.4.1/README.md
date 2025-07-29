# jbussdieker-app

A modern Python development toolkit plugin for creating and managing Flask web applications. This plugin integrates with the jbussdieker CLI framework to provide a streamlined development experience for Flask applications.

## 🚀 Features

- **Flask Application Generator**: Quickly create and run Flask applications
- **Bootstrap Integration**: Built-in Bootstrap 5 support for modern UI components
- **Health Check Endpoint**: Automatic `/healthz` endpoint for monitoring
- **Development Server**: Easy-to-use development server with configurable host
- **CLI Integration**: Seamless integration with the jbussdieker CLI framework
- **Modern Python**: Built with Python 3.9+ and modern Flask practices

## 📦 Installation

```bash
pip install jbussdieker-app --upgrade
```

## 🔧 Prerequisites

- Python 3.9 or higher
- jbussdieker CLI framework
- Flask and related dependencies (automatically installed)

## 🎯 Usage

### Basic Usage

Create and run a Flask application:

```bash
jbussdieker app
```

This will start a Flask development server on `http://0.0.0.0:9000`.

### Custom Host Configuration

Specify a custom host for the development server:

```bash
jbussdieker app --host 127.0.0.1
```

### Available Endpoints

- **Root (`/`)**: Displays application version information
- **Health Check (`/healthz`)**: Returns "OK" for health monitoring

## 🏗️ Project Structure

The plugin creates a Flask application with the following structure:

```
src/jbussdieker/app/
├── __init__.py      # Package initialization
├── cli.py           # CLI interface and argument parsing
├── factory.py       # Flask application factory
└── blueprint.py     # Route definitions and views
```

## 🔍 How It Works

1. **CLI Registration**: Registers the `app` command with jbussdieker CLI
2. **Application Factory**: Uses Flask's application factory pattern for clean architecture
3. **Bootstrap Integration**: Automatically configures Bootstrap 5 for modern styling
4. **Blueprint Registration**: Organizes routes using Flask blueprints
5. **Development Server**: Runs the Flask development server with configurable options

## 🛠️ Development

This plugin is part of the jbussdieker ecosystem. It integrates seamlessly with the jbussdieker CLI framework.

### Dependencies

- Flask: Web framework
- Bootstrap-Flask: Bootstrap 5 integration
- Flask-SQLAlchemy: Database ORM (available for future use)

### Extending the Application

You can extend the Flask application by:

1. Adding new routes to `blueprint.py`
2. Creating additional blueprints for modular organization
3. Configuring database models with Flask-SQLAlchemy
4. Adding custom middleware or extensions

## 📝 License

This project is licensed under **MIT**.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📚 Related

- [jbussdieker](https://pypi.org/project/jbussdieker/) - The main CLI framework
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [Bootstrap](https://getbootstrap.com/) - CSS framework
