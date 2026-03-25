# Multi-Agent Economic Analysis System

This system uses LangChain, LangGraph, and Ollama to provide interactive economic insights from CPI and vehicle sales data.

## Prerequisites

- Python 3.8+
- Ollama installed and running locally
- Pull the llama3 model: `ollama pull llama3`

## Installation

1. Clone or download the project.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
   (Or manually: langchain langgraph langchain-community pandas numpy matplotlib seaborn)

## Files

- `main.py`: Entry point, prompts for user query.
- `graph.py`: Defines the LangGraph workflow.
- `router.py`: Routes user query to analysis type.
- `agents/`: Contains agent functions.
- `utils/visualization.py`: Plotting functions.

## Usage

Run the system:
```
python main.py
```

Enter a query like:
- "Show CPI trends over time"
- "Compare vehicle sales with CPI"
- "Give me correlation between CPI categories"
- "Show histogram of CPI food category"
- "Summarize key economic insights"

The system will process the data and generate the requested output.

## Output

- Plots saved as PNG files.
- LLM insights saved to `insights.txt`.
- Results printed to console.

## Data Files

Uses existing local files:
- `CPI_Historic_Values_Zindi_Feb_23.csv`
- `Naamsa_Vehicle_Sales.csv`

Ensure these files are in the project directory.