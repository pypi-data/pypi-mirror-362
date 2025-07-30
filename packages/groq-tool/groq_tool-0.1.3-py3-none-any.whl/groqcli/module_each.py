from . import cli
from . import VERSION
import click
import os
from rich.console import Console
from rich.markup import escape
from rich.prompt import Prompt
from rich.panel import Panel

console = Console()

def recusive_files(directory) -> list[str]:
    all_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            all_files.append(os.path.join(root, file))
    return all_files

@click.command()
@click.version_option(VERSION, prog_name="groqcli-files")
@click.argument("directory", type=click.Path(dir_okay=True, file_okay=False), required=True)
@click.option("--prompt", type=str, default=None)
@click.option("--model", default=cli.DEFAULT_MODEL, show_default=True, help="Model to use")
@click.option("--temperature", default=cli.TEMPERATURE, show_default=True, help="Temperature for generation")
@click.option("--max-tokens", default=cli.MAX_TOKENS, show_default=True, help="Max tokens in response")
@click.option("--top-p", default=cli.TOP_P, show_default=True, help="Top-p (nucleus sampling) parameter")
@click.option("--system", type=str, help="System prompt alias or custom system prompt text")
@click.option("--output-file", '-f', default=None, type=click.Path(), help="Output file (optional)")
@click.option("--each-output", '-e', flag_value=True, default=False, help="Output each response to a file")
@click.option("--send-path", '-p', flag_value=True, default=True, help="Send the file path to the llm")
def cli_files(directory: click.Path, model, temperature, max_tokens, top_p, system, each_output, output_file, send_path, prompt):
    """Send each file of a directory to the llm"""

    all_files = recusive_files(directory)
    for file_path in all_files:
        console.print(f"[bold blue]Processing file ({all_files.index(file_path)+1}/{len(all_files)}):[/bold blue]", file_path)

        prompt = prompt or ''
        if send_path:
            prompt += f"\n\n{file_path}"
        try:
            prompt +=f"\n{open(file_path, 'r', encoding='utf-8').read()}"
        except Exception as e:
            # prompt += f"\n{str(open(file_path, 'rb').read())}"
            console.print(f"[bold red]Error reading file {file_path}:[/bold red] {e}")
            continue

        ctx = click.Context(cli.chat)
        response = ctx.invoke(cli.chat,
            input_text_or_file=prompt,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            system=system,
            raw=True,
            no_save=True
        )
        
        if not response:
            console.print("[bold red]No response from the llm[/bold red]")
            continue

        if each_output:
            output_file = file_path + ".groq"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(response)
            console.print("[bold blue]Response saved to:[/bold blue]", output_file)
        elif output_file:
            with open(output_file, "a", encoding="utf-8") as f:
                f.write(f"\n\n{file_path}\n" + response)
            console.print("[bold blue]Response saved to:[/bold blue]", output_file)
        else:
            console.print(response)
    console.print("[bold green]Finished task ![/bold green]")

    
