from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional
import pandas as pd

from agents.data_collector import data_collector_agent
from agents.data_cleaner import data_cleaner_agent
from agents.analyst import analyst_agent
from router import router

class State(TypedDict):
    user_query: str
    vehicle_data: Optional[pd.DataFrame]
    cpi_data: Optional[pd.DataFrame]
    cleaned_vehicle_data: Optional[pd.DataFrame]
    cleaned_cpi_data: Optional[pd.DataFrame]
    results: Optional[str]
    insights: Optional[str]
    errors: list
    analysis_type: Optional[str]
    column: Optional[str]

graph = StateGraph(State)

graph.add_node("data_collector", data_collector_agent)
graph.add_node("data_cleaner", data_cleaner_agent)
graph.add_node("router", router)
graph.add_node("analyst", analyst_agent)

graph.set_entry_point("data_collector")

graph.add_edge("data_collector", "data_cleaner")
graph.add_edge("data_cleaner", "router")
graph.add_edge("router", "analyst")
graph.add_edge("analyst", END)

app = graph.compile()