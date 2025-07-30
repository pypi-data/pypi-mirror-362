# groqcli (groq-tool)

A Modern Command-Line Tool for Interacting with Grog LLMs

[![Upload Python Package](https://github.com/daisseur/groqcli/actions/workflows/python-publish.yml/badge.svg)](https://github.com/daisseur/groqcli/actions/workflows/python-publish.yml)

## Table of Contents


* [Features](#features)
* [Installation](#installation)
* [Usage](#usage)
* [Commands](#commands)
* [Predefined System Prompts](#predefined-system-prompts)
* [Extensibility](#extensibility)
* [Troubleshooting](#troubleshooting)

## Features


### 1. **Direct Prompt**

* Run a command with a direct prompt
* Example: `groqcli chat "Explain black holes in 3 points"`

### 2. **File-Based Prompt**

* Run a command with a file-based prompt
* Example: `groqcli chat my_file.txt`

### 3. **Predefined System Prompts**

* Use predefined system prompts to customize the response
* Example: `groqcli chat "Transform this script into TypeScript" --system formatScript`
* Available: `uwu`, `formatScript`, `friendly`, `tech`, `json`, `default`, `fr-default`

### 4. **Save Conversation**

* Save the current conversation
* Example: `groqcli --save`

### 5. **Resume Previous Session**

* Resume a previous conversation
* Example: `groqcli resume --last 1`

### 6. **List Available Models**

* List available models
* Example: `groqcli models`

### 7. **Edit Predefined System Prompts**

* Edit predefined system prompts
* Example: `groqcli prompts edit`

### 8. **Role-Based Prompt**

* Use roles to customize the response
* Example: `groqcli "[SYSTEM] Explain black holes in 3 points"`

### 9. **Automatic History**

* View previous conversation history
* Example: `groqcli --history`

### 10. **Rich UI**

* Use a rich UI with colors, emojis, etc.
* Example: `groqcli "Explain black holes in 3 points" --rich`

**Note**: These examples are brief and illustrate the features, but you can customize them to fit your needs.

## Installation


### Using pipx (Recommended)

```bash
pipx install groq-tool
```


```bash
pipx install git+https://github.com/daisseur/groqcli.git
```

### Using pip

```bash
pip install groq-tool
```

### From Source

```bash
git clone https://github.com/daisseur/groqcli.git
cd groqcli
pip install .
```

## Usage


### Direct Prompt

```bash
groqcli chat "Explain black holes in 3 points"
```

### File-Based Prompt

```bash
groqcli chat my_file.txt
```

### With Predefined System Prompt

```bash
groqcli chat "Transform this script into TypeScript" --system formatScript
```

### Resume Previous Session

```bash
groqcli chat --last 1
```

### Saving session and resume them later
```bash
groqcli chat --save-session myfile.groq
```
```bash
groqcli chat --load-session myfile.groq
```
> Compatible with `--last` (it does not save the next answer in another timestamp file)


## Commands


* `groqcli`: Run the command-line tool
* `groqcli --system <prompt>`: Use a predefined system prompt
* `groqcli --save`: Save the current conversation
* `groqcli resume`: Load a previous conversation
* `groqcli models`: List available models
* `groqcli prompts edit`: Edit predefined system prompts

## Predefined System Prompts


* `uwu`: Cute and cheerful tone (UwU)
* `formatScript`: Script format only
* `friendly`: Friendly and helpful tone
* `tech`: Precise and technical explanations
* `json`: JSON format only
* `default`: Default helpful assistant
* `fr-default`: French-speaking helpful assistant




## Module `groqcli-files` (installed by default)

### Overview

GroqCLI Files is a module of the GroqCLI ecosystem that allows you to manage and interact with files in a convenient and efficient way. This module provides a set of commands and options that enable you to send multiple files to groq llms.


### Examples


* Get documentations for a directory of API endpoints:
> Set up a useful system prompt
```bash
groqcli set-system endpointFormat "You have to answer using this format: # {endoint path}\nEach params (both required and optional) * `{params}`: `{type}`"
```
> Run the command
```bash
groqcli-files ./APIEndpoints -f ~/Server/Work/Max/HubRP/endpoints.md --system endpointFormat
```

### Usage

To use GroqCLI Files, simply run the `groqcli-files` command followed by the desired options.


## Extensibility

GroqCLI is fully extensible and can be customized to fit your needs. You can add new features, commands, and prompts by modifying the source code.

## Troubleshooting

If you encounter any issues or have questions, please open an issue on the GitHub repository

---

Special thanks to [@gmfunk9](https://github.com/gmfunk9/groq_cli) for providing the inspiration for this project.
