"""Starter module for the Flexographic Workflow Management System."""

WORKFLOW_STATES = [
    "requested", "plate_making", "plates_made", "mounting",
    "production_ready", "production", "shipping_ready", "shipped", "closed"
]

def health_check():
    return {"status": "ok", "service": "flexo-workflow"}
