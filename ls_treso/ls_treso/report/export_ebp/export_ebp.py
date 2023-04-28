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
		{ "label": _("Code Journal"), "fieldtype": "Data", "fieldname": "journal", "width": 100, },
		{ "label": _("Date"), "fieldtype": "Date",	"fieldname": "date", "width": 100, },
		{ "label": _("Compte"), "fieldtype": "Link", "fieldname": "compte", "options": "Compte General", "width": 100, },
		{ "label": _("Compte Auxiliaire"), "fieldtype": "Link", "fieldname": "tiers", "options": "Tiers", "width": 100, },
		{ "label": _("N° Pièce"), "fieldtype": "Data",	"fieldname": "name", "width": 100, },
		{ "label": _("Date Pièce"), "fieldtype": "Date",	"fieldname": "date", "width": 100, },
		{ "label": _("Libellé"), "fieldtype": "Data", "fieldname": "designation", "width": 100, },
		{ "label": _("Débit"), "fieldtype": "Currency", "fieldname": "debit", "options": "devise_caisse", "width": 100, },
		{ "label": _("Crédit"), "fieldtype": "Currency", "fieldname": "credit", "options": "devise_caisse", "width": 100, },
		{ "label": _("Montant seul (+/-)"), "fieldtype": "Currency", "fieldname": "montant_seul", "options": "devise_caisse", "width": 100, },
		{ "label": _("Montant (associé au sens)"), "fieldtype": "Currency", "fieldname": "montant", "options": "devise_caisse", "width": 100, },
		{ "label": _("Sens"), "fieldtype": "Data", "fieldname": "sens_2", "width": 100, },
		{ "label": _("Status"), "fieldtype": "Data", "fieldname": "status", "width": 100, },
		{ "label": _("Devise Caisse"), "fieldtype": "Link", "fieldname": "devise_caisse", "options": "Devise", "width": 100, "hidden": 1, },
		{ "label": _("Devise"), "fieldtype": "Link", "fieldname": "devise", "options": "Devise", "width": 100, "hidden": 0, },
		{ "label": _("Débit devise"), "fieldtype": "Currency", "fieldname": "debit_2", "options": "devise", "width": 100, },
		{ "label": _("Crédit devise"), "fieldtype": "Currency", "fieldname": "credit_2", "options": "devise", "width": 100, },
		{ "label": _("Montant devise seul (+/-)"), "fieldtype": "Currency", "fieldname": "montant_seul_2", "options": "devise", "width": 100, },
		{ "label": _("Montant Devise (associé au sens)"), "fieldtype": "Currency", "fieldname": "montant_2", "options": "devise", "width": 100, },
		{ "label": _("Sens"), "fieldtype": "Data", "fieldname": "sens_2", "width": 100, },
		{ "label": _("Status"), "fieldtype": "Data", "fieldname": "status", "width": 100, },
		
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
		d.montant * o.cours AS montant_2,
		o.journal,
		o.devise,
		o.devise_caisse,
		d.compte_analytique,
		d.compte_analytique_2,
		d.compte_analytique_3,
		d.compte_analytique_4,
		d.compte_analytique_5,
		CASE WHEN d.sens = 'Debit' THEN d.montant else NULL END AS debit,
		CASE WHEN d.sens = 'Credit' THEN d.montant else NULL END AS credit,
		CASE WHEN d.sens = 'Debit' THEN d.montant else -d.montant END AS montant_seul,
		CASE WHEN d.sens = 'Debit' THEN 'D' else 'C' END AS sens_2,
		CASE WHEN d.sens = 'Debit' THEN d.montant / o.cours else NULL END AS debit_2,
		CASE WHEN d.sens = 'Credit' THEN d.montant / o.cours else NULL END AS credit_2,
		CASE WHEN d.sens = 'Debit' THEN d.montant / o.cours else -d.montant / o.cours END AS montant_seul_2
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

