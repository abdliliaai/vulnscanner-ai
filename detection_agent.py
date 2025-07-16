def detect_threat(state):
    log = state.get("raw_log", "")
    if "failed login" in log.lower():
        state["threat_detected"] = True
        state["detection_details"] = "Brute-force attempt detected"
    else:
        state["threat_detected"] = False
        state["detection_details"] = "No threat found"
    return state
