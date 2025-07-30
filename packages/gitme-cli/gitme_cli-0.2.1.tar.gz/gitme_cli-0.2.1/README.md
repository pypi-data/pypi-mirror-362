# A git commit message generator.

```bash
git commit -a -m "ugh... what did I do? what do I even say here?"
```
➤
```bash
gitme -c
```

```bash
gitme show -n 5
```

![gitme-cli](https://github.com/wangjing0/gitme/raw/main/commits.png)

## Features

- Analyzes git diffs to generate contextually relevant commit messages
- Supports staged changes only or all modified files
- Saves message history for review
- Direct commit creation with confirmation
- Multiple Claude model options
- Repository-specific message storage

## Installation

Install from PyPI:

```bash
pip install gitme-cli
```

Or install directly from GitHub:

```bash
pip install git+https://github.com/wangjing0/gitme.git
```

Or install from source:

```bash
git clone https://github.com/wangjing0/gitme.git
cd gitme
pip install -e .
```

## Setup

Set Anthropic API key if not already set in your environment:

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

## Usage

### Basic Usage

```bash
# Generate message for staged changes (default)
gitme

# Generate message for all changes
gitme -a

# Generate message and commit
gitme -c

# Use different model
gitme -m claude-3-haiku-20240307
```

### Message History

```bash
# Show previous messages
gitme show

# Show last 5 messages
gitme show -n 5

# Show from all repositories
gitme show -r

# Clear history
gitme show --clear
```

## Options

### Generate Options

- `-s, --staged`: Analyze only staged changes
- `-a, --all`: Analyze all changes (staged and unstaged)
- `-m, --model`: Claude model to use
- `-c, --commit`: Create commit with generated message (uses `git commit -a -m "auto-generated message"`)

### Show Options

- `-n, --limit`: Number of messages to show
- `-r, --all-repos`: Show messages from all repositories
- `--clear`: Clear message history

## Requirements

- Python 3.8+
- Git
- Anthropic API key

## License

MIT