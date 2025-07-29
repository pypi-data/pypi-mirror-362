# jbussdieker-config

A modern Python development toolkit plugin for managing configuration settings within the jbussdieker CLI framework. This plugin provides a simple and intuitive way to view, set, and manage configuration values for the jbussdieker ecosystem.

## 🚀 Features

- **Configuration Management**: View and modify configuration settings for jbussdieker plugins
- **JSON-Based Storage**: Persistent configuration stored in JSON format
- **Custom Settings**: Support for custom configuration values beyond built-in settings
- **Type-Aware**: Automatic type conversion for boolean, string, and other data types
- **Environment Override**: Configurable config file location via environment variables
- **Default Values**: Sensible defaults for common development settings

## 📦 Installation

```bash
pip install jbussdieker-config --upgrade
```

## 🔧 Prerequisites

- Python 3.9 or higher
- jbussdieker CLI framework

## 🎯 Usage

### View Current Configuration

Display all current configuration settings:

```bash
jbussdieker config
```

### Set Configuration Values

Set a configuration value using the `KEY=VALUE` format:

```bash
jbussdieker config --set user_name="John Doe"
jbussdieker config --set user_email="john@example.com"
jbussdieker config --set private=false
```

### Custom Settings

Set custom configuration values that aren't part of the built-in settings:

```bash
jbussdieker config --set custom_setting="value"
```

## 📋 Configuration Settings

The plugin manages the following built-in configuration settings:

### User Information
- `user_name`: Your full name (default: "Joshua B. Bussdieker")
- `user_email`: Your email address (default: "jbussdieker@gmail.com")
- `github_org`: Your GitHub organization (default: "jbussdieker")

### Project Settings
- `private`: Whether projects should be private by default (default: true)
- `storage_url`: URL for storage configuration
- `openai_api_key`: OpenAI API key for AI-powered features

### Logging Configuration
- `log_level`: Logging level (default: "INFO")
- `log_format`: Log format string (default: "%(levelname)s: %(message)s")

### Custom Settings
- `custom_settings`: Dictionary for storing custom configuration values

## 🔍 How It Works

1. **Configuration Storage**: Settings are stored in `~/.jbussdieker.json` by default
2. **Environment Override**: Use `JBUSSDIEKER_CONFIG` environment variable to specify a custom config file path
3. **Type Conversion**: Boolean values are automatically converted from string representations
4. **Persistence**: Changes are immediately saved to the configuration file
5. **Validation**: Built-in settings are validated against expected types

## 🛠️ Development

This plugin is part of the jbussdieker ecosystem. It integrates seamlessly with the jbussdieker CLI framework.

### Project Structure

```
src/jbussdieker/config/
├── __init__.py      # Package initialization and version
├── cli.py           # CLI interface and argument parsing
└── config.py        # Configuration management and storage
```

### Configuration File Location

By default, the configuration is stored in:
- `~/.jbussdieker.json`

You can override this by setting the `JBUSSDIEKER_CONFIG` environment variable:

```bash
export JBUSSDIEKER_CONFIG="/path/to/custom/config.json"
```

## 📝 License

This project is licensed under **MIT**.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📚 Related

- [jbussdieker](https://pypi.org/project/jbussdieker/) - The main CLI framework
- [jbussdieker-commit](https://pypi.org/project/jbussdieker-commit/) - AI-powered commit message generation
