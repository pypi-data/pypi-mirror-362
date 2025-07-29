# jbussdieker-service

A modern Python development toolkit plugin for managing systemd services. This plugin integrates with the jbussdieker CLI framework to provide easy systemd service installation and management capabilities.

## 🚀 Features

- **Systemd Service Installation**: Automatically creates and configures systemd service files
- **Service Management**: Provides commands to install and manage jbussdieker services
- **CLI Integration**: Seamlessly integrates with the jbussdieker CLI framework
- **Automatic Restart**: Configures automatic restart on failure with configurable intervals
- **Logging Integration**: Proper logging configuration with journald integration
- **User Management**: Configures proper user and group permissions

## 📦 Installation

```bash
pip install jbussdieker-service --upgrade
```

## 🔧 Prerequisites

- Python 3.9 or higher
- Linux system with systemd
- jbussdieker CLI framework installed
- Appropriate user permissions for systemd service management

## 🎯 Usage

### Install Systemd Service

Install the jbussdieker service as a systemd service:

```bash
jbussdieker service install
```

This command will:
- Create a systemd service file at `/etc/systemd/system/jbussdieker.service`
- Configure the service with proper restart policies
- Set up logging to journald
- Configure user and group permissions

### Start the Service

After installation, you can manage the service using standard systemd commands:

```bash
# Start the service
sudo systemctl start jbussdieker

# Enable the service to start on boot
sudo systemctl enable jbussdieker

# Check service status
sudo systemctl status jbussdieker

# View service logs
sudo journalctl -u jbussdieker -f
```

## 🔍 How It Works

1. **Service Installation**: Creates a systemd service file with proper configuration
2. **Service Configuration**: Sets up restart policies, logging, and user permissions
3. **Integration**: Integrates with the jbussdieker CLI framework for seamless operation
4. **Monitoring**: Provides continuous service operation with proper logging

## 🛠️ Development

This plugin is part of the jbussdieker ecosystem. It integrates seamlessly with the jbussdieker CLI framework.

### Project Structure

```
src/jbussdieker/service/
├── __init__.py
└── cli.py          # CLI interface and service management
```

### Service Configuration

The plugin creates a systemd service with the following configuration:

- **Type**: Simple service
- **Restart Policy**: Restart on failure with 5-second intervals
- **User**: jbussdieker
- **Group**: jbussdieker
- **Working Directory**: /tmp
- **Logging**: Integrated with systemd journal

## 📝 License

This project is licensed under **MIT**.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📚 Related

- [jbussdieker](https://pypi.org/project/jbussdieker/) - The main CLI framework
- [systemd](https://systemd.io/) - System and service manager
