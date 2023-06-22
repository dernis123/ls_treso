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
		{ "label": _("N°"), "fieldtype": "Data",	"fieldname": "numero", "width": 100, },
		{ "label": _("Date"), "fieldtype": "Date", "fieldname": "date", "width": 100, },
		{ "label": _("N° Compte"), "fieldtype": "Link", "fieldname": "compte", "options": "Compte General", "width": 100, },
		{ "label": _("Service"), "fieldtype": "Data",	"fieldname": "department", "width": 100, },
		{ "label": _("Bénéficiaire"), "fieldtype": "Data", "fieldname": "remettant", "width": 100, },
		{ "label": _("Intitulé du Compte"), "fieldtype": "Data", "fieldname": "designation", "width": 100, },
		{ "label": _("Libellé"), "fieldtype": "Data", "fieldname": "commentaire", "width": 100, },
		{ "label": _("USD"), "fieldtype": "Currency", "fieldname": "usd", "width": 100, },
		{ "label": _("CDF"), "fieldtype": "Currency", "fieldname": "cdf", "width": 100, },
	]
	return columns


def get_data(filters):
	data = frappe.db.sql(
        """
        SELECT d.name AS numero,d.date,n.compte_comptable AS compte,d.remettant as beneficiaire,c.designation,e.department,d.commentaire, 
			CASE WHEN d.devise = 'USD' THEN o.montant_devise ELSE 0 END usd,
			CASE WHEN d.devise = 'CDF' THEN o.montant_devise ELSE 0 END cdf,
			'' AS Observation
		FROM `tabDemande Paiement` d INNER JOIN `tabDetails Operation de Caisse` o ON d.name = o.parent
			INNER JOIN `tabNature Operations` n ON o.nature_operations = n.name
			INNER JOIN `tabCompte General` c ON c.name = n.compte_comptable
			LEFT JOIN tabEmployee e ON d.owner = e.user_id
		WHERE o.parenttype = 'Demande Paiement' AND d.date >= %(date)s
        """,{"date": filters.date }, as_dict = 1
    )

	return data

