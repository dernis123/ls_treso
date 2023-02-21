# Copyright (c) 2022, Kossivi Amouzou and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class CaisseInitialisation(Document):

	def validate(self):
		nb = frappe.db.count('Caisse Initialisation', {"docstatus": 0, "caisse": self.caisse, "name": ["!=", self.name]})
		#test = frappe.db.get_list('Caisse Initialisation', filters = {"docstatus": 0, "caisse": self.caisse}, fields=["name"])
		if nb > 0 :
			#frappe.msgprint(str(test))
			frappe.throw("Veuillez cloturer la journée précédente")

		nb = frappe.db.count('Caisse Initialisation', 
				{
					"date_initialisation": [">", self.date_initialisation], 
					"caisse": self.caisse, 
				}
			)
		if nb > 0 :
			frappe.throw("Une date ultérieure à la date choisie existe déjà. Veuillez choisir une date plus récente")
	
	def before_submit(self):
		operations = frappe.db.get_list("Operation de Caisse", fields = ["name"], filters = {"docstatus": 0})
		for o in operations:
			operation = frappe.get_doc("Operation de Caisse", o.name)
			operation.submit()

		if len(self.billetage) == 0:
			frappe.throw("Veuillez saisir le billetage")

		total = 0
		for b in self.billetage:
			total += b.valeur_finale
		if self.solde_final != total:
			frappe.throw("Le solde physique de la caisse est différent du solde final. Veuillez recompter!") 

	def on_cancel(self):
		nb = frappe.db.count('Caisse Initialisation', 
				{
					"date_initialisation": [">", self.date_initialisation], 
					"caisse": self.caisse, 
				}
			)
		if nb > 0 :
			frappe.throw("Vous ne pouvez annuler cette journée de caisse alors que des dates plus récentes existes. prière d'annuler d'abord les entrées plus récentes!")

	@frappe.whitelist()
	def recalcul(self):
		if self.docstatus == 1:
			frappe.throw("Vous ne pouvez pas recalculer une journée déjà fermée!") 
		mt = frappe.db.sql(
		"""
			SELECT SUM(CASE WHEN code_type = 'ENC' THEN montant else - montant END) AS montant
			FROM `tabOperation de Caisse`
			WHERE initialisation = %(name)s AND docstatus = 1
		""" , {"name": self.name}, as_dict = 1
		)[0].montant
		if self.solde_final < mt :
			frappe.throw("Vous avez une inconsistance dans les montants saisis, veuillez appeler l'administrateur!") 
		
		frappe.db.sql(
		"""
			UPDATE `tabCaisse Initialisation` SET solde_final = solde_initial + 
				(SELECT SUM(CASE WHEN code_type = 'ENC' THEN montant else - montant END) AS montant
				FROM `tabOperation de Caisse`
				WHERE initialisation = %(name)s AND docstatus = 1)
			WHERE name = %(name)s AND docstatus = 0
		""" , {"name": self.name}, as_dict = 1
		)

	@frappe.whitelist()
	def cloture(self):
		operations = frappe.db.get_list('Operation de Caisse',
			filters={
				'docstatus': 0,
				'initialisation': self.name
			},
			fields=['name'],
			order_by='name',
		)

		for o in operations:
			op_doc = frappe.get_doc('Operation de Caisse', o.name)
			op_doc.submit()

@frappe.whitelist()
def get_caisse_devise(caisse):
	return frappe.db.get_value('Caisse', caisse, 'devise')

@frappe.whitelist()
def get_solde_final(caisse, date):
	init = frappe.db.sql(
		"""
			SELECT solde_final
				FROM(
				SELECT max(date_initialisation) AS date_initialisation, caisse
				FROM `tabCaisse Initialisation`
				WHERE caisse = %s AND date_initialisation < %s
				GROUP BY caisse
			) d INNER JOIN `tabCaisse Initialisation` i ON i.date_initialisation = d.date_initialisation AND i.caisse = d.caisse
		""", (caisse,date)
	)
	if len(init) > 0:
		return init[0][0]
	else:
		return 0


@frappe.whitelist()
def get_last_billetage(caisse, date):
	billetage = frappe.db.sql(
		"""
			SELECT b.nom, b.nombre_final, b.valeur_finale
				FROM(
				SELECT max(date_initialisation) AS date_initialisation, caisse
				FROM `tabCaisse Initialisation`
				WHERE caisse = %s AND date_initialisation < %s
				GROUP BY caisse
			) d INNER JOIN `tabCaisse Initialisation` i ON i.date_initialisation = d.date_initialisation  AND i.caisse = d.caisse
				INNER JOIN `tabBilletage` b ON b.parent = i.name
		""" , (caisse,date), as_dict = 1
	)
	return billetage
	#for b in billetage:
	#	for b2 in doc.billetage:
	#		if b.nom == b2.nom:
	#			b2.nombre_initial = b.nombre_final
	#			b2.valeur_initiale = b.valeur_finale

def transfert(caisse_de, caisse_a, montant, devise,caisse_doc,type_operation):
	nature_doc = frappe.db.sql(
		"""
		SELECT name
		FROM `tabNature Operations`
		WHERE echange = 1 AND type_operation = %s
		""", (type_operation),
		as_dict = 1
	)

	if len(caisse_doc) > 0:
		#if caisse_doc[0].solde_final >= montant :
		args = frappe._dict(
			{
				"doctype": "Operation de Caisse", 
				"caisse": caisse_de,
				"initialisation": caisse_doc[0].name,
				"designation": 'Envoi de fond' if type_operation == 'Decaissement' else 'Reception de fond',
				"type_operation": type_operation,
				"date": caisse_doc[0].date_initialisation,					
				"devise": devise,
				"montant": montant,
				"montant_reference": montant,
				"remettant": caisse_a,
				"details_operation_de_caisse": [{
					"nature_operations":  nature_doc[0].name,
					#"tiers": caisse_a,
					"montant_devise": montant,
					"montant_devise_ref": montant
				}]
			}
		)

		op_doc = frappe.get_doc(args)
		#op_doc.insert()
		op_doc.submit()

@frappe.whitelist()
def save_operation(caisse_de, caisse_a, date, montant, devise):
	caisse_doc = frappe.db.sql(
		"""
		SELECT name, solde_final, DATE(date_initialisation) AS date_initialisation
		FROM `tabCaisse Initialisation`
		WHERE DATE(date_initialisation) = DATE(%s) AND caisse = %s AND docstatus = 0
		""", (date,caisse_de),
		as_dict = 1
	)
	#frappe.msgprint("1")
	try:
		type_operation = 'Decaissement' 
		transfert(caisse_de, caisse_a, montant, devise,caisse_doc,type_operation)

		caisse_doc = frappe.db.sql(
			"""
			SELECT name, solde_final, DATE(date_initialisation) AS date_initialisation
			FROM `tabCaisse Initialisation`
			WHERE DATE(date_initialisation) = DATE(%s) AND caisse = %s AND docstatus = 0
			""", (date,caisse_a),
			as_dict = 1
		)

		type_operation = 'Encaissement'
		transfert(caisse_a, caisse_de, montant, devise,caisse_doc,type_operation)
	except Exception as e:
		frappe.msgprint(str(e))
		frappe.db.rollback()

	

	