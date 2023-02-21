# Copyright (c) 2022, Kossivi Amouzou and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate

class OperationdeCaisse(Document):

	def validate(self):
		self.date = frappe.utils.getdate(self.date)
		
	def before_save(self):
		if len(self.details_operation_de_caisse) == 0:
			frappe.throw("Veuillez saisir au moins une ligne détail")

		exist = frappe.db.exists({
			"doctype": "Caisse Initialisation", 
			"name": self.initialisation,
			"docstatus": 1
		})
		if exist:
			frappe.throw("Vous ne pouvez enregistrer d'opérations sur le Numéro: " + self.initialisation + ". Veuillez choisir un numéro valide!")
		
		date_init = getdate(frappe.db.get_value('Caisse Initialisation', self.initialisation, 'date_initialisation'))
		date_split = str(date_init).split(":")[0]
		if date_split != str(self.date):
			frappe.throw("La date de saisie " + str(self.date) + " doit être conforme à la date d'initialisation " + date_split)
	
	def before_submit(self):
		total = 0.00
		for details in self.details_operation_de_caisse :
			total += float(details.montant_devise_ref)

		if float(total) != float(self.montant_reference):
			frappe.throw("Le montant saisie en entête de l'opération " + self.montant_reference + " est différent du total des montants en détails " + str(total) )

		init_doc = frappe.get_doc("Caisse Initialisation", self.initialisation)
		if self.type_operation != "Encaissement" :
			if float(init_doc.solde_final) < float(self.montant) :
					frappe.throw("Le montant actuellement en caisse ne permet pas de faire cette opération.\n Il faut augmenter le solde!!!")

	def on_submit(self):
		init_doc = frappe.get_doc("Caisse Initialisation", self.initialisation)
		if self.type_operation == "Encaissement" :
			init_doc.solde_final += float(self.montant_reference)
		else:
			init_doc.solde_final -= float(self.montant_reference)
		init_doc.save()

	def on_cancel(self):
		init_doc = frappe.get_doc("Caisse Initialisation", self.initialisation)
		if self.type_operation == "Encaissement" :
			init_doc.solde_final -= float(self.montant_reference)
		else:
			init_doc.solde_final += float(self.montant_reference)
		init_doc.save()

		

