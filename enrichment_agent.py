def enrich_threat(state):
    if state.get("threat_detected"):
        state["geo_location"] = "USA"
        state["user_behavior"] = "Unusual access time"
    return state
