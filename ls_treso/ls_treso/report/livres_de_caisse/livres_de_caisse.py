# Copyright (c) 2023, Kossivi Amouzou and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from operator import itemgetter
from frappe.utils import getdate

def execute(filters=None):
	filters = frappe._dict(filters or {})
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data


def get_columns(filters):
	columns = [
		{ "label": _("Date"), "fieldtype": "Date",	"fieldname": "date", "width": 100, },
		{ "label": _("Caisse"), "fieldtype": "Link", "fieldname": "caisse", "options": "Caisse", "width": 100, },
		{ "label": _("N° Pièce"), "fieldtype": "Data",	"fieldname": "name", "width": 100, },
		{ "label": _("Bénéficiaire"), "fieldtype": "Data", "fieldname": "remettant", "width": 100, },
		{ "label": _("Désignation"), "fieldtype": "Data", "fieldname": "designation", "width": 100, },
		{ "label": _("Référence"), "fieldtype": "Data", "fieldname": "reference", "width": 100, },
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
		select CASE WHEN MAX(w.date) IS NULL THEN '' ELSE MAX(w.date) END AS date, 
		NULL AS name,
		NULL AS remettant,
		'OPENING' AS designation,
		NULL AS reference,
		0 as 'recette',
		0 as 'depense', 
		SUM(w.solde) as 'solde',
		CASE WHEN MIN(w.devise) IS NULL THEN (SELECT devise FROM tabCaisse WHERE name = 'CA00') ELSE MIN(w.devise) END AS devise,
		'' as creation, 'i' AS line, MAX(w.caisse) as caisse
		from (
			select DISTINCT o.date, 
			o.name,
			o.remettant,
			o.designation,
			o.reference,
			case when n.type_operation = 'Encaissement' THEN o.montant ELSE 0 END as 'recette',
			case when n.type_operation <> 'Encaissement' THEN o.montant ELSE 0 END as 'depense', 
			case when n.type_operation = 'Encaissement' THEN o.montant ELSE -o.montant END as 'solde',
			o.devise,
			o.creation, 'd' AS line, o.caisse
			from (
				SELECT c.*
				FROM tabEncaissement c INNER JOIN `tabCaisse Initialisation` i ON i.name = c.initialisation
				WHERE CASE WHEN %(valide)s= 1 THEN  i.docstatus =1 ELSE i.docstatus <> 2 END AND  c.docstatus = 1
				UNION
				SELECT c.*
				FROM tabDecaissement c INNER JOIN `tabCaisse Initialisation` i ON i.name = c.initialisation
				WHERE CASE WHEN %(valide)s= 1 THEN  i.docstatus =1 ELSE i.docstatus <> 2 END AND  c.docstatus = 1
				) o 
			INNER JOIN `tabDetails Operation de Caisse` d on o.name = d.parent
			INNER JOIN `tabNature Operations` n on d.nature_operations = n.name
			where o.date < %(date_debut)s and (o.caisse LIKE %(caisse)s )
			) w 
		UNION
        select o.date, 
		o.name,
		o.remettant,
		o.designation,
		o.reference,
		case when n.type_operation = 'Encaissement' THEN o.montant ELSE 0 END as 'recette',
		case when n.type_operation <> 'Encaissement' THEN o.montant ELSE 0 END as 'depense', 
		case when n.type_operation = 'Encaissement' THEN o.montant ELSE -o.montant END as 'solde',
		o.devise,
		o.creation, 'd' AS line, o.caisse
		from (
			SELECT c.*
			FROM tabEncaissement c INNER JOIN `tabCaisse Initialisation` i ON i.name = c.initialisation
			WHERE CASE WHEN %(valide)s= 1 THEN  i.docstatus =1 ELSE i.docstatus <> 2 END AND  c.docstatus = 1
			UNION
			SELECT c.*
			FROM tabDecaissement c INNER JOIN `tabCaisse Initialisation` i ON i.name = c.initialisation
			WHERE CASE WHEN %(valide)s= 1 THEN  i.docstatus =1 ELSE i.docstatus <> 2 END AND  c.docstatus = 1
			) o 
		INNER JOIN `tabDetails Operation de Caisse` d on o.name = d.parent
		INNER JOIN `tabNature Operations` n on d.nature_operations = n.name
		where o.date >= %(date_debut)s  and o.date <= %(date_fin)s  and (o.caisse LIKE %(caisse)s )
""",{"date_debut": filters.date_debut, "date_fin": filters.date_fin, "caisse": filters.caisse if filters.caisse !=  None else "%", "valide" : filters.valide}, as_dict = 1
    )
	data = sorted(data, key=itemgetter('date', 'creation'))
	montant = 0
	#recette = 0
	#depense = 0
	recette_jour = 0
	depense_jour = 0
	date = ''
	data2 = []
	date_final = ''
	last_line = ''
	devise = ''
	caisse = ''
	for d in data:
		if d['line'] == 'i':
			data2.append(d)
			date = d['date']
			last_line = 'i'
		else :
			if last_line == 'i' :
				data2.append(d)
			else:
				if(date != d['date']):
					#creation lines
					data2.append({'date' : date,'name' : 'Solde Final', 'recette': recette_jour, 'depense' : depense_jour, 'solde' : montant, 'line': 'f', 'devise' : devise, 'caisse' : caisse })
					data2.append({'date' : d['date'],'name' : 'Report', 'recette': recette_jour, 'depense' : depense_jour, 'solde' : montant, 'line': 'i', 'devise' : devise, 'caisse' : caisse })
					data2.append(d)
					recette_jour = 0
					depense_jour = 0
				else:
					data2.append(d)
			date = d['date']
			last_line = 'd'

		#recette += d.recette if d.recette else 0
		#depense += d.depense if d.depense else 0
		recette_jour += d.recette if d.recette else 0
		depense_jour += d.depense if d.depense else 0
		montant += d.solde if d.solde else 0
		d.solde = montant
		date_final = d.date
		devise = d.devise
		caisse = d.caisse
		

	#data.append({'date' : date_final,'name' : 'Solde Final', 'recette': recette, 'depense' : depense, 'solde' : montant, 'line': 'f', 'devise' : devise})
	data2.append({'date' : date_final,'name' : 'Solde Final', 'recette': recette_jour, 'depense' : depense_jour, 'solde' : montant, 'line': 'f', 'devise' : devise, 'caisse' : caisse})	

	

	
	

	return data2

