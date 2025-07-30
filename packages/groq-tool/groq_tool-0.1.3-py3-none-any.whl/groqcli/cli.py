# groqcli/__main__.py

import os
import sys
import json
import time
import re
from pathlib import Path
import click
from rich.console import Console
from rich.markup import escape
from rich.prompt import Prompt
from rich.panel import Panel
from rich.syntax import Syntax
from groq import Groq
from .config import get_key, save_key, get_model, set_model, edit_system_prompt, get_predifined_system_prompts, get_system_prompt
from . import VERSION

console = Console()


# Constants
DEFAULT_MODEL = get_model() or "llama3-8b-8192"
MAX_TOKENS = None
TEMPERATURE = None
TOP_P = 1
MAX_RETRIES = 3

CONFIG_DIR = Path.home() / ".groqcli"
SESSIONS_DIR = CONFIG_DIR / "sessions"
HISTORY_FILE = CONFIG_DIR / "history.json"

API_KEY = None
RAW_OUTPUT = False

def cprint(*args, **kwargs):
    """Check `RAW_OUTPUT` mode before printing with rich"""
    if not RAW_OUTPUT:
        console.print (*args, **kwargs)

def ensure_dirs():
    CONFIG_DIR.mkdir(exist_ok=True)
    SESSIONS_DIR.mkdir(exist_ok=True)
    if not HISTORY_FILE.exists():
        HISTORY_FILE.write_text("[]")

def load_history():
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history[-10:], f, indent=2)  # keep last 10

def add_to_history(session_path):
    history = load_history()
    session_path_str = str(session_path)
    if session_path_str in history:
        history.remove(session_path_str)
    history.append(session_path_str)
    save_history(history)

def get_last_session(n):
    history = load_history()
    if not history:
        return None
    idx = -n
    if abs(idx) > len(history):
        return None
    return Path(history[idx])

def parse_messages(content):
    blocks = re.split(r'\[(SYSTEM|USER|ASSISTANT)\]\n', content, flags=re.IGNORECASE)
    messages = []
    for i in range(1, len(blocks), 2):
        role = blocks[i].lower()
        content = blocks[i+1].strip()
        if content:
            messages.append({"role": role, "content": content})
    return messages

def format_messages(messages):
    # Back to text format with role labels
    out = ""
    for msg in messages:
        role = msg["role"].upper()
        out += f"[{role}]\n{msg['content']}\n\n"
    return out.strip()

def fetch_completion(client, messages, model, temperature, max_tokens, top_p, stream=False):
    for attempt in range(MAX_RETRIES):
        try:
            return client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                stream=stream,
            )
        except Exception as e:
            if attempt == MAX_RETRIES - 1:
                cprint(f"[red]Max retries reached. Error: {e}[/red]")
                return None
            time.sleep(2 ** attempt)

def print_completion_stream(completion):
    response = ''
    for chunk in completion:
        content = chunk.choices[0].delta.content or ""
        response += content
        print(content, end="", flush=True)
        if not RAW_OUTPUT:
            time.sleep(0.025)
    cprint()
    return response

def save_session_cmd(messages, path):
    text = format_messages(messages)
    path.write_text(text, encoding="utf-8")
    if os.path.basename(path) == str(path):
        print("getting absolute path")
        path = os.path.abspath(path)
    add_to_history(path)
    cprint(f"[green]💾 Session saved to {escape(str(path))}[/green]")

def load_session_cmd(path):
    if not path.exists():
        cprint(f"[red]❌ Session file {escape(str(path))} not found[/red]")
        sys.exit(1)
    content = path.read_text(encoding="utf-8")
    return parse_messages(content)

def not_invoked(ctx, commands: list[str]):

    invoked = ctx.invoked_subcommand
    if invoked not in commands:
       return True

@click.group()
@click.version_option(VERSION, prog_name="groqcli")
@click.option('--key', help='Groq API Key (overrides config/env)')
@click.option("--raw", is_flag=True, help="Only echoing response from the llm")
@click.pass_context
def cli(ctx, key, raw):
    """groqcli - A useful cli for Groq LLMs"""

    global RAW_OUTPUT
    RAW_OUTPUT = raw

    global API_KEY
    API_KEY = get_key(key)
    if API_KEY is None and not_invoked(ctx, "save-key"):
        cprint("[bold red]❌ No Groq API Key found ![/bold red] Please use [italic]--key[/italic] or [italic]groqcli save-key[/italic]\nIf you don't have one, you can create one here: https://console.groq.com/keys")
        sys.exit(1)
        


@cli.command(name="save-key")
@click.argument("api_key", type=str)
def save_key_cmd(api_key: str):
    """Enregistré la clé api"""
    if not api_key:
        api_key = Prompt.ask("Please enter your Groq API key", password=True).strip()
    if api_key:
        save_key(api_key)
        cprint("[green]💾 The api key was sucessfully saved to ~/.groqcli/config.json ![/green]")

@cli.command(name="set-model")
@click.argument("model", required=True, type=str)
def set_model_cmd(model: str):
    """Set the default model to use"""
    if model:
        set_model(model)
        cprint(f"[green]💾 Model '{model}' was sucessfully saved to ~/.groqcli/config.json ![/green]")
    else:
        cprint("[red]❌ Modèle non spécifié ![/red]")

@cli.command(name="set-system")
@click.argument("key", required=True, type=str)
@click.argument("system_prompt", required=True, type=str)
def set_system_cmd(key: str, system_prompt: str):
    """Set an alias for a system prompt (key:`default` when no system prompt is specified using chat command)"""
    if key and system_prompt:
        edit_system_prompt(key, system_prompt)
        cprint(f"[green]💾 System prompt '{key}' was sucessfully saved to ~/.groqcli/config.json ![/green]")
    else:
        cprint("[red]❌ Not enough arguments ![/red]")

@cli.command(name="get-system")
@click.argument("key", required=True, type=str)
def get_system_cmd(key: str):
    """Get a system prompt by its alias"""
    system_prompt = get_system_prompt(key)
    if system_prompt:
        cprint(f"[blue]System prompt '{key}':[/blue]\n{system_prompt}")
    else:
        cprint(f"[red]❌ System prompt '{key}' not found ![/red]")

@cli.command()
def models():
    """List available Groq models"""
    global API_KEY

    import requests
    API_KEY = API_KEY or get_key()
    try:
        resp = requests.get(
            "https://api.groq.com/openai/v1/models",
            headers={"Authorization": f"Bearer {API_KEY}"},
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        models = data.get("data", [])
        if not models:
            cprint("[yellow]No models found[/yellow]")
            return
        cprint("[bold magenta]Available Groq Models:[/bold magenta]")
        for m in models:
            cprint(f"- [cyan]{m['id']}[/cyan]")
    except Exception as e:
        cprint(f"[red]Failed to fetch models: {e}[/red]")

@cli.command()
@click.argument("input_text_or_file", required=False)
@click.option("--raw", is_flag=True, help="Only echoing response from the llm")
@click.option("--model", default=DEFAULT_MODEL, show_default=True, help="Model to use")
@click.option("--temperature", default=TEMPERATURE, show_default=True, help="Temperature for generation")
@click.option("--max-tokens", default=MAX_TOKENS, show_default=True, help="Max tokens in response")
@click.option("--top-p", default=TOP_P, show_default=True, help="Top-p (nucleus sampling) parameter")
@click.option("--system", type=str, help="System prompt alias or custom system prompt text")
@click.option("--load-session", type=click.Path(exists=True), help="Load previous session file (path)")
@click.option("--save-session", type=click.Path(), help="Save session to file (path)")
@click.option("--last", type=click.IntRange(1,3), help="Load last n-th session from history (1,2,3)")
@click.option("--no-stream", is_flag=True, help="Disable streaming output")
@click.option("--no-save", is_flag=True, help="Disable saving session")
def chat(
    input_text_or_file,
    model,
    temperature,
    max_tokens,
    top_p,
    system,
    load_session,
    save_session,
    last,
    no_stream,
    no_save,
    raw
):
    """Chat with Groq LLM.

    INPUT_TEXT_OR_FILE can be a prompt string or a path to a conversation file.
    """

    global RAW_OUTPUT
    if raw:
        RAW_OUTPUT = True

    global API_KEY
    ensure_dirs()
    API_KEY = API_KEY or get_key()
    client = Groq(api_key=API_KEY)
    messages = []

    # Load conversation messages
    if load_session:
        messages = load_session(Path(load_session))
        cprint(f"[green]💬 Loaded session from {load_session}[/green]")
    elif last:
        path = get_last_session(last)
        if not path:
            cprint(f"[red]❌ No session found for last {last}[/red]")
            sys.exit(1)
        messages = load_session_cmd(path)
        if not save_session:
            save_session = path
        cprint(f"[green]💬 Loaded last session #{last} from {path}[/green]")
    if input_text_or_file and len(input_text_or_file) < 300 and Path(input_text_or_file).exists():
        content = Path(input_text_or_file).read_text(encoding="utf-8")
        messages = parse_messages(content)
    elif input_text_or_file:
        user_message = {"role": "user", "content": input_text_or_file.strip()}
        if messages:
            messages.append(user_message)
        else:
            messages = [user_message]
    else:
        if not messages or messages[-1]["role"] == "assistant":
            if messages:
                cprint(Panel.fit(f"[blue bold]{messages[-1]['role']}[/blue bold]\n" + escape(messages[-1]["content"]), title="Last message"))
            # Interactive prompt
            cprint("[blue]")
            cprint("[bold green]Enter your prompt (empty line to send):[/bold green]")
            lines = []
            while True:
                line = Prompt.ask("> ")
                if not line.strip():
                    break
                lines.append(line)
            prompt = "\n".join(lines).strip()
            if not prompt:
                cprint("[red]No prompt provided. Bye bye![/red]")
                sys.exit(0)
            messages.append({"role": "user", "content": prompt})

    # Insert system prompt at the beginning
    if system:
        system_msg = {"role": "system", "content": get_system_prompt(system) or system}
    else:
        system_msg = {"role": "system", "content": get_system_prompt("default") or ''}

    # If messages start with system, replace it, else insert
    if messages and messages[0]["role"] == "system":
        messages[0] = system_msg
    else:
        messages.insert(0, system_msg)

    # Display input nicely
    cprint(Panel.fit("[bold]Input Messages:[/bold]\n" + escape(format_messages(messages)), title="📝"))

    stream = not no_stream and sys.stdout.isatty()

    completion = fetch_completion(
        client,
        messages=messages,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        stream=stream,
    )
    if not completion:
        cprint("[red]❌ Failed to get completion.[/red]")
        sys.exit(1)

    cprint(Panel.fit("[bold]Response:[/bold]", title="🤖"))

    if stream:
        text = print_completion_stream(completion)
    else:
        text = completion.choices[0].message.content
        print(text)

    if not no_save:
        # Save session to file
        timestamp = int(time.time())
        session_file = Path(save_session) if save_session else (SESSIONS_DIR / f"session_{timestamp}.txt")
        if text.strip():
            save_session_cmd(messages + [{"role": "assistant", "content": text}], session_file)
        else:
            save_session_cmd(messages, session_file)

    return text

if __name__ == "__main__":
    cli()
