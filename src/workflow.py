ALLOWED_TRANSITIONS = {
    "requested": {"plate_making"},
    "plate_making": {"plates_made"},
    "plates_made": {"mounting"},
    "mounting": {"production_ready"},
    "production_ready": {"production", "shipping_ready"},
    "production": {"closed"},
    "shipping_ready": {"shipped"},
    "shipped": {"closed"},
}

def can_transition(current_state, next_state):
    return next_state in ALLOWED_TRANSITIONS.get(current_state, set())
