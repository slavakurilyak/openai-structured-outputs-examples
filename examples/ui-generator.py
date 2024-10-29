# Dynamically generating user interfaces based on the user’s intent

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
import json
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.syntax import Syntax
from rich.markdown import Markdown

load_dotenv()

class UIComponentType(str, Enum):
    div = "div"
    button = "button"
    header = "header"
    section = "section"
    field = "field"
    form = "form"

class Attribute(BaseModel):
    name: str
    value: str

class UIComponent(BaseModel):
    type: UIComponentType
    label: str
    children: Optional[List['UIComponent']] = []
    attributes: List[Attribute] = []

UIComponent.update_forward_refs()

class UI(BaseModel):
    components: List[UIComponent]

client = OpenAI()

# Add console instance
console = Console()

def generate_ui(user_intent: str) -> UI:
    completion = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=[
            {
                "role": "system",
                "content": "You are a user interface assistant. Your job is to help users visualize their website and app ideas by generating UI components based on their intent."
            },
            {
                "role": "user",
                "content": f"Generate a JSON representation of a UI component based on this intent: {user_intent}. Include 'json' in your response."
            }
        ],
        response_format={"type": "json_object"},
        functions=[
            {
                "name": "create_ui",
                "description": "Create a UI based on the user's intent",
                "parameters": UI.schema()
            }
        ],
        function_call={"name": "create_ui"}
    )

    ui_data = completion.choices[0].message.function_call.arguments
    return UI.parse_raw(ui_data)

def render_ui(ui: UI, indent: int = 0) -> str:
    result = ""
    for component in ui.components:
        result += render_component(component, indent)
    return result

def render_component(component: UIComponent, indent: int = 0) -> str:
    attributes = " ".join([f'{attr.name}="{attr.value}"' for attr in component.attributes])
    result = f"{'  ' * indent}<{component.type.value} {attributes}>\n"
    
    if component.label:
        result += f"{'  ' * (indent + 1)}{component.label}\n"
    
    for child in component.children:
        result += render_component(child, indent + 1)
    
    result += f"{'  ' * indent}</{component.type.value}>\n"
    return result

def main():
    # Create a welcome message
    welcome = """
    # UI Generator
    
    This tool helps you generate UI components based on your description.
    You can describe what kind of interface you want, and it will generate 
    the appropriate UI structure.
    """
    console.print(Markdown(welcome))
    
    # Get user input with Rich prompt
    user_intent = Prompt.ask("\n[bold blue]Describe the UI you want to create[/bold blue]")
    
    with console.status("[bold green]Generating UI structure...[/bold green]"):
        generated_ui = generate_ui(user_intent)
    
    # Display the JSON structure with syntax highlighting
    console.print("\n[bold]Generated UI Structure:[/bold]")
    json_str = json.dumps(generated_ui.model_dump(), indent=2)
    syntax = Syntax(json_str, "json", theme="monokai", line_numbers=True)
    console.print(Panel(syntax))
    
    # Display the rendered UI with syntax highlighting
    console.print("\n[bold]Rendered UI:[/bold]")
    rendered = render_ui(generated_ui)
    html_syntax = Syntax(rendered, "html", theme="monokai", line_numbers=True)
    console.print(Panel(html_syntax))
    
    # Ask if user wants to try again
    if Prompt.ask("\n[bold]Would you like to generate another UI?[/bold]", 
                  choices=["y", "n"], default="n") == "y":
        main()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red]Program terminated by user[/bold red]")
    except Exception as e:
        console.print_exception()