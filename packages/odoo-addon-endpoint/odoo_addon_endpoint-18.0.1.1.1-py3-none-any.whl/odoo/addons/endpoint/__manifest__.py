# Copyright 2021 Camptocamp SA
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Endpoint",
    "summary": """Provide custom endpoint machinery.""",
    "version": "18.0.1.1.1",
    "license": "LGPL-3",
    "development_status": "Beta",
    "author": "Camptocamp,Odoo Community Association (OCA)",
    "maintainers": ["simahawk"],
    "website": "https://github.com/OCA/web-api",
    "depends": ["endpoint_route_handler", "rpc_helper"],
    "data": [
        "data/server_action.xml",
        "security/ir.model.access.csv",
        "security/ir_rule.xml",
        "views/endpoint_view.xml",
    ],
    "demo": [
        "demo/endpoint_demo.xml",
    ],
}
