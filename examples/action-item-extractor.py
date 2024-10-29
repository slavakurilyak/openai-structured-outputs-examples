# Extracting structured data from unstructured data

from typing import List, Optional
from pydantic import BaseModel, Field
from openai import OpenAI
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table

class ActionItem(BaseModel):
    description: str = Field(..., description="Description of the action item.")
    due_date: Optional[str] = Field(description="Due date for the action item, can be null if not specified.")
    owner: Optional[str] = Field(description="Owner responsible for the action item, can be null if not specified.")

class ActionItems(BaseModel):
    action_items: List[ActionItem] = Field(..., description="List of action items from the meeting.")

client = OpenAI()
console = Console()

def extract_action_items(notes: str) -> ActionItems:
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {
                "role": "system",
                "content": "Extract action items, due dates, and owners from meeting notes."
            },
            {
                "role": "user",
                "content": notes
            }
        ],
        response_format=ActionItems
    )
    return completion.choices[0].message.parsed

def display_action_items(items: ActionItems):
    # Create a table for action items
    table = Table(title="Action Items", show_header=True, header_style="bold magenta")
    table.add_column("Description", style="cyan")
    table.add_column("Due Date", style="green")
    table.add_column("Owner", style="yellow")
    
    for item in items.action_items:
        table.add_row(
            item.description,
            item.due_date or "[italic red]Not specified[/italic red]",
            item.owner or "[italic red]Not specified[/italic red]"
        )
    
    console.print(table)

def main():
    # Create a welcome message
    welcome = """
    # Meeting Notes Action Item Extractor
    
    This tool helps extract action items, due dates, and owners from meeting notes.
    Paste your meeting notes below.
    """
    console.print(Markdown(welcome))
    
    while True:
        # Get meeting notes from user
        notes = Prompt.ask("\n[bold blue]Enter your meeting notes[/bold blue]", 
                          default="Press Enter to use sample notes")
        
        # Use sample notes if no input provided
        if notes == "Press Enter to use sample notes":
            notes = """
            Meeting Notes:
            1. John to prepare Q3 report by next Friday.
            2. Sarah will contact the client about project extension.
            3. Team to brainstorm new product ideas for Q4.
            4. Mike to update the website with new features by end of month.
            5. Schedule next team building event.
            """
        
        # Process the notes
        with console.status("[bold green]Extracting action items...[/bold green]"):
            try:
                result = extract_action_items(notes)
                display_action_items(result)
            except Exception as e:
                console.print(f"\n[bold red]Error processing notes:[/bold red] {str(e)}")
        
        # Ask if user wants to process more notes
        if Prompt.ask("\n[bold]Would you like to process more notes?[/bold]", 
                     choices=["y", "n"], default="n") == "n":
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red]Program terminated by user[/bold red]")
    except Exception as e:
        console.print_exception()