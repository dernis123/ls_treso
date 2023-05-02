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
		{ "label": _("Colonne 1"), "fieldtype": "Data", "fieldname": "col_1", "width": 100, },
		{ "label": _("Colonne 2"), "fieldtype": "Data",	"fieldname": "col_2", "width": 100, },
		{ "label": _("Colonne 3"), "fieldtype": "Data", "fieldname": "col_3", "width": 100, },
		{ "label": _("Colonne 4"), "fieldtype": "Data", "fieldname": "col_4", "width": 100, },
		{ "label": _("Colonne 5"), "fieldtype": "Data",	"fieldname": "col_5", "width": 100, },
		{ "label": _("Colonne 6"), "fieldtype": "Data",	"fieldname": "col_6", "width": 100, },
		{ "label": _("Colonne 7"), "fieldtype": "Data", "fieldname": "col_7", "width": 100, },
		{ "label": _("Colonne 8"), "fieldtype": "Data", "fieldname": "col_8", "width": 100, },
		{ "label": _("Colonne 9"), "fieldtype": "Data", "fieldname": "col_9", "width": 100, },
		{ "label": _("Colonne 10"), "fieldtype": "Data", "fieldname": "col_10", "width": 100, },
		{ "label": _("Colonne 11"), "fieldtype": "Data", "fieldname": "col_11", "width": 100, },
		{ "label": _("Colonne 12"), "fieldtype": "Data", "fieldname": "col_12", "width": 100, },
		{ "label": _("Colonne 13"), "fieldtype": "Data", "fieldname": "col_13", "width": 100, },
		{ "label": _("Colonne 14"), "fieldtype": "Data", "fieldname": "col_14", "width": 100, },
		{ "label": _("Colonne 15"), "fieldtype": "Data", "fieldname": "col_15", "width": 100, },
		{ "label": _("Colonne 16"), "fieldtype": "Data", "fieldname": "col_16", "width": 100, },
		{ "label": _("Colonne 17"), "fieldtype": "Data", "fieldname": "col_17", "width": 100, },
		{ "label": _("Colonne 18"), "fieldtype": "Data", "fieldname": "col_18", "width": 100, },
		{ "label": _("Colonne 19"), "fieldtype": "Data", "fieldname": "col_19", "width": 100, },
		{ "label": _("Colonne 20"), "fieldtype": "Data", "fieldname": "col_20", "width": 100, },
		{ "label": _("Colonne 21"), "fieldtype": "Data", "fieldname": "col_21", "width": 100, },
		
	]
	return columns


def get_data(filters):

	#frappe.msgprint(str(filters))
	company_currency = frappe.db.get_value("Societe",filters.societe,"devise_de_base") 
	data = []
	line = frappe._dict({})

	names = frappe.db.sql(
        """
        SELECT name
		FROM (
			SELECT *
			FROM tabEncaissement
			UNION
			SELECT *
			FROM tabDecaissement
			) o 
		WHERE o.date >= %(date_debut)s AND o.date <= %(date_fin)s AND docstatus = 1 AND o.caisse LIKE %(caisse)s
		GROUP BY name
        """,{"date_debut": filters.date_debut, "date_fin": filters.date_fin, "caisse": filters.caisse if filters.caisse else '%' }, as_dict = 1
    )

	for n in names:
		details = frappe.db.sql(
			"""
			SELECT *,%(currency)s as company_currency 
			FROM (
				SELECT *
				FROM tabEncaissement
				UNION
				SELECT *
				FROM tabDecaissement
				) o 
			INNER JOIN `tabComptabilisation` d on o.name = d.parent
			WHERE o.name = %(name)s 
			""",{"name": n.name, "currency":company_currency }, as_dict = 1
    	)

		line = { "col_1": "G", "col_2": "ZACCN", "col_3": "", "col_4": details[0].site, "col_5": details[0].societe, "col_6": details[0].journal, 
	   			 "col_7": details[0].date, "col_8": details[0].date, "col_9": details[0].devise, "col_10": 1, }
		data.append(line)
    
		i = 0
		for d in details:
			i = i + 1
			line = { "col_1": "D", "col_2": i, "col_3": 1, "col_4": i, "col_5": d.site, "col_6": d.control, "col_7": d.compte, "col_8": d.tiers, "col_9": d.description,
					"col_10": 1 if d.sens == 'Debit' else -1, "col_11": d.montant, }
			data.append(line)
			
			if d.compte_analytique :
				line = { "col_1": "A", "col_2": 1, "col_3": "CCT", "col_4": d.compte_analytique, "col_5": "PRD", "col_6": d.compte_analytique_2,
						"col_7": "ITM", "col_8": d.compte_analytique_3, "col_9": "BPT", "col_10": d.compte_analytique_4,
						"col_11": "EMP", "col_12": d.compte_analytique_5, "col_13": "", "col_14": "", "col_15": "", "col_16": "", "col_17": "",
						"col_18": "", "col_19": "", "col_20": "", "col_21": d.montant, }
				data.append(line)
		

	return data

