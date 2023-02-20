# Copyright (c) 2022, Kossivi Amouzou and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Caisse(Document):

	def before_save(self):
		self.solde = self.solde_initial

	def before_submit(self):
		self.solde = self.solde_initial
		self.date_solde = self.date_lancement
	
	def on_submit(self):
		if self.solde_initial == 0:
			return
			
		billetage = []
		for billet in self.billetage:
			sub_args = frappe._dict({
				"doctype": "Billetage",
				"nom": billet.nom,
				"unite": billet.unite,
				#"image": billet.image,
				"nombre_initial": billet.nombre_initial,
				"valeur_initiale": billet.valeur_initiale,
				"nombre_final": billet.nombre_final,
				"valeur_finale": billet.valeur_finale,
				"parrenttype": "Caisse Initialisation",
				"parentfield": "billetage",
			})
			billetage.append(sub_args)
		
		args = frappe._dict(
			{
				"doctype": "Caisse Initialisation",
				"caisse": self.name,
				"date_initialisation": self.date_lancement,
				"date_fermeture": self.date_lancement,
				"devise": self.devise,
				"cours": self.cours,
				"solde_initial": 0,
				"solde_final": 0,
				"billetage": billetage,
			}
		)

		caisse_init = frappe.get_doc(args)
		caisse_init.insert()
		
		# Remplissage de l'opération de compte de solde initial
		init = frappe.db.sql(
			"""
			SELECT name
			FROM `tabNature Operations`
			WHERE solde_initial = 1
			"""
		)[0][0]

		operation_sub = []
		sub_args = frappe._dict({
			"doctype": "Details Operation de Caisse",
			"nature_operations": init,
			"montant_devise": self.solde,
			"montant_devise_ref":self.solde,
			"devise": self.devise,
			"cours": self.cours,
			"montant_devise_ref": self.solde,
			"parrenttype": "Operation de Caisse",
			"parentfield": "details_operation_de_caisse",
		})
		operation_sub.append(sub_args)

		args = frappe._dict(
			{
				"doctype": "Operation de Caisse",
				"caisse": self.name,
				"initialisation": caisse_init.name,
				"designation": "Solde Initial",
				"date": self.date_lancement,
				"devise": self.devise,
				"cours": self.cours,
				"remettant": frappe.session.user,
				"montant": self.solde,
				"montant_reference": self.solde,
				"details_operation_de_caisse": operation_sub,
			}
		)

		ci_name = caisse_init.name

		operation = frappe.get_doc(args)
		operation.submit()
		caisse_init = frappe.get_doc("Caisse Initialisation",ci_name)
		caisse_init.submit()

		

