def explain_threat(state):
    if state.get("threat_detected"):
        state["explanation"] = (
            f"A brute-force login attempt was detected. "
            f"Tactic: {state.get('mitre_tactic')}, "
            f"Technique: {state.get('mitre_technique')}."
        )
    return state
