def router(state):
    user_query = state["user_query"].lower()
    if "trend" in user_query:
        if "cpi" in user_query:
            state["analysis_type"] = "plot_cpi_trend"
        elif "vehicle" in user_query:
            state["analysis_type"] = "plot_vehicle_trend"
        else:
            state["analysis_type"] = "plot_cpi_trend"  # default
    elif "compare" in user_query:
        state["analysis_type"] = "compare_cpi_vs_vehicle"
    elif "correlation" in user_query:
        state["analysis_type"] = "generate_correlation_heatmap"
    elif "histogram" in user_query:
        if "food" in user_query:
            state["analysis_type"] = "generate_histogram"
            state["column"] = "Food and non-alcoholic beverages"
        else:
            state["analysis_type"] = "generate_histogram"
            state["column"] = "Headline_CPI"
    elif "predict" in user_query:
        state["analysis_type"] = "generate_prediction"
    elif "summary" in user_query or "insights" in user_query:
        state["analysis_type"] = "generate_summary_with_llm"
    else:
        state["analysis_type"] = "generate_summary_with_llm"  # default
    return state