# Novara cli

This is the cli for the novara api

## Commands

### configure

This command configures the cli to use a server and fetches some configs from it

### generate

This command will regenerate the Dockerfile from the novara.toml. Additionally the command can add dependencies to the toml file.

### init

This command initializes a new directory with a template already configured for the given service

### run

This command can either run the exploit locally or upload it to remote to execute it.

### status

This command will retreive the info for a container or optionally all containers including their current health

### stop

This command stops the currently running remote container.

### remove

This command will delete a exploit.

## Installation

```sh
poetry build -f wheel
pip install dist/*.whl
```

The cli can then be access by running `novara [OPTIONS] command` in your terminal.

# Development

To install the cli for development use, use

```sh
poetry install
poetry shell
```

- configs.py manages all the configurations for the cli.
- main.py manages all available commands.
- all commands are implemented in a file name command_name.py in commands/
- utils.py contains some usefull helpers like a Logger class
