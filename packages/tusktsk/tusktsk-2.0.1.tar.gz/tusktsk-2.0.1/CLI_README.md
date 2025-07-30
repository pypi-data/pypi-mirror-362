# TuskLang Python SDK CLI

A comprehensive command-line interface for the TuskLang Python SDK, providing powerful tools for development, testing, configuration management, AI integration, and more.

## 🚀 Quick Start

### Installation

```bash
# Run the setup script
python setup_cli.py

# Or install manually
pip install -r requirements.txt
python -m cli.main
```

### Basic Usage

```bash
# Check version
tsk version

# Get help
tsk help

# Interactive mode
tsk
```

## 📋 Available Commands

### 📊 Database Operations

```bash
# Check database connection status
tsk db status

# Run migration file
tsk db migrate schema.sql

# Open interactive database console
tsk db console

# Backup database
tsk db backup backup.sql

# Restore from backup
tsk db restore backup.sql

# Initialize SQLite database
tsk db init
```

### 🚀 Development

```bash
# Start development server
tsk serve 3000

# Compile .tsk file
tsk compile app.tsk

# Optimize .tsk file for production
tsk optimize app.tsk
```

### 🧪 Testing

```bash
# Run all tests
tsk test all

# Run specific test suite
tsk test parser
tsk test fujsen
tsk test sdk
tsk test performance

# Run with specific flags
tsk test --parser
tsk test --fujsen
tsk test --sdk
tsk test --performance
```

### 🔧 Services

```bash
# Start all TuskLang services
tsk services start

# Stop all services
tsk services stop

# Restart all services
tsk services restart

# Show service status
tsk services status
```

### 💾 Cache Management

```bash
# Clear all caches
tsk cache clear

# Show cache status and statistics
tsk cache status

# Pre-warm caches
tsk cache warm

# Memcached operations
tsk cache memcached status
tsk cache memcached stats
tsk cache memcached flush
tsk cache memcached restart
tsk cache memcached test

# Show distributed cache status
tsk cache distributed
```

### ⚙️ Configuration

```bash
# Get configuration value by path
tsk config get server.port

# Check configuration hierarchy
tsk config check .

# Validate entire configuration chain
tsk config validate

# Auto-compile all peanu.tsk files
tsk config compile

# Generate configuration documentation
tsk config docs

# Clear configuration cache
tsk config clear-cache

# Show configuration performance statistics
tsk config stats
```

### 🔢 Binary Operations

```bash
# Compile to binary format (.tskb)
tsk binary compile app.tsk

# Execute binary file directly
tsk binary execute app.tskb

# Compare binary vs text performance
tsk binary benchmark app.tsk

# Optimize binary for production
tsk binary optimize app.tskb
```

### 🤖 AI Operations

```bash
# Query Claude AI
tsk ai claude "Hello, how are you?"

# Query ChatGPT
tsk ai chatgpt "Explain TuskLang"

# Query custom AI API
tsk ai custom https://api.example.com/ai "Custom prompt"

# Show AI configuration
tsk ai config

# Interactive AI setup
tsk ai setup

# Test all configured AI connections
tsk ai test

# AI-powered code completion
tsk ai complete app.tsk 10 5

# AI code analysis
tsk ai analyze app.tsk

# AI performance optimization
tsk ai optimize app.tsk

# AI security scan
tsk ai security app.tsk
```

### 🛠️ Utilities

```bash
# Parse and display TSK file contents
tsk parse config.tsk

# Validate TSK file syntax
tsk validate config.tsk

# Convert between formats
tsk convert -i input.tsk -o output.json
tsk convert -i input.json -o output.tsk
tsk convert -i input.tsk -o output.yaml
tsk convert -i input.yaml -o output.tsk

# Get value by key path
tsk get config.tsk server.port

# Set value by key path
tsk set config.tsk server.port 8080

# Show version information
tsk version

# Show help for specific command
tsk help db
tsk help ai
```

## 🔧 Global Options

All commands support these global options:

```bash
--verbose, -v          # Enable verbose output
--quiet, -q            # Suppress non-error output
--json                 # Output in JSON format
--config <file>        # Use alternate config file
```

## 🎯 Examples

### Development Workflow

```bash
# Start development server
tsk serve 3000

# In another terminal, run tests
tsk test all

# Check database status
tsk db status

# Validate configuration
tsk config validate
```

### AI-Powered Development

```bash
# Set up AI services
tsk ai setup

# Get AI help with code
tsk ai claude "How do I optimize this TuskLang code?"

# Get code completion
tsk ai complete app.tsk 15 10

# Analyze code for issues
tsk ai analyze app.tsk

# Get security scan
tsk ai security app.tsk
```

### Configuration Management

```bash
# Get server configuration
tsk config get server.port

# Check configuration hierarchy
tsk config check .

# Compile all configuration files
tsk config compile

# Generate documentation
tsk config docs
```

### File Operations

```bash
# Parse and validate file
tsk parse config.tsk
tsk validate config.tsk

# Convert between formats
tsk convert -i config.tsk -o config.json

# Get specific values
tsk get config.tsk database.host
tsk set config.tsk database.port 5432
```

## 🔧 Configuration

### AI Configuration

AI services are configured in `~/.tsk/ai_config.json`:

```json
{
  "claude_api_key": "your-claude-api-key",
  "chatgpt_api_key": "your-chatgpt-api-key"
}
```

### Environment Variables

- `TSK_CONFIG_PATH`: Path to configuration directory
- `TSK_VERBOSE`: Enable verbose output
- `TSK_JSON_OUTPUT`: Always output in JSON format

## 🚀 Advanced Features

### Interactive Mode

Run `tsk` without arguments to enter interactive mode:

```bash
tsk> db status
tsk> test all
tsk> ai claude "Hello"
tsk> exit
```

### JSON Output

Use `--json` flag for machine-readable output:

```bash
tsk --json db status
tsk --json config get server.port
tsk --json ai claude "Hello"
```

### Bash Completion

Add to your `~/.bashrc`:

```bash
source ~/.tsk/tsk-completion.bash
```

Then enjoy tab completion for all commands and subcommands.

## 🔍 Troubleshooting

### Common Issues

1. **Import Errors**: Make sure you're running from the correct directory
2. **Permission Errors**: Use `sudo` for global installation
3. **AI API Errors**: Run `tsk ai setup` to configure API keys
4. **Database Errors**: Check database connection with `tsk db status`

### Debug Mode

Enable verbose output for debugging:

```bash
tsk --verbose db status
tsk --verbose test all
```

### Getting Help

```bash
# General help
tsk help

# Command-specific help
tsk help db
tsk help ai
tsk help config

# Version information
tsk version
```

## 📚 API Reference

### Database Commands

- `tsk db status`: Check database connection status
- `tsk db migrate <file>`: Run migration file
- `tsk db console`: Open interactive database console
- `tsk db backup [file]`: Backup database
- `tsk db restore <file>`: Restore from backup
- `tsk db init`: Initialize SQLite database

### AI Commands

- `tsk ai claude <prompt>`: Query Claude AI
- `tsk ai chatgpt <prompt>`: Query ChatGPT
- `tsk ai custom <api> <prompt>`: Query custom AI API
- `tsk ai config`: Show AI configuration
- `tsk ai setup`: Interactive AI setup
- `tsk ai test`: Test AI connections
- `tsk ai complete <file> [line] [col]`: AI code completion
- `tsk ai analyze <file>`: AI code analysis
- `tsk ai optimize <file>`: AI performance optimization
- `tsk ai security <file>`: AI security scan

### Configuration Commands

- `tsk config get <key_path> [dir]`: Get configuration value
- `tsk config check [path]`: Check configuration hierarchy
- `tsk config validate [path]`: Validate configuration
- `tsk config compile [path]`: Auto-compile peanu.tsk files
- `tsk config docs [path]`: Generate documentation
- `tsk config clear-cache [path]`: Clear configuration cache
- `tsk config stats`: Show performance statistics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- Documentation: [TuskLang Docs](https://tusklang.org/docs)
- Issues: [GitHub Issues](https://github.com/cyber-boost/python-sdk/issues)
- Community: [TuskLang Discord](https://discord.gg/tusklang) 