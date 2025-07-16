def generate_summary(state):
    summary = f"""
    Threat: {state.get('detection_details')}
    MITRE Mapping: {state.get('mitre_tactic')} / {state.get('mitre_technique')}
    Explanation: {state.get('explanation')}
    Action Taken: {state.get('action_executed')}
    """
    state["summary"] = summary.strip()
    return state
