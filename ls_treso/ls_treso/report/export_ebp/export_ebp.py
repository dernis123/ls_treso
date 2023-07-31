# Copyright (c) 2023, Kossivi Amouzou and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from operator import itemgetter

def execute(filters=None):
	filters = frappe._dict(filters or {})
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data


def get_columns(filters):
	columns = [
		{ "label": _("Code Journal"), "fieldtype": "Data", "fieldname": "journal", "width": 100, },
		{ "label": _("Date"), "fieldtype": "Date",	"fieldname": "date", "width": 100, },
		{ "label": _("N° de compte"), "fieldtype": "Link", "fieldname": "compte", "options": "Compte General", "width": 100, },
		{ "label": _("Compte Auxiliaire"), "fieldtype": "Link", "fieldname": "tiers", "options": "Tiers", "width": 100, },
		{ "label": _("Pièce"), "fieldtype": "Data",	"fieldname": "name", "width": 100, },
		{ "label": _("Date de pièce"), "fieldtype": "Date",	"fieldname": "date", "width": 100, },
		{ "label": _("Libellé"), "fieldtype": "Data", "fieldname": "designation", "width": 100, },
		{ "label": _("Montant (associé au sens)"), "fieldtype": "Currency", "fieldname": "montant", "options": "company_currency", "width": 100, },
		{ "label": _("Sens"), "fieldtype": "Data", "fieldname": "sens_2", "width": 100, },
		{ "label": _("Statut"), "fieldtype": "Data",	"fieldname": "statut", "width": 100, },
		{ "label": _("N° de ligne pour les documents associés"), "fieldtype": "Data",	"fieldname": "line_doc", "width": 100, },
		{ "label": _("N° de ligne pour les ventilations analytiques"), "fieldtype": "Data",	"fieldname": "line_ana", "width": 100, },
		{ "label": _("Plan analytique"), "fieldtype": "Data",	"fieldname": "plan", "width": 100, },
		{ "label": _("Poste analytique"), "fieldtype": "Data",	"fieldname": "poste", "width": 100, },	
		{ "label": _("Montant de la ventilation analytique"), "fieldtype": "Currency", "fieldname": "montant_ana", "options": "company_currency", "width": 100, },	

		
	]
	return columns


def get_data(filters):

	#frappe.msgprint(str(filters))
	company_currency = frappe.db.get_value("Societe",filters.societe,"devise_de_base") 

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
		CASE WHEN d.sens = 'Debit' THEN 'D' else 'C' END AS sens_2,
		o.journal,
		o.devise,
		o.devise_caisse,
		d.compte_analytique,
		s1.correspondance AS axe,
		d.compte_analytique_2,
		s2.correspondance AS axe_2,
		d.compte_analytique_3,
		s3.correspondance AS axe_3,
		d.compte_analytique_4,
		s4.correspondance AS axe_4,
		d.compte_analytique_5,
		s5.correspondance AS axe_5,
		%(currency)s as company_currency, 1 AS statut, NULL AS line_doc, NULL AS line_ana, NULL AS plan, NULL AS poste, NULL AS montant_ana
		FROM (
			SELECT *
			FROM tabEncaissement
			WHERE docstatus = 1
			UNION
			SELECT *
			FROM tabDecaissement
			WHERE docstatus = 1
			) o 
		INNER JOIN `tabComptabilisation` d on o.name = d.parent
		LEFT JOIN `tabSection Analytique` s1 ON s1.name = d.compte_analytique
		LEFT JOIN `tabSection Analytique` s2 ON s2.name = d.compte_analytique_2
		LEFT JOIN `tabSection Analytique` s3 ON s3.name = d.compte_analytique_3
		LEFT JOIN `tabSection Analytique` s4 ON s4.name = d.compte_analytique_4
		LEFT JOIN `tabSection Analytique` s5 ON s5.name = d.compte_analytique_5
		WHERE o.date >= %(date_debut)s AND o.date <= %(date_fin)s AND o.caisse LIKE %(caisse)s
		ORDER BY name, CASE WHEN d.sens = 'Debit' THEN 'D' else 'C' END DESC
        """,{"date_debut": filters.date_debut, "date_fin": filters.date_fin, "currency":company_currency,"caisse": filters.caisse if filters.caisse else '%' }, as_dict = 1
    )

	#data = sorted(data, key=itemgetter('name', 'sens_2'))
	data2 = []
	i = 0

	for d in data:
		i += 1
		d['line_doc'] = i
		d['line_ana'] = i
		data2.append(d)
		if d['compte_analytique']:
			new_d = dict(d)
			new_d['plan'] = new_d['axe']
			new_d['poste'] = new_d['compte_analytique']
			new_d['montant_ana'] = d['montant']
			new_d['line_doc'] = i
			new_d['line_ana'] = i
			data2.append(new_d)
		if d['compte_analytique_2']:
			new_d = dict(d)
			new_d['plan'] = new_d['axe_2']
			new_d['poste'] = new_d['compte_analytique_2']
			new_d['montant_ana'] = d['montant']
			new_d['line_doc'] = i
			new_d['line_ana'] = i
			data2.append(new_d)
		if d['compte_analytique_3']:
			new_d = dict(d)
			new_d['plan'] = new_d['axe_3']
			new_d['poste'] = new_d['compte_analytique_3']
			new_d['montant_ana'] = d['montant']
			new_d['line_doc'] = i
			new_d['line_ana'] = i
			data2.append(new_d)
		if d['compte_analytique_4']:
			new_d = dict(d)
			new_d['plan'] = new_d['axe_4']
			new_d['poste'] = new_d['compte_analytique_4']
			new_d['montant_ana'] = d['montant']
			new_d['line_doc'] = i
			new_d['line_ana'] = i
			data2.append(new_d)
		if d['compte_analytique_5']:
			new_d = dict(d)
			new_d['plan'] = new_d['axe_5']
			new_d['poste'] = new_d['compte_analytique_5']
			new_d['montant_ana'] = d['montant']
			new_d['line_doc'] = i
			new_d['line_ana'] = i
			data2.append(new_d)

	return data2

