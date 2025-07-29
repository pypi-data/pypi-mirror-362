# TestZeus CLI

A powerful command-line interface for the TestZeus testing platform.

## Installation

```bash
pip install testzeus-cli
```

## Authentication

Before using the CLI, you need to authenticate with the TestZeus platform:

```bash
testzeus login
```

You will be prompted to enter your email and password. Your credentials are securely stored in your system's keyring.

```bash
testzeus login --profile dev
```

Authentication automatically detects and stores your tenant information, which will be used for all subsequent commands.

### Auth Commands

| Command | Description |
|---------|-------------|
| `login` | Authenticate with TestZeus |
| `logout` | Log out and remove stored credentials |
| `whoami` | Display current authentication status |

## Global Options

The following options can be used with any command:

| Option | Description |
|--------|-------------|
| `--profile` | Configuration profile to use (default: "default") |
| `--api-url` | Custom TestZeus API URL |
| `--verbose` | Enable verbose output |
| `--format` | Output format: json, table, or yaml (default: table) |

## Managing Tests

### List Tests

```bash
testzeus tests list
```

Filter test list with key-value pairs:
```bash
testzeus tests list --filters status=draft
```

Sort and expand related entities:
```bash
testzeus tests list --sort created --expand tags,test_data
```

### Get Test Details

```bash
testzeus tests get <test-id>
testzeus tests get <test-id> --expand tags,test_data
```

### Create Test

Create a test with text-based features:

```bash
testzeus tests create --name "My Test" --feature "Feature: Test something"
```

Create a test with features from a file:

```bash
testzeus tests create --name "My Test" --feature-file ./features.txt
```

Additional options:
```bash
testzeus tests create --name "My Test" --feature-file ./features.txt --status ready --data data_id1 --data data_id2 --tags tag1 --tags tag2 --environment env_id --execution-mode strict
```

### Update Test

Update test name:

```bash
testzeus tests update <test-id> --name "New Name"
```

Update test features from text:

```bash
testzeus tests update <test-id> --feature "Updated feature content"
```

Update test features from a file:

```bash
testzeus tests update <test-id> --feature-file ./updated_features.txt
```

Update other properties:
```bash
testzeus tests update <test-id> --status ready --data data_id1 --tags tag1 --environment env_id
```

### Delete Test

```bash
testzeus tests delete <test-id>
```

## Test Runs

### List Test Runs

```bash
testzeus test-runs list
```

Filter runs by status:

```bash
testzeus test-runs list --filters status=running
```

### Get Test Run Details

```bash
testzeus test-runs get <run-id>
```

Get expanded details including all outputs and steps:

```bash
testzeus test-runs get-expanded <run-id>
```

### Create and Start Test Run

```bash
testzeus test-runs create --name "Run 1" --test <test-id>
```

Create test run with environment or tag:

```bash
testzeus test-runs create --name "Run 1" --test <test-id> --env <env-id> --tag <tag-name>
```

### Cancel Test Run

```bash
testzeus test-runs cancel <run-id>
```

### Watch Test Run Progress

```bash
testzeus test-runs watch <run-id>
testzeus test-runs watch <run-id> --interval 10
```

### Get Test Run Status

```bash
testzeus test-runs status <run-id>
```

### Download Test Run Attachments

```bash
testzeus test-runs download-attachments <run-id>
testzeus test-runs download-attachments <run-id> --output-dir ./my-attachments
```

## Test Data

### List Test Data

```bash
testzeus test-data list
```

Filter by type:
```bash
testzeus test-data list --filters type=test
```

### Get Test Data Details

```bash
testzeus test-data get <data-id>
testzeus test-data get <data-id> --expand related_entities
```

### Create Test Data

Create with inline content:

```bash
testzeus test-data create --name "Test Data 1" --data "{\"key\":\"value\"}"
```

Create with data from a file:

```bash
testzeus test-data create --name "Test Data" --data-file ./data.json
```

Additional options:
```bash
testzeus test-data create --name "Test Data" --type test --status ready --data-file ./data.json
```

### Update Test Data

Update name and other properties:

```bash
testzeus test-data update <data-id> --name "New Data Name" --type updated --status ready
```

Update data content from text:

```bash
testzeus test-data update <data-id> --data "{\"key\":\"updated\"}"
```

Update data content from a file:

```bash
testzeus test-data update <data-id> --data-file ./updated_data.json
```

### Delete Test Data

```bash
testzeus test-data delete <data-id>
```

### File Management for Test Data

Upload a file to test data:

```bash
testzeus test-data upload-file <data-id> <file-path>
```

Delete all files from test data:

```bash
testzeus test-data delete-all-files <data-id>
```

## Environments

### List Environments

```bash
testzeus environments list
```

Filter environments:
```bash
testzeus environments list --filters status=ready
```

### Get Environment Details

```bash
testzeus environments get <env-id>
testzeus environments get <env-id> --expand related_entities
```

### Create Environment

Create with inline data:

```bash
testzeus environments create --name "Test Environment" --data "{\"key\":\"value\"}"
```

Create with data from a file:

```bash
testzeus environments create --name "Test Environment" --data-file ./env_data.json
```

Additional options:
```bash
testzeus environments create --name "Test Environment" --status ready --data-file ./env_data.json --tags "tag1,tag2"
```

### Update Environment

Update environment properties:

```bash
testzeus environments update <env-id> --name "New Name" --status ready
```

Update environment data:

```bash
testzeus environments update <env-id> --data "{\"key\":\"updated\"}"
testzeus environments update <env-id> --data-file ./updated_env_data.json
```

### Delete Environment

```bash
testzeus environments delete <env-id>
```

### File Management for Environments

Upload a file to environment:

```bash
testzeus environments upload-file <env-id> <file-path>
```

Remove a file from environment:

```bash
testzeus environments remove-file <env-id> <file-path>
```

Delete all files from environment:

```bash
testzeus environments delete-all-files <env-id>
```

## Tags

### List Tags

```bash
testzeus tags list
```

Filter tags:
```bash
testzeus tags list --filters name=test
```

### Get Tag Details

```bash
testzeus tags get <tag-id>
```

### Create Tag

```bash
testzeus tags create --name "test-tag" --value "test-value"
```

Create tag without value:

```bash
testzeus tags create --name "simple-tag"
```

### Update Tag

```bash
testzeus tags update <tag-id> --name "new-name" --value "new-value"
```

### Delete Tag

```bash
testzeus tags delete <tag-name>
```

## Configuration

The CLI stores configuration and credentials in your user's config directory. Different profiles can be used to manage multiple TestZeus environments.

Default configuration location:
- Linux/Mac: `~/.testzeus/config.yaml`
- Windows: `%APPDATA%\testzeus\config.yaml`

Passwords are securely stored in your system's keyring.

## Examples

### Complete Workflow

```bash
# Login to TestZeus
testzeus login

# Create test data
testzeus test-data create --name "User Data" --data "{\"username\":\"testuser\"}" 

# Create a new test with features from a file
testzeus tests create --name "Login Test" --feature-file ./features/login.feature --data <test_data_id>

# Run the test
testzeus test-runs create --name "Login Run 1" --test <test_id>

# Watch the test run progress
testzeus test-runs watch <test_run_id>

# Check detailed results
testzeus test-runs get-expanded <test_run_id>

# Download any attachments generated during the run
testzeus test-runs download-attachments <test_run_id> --output-dir ./results
```

### Working with Environments

```bash
# Create an environment with data
testzeus environments create --name "Production Environment" --data-file ./prod_config.json --status ready

# Upload additional files to the environment
testzeus environments upload-file <env-id> ./additional_config.yaml

# Create a test that uses the environment
testzeus tests create --name "Production Test" --feature-file ./test.feature --environment <env-id>
```

### Managing Tags

```bash
# Create tags for organizing tests
testzeus tags create --name "regression" --value "suite"
testzeus tags create --name "priority" --value "high"

# Create a test with tags
testzeus tests create --name "Critical Test" --feature-file ./critical.feature --tags tag1 --tags tag2
```

## Error Handling

When an error occurs, the CLI will display an error message. For more detailed information, run any command with the `--verbose` flag:

```bash
testzeus tests list --verbose
```

## Output Formats

The CLI supports multiple output formats:

- `table`: Human-readable tabular format (default)
- `json`: JSON format for programmatic usage
- `yaml`: YAML format

Example:
```bash
testzeus tests list --format json
```

## Development and Contribution

To contribute to the TestZeus CLI, fork the repository and install development dependencies:

```bash
pip install -e ".[dev]"
```

### Release Process

The TestZeus CLI uses GitHub Actions for automated releases to PyPI. To create a release:

1. Use the Makefile's release target: `make release`
2. This will:
   - Prompt for version bump type (patch, minor, major)
   - Update the version in pyproject.toml
   - Commit and create a git tag
   - Push changes and tags to GitHub
3. The tag push will automatically trigger the GitHub Actions publish workflow 