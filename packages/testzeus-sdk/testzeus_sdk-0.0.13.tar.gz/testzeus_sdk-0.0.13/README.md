# TestZeus SDK

Python SDK for the TestZeus testing platform.

## Installation

Install the package using pip:

```bash
pip install testzeus-sdk
```

Or use Poetry:

```bash
poetry add testzeus-sdk
```

## Components

### Python SDK
The TestZeus SDK provides programmatic access to the TestZeus testing platform through a Python interface.

### Command Line Interface (CLI)
The TestZeus CLI provides a command-line interface for interacting with the TestZeus platform. For detailed CLI documentation, see the [CLI README](testzeus-cli/README.md).

```bash
# Install CLI
pip install testzeus-cli

# Login to TestZeus
testzeus login

# List tests
testzeus tests list
```

## Getting Started with SDK

```python
import asyncio
from testzeus_sdk import TestZeusClient

async def main():
    # Create a client with email/password
    client = TestZeusClient(email="your-email", password="your-password")
    
    # Use as a context manager
    async with client:
        # Your code here
        pass

# Run the example
asyncio.run(main())
```

## Authentication

The SDK supports three authentication methods:

### Email/Password

```python
client = TestZeusClient(email="your-email", password="your-password")
```

### Environment Variables

```
export TESTZEUS_EMAIL="your-email"
export TESTZEUS_PASSWORD="your-password"
```

Then create the client without parameters:

```python
client = TestZeusClient()
```

## Core Functionality

### Tests Management

#### List Tests
```python
# Get list of tests with filters and sorting
tests = await client.tests.get_list(
    expand='tags',  # Expand related entities
    sort='id',      # Sort by field
    filters={       # Filter results
        'id': 'y9b88f17vabx476'
    }
)
print(tests)
print(tests['items'][0].data)  # Access test data
```

#### Advanced Filtering

The SDK supports powerful filtering capabilities using PocketBase filter syntax. All managers that extend `BaseManager` support these filtering options:

##### Simple Filters (Backward Compatible)
```python
# Basic field matching
filters = {
    "name": "Test Name",
    "status": "active",
    "priority": 5
}

# List values (OR condition)
filters = {
    "status": ["active", "pending", "draft"]  # status = "active" OR status = "pending" OR status = "draft"
}
```

##### Advanced Operators
```python
# Use complex operators with value objects
filters = {
    "created": {"operator": ">", "value": "2023-01-01"},           # created > "2023-01-01"
    "priority": {"operator": ">=", "value": 3},                   # priority >= 3
    "name": {"operator": "~", "value": "test"},                   # name LIKE "%test%"
    "description": {"operator": "!~", "value": "old"}            # description NOT LIKE "%old%"
}
```

##### Supported Operators

**Comparison Operators:**
- `=` - Equal (default when no operator specified)
- `!=` - Not equal
- `>` - Greater than
- `>=` - Greater than or equal
- `<` - Less than
- `<=` - Less than or equal

**String Operators:**
- `~` - Like/Contains (auto-wraps with % for wildcard matching)
- `!~` - Not Like/Contains

**Array Operators (for multi-value fields):**
- `?=` - Any/At least one equal
- `?!=` - Any/At least one not equal
- `?>` - Any/At least one greater than
- `?>=` - Any/At least one greater than or equal
- `?<` - Any/At least one less than
- `?<=` - Any/At least one less than or equal
- `?~` - Any/At least one like/contains
- `?!~` - Any/At least one not like/contains

##### Array Operators with Lists
```python
# Check if any tag matches the values
filters = {
    "tags": {"operator": "?=", "value": ["urgent", "important"]}
}
# Result: (tags ?= "urgent" || tags ?= "important")
```

##### Logical Grouping

**AND Conditions:**
```python
filters = {
    "$and": [
        {"status": "active"},
        {"priority": {"operator": ">", "value": 3}},
        {"created": {"operator": ">", "value": "2023-01-01"}}
    ]
}
# Result: (status = "active" && priority > 3 && created > "2023-01-01")
```

**OR Conditions:**
```python
filters = {
    "$or": [
        {"status": "urgent"},
        {"priority": {"operator": ">=", "value": 8}}
    ]
}
# Result: (status = "urgent" || priority >= 8)
```

**Complex Combinations:**
```python
filters = {
    "tenant": "abc123",  # Always filter by current tenant
    "$or": [
        {"status": "active"},
        {
            "$and": [
                {"status": "draft"},
                {"modified": {"operator": ">", "value": "2023-01-01"}},
                {"tags": {"operator": "?=", "value": ["review", "pending"]}}
            ]
        }
    ]
}
# Result: tenant = "abc123" && (status = "active" || (status = "draft" && modified > "2023-01-01" && (tags ?= "review" || tags ?= "pending")))
```

##### Practical Examples

**Filter tests by date range:**
```python
tests = await client.tests.get_list(
    filters={
        "$and": [
            {"created": {"operator": ">=", "value": "2023-01-01"}},
            {"created": {"operator": "<", "value": "2023-12-31"}}
        ]
    }
)
```

**Filter by multiple statuses and search in name:**
```python
tests = await client.tests.get_list(
    filters={
        "status": ["active", "pending"],
        "name": {"operator": "~", "value": "integration"}
    }
)
```

**Filter test runs by status and date:**
```python
test_runs = await client.test_runs.get_list(
    filters={
        "$and": [
            {"status": {"operator": "!=", "value": "draft"}},
            {"start_time": {"operator": ">", "value": "2023-01-01T00:00:00Z"}}
        ]
    },
    sort="-created"  # Sort by created date descending
)
```

**Filter environments by tags:**
```python
environments = await client.environments.get_list(
    filters={
        "tags": {"operator": "?=", "value": ["production", "staging"]}
    }
)
```

#### Get Single Test
```python
# Get test by ID
test = await client.tests.get_one('311137kown88nd6')
print(test.data)
```

#### Create Test
```python
# Create a new test
new_test = await client.tests.create(
    name="New Test",
    test_feature="Example feature",
    status="draft",  # Optional: 'draft', 'ready', 'deleted'
    test_data=["data_id1", "data_id2"],  # Optional: List of test data IDs
    tags=["tag1", "tag2"],  # Optional: List of tag IDs
    environment="env_id"  # Optional: Environment ID
)
```

#### Update Test
```python
# Update test properties
updated_test = await client.tests.update(
    'test_id',
    name='Updated Test Name'
)
print(updated_test.data)
```

#### Delete Test
```python
# Delete a test
await client.tests.delete('test_id')
```

### Test Runs Management

#### Create and Start Test Run
```python
# Create and start a test run
test_run = await client.test_runs.create_and_start(
    name="Test Run Name",
    test="Test Name or ID"
)
print(test_run.data)
```

#### Track Test Run Status
```python
# Get test run by ID
test_run = await client.test_runs.get_one('test_run_id')

# Check test run status
if test_run.is_running():
    print("Test is currently running")
elif test_run.is_completed():
    print("Test has completed successfully")
elif test_run.is_failed():
    print("Test has failed")
elif test_run.is_crashed():
    print("Test has crashed")
elif test_run.is_cancelled():
    print("Test was cancelled")
elif test_run.is_pending():
    print("Test is pending")

# Get test run duration
duration = test_run.get_duration()
if duration:
    print(f"Test run took {duration} seconds")
```

#### Get Detailed Test Run Information
```python
# Get expanded test run details including all outputs, steps, and attachments
expanded_test_run = await client.test_runs.get_expanded('test_run_id')

# Access different components of the test run
test_run_data = expanded_test_run['test_run']
test_run_dashs = expanded_test_run['test_run_dashs']
test_run_dash_outputs = expanded_test_run['test_run_dash_outputs']
test_run_dash_output_steps = expanded_test_run['test_run_dash_output_steps']
test_run_dash_outputs_attachments = expanded_test_run['test_run_dash_outputs_attachments']

# Print test run details
print(f"Test Run Name: {test_run_data['name']}")
print(f"Status: {test_run_data['status']}")
print(f"Start Time: {test_run_data['start_time']}")
print(f"End Time: {test_run_data['end_time']}")

# Print test run steps
for step in test_run_dash_output_steps:
    print(f"Step: {step['name']}")
    print(f"Status: {step['status']}")
    print(f"Is Passed: {step['is_passed']}")
    print(f"Assert Summary: {step['assert_summary']}")
```

#### Cancel Test Run
```python
# Cancel a running test
try:
    cancelled_test = await client.test_runs.cancel('test_run_id')
    print(f"Test run cancelled: {cancelled_test.status}")
except ValueError as e:
    print(f"Cannot cancel test: {str(e)}")
```

#### Download Test Run Attachments
```python
# Download all attachments for a test run
download_attachment = await client.test_runs.download_all_attachments(
    'test_run_id',
    'local/path/to/save'
)

# Download specific attachment
attachment = await client.test_run_dash_outputs_attachments.download_attachment(
    'attachment_id',
    'local/path/to/save'
)
```

#### Monitor Test Run Progress
```python
import asyncio
import time

async def monitor_test_run(test_run_id: str, check_interval: int = 5):
    """
    Monitor a test run's progress until completion
    
    Args:
        test_run_id: ID of the test run to monitor
        check_interval: Time between status checks in seconds
    """
    while True:
        test_run = await client.test_runs.get_one(test_run_id)
        
        if test_run.is_completed():
            print("Test run completed successfully!")
            break
        elif test_run.is_failed():
            print("Test run failed!")
            break
        elif test_run.is_crashed():
            print("Test run crashed!")
            break
        elif test_run.is_cancelled():
            print("Test run was cancelled!")
            break
            
        print(f"Test run status: {test_run.status}")
        await asyncio.sleep(check_interval)

# Usage
await monitor_test_run('test_run_id')
```

### Test Data Management

```python
# Create test data
test_data = await client.test_data.create({
    "name": "Test Data",
    "type": "test",  # Optional: defaults to "test"
    "status": "draft"  # Optional: defaults to "draft"
})
```

### Environment Management

```python
# List environments
environments = await client.environments.get_list()

# Get environment by ID
environment = await client.environments.get_one('env_id')
```

### Tags Management

```python
# List tags
tags = await client.tags.get_list()

# Create tag
tag = await client.tags.create({
    "name": "New Tag"
})
```

## Available Managers

The SDK provides managers for all TestZeus collections:

- `client.tests` - Tests
- `client.test_runs` - Test Runs
- `client.test_run_dashs` - Test Run Dashboards
- `client.test_data` - Test Data
- `client.environments` - Environments
- `client.tags` - Tags
- `client.agent_configs` - Agent Configurations
- `client.test_devices` - Test Devices
- `client.test_designs` - Test Designs
- `client.test_run_dash_outputs` - Test Run Dashboard Outputs
- `client.test_run_dash_output_steps` - Test Run Dashboard Output Steps
- `client.tenant_consumption` - Tenant Consumption
- `client.tenant_consumption_logs` - Tenant Consumption Logs

## Contributing

1. Clone the repository
2. Install dependencies with Poetry: `poetry install`
3. Run tests: `poetry run pytest`

## License

MIT

## Release Process

This project uses automated releases through GitHub Actions. The process is:

1. To create a new release, use one of the following make commands:
   ```bash
   # Interactive version bump (will prompt for version type)
   make release

   # Specific version bumps
   make release-patch   # Increments the patch version (e.g., 1.0.0 -> 1.0.1)
   make release-minor   # Increments the minor version (e.g., 1.0.0 -> 1.1.0)
   make release-major   # Increments the major version (e.g., 1.0.0 -> 2.0.0)
   make release-custom  # Set a custom version (will prompt for version)
   ```

2. The command will:
   - Update the version in pyproject.toml
   - Commit the change with a release message
   - Create a git tag for the version (e.g., v1.0.1)
   - Push the commit and tag to GitHub

3. The GitHub Actions workflow will automatically:
   - Detect the new tag
   - Build the package
   - Run tests
   - Publish the package to PyPI

Note: The release workflow only runs on tagged releases (not on pushes to the main branch).
