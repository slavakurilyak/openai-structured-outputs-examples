# OpenAI Structured Outputs Examples

This repository demonstrates how to use OpenAI's structured outputs with Pydantic in Python applications. Each example showcases different approaches to handling AI-generated structured data.

## Features

- Type-safe responses using Pydantic models
- Rich CLI interfaces with interactive prompts
- Error handling and graceful termination
- OpenAI's function calling and JSON response formats

## Examples

1. **UI Generator** ([ui-generator.py](examples/ui-generator.py))
   - Dynamically generates UI components based on natural language descriptions
   - Outputs both JSON structure and HTML representation
   - Supports nested components with attributes
   - Uses Rich for beautiful console output

2. **Reasoning Assistant** ([reasoning-engine.py](examples/reasoning-engine.py))
   - Separates step-by-step reasoning from final answers
   - Structured output with reasoning steps and conclusions
   - Interactive Q&A format
   - Color-coded output for better readability

3. **Action Item Extractor** ([action-item-extractor.py](examples/action-item-extractor.py))
   - Extracts structured data from unstructured meeting notes
   - Identifies action items, due dates, and owners
   - Presents data in a formatted table
   - Includes sample data for demonstration

## Prerequisites

- Python 3.11+
- Poetry for dependency management
- OpenAI API key (set in `.env` file)

## Installation

```bash
poetry install
```

## Usage

Run individual examples:

```bash
poetry run python examples/ui-generator.py
poetry run python examples/reasoning-engine.py
poetry run python examples/action-item-extractor.py
```

## Environment Setup

1. Create a `.env` file in the root directory
2. Add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Dependencies

- `openai`: OpenAI API client
- `pydantic`: Data validation using Python type annotations
- `python-dotenv`: Environment variable management
- `rich`: Terminal formatting and interactive interface

## Error Handling

All examples include robust error handling for:
- Keyboard interrupts (Ctrl+C)
- API errors
- Invalid input data

## Contributing

Feel free to submit issues and enhancement requests!