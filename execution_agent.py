def execute_response(state):
    if state.get("approved") and state.get("recommended_action"):
        state["action_executed"] = state["recommended_action"]
    return state
