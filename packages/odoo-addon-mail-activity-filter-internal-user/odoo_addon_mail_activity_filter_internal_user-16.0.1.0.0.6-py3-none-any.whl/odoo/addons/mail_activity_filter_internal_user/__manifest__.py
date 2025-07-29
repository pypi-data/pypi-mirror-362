# SPDX-FileCopyrightText: 2022 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "Mail Activity Filter Internal User",
    "summary": """
        Filter on internal user by default when assigning someone to an activity.""",
    "version": "16.0.1.0.0",
    "category": "Uncategorized",
    "website": "https://github.com/OCA/social",
    "author": "Coop IT Easy SC, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "depends": ["mail"],
    "excludes": [],
    "data": [
        "views/mail_activity.xml",
    ],
    "demo": [],
    "qweb": [],
}
