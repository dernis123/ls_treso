# Copyright (c) 2023, Kossivi Amouzou and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	filters = frappe._dict(filters or {})
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data


def get_columns(filters):
	columns = [
		{ "label": _("Caisse"), "fieldtype": "Data",	"fieldname": "name", "width": 100, },
		{ "label": _("Désignation"), "fieldtype": "Data", "fieldname": "designation", "width": 100, },
		{ "label": _("Solde"), "fieldtype": "Currency", "fieldname": "solde", "options": "devise", "width": 100, },
		{ "label": _("Devise"), "fieldtype": "Data", "fieldname": "devise", "width": 100, "hidden": 1, },
	]
	return columns


def get_data(filters):

	#frappe.msgprint(str(filters))

	data = frappe.db.sql(
        """
        SELECT name, designation, date_solde, solde, devise
		FROM `tabCaisse`
		WHERE name = %(name)s
        """,{ "name": filters.name }, as_dict = 1
    )

	return data

