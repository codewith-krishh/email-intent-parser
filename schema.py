EMAIL_SCHEMA = {
    "type": "json_schema",
    "json_schema": {
        "name": "email_analysis",
        "schema": {
            "type": "object",
            "properties": {
                "sender_intent": {
                    "type": "string",
                    "enum": ["billing", "bug_report", "feature_request", "sales_inquiry", "churn_risk", "general"]
                },
                "urgency_score": {
                    "type": "integer",
                    "description": "1 (low) to 5 (critical)"
                },
                "tone": {
                    "type": "string",
                    "enum": ["neutral", "frustrated", "angry", "confused", "positive"]
                },
                "action_required": {
                    "type": "string",
                    "description": "One concrete next step for the support/sales team"
                }
            },
            "required": ["sender_intent", "urgency_score", "tone", "action_required"],
            "additionalProperties": False
        },
        "strict": True
    }
}