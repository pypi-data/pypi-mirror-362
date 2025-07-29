# Copyright 2024-SomItCoop SCCL(<https://gitlab.com/somitcoop>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "widget_list_row_color",
    "version": "16.0.1.0.1",
    "depends": [
        "web",
    ],
    "author": """
        Som It Cooperatiu SCCL,
        Som Connexió SCCL,
        Odoo Community Association (OCA)
    """,
    "category": "web",
    "website": "https://gitlab.com/somitcoop/erp-research/odoo-helpdesk",
    "license": "AGPL-3",
    "summary": """
        SomItCoop ODOO widget to set background-color and color on list view
    """,
    "data": [],
    "assets": {
        "web.assets_backend": [
            "widget_list_row_color/static/src/js/list_renderer.js",
        ],
    },
    "qweb": [],
    "application": False,
    "installable": True,
}
