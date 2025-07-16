def recommend_response(state):
    if state.get("threat_detected"):
        state["recommended_action"] = "Block IP and reset admin password"
    else:
        state["recommended_action"] = "No action needed"
    return state
