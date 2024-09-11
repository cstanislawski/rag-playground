import argparse
from rag_setup import main as setup_main
from rag_search import rag_pipeline, generate_response
import logging
import os
import signal
import sys
from dotenv import load_dotenv
from rich.logging import RichHandler
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel

load_dotenv()

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)

logger = logging.getLogger("main")
console = Console()


def setup():
    logger.info("Running setup process")
    setup_main()


def search(query):
    logger.info(f"Executing search for query: {query}")
    response = rag_pipeline(query)
    console.print("\n[bold green]Response:[/bold green]")
    console.print(response)


def handle_exit(signum, frame):
    console.print("\n[bold yellow]Exiting the program. Goodbye![/bold yellow]")
    sys.exit(0)


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def display_help(multi_turn=False):
    help_text = f"""
    [bold]Available commands:[/bold]
    [cyan]help[/cyan]    : Display this help message
    [cyan]exit[/cyan]    : Exit the program
    [cyan]Ctrl+C[/cyan]  : Force exit the program
    """
    if multi_turn:
        help_text += (
            "[cyan]clear[/cyan]   : Clear the conversation history and screen\n"
        )

    help_text += """
    [bold]Tips:[/bold]
    - Ask questions about products in the database
    - The system will provide product recommendations based on your queries
    """
    if multi_turn:
        help_text += "- You can refer to previous conversation context\n"

    console.print(Panel(help_text, title="Help", expand=False))


def continuous_mode():
    console.print(
        "[bold yellow]Entering continuous mode. Type 'help' for available commands.[/bold yellow]"
    )
    signal.signal(signal.SIGINT, handle_exit)

    while True:
        try:
            query = Prompt.ask("\n[bold cyan]Enter your query[/bold cyan]")
            if query.lower() == "exit":
                break
            elif query.lower() == "help":
                display_help(multi_turn=False)
                continue
            search(query)
        except KeyboardInterrupt:
            handle_exit(None, None)


def multi_turn_mode():
    console.print(
        "[bold yellow]Entering multi-turn mode. Type 'help' for available commands.[/bold yellow]"
    )
    signal.signal(signal.SIGINT, handle_exit)

    context = []
    while True:
        try:
            query = Prompt.ask("\n[bold cyan]Enter your query[/bold cyan]")
            if query.lower() == "exit":
                break
            elif query.lower() == "clear":
                context = []
                clear_screen()
                console.print(
                    "[bold magenta]Conversation history cleared and screen cleared.[/bold magenta]"
                )
                continue
            elif query.lower() == "help":
                display_help(multi_turn=True)
                continue

            context.append(f"User: {query}")

            response, results = rag_pipeline(query, return_results=True)

            full_context = "\n".join(context)
            response = generate_response(query, results, full_context)

            console.print("\n[bold green]Response:[/bold green]")
            console.print(response)

            context.append(f"Assistant: {response}")

            context = context[-10:]
        except KeyboardInterrupt:
            handle_exit(None, None)


def main():
    parser = argparse.ArgumentParser(description="RAG System CLI")
    parser.add_argument("action", choices=["setup", "search"], help="Action to perform")
    parser.add_argument(
        "-q",
        "--query",
        help="Search query (required for 'search' action unless in interactive mode)",
    )
    parser.add_argument(
        "-c",
        "--continuous",
        action="store_true",
        help="Enable continuous mode for multiple one-turn queries",
    )
    parser.add_argument(
        "-m",
        "--multi-turn",
        action="store_true",
        help="Enable multi-turn mode for interactive conversation with context",
    )

    args = parser.parse_args()

    if args.action == "setup":
        setup()
    elif args.action == "search":
        if args.multi_turn:
            multi_turn_mode()
        elif args.continuous:
            continuous_mode()
        elif args.query:
            search(args.query)
        else:
            parser.error(
                "Either -q/--query, -c/--continuous, or -m/--multi-turn is required for 'search' action"
            )


if __name__ == "__main__":
    main()
