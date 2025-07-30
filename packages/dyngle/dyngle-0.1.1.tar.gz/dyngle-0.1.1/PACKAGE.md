# Dyngle

## Run lightweight local workflows

Dyngle is a simple workflow runner that executes sequences of commands defined in configuration files. It's like a lightweight combination of Make and a task runner, designed for automating common development and operational tasks.

## Basic usage

Create a configuration file (e.g., `config.yml`) with your workflows:

```yaml
dyngle:
  flows:
    build:
      - python -m pip install -e .
      - python -m pytest
    deploy:
      - docker build -t myapp .
      - docker push myapp
    clean:
      - rm -rf __pycache__
      - rm -rf .pytest_cache
```

Run a workflow:

```bash
dyngle --config config.yml run build
```

## Configuration

Dyngle reads configuration from YAML files. You can specify the config file location using:

- `--config` command line option
- `DYNGLE_CONFIG` environment variable  
- `.dyngle.yml` in current directory
- `~/.dyngle.yml` in home directory

## Workflow structure

Each workflow (called a "flow") is defined as a list of tasks under `dyngle.flows`. Tasks are executed sequentially using Python's subprocess module for security.

Example with multiple flows:

```yaml
dyngle:
  flows:
    test:
      - python -m unittest discover
      - python -m coverage report
    docs:
      - sphinx-build docs docs/_build
      - open docs/_build/index.html
    setup:
      - python -m venv venv
      - source venv/bin/activate
      - pip install -r requirements.txt
```

## Security

Commands are executed using Python's `subprocess.run()` with arguments split by spaces. The shell is not used, preventing shell injection attacks.

## Quick installation (MacOS)

```bash
brew install python@3.11
python3.11 -m pip install pipx
pipx install kwark
```
