from graph import app

def main():
    try:
        user_query = input("What insight would you like to generate? ")
    except EOFError:
        print("No input provided. Using default query: 'summarize'")
        user_query = "summarize"
    initial_state = {
        "user_query": user_query,
        "vehicle_data": None,
        "cpi_data": None,
        "cleaned_vehicle_data": None,
        "cleaned_cpi_data": None,
        "results": None,
        "insights": None,
        "errors": [],
        "analysis_type": None,
        "column": None
    }
    final_state = app.invoke(initial_state)
    if final_state["errors"]:
        print("Errors:", final_state["errors"])
    if final_state["results"]:
        print("Results:", final_state["results"])
    if final_state["insights"]:
        print("Insights:", final_state["insights"])

if __name__ == "__main__":
    main()