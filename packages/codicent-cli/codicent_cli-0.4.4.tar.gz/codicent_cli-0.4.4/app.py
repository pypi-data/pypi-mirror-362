import sys
import os
import logging
from codicentpy import Codicent
from rich.console import Console
from rich.markdown import Markdown

# Configure logging
logging.basicConfig(level=logging.WARNING, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def show_help():
    """Display help information."""
    help_text = """
Codicent CLI - Command-line interface for the Codicent API

USAGE:
    codicent [OPTIONS] [QUESTION]
    codicent [OPTIONS] < file.txt
    echo "question" | codicent [OPTIONS]

OPTIONS:
    -t, --interactive    Start interactive chat mode
    -h, --help          Show this help message
    -v, --version       Show version information
    --verbose           Enable verbose logging
    --quiet             Suppress non-essential output

EXAMPLES:
    codicent "What is Python?"
    codicent -t
    codicent "@mention Hello there"
    echo "Help me debug this" | codicent

ENVIRONMENT:
    CODICENT_TOKEN     Your Codicent API token (required)

For more information, visit: https://github.com/izaxon/codicent-cli
"""
    print(help_text.strip())

def show_version():
    """Display version information."""
    print("Codicent CLI v0.4.4")

def validate_input(question):
    """Validate user input."""
    if not question or not question.strip():
        return False, "Empty question provided"
    
    if len(question) > 10000:  # Reasonable limit
        return False, "Question too long (max 10,000 characters)"
    
    return True, None

def main():
    # Parse command line arguments
    if "-h" in sys.argv or "--help" in sys.argv:
        show_help()
        return 0
    
    if "-v" in sys.argv or "--version" in sys.argv:
        show_version()
        return 0
    
    # Set logging level based on flags
    if "--verbose" in sys.argv:
        logging.getLogger().setLevel(logging.INFO)
        sys.argv.remove("--verbose")
        logger.info("Verbose logging enabled")
    
    if "--quiet" in sys.argv:
        logging.getLogger().setLevel(logging.ERROR)
        sys.argv.remove("--quiet")
    
    # Validate environment
    token = os.getenv("CODICENT_TOKEN")
    if not token:
        print("Error: CODICENT_TOKEN environment variable is not set.")
        print("Please set it with your Codicent API token:")
        print("  export CODICENT_TOKEN='your_token_here'")
        print("Or visit the Codicent documentation for setup instructions.")
        return 1
    
    # Initialize API client with error handling
    try:
        codicent = Codicent(token)
        logger.info("Codicent API client initialized successfully")
    except Exception as e:
        print(f"Error: Failed to initialize Codicent API client: {e}")
        logger.error(f"API client initialization failed: {e}")
        return 1
    
    conversationId = None

    # Parse interactive mode flags
    interactive = False
    if "-t" in sys.argv or "--interactive" in sys.argv:
        interactive = True
        if "-t" in sys.argv:
            sys.argv.remove("-t")
        if "--interactive" in sys.argv:
            sys.argv.remove("--interactive")
    elif len(sys.argv) == 1:
        interactive = True
        
    # Get input based on mode
    if not interactive:
        if len(sys.argv) < 2:
            if sys.stdin.isatty():
                print("Usage: codicent <question> or codicent < chat.txt or cat chat.txt | codicent or codicent (equal to codicent -t)")
                print("Use 'codicent --help' for more information.")
                return 1
            try:
                question = sys.stdin.read().strip()
            except (KeyboardInterrupt, EOFError):
                return 1
        else:
            question = " ".join(sys.argv[1:])
    else:
        if len(sys.argv) > 1:
            question = " ".join(sys.argv[1:])
        elif not sys.stdin.isatty():
            try:
                question = sys.stdin.read().strip()
            except (KeyboardInterrupt, EOFError):
                return 1
        else: 
            question = ""

    def handle_question(question):
        nonlocal conversationId
        
        # Validate input
        is_valid, error_msg = validate_input(question)
        if not is_valid:
            print(f"Error: {error_msg}")
            logger.warning(f"Invalid input: {error_msg}")
            return False
        
        console = Console()
        
        try:
            if question.strip().startswith("@"):
                logger.info("Sending message to Codicent API")
                with console.status("[dim]Sending message...[/dim]", spinner="dots"):
                    response = codicent.post_message(question, type="info")
                console.print("[green]✅ Message posted successfully.[/green]")
            else:
                logger.info("Sending chat reply to Codicent API")
                with console.status("[dim]🤔 Thinking...[/dim]", spinner="dots"):
                    response = codicent.post_chat_reply(question, conversationId)
                conversationId = response["id"]
                logger.info(f"Updated conversation ID: {conversationId}")
                
                # Show bot response with markdown formatting in green
                if interactive:
                    console.print()
                
                # Create markdown with green styling
                from rich.text import Text
                markdown_content = Markdown(response["content"])
                console.print(markdown_content, style="green")
                console.print()
            
            return True
            
        except KeyboardInterrupt:
            console.print("\n[yellow]Operation cancelled by user[/yellow]")
            return False
        except ConnectionError as e:
            console.print(f"[red]Network error: Unable to connect to Codicent API[/red]")
            logger.error(f"Connection error: {e}")
            return False
        except Exception as e:
            console.print(f"[red]API error: {e}[/red]")
            logger.error(f"API call failed: {e}")
            return False

    # Handle initial question if provided
    if question != "":
        success = handle_question(question)
        if not success and not interactive:
            return 1
    
    # Interactive mode loop
    if interactive:
        console = Console()
        console.print("\n[bold green]🤖 Codicent CLI Interactive Mode[/bold green]")
        console.print("[dim]Type your questions or use Ctrl+C to exit.[/dim]")
        console.print("[dim]Prefix with @ for info messages.[/dim]")
        console.print("─" * 50)
        
        while True:
            try:
                question = input("¤ ")
            except KeyboardInterrupt:
                console.print("\n[yellow]👋 Goodbye![/yellow]")
                break
            except EOFError:
                break
            
            if question.strip() != "":
                handle_question(question)
                # Add a separator line after each interaction
                if question.strip() != "" and not question.strip().startswith("@"):
                    console.print("[dim]" + "─" * 50 + "[/dim]")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
