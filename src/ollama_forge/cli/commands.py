"""
CLI command implementations for Ollama Forge. ⚙️🔮⚡
╔═══════════════════════════════════════════════════════════╗
║ Eidosian Minimalism, Humor, Flow, and Self-Awareness      ║
╚═══════════════════════════════════════════════════════════╝

All functionality remains intact, refined with clarity and style.
"""

import argparse
import sys
import textwrap

from ..config import DEFAULT_CHAT_MODEL, DEFAULT_EMBEDDING_MODEL, get_version_string
from ..core.client import OllamaClient


def create_parser() -> argparse.ArgumentParser:
    """
    Create an elegant command parser with layered subcommand structure. 🏛️
    """
    parser = argparse.ArgumentParser(
        prog="ollama-forge",
        description=textwrap.dedent(
            """
            ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
            ┃ Ollama Forge CLI - Seamless Model Interaction ┃
            ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
            ⚡ Experience fluid commands for all Ollama capabilities.
            """
        ),
    )
    parser.add_argument(
        "--version", action="version", version=f"Ollama Forge v{get_version_string()}"
    )
    parser.add_argument(
        "--api-url",
        help="Ollama API URL (default: http://localhost:11434)",
        default=None,
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    generate_parser = subparsers.add_parser(
        "generate", help="Generate text from a prompt"
    )
    generate_parser.add_argument(
        "--model", "-m", default=DEFAULT_CHAT_MODEL, help="Model name"
    )
    generate_parser.add_argument(
        "--temperature", "-t", type=float, default=0.7, help="Sampling temperature"
    )
    generate_parser.add_argument(
        "--stream", "-s", action="store_true", help="Stream output tokens"
    )
    generate_parser.add_argument("prompt", help="The prompt to generate from")

    chat_parser = subparsers.add_parser("chat", help="Chat with a model")
    chat_parser.add_argument(
        "--model", "-m", default=DEFAULT_CHAT_MODEL, help="Model name"
    )
    chat_parser.add_argument(
        "--system", default="You are a helpful assistant.", help="System message"
    )
    chat_parser.add_argument("message", help="User message to send")

    chat_session_parser = subparsers.add_parser(
        "chat-session", help="Start interactive chat session"
    )
    chat_session_parser.add_argument(
        "--model", "-m", default=DEFAULT_CHAT_MODEL, help="Model name"
    )
    chat_session_parser.add_argument(
        "--system", default="You are a helpful assistant.", help="System message"
    )

    embed_parser = subparsers.add_parser("embed", help="Generate embeddings for text")
    embed_parser.add_argument(
        "--model", "-m", default=DEFAULT_EMBEDDING_MODEL, help="Model name"
    )
    embed_parser.add_argument("text", help="Text to embed")

    subparsers.add_parser("list", help="List available models")

    pull_parser = subparsers.add_parser("pull", help="Pull a model")
    pull_parser.add_argument("model", help="Model name to pull")

    return parser


def handle_generate(args: argparse.Namespace, client: OllamaClient) -> int:
    """
    Eidosian text generation with streaming option.
    """
    if args.stream:
        print(f"Generating with {args.model} (streaming)...")
        for chunk in client.generate(
            model=args.model,
            prompt=args.prompt,
            stream=True,
            options={"temperature": args.temperature},
        ):
            if "response" in chunk:
                print(chunk["response"], end="", flush=True)
        print()
    else:
        print(f"Generating with {args.model}...")
        response = client.generate(
            model=args.model,
            prompt=args.prompt,
            options={"temperature": args.temperature},
        )
        print(response.get("response", ""))
    return 0


def handle_chat(args: argparse.Namespace, client: OllamaClient) -> int:
    """
    Eidosian chat command.
    """
    messages = [
        {"role": "system", "content": args.system},
        {"role": "user", "content": args.message},
    ]
    print("Assistant: ", end="", flush=True)
    for chunk in client.chat(model=args.model, messages=messages, stream=True):
        if "message" in chunk and "content" in chunk["message"]:
            print(chunk["message"]["content"], end="", flush=True)
    print()
    return 0


def handle_chat_session(args: argparse.Namespace, client: OllamaClient) -> int:
    """
    Fluid, interactive chat session with color-coded prompts.
    Escape with 'exit' or 'quit'. 🎨🔮
    """
    from colorama import Fore, Style, init

    init()

    messages = [{"role": "system", "content": args.system}]
    print(f"{Fore.CYAN}Welcome to Ollama Forge Chat Session{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Model: {args.model}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}System: {args.system}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Type 'exit' or 'quit' to end the session{Style.RESET_ALL}")
    print("─" * 50)

    while True:
        try:
            user_input = input(f"{Fore.GREEN}You: {Style.RESET_ALL}")
            if user_input.lower() in ("exit", "quit", "/exit", "/quit"):
                break
            messages.append({"role": "user", "content": user_input})
            print(f"{Fore.BLUE}Assistant: {Style.RESET_ALL}", end="")

            for chunk in client.chat(model=args.model, messages=messages, stream=True):
                if "message" in chunk and "content" in chunk["message"]:
                    print(chunk["message"]["content"], end="", flush=True)

            response = client.chat(model=args.model, messages=messages, stream=False)
            if "message" in response:
                messages.append(response["message"])

            print("\n" + "─" * 50)

        except KeyboardInterrupt:
            print("\nExiting chat session...")
            break
        except Exception as e:
            print(f"\n{Fore.RED}Error: {e}{Style.RESET_ALL}")
    return 0


def handle_embed(args: argparse.Namespace, client: OllamaClient) -> int:
    """
    Eidosian embedding generation.
    """
    result = client.create_embedding(model=args.model, prompt=args.text)
    print(
        f"Generated embedding with {args.model} (dimensions: {len(result['embedding'])})"
    )
    if args.verbose:
        print(result["embedding"])
    return 0


def handle_list(args: argparse.Namespace, client: OllamaClient) -> int:
    """
    List available models with impeccable formatting.
    """
    models = client.list_models().get("models", [])
    if not models:
        print("No models available")
        return 0
    print(f"Available models ({len(models)}):")
    for model in models:
        print(f"  • {model['name']} ({model.get('size', 'unknown size')})")
    return 0


def handle_pull(args: argparse.Namespace, client: OllamaClient) -> int:
    """
    Pull a model with progress tracking.
    """
    from tqdm import tqdm

    print(f"Pulling model: {args.model}")
    with tqdm(unit="B", unit_scale=True, desc=args.model) as pbar:
        last_total = 0
        for progress in client.pull(args.model, stream=True):
            if "completed" in progress and progress.get("total", 0) > 0:
                completed = int(progress["completed"])
                total = int(progress["total"])
                pbar.total = total
                diff = completed - last_total
                if diff > 0:
                    pbar.update(diff)
                    last_total = completed
    print(f"Model {args.model} pulled successfully!")
    return 0


def generate_command(args: argparse.Namespace) -> int:
    """
    Command function for text generation via the generate subcommand.
    Follows Eidosian principle of elegant delegation.

    Args:
        args: Parsed command arguments

    Returns:
        Exit code (0 for success)
    """
    client = OllamaClient(api_url=args.api_url if hasattr(args, "api_url") else None)
    return handle_generate(args, client)


def chat_command(args: argparse.Namespace) -> int:
    """
    Command function for interactive chat via the chat subcommand.
    Follows Eidosian principle of elegant delegation.

    Args:
        args: Parsed command arguments

    Returns:
        Exit code (0 for success)
    """
    client = OllamaClient(api_url=args.api_url if hasattr(args, "api_url") else None)
    if getattr(args, "session", False):
        return handle_chat_session(args, client)
    return handle_chat(args, client)


def embedding_command(args: argparse.Namespace) -> int:
    """
    Command function for embedding generation via the embed subcommand.
    Follows Eidosian principle of elegant delegation.

    Args:
        args: Parsed command arguments

    Returns:
        Exit code (0 for success)
    """
    client = OllamaClient(api_url=args.api_url if hasattr(args, "api_url") else None)
    return handle_embed(args, client)


def models_command(args: argparse.Namespace) -> int:
    """
    Command function for model management via the models subcommand.
    Follows Eidosian principle of elegant delegation.

    Args:
        args: Parsed command arguments

    Returns:
        Exit code (0 for success)
    """
    client = OllamaClient(api_url=args.api_url if hasattr(args, "api_url") else None)
    return handle_list(args, client)


def health_command(args: argparse.Namespace) -> int:
    """
    Command function for health check via the health subcommand.
    Follows Eidosian principle of elegant simplicity.

    Args:
        args: Parsed command arguments

    Returns:
        Exit code (0 for success)
    """
    try:
        client = OllamaClient(
            api_url=args.api_url if hasattr(args, "api_url") else None
        )
        version = client.get_version()
        print(
            f"✅ Ollama server is healthy! (version {version.get('version', 'unknown')})"
        )
        return 0
    except Exception as e:
        print(f"❌ Ollama server health check failed: {e}")
        return 1


def main() -> int:
    """
    Main method guiding CLI invocation. 🏁🚀
    """
    parser = create_parser()
    args = parser.parse_args()

    client = OllamaClient(api_url=args.api_url)

    if args.command == "generate":
        return handle_generate(args, client)
    elif args.command == "chat":
        return handle_chat(args, client)
    elif args.command == "chat-session":
        return handle_chat_session(args, client)
    elif args.command == "embed":
        return handle_embed(args, client)
    elif args.command == "list":
        return handle_list(args, client)
    elif args.command == "pull":
        return handle_pull(args, client)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
