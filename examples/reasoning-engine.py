# Separating a final answer from supporting reasoning or additional commentary

from typing import List
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.markdown import Markdown

load_dotenv()

class ReasoningResponse(BaseModel):
    reasoning_steps: List[str]
    answer: str

client = OpenAI()

# Add console instance
console = Console()

def generate_reasoning_response(question: str) -> ReasoningResponse:
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant. Provide step-by-step reasoning before giving the final answer."
            },
            {
                "role": "user",
                "content": question
            }
        ],
        response_format=ReasoningResponse
    )

    return completion.choices[0].message.parsed

def main():
    # Create a welcome message
    welcome = """
    # Reasoning Assistant
    
    This tool helps break down questions with step-by-step reasoning
    before providing a final answer.
    """
    console.print(Markdown(welcome))
    
    while True:
        # Get user input with Rich prompt
        question = Prompt.ask("\n[bold blue]Enter your question[/bold blue]")
        
        with console.status("[bold green]Thinking...[/bold green]"):
            response = generate_reasoning_response(question)
        
        # Display reasoning steps in a panel
        console.print("\n[bold]Reasoning Process:[/bold]")
        steps = "\n".join(f"[cyan]Step {i+1}:[/cyan] {step}" 
                         for i, step in enumerate(response.reasoning_steps))
        console.print(Panel(steps, title="Steps", border_style="blue"))
        
        # Display final answer in a panel
        console.print("\n[bold]Final Answer:[/bold]")
        console.print(Panel(response.answer, border_style="green"))
        
        # Ask if user wants to try again
        if Prompt.ask("\n[bold]Would you like to ask another question?[/bold]", 
                     choices=["y", "n"], default="n") == "n":
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red]Program terminated by user[/bold red]")
    except Exception as e:
        console.print_exception()