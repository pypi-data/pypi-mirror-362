S_TICKET_CREATE = {
    "summary": {"type": "string", "required": True},
    "description": {"type": "string", "required": True},
    "partner_ref": {
        "type": "string",
        "required": True,
        "excludes": ["partner_email", "partner_vat", "contract_code"],
    },
    "partner_email": {
        "type": "string",
        "required": True,
        "excludes": ["partner_ref", "partner_vat", "contract_code"],
    },
    "partner_vat": {
        "type": "string",
        "required": True,
        "excludes": ["partner_ref", "partner_email", "contract_code"],
    },
    "contract_code": {
        "type": "string",
        "required": True,
        "excludes": ["partner_ref", "partner_email", "partner_vat"],
    },
    "team": {"type": "string"},
    "category": {"type": "string"},
    "channel": {"type": "string"},
    "priority": {"type": "string", "allowed": ["0", "1", "2", "3"]},
    "stage": {"type": "string"},
    "tags": {"type": "string"},
    "attachments": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "filename": {"type": "string", "required": True},
                "content": {"type": "string", "required": True},
                "mimetype": {"type": "string", "required": True},
            },
        },
    },
}

S_TICKET_RETURN_CREATE = {"id": {"type": "integer"}}

S_TICKET_LIST = {
    "partner_ref": {
        "type": "string",
        "required": True,
        "excludes": ["contract_code"],
    },
    "contract_code": {
        "type": "string",
        "required": True,
        "excludes": ["partner_ref"],
    },
    "stage": {"type": "string"},
}

S_TICKET_RETURN_LIST = {
    "tickets": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "id": {"type": "integer", "required": True},
                "name": {"type": "string", "required": True},
                "description": {"type": "string", "required": True},
                "date_open": {"type": "string", "required": True},
                "date_updated": {"type": "string", "required": True},
                "priority": {"type": "string"},
                "stage": {"type": "string"},
                "assigned_user": {"type": "string"},
                "channel": {"type": "string"},
                "tags": {"type": "list", "schema": {"type": "string"}},
            },
        },
    }
}
