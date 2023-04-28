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
		{ "label": _("Date"), "fieldtype": "Date",	"fieldname": "date", "width": 100, },
		{ "label": _("N° Pièce"), "fieldtype": "Data",	"fieldname": "name", "width": 100, },
		{ "label": _("Compte"), "fieldtype": "Link", "fieldname": "compte", "options": "Compte General", "width": 100, },
		{ "label": _("Tiers"), "fieldtype": "Link", "fieldname": "tiers", "options": "Tiers", "width": 100, },
		{ "label": _("Libellé"), "fieldtype": "Data", "fieldname": "designation", "width": 100, },
		{ "label": _("Parité|cours"), "fieldtype": "Float", "fieldname": "cours", "width": 100, },
		{ "label": _("Montant devise"), "fieldtype": "Currency", "fieldname": "montant", "options": "devise", "width": 100, },
		{ "label": _("Code Journal"), "fieldtype": "Data", "fieldname": "journal", "width": 100, },
		{ "label": _("Débit"), "fieldtype": "Currency", "fieldname": "debit", "options": "devise", "width": 100, },
		{ "label": _("Crédit"), "fieldtype": "Currency", "fieldname": "credit", "options": "devise", "width": 100, },
		{ "label": _("Devise"), "fieldtype": "Link", "fieldname": "devise", "options": "Devise", "width": 100, "hidden": 1, },

		{ "label": _("Imputation Analytique"), "fieldtype": "Link", "fieldname": "compte_analytique", "options": "Compte Analytique", "width": 100, "hidden": 0, },
		{ "label": _("Imputation Analytique 2"), "fieldtype": "Link", "fieldname": "compte_analytique_2", "options": "Compte Analytique 2", "width": 100, "hidden": 0, },
		{ "label": _("Imputation Analytique 3"), "fieldtype": "Link", "fieldname": "compte_analytique_3", "options": "Compte Analytique 3", "width": 100, "hidden": 0, },
		{ "label": _("Imputation Analytique 4"), "fieldtype": "Link", "fieldname": "compte_analytique_4", "options": "Compte Analytique 4", "width": 100, "hidden": 0, },
		{ "label": _("Imputation Analytique 5"), "fieldtype": "Link", "fieldname": "compte_analytique_5", "options": "Compte Analytique 5", "width": 100, "hidden": 0, },
	]
	return columns


def get_data(filters):

	#frappe.msgprint(str(filters))

	data = frappe.db.sql(
        """
        SELECT o.date, 
		o.name, 
		d.compte,
		d.tiers,
		o.designation,
		o.cours,
		d.montant,
		o.journal,
		o.devise,
		d.compte_analytique,
		d.compte_analytique_2,
		d.compte_analytique_3,
		d.compte_analytique_4,
		d.compte_analytique_5,
		CASE WHEN d.sens = 'Debit' THEN d.montant else NULL END AS debit,
		CASE WHEN d.sens = 'Credit' THEN d.montant else NULL END AS credit
		FROM (
			SELECT *
			FROM tabEncaissement
			UNION
			SELECT *
			FROM tabDecaissement
			) o 
		INNER JOIN `tabComptabilisation` d on o.name = d.parent
		WHERE o.date >= %(date_debut)s AND o.date <= %(date_fin)s
        """,{"date_debut": filters.date_debut, "date_fin": filters.date_fin, }, as_dict = 1
    )

	return data

