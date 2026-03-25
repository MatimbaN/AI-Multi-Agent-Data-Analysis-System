from utils.visualization import plot_cpi_trend, plot_vehicle_trend, compare_cpi_vs_vehicle, generate_histogram, generate_correlation_heatmap, generate_prediction
from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="llama3")

def analyst_agent(state):
    analysis_type = state.get("analysis_type")
    if not analysis_type:
        state["errors"].append("No analysis type decided")
        return state
    try:
        if analysis_type == "plot_cpi_trend":
            result = plot_cpi_trend(state["cleaned_cpi_data"])
            state["results"] = result
        elif analysis_type == "plot_vehicle_trend":
            result = plot_vehicle_trend(state["cleaned_vehicle_data"])
            state["results"] = result
        elif analysis_type == "compare_cpi_vs_vehicle":
            result = compare_cpi_vs_vehicle(state["cleaned_cpi_data"], state["cleaned_vehicle_data"])
            state["results"] = result
        elif analysis_type == "generate_correlation_heatmap":
            result = generate_correlation_heatmap(state["cleaned_cpi_data"])
            state["results"] = result
        elif analysis_type == "generate_histogram":
            column = state.get("column", "Headline_CPI")
            result = generate_histogram(state["cleaned_cpi_data"], column)
            state["results"] = result
        elif analysis_type == "generate_prediction":
            result = generate_prediction(state["cleaned_cpi_data"], state["cleaned_vehicle_data"])
            state["results"] = result
        elif analysis_type == "generate_summary_with_llm":
            insights = generate_summary_with_llm(state)
            state["insights"] = insights
    except Exception as e:
        state["errors"].append(str(e))
    return state

def generate_summary_with_llm(state):
    cpi_df = state["cleaned_cpi_data"]
    vehicle_df = state["cleaned_vehicle_data"]
    cpi_summary = cpi_df.describe().to_string()
    vehicle_summary = vehicle_df.describe().to_string()
    prompt = f"Summarize key economic insights from the following data:\n\nCPI Data Summary:\n{cpi_summary}\n\nVehicle Sales Data Summary:\n{vehicle_summary}\n\nProvide trends, economic meaning, and observations."
    response = llm.invoke(prompt)
    with open("insights.txt", "w") as f:
        f.write(response)
    return response