# llm-chutes

[![PyPI](https://img.shields.io/pypi/v/llm-chutes.svg)](https://pypi.org/project/llm-chutes/)
[![Changelog](https://img.shields.io/github/v/release/rajashekar/llm-chutes?include_prereleases&label=changelog)](https://github.com/rajashekar/llm-chutes/releases)
[![Tests](https://github.com/rajashekar/llm-chutes/workflows/Test/badge.svg)](https://github.com/rajashekar/llm-chutes/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/rajashekar/llm-chutes/blob/main/LICENSE)

[LLM](https://llm.datasette.io/) plugin for models hosted by [Chutes AI](https://chutes.ai/)

## Installation

First, [install the LLM command-line utility](https://llm.datasette.io/en/stable/setup.html).

Now install this plugin in the same environment as LLM.
```bash
llm install llm-chutes
```

## Configuration

You will need an API key from Chutes AI. You can obtain one from their platform.

You can set that as an environment variable called `CHUTES_API_KEY`, or add it to the `llm` set of saved keys using:

```bash
llm keys set chutes
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
chutes: chutes/deepseek-ai/DeepSeek-R1
chutes: chutes/deepseek-ai/DeepSeek-V3-0324
chutes: chutes/NousResearch/DeepHermes-3-Mistral-24B-Preview
chutes: chutes/moonshotai/Kimi-K2-Instruct
chutes: chutes/Qwen/Qwen3-32B
...
```

To run a prompt against a model, pass its full model ID to the `-m` option, like this:
```bash
llm -m chutes/deepseek-ai/DeepSeek-R1 "Five spooky names for a pet tarantula"
```

You can set a shorter alias for a model using the `llm aliases` command like so:
```bash
llm aliases set deepseek chutes/deepseek-ai/DeepSeek-R1
```
Now you can prompt the model using:
```bash
llm -m deepseek "What is the meaning of life?"
```

### Listing models

The `llm models -q chutes` command will display all available models, or you can use this command to see more detailed information:

```bash
llm chutes models
```
Output starts like this:
```yaml
- id: deepseek-ai/DeepSeek-R1
  name: deepseek-ai/DeepSeek-R1
  context_length: 163,840
  supports_schema: True
  pricing: input $0.27216/M, output $0.27216/M

- id: deepseek-ai/DeepSeek-V3-0324
  name: deepseek-ai/DeepSeek-V3-0324
  context_length: 163,840
  supports_schema: True
  pricing: input $0.27216/M, output $0.27216/M
```

Add `--json` to get back JSON instead:
```bash
llm chutes models --json
```

### Refreshing models

To refresh the cached list of models from the Chutes AI API:

```bash
llm chutes refresh
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-chutes
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

## API Endpoint

This plugin connects to the Chutes AI API at `https://llm.chutes.ai/v1/`

## License

Apache License 2.0