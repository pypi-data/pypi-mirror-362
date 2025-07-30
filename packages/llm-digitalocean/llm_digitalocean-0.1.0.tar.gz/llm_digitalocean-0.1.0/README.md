# llm-digitalocean

[![PyPI](https://img.shields.io/pypi/v/llm-digitalocean.svg)](https://pypi.org/project/llm-digitalocean/)
[![Changelog](https://img.shields.io/github/v/release/rajashekar/llm-digitalocean?include_prereleases&label=changelog)](https://github.com/rajashekar/llm-digitalocean/releases)
[![Tests](https://github.com/rajashekar/llm-digitalocean/workflows/Test/badge.svg)](https://github.com/rajashekar/llm-digitalocean/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/rajashekar/llm-digitalocean/blob/main/LICENSE)

[LLM](https://llm.datasette.io/) plugin for models hosted by [DigitalOcean AI](https://www.digitalocean.com/products/ai)

## Installation

First, [install the LLM command-line utility](https://llm.datasette.io/en/stable/setup.html).

Now install this plugin in the same environment as LLM:
```bash
llm install llm-digitalocean
```

## Configuration

You will need an API key from DigitalOcean. You can obtain one from the [DigitalOcean Control Panel](https://cloud.digitalocean.com/account/api/tokens).

You can set that as an environment variable called `DIGITAL_OCEAN`, or add it to the `llm` set of saved keys using:

```bash
llm keys set digitalocean
```
```
Enter key: <paste key here>
```

## Usage

To list available models, run:
```bash
llm models list
```
You should see a list that looks something like this:
```
DigitalOcean: digitalocean/meta-llama/Meta-Llama-3.1-405B-Instruct
DigitalOcean: digitalocean/meta-llama/Meta-Llama-3.1-70B-Instruct
DigitalOcean: digitalocean/meta-llama/Meta-Llama-3.1-8B-Instruct
...
```

To run a prompt against a model, pass its full model ID to the `-m` option, like this:
```bash
llm -m digitalocean/meta-llama/Meta-Llama-3.1-70B-Instruct "Five creative names for a pet robot"
```

You can set a shorter alias for a model using the `llm aliases` command like so:
```bash
llm aliases set llama3.1 digitalocean/meta-llama/Meta-Llama-3.1-70B-Instruct
```
Now you can prompt the model using:
```bash
cat llm_digitalocean.py | llm -m llama3.1 -s 'write some pytest tests for this'
```

### Vision models

Some DigitalOcean models can accept image attachments. Run this command:

```bash
llm models --options -q digitalocean
```
And look for models that list these attachment types:

```
  Attachment types:
    image/gif, image/jpeg, image/png, image/webp
```

You can feed these models images as URLs or file paths, for example:

```bash
curl https://static.simonwillison.net/static/2024/pelicans.jpg | llm \
    -m digitalocean/gpt-4o 'describe this image' -a -
```

### Listing models

The `llm models -q digitalocean` command will display all available models, or you can use this command to see more detailed information:

```bash
llm digitalocean models
```
Output starts like this:
```yaml
- id: meta-llama/Meta-Llama-3.1-405B-Instruct
  name: model
  created: 2024-07-15 12:00:00
  owned_by: meta-llama
  supports_schema: False
  supports_vision: False

- id: meta-llama/Meta-Llama-3.1-70B-Instruct
  name: model
  created: 2024-07-15 12:00:00
  owned_by: meta-llama
  supports_schema: False
  supports_vision: False
```

Add `--json` to get back JSON instead:
```bash
llm digitalocean models --json
```

### Plugin Commands

The plugin provides several commands under the `llm digitalocean` namespace:

#### Refresh Cache
```bash
llm digitalocean refresh
```
Refreshes the cached model information. The plugin automatically caches model data for 1 hour to improve performance and reduce API calls.

#### Cache Information
```bash
llm digitalocean cache-info
```
Shows information about the current cache, including file location, age, and number of cached models.

## Features

### Automatic Caching
The plugin automatically caches model information in your LLM user directory to improve performance and reduce API calls. The cache is valid for 1 hour and can be manually refreshed using the `refresh` command.

### Streaming Support
The plugin supports both streaming and non-streaming responses from DigitalOcean AI models.

### Vision Model Support
The plugin automatically detects and enables vision capabilities for models that support image inputs.

### Error Handling
Comprehensive error handling for:
- Missing API keys
- Network connectivity issues
- API rate limits and errors
- Invalid model names
- Malformed responses

## API Endpoint

This plugin uses the DigitalOcean AI inference API:
- Base URL: `https://inference.do-ai.run/v1/`
- Models endpoint: `GET /models`
- Chat completions: `POST /chat/completions`

## Cache Location

Model information is cached in your LLM user directory:
- macOS: `~/Library/Application Support/io.datasette.llm/digitalocean_models.json`
- Linux: `~/.config/io.datasette.llm/digitalocean_models.json`
- Windows: `%APPDATA%\io.datasette.llm\digitalocean_models.json`

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-digitalocean
python3 -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
llm install -e '.[test]'
```
To run the tests:
```bash
pytest
```

## Example Usage

```bash
# List all available models
llm digitalocean models

# Use a specific model
llm -m digitalocean/meta-llama/Meta-Llama-3.1-70B-Instruct "Explain quantum computing"

# Set up an alias for easier use
llm aliases set llama digitalocean/meta-llama/Meta-Llama-3.1-70B-Instruct
llm -m llama "What is machine learning?"

# Check cache status
llm digitalocean cache-info

# Refresh the model cache
llm digitalocean refresh

# Use with image input (if model supports vision)
llm -m digitalocean/gpt-4o "What's in this image?" -a image.jpg
```

## License

Apache License 2.0