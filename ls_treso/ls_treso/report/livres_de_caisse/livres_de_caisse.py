# Copyright (c) 2023, Kossivi Amouzou and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from operator import itemgetter
import json 

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
		{ "label": _("Line"), "fieldtype": "Data", "fieldname": "line", "width": 100, "hidden": 1, },
	]
	return columns


def get_data(filters):

	#frappe.msgprint(str(filters))

	data = frappe.db.sql(
        """
		select CASE WHEN MAX(o.date) IS NULL THEN '' ELSE MAX(o.date) END AS date, 
		NULL AS name,
		NULL AS remettant,
		'OPENING' AS designation,
		SUM(case when n.type_operation = 'Encaissement' THEN o.montant ELSE 0 END) as 'recette',
		SUM(case when n.type_operation <> 'Encaissement' THEN o.montant ELSE 0 END) as 'depense', 
		SUM(case when n.type_operation = 'Encaissement' THEN o.montant ELSE -o.montant END) as 'solde',
		MIN(o.devise) AS devise,
		'' as creation, 'i' AS line
		from (
			SELECT c.*
			FROM tabEncaissement c INNER JOIN `tabCaisse Initialisation` i ON i.name = c.initialisation
			WHERE i.docstatus = 1
			UNION
			SELECT c.*
			FROM tabDecaissement c INNER JOIN `tabCaisse Initialisation` i ON i.name = c.initialisation
			WHERE i.docstatus = 1
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
		o.devise,
		o.creation, 'd' AS line
		from (
			SELECT c.*
			FROM tabEncaissement c INNER JOIN `tabCaisse Initialisation` i ON i.name = c.initialisation
			WHERE i.docstatus = 1
			UNION
			SELECT c.*
			FROM tabDecaissement c INNER JOIN `tabCaisse Initialisation` i ON i.name = c.initialisation
			WHERE i.docstatus = 1
			) o 
		INNER JOIN `tabDetails Operation de Caisse` d on o.name = d.parent
		INNER JOIN `tabNature Operations` n on d.nature_operations = n.name
		where o.date >= %(date_debut)s  and o.date <= %(date_fin)s  and (o.caisse LIKE %(caisse)s )
        """,{"date_debut": filters.date_debut, "date_fin": filters.date_fin, "caisse": filters.caisse if filters.caisse !=  None else "%"}, as_dict = 1
    )
	data = sorted(data, key=itemgetter('date', 'creation'))
	montant = 0
	recette = 0
	depense = 0
	date = ''
	data2 = []
	date_final = ''
	for d in data:
		recette += d.recette if d.recette else 0
		depense += d.depense if d.depense else 0
		montant += d.solde if d.solde else 0
		d.solde = montant
		date_final = d.date

		if d['line'] == 'i':
			if(date != d['date']):
				data2.append(d)
				date = d['date']
		elif d['line'] == 'd':
			if(date != d['date']):
				#creation lines
				data2.append(d)
				data2.append({'name' : 'Solde Final au ' + str(date), 'recette': recette, 'depense' : depense, 'solde' : montant, 'line': 'f'})
				data2.append({'name' : ' ', 'recette': ' ', 'depense' : ' ', 'solde' : ' ', 'line': 'b'})
				data2.append({'name' : 'Report au ' + str(d['date']), 'recette': recette, 'depense' : depense, 'solde' : montant, 'line': 'i'})
				date = d['date']
		else:
			data2.append(d)
		

	data.append({'date' : date_final,'name' : 'Solde Final', 'recette': recette, 'depense' : depense, 'solde' : montant, 'line': 'f'})
	#data2.append({'date' : date_final,'name' : 'Solde Final', 'recette': recette, 'depense' : depense, 'solde' : montant, 'line': 'f'})	

	
	

	return data

