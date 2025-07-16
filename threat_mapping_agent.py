def map_to_mitre(state):
    if state.get("threat_detected"):
        state["mitre_tactic"] = "Credential Access"
        state["mitre_technique"] = "T1110 - Brute Force"
    return state
