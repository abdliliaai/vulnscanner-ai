def human_in_loop(state):
    state["trust_level"] = "low"
    state["approved"] = True if state["trust_level"] == "low" else False
    return state
