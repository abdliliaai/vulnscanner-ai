"""
Eventra-AI Main Entry Point
Full SOC Level 1 Workflow Using LangGraph and Modular Agents
"""

from langgraph.graph import StateGraph, END
from eventra_ai.agents.detection_agent import detect_threat
from eventra_ai.agents.enrichment_agent import enrich_threat
from eventra_ai.agents.threat_mapping_agent import map_to_mitre
from eventra_ai.agents.explainability_agent import explain_threat
from eventra_ai.agents.response_agent import recommend_response
from eventra_ai.agents.approval_agent import human_in_loop
from eventra_ai.agents.execution_agent import execute_response
from eventra_ai.agents.summary_agent import generate_summary

# Build the graph
graph = StateGraph()
graph.add_node("detect", detect_threat)
graph.add_node("enrich", enrich_threat)
graph.add_node("map_mitre", map_to_mitre)
graph.add_node("explain", explain_threat)
graph.add_node("recommend", recommend_response)
graph.add_node("approve", human_in_loop)
graph.add_node("execute", execute_response)
graph.add_node("summarize", generate_summary)

graph.set_entry_point("detect")
graph.add_edge("detect", "enrich")
graph.add_edge("enrich", "map_mitre")
graph.add_edge("map_mitre", "explain")
graph.add_edge("explain", "recommend")
graph.add_edge("recommend", "approve")
graph.add_edge("approve", "execute")
graph.add_edge("execute", "summarize")
graph.add_edge("summarize", END)

# Run the workflow
workflow = graph.compile()
input_data = {
    "raw_log": "Multiple failed login attempts from IP 192.168.1.100 on user admin."
}
result = workflow.invoke(input_data)

print("\n=== Final Case Summary ===")
print(result.get("summary", "No summary generated."))
