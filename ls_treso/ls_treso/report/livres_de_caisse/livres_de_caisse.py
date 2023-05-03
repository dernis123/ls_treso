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
		{ "label": _("Bénéficiaire"), "fieldtype": "Data", "fieldname": "remettant", "width": 100, },
		{ "label": _("Désignation"), "fieldtype": "Data", "fieldname": "designation", "width": 100, },
		{ "label": _("Recette"), "fieldtype": "Currency", "fieldname": "recette", "options": "devise", "width": 100, },
		{ "label": _("Dépense"), "fieldtype": "Currency", "fieldname": "depense", "options": "devise", "width": 100, },
		{ "label": _("Solde"), "fieldtype": "Currency", "fieldname": "solde", "options": "devise", "width": 100, },
		{ "label": _("Devise"), "fieldtype": "Link", "fieldname": "devise", "options": "Devise", "width": 100, },
	]
	return columns


def get_data(filters):

	#frappe.msgprint(str(filters))

	data = frappe.db.sql(
        """
		select MAX(o.date) AS date, 
		NULL AS name,
		NULL AS remettant,
		'OPENING' AS designation,
		SUM(case when n.type_operation = 'Encaissement' THEN o.montant ELSE 0 END) as 'recette',
		SUM(case when n.type_operation <> 'Encaissement' THEN o.montant ELSE 0 END) as 'depense', 
		SUM(case when n.type_operation = 'Encaissement' THEN o.montant ELSE -o.montant END) as 'solde',
		MIN(o.devise) AS devise
		from (
			SELECT *
			FROM tabEncaissement
			UNION
			SELECT *
			FROM tabDecaissement
			) o 
		INNER JOIN `tabDetails Operation de Caisse` d on o.name = d.parent
		INNER JOIN `tabNature Operations` n on d.nature_operations = n.name
		where o.date < %(date_debut)s and (o.caisse LIKE %(caisse)s )
		UNION
        select o.date, 
		o.name,
		o.remettant,
		o.designation,
		case when n.type_operation = 'Encaissement' THEN o.montant ELSE 0 END as 'recette',
		case when n.type_operation <> 'Encaissement' THEN o.montant ELSE 0 END as 'depense', 
		case when n.type_operation = 'Encaissement' THEN o.montant ELSE -o.montant END as 'solde',
		o.devise
		from (
			SELECT *
			FROM tabEncaissement
			UNION
			SELECT *
			FROM tabDecaissement
			) o 
		INNER JOIN `tabDetails Operation de Caisse` d on o.name = d.parent
		INNER JOIN `tabNature Operations` n on d.nature_operations = n.name
		where o.date >= %(date_debut)s  and o.date <= %(date_fin)s  and (o.caisse LIKE %(caisse)s )
        """,{"date_debut": filters.date_debut, "date_fin": filters.date_fin, "caisse": filters.caisse if filters.caisse !=  None else "%"}, as_dict = 1
    )
	data2 = []
	montant = 0
	recette = 0
	depense = 0
	for d in data:
		recette = recette + d.recette if d.recette else 0
		depense = depense + d.depense if d.depense else 0
		montant = montant + d.solde if d.solde else 0
		d.solde = montant
	
	data.append({'name' : 'Solde Final', 'recette': recette, 'depense' : depense, 'solde' : montant})

	return data

