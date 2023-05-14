// Copyright (c) 2023, Kossivi Amouzou and contributors
// For license information, please see license.txt

frappe.ui.form.on('Encaissement', {
	setup: function(frm) {
		frm.set_query("initialisation", function() {
			return {
				"filters": {
					"docstatus": 0
				}
			};
		});

		frm.set_query("nature_operations","details_operation_de_caisse", function() {
			return {
				"filters": {
					"type_operation": frm.doc.type_operation || 'N/A',
				}
			};
		});

		frm.set_query("imputation_analytique","details_operation_de_caisse", function() {
			return {
				"filters": {
					"type": 'Axe 1',
				}
			};
		});
		frm.set_query("imputation_analytique_2","details_operation_de_caisse", function() {
			return {
				"filters": {
					"type": 'Axe 2',
				}
			};
		});
		frm.set_query("imputation_analytique_3","details_operation_de_caisse", function() {
			return {
				"filters": {
					"type": 'Axe 3',
				}
			};
		});
		frm.set_query("imputation_analytique_4","details_operation_de_caisse", function() {
			return {
				"filters": {
					"type": 'Axe 4',
				}
			};
		});
		frm.set_query("imputation_analytique_5","details_operation_de_caisse", function() {
			return {
				"filters": {
					"type": 'Axe 5',
				}
			};
		});

		frm.set_value('type_operation', 'Encaissement');
	},
	refresh: function(frm){
		/*
		if(frappe.has_route_options()){
			if(frappe.route_options.state === 1){
				frm.page.btn_primary.hide();
				frm.page.btn_secondary.hide();
				frm.page.clear_primary_action();

				var span;
				var a;
				var li;
				span = document.querySelector('[data-label="New%20Encaissement"]');
				if(span){
					a = span.parentElement;
					li = a.parentElement;
					li.style.display = "None";
				}
				span = document.querySelector('[data-label="Duplicate"]');
				if(span){
					a = span.parentElement;
					li = a.parentElement;
					li.style.display = "None";
				}
				span = document.querySelector('[data-label="Rename"]');
				if(span){
					a = span.parentElement;
					li = a.parentElement;
					li.style.display = "None";
				}
			}
		}*/
	},
	devise: function(frm) {
		if(!frm.doc.devise_caisse) return;
		frappe.call({
			method: "ls_treso.ls_treso.doctype.devise.devise.get_cours",
			args: {
				reference: frm.doc.devise_caisse,
				devise: frm.doc.devise,
			},
			callback: function (r) {
				if (r.message) {
                    if(r.message.length > 0) {
						frm.set_value('cours', r.message[0].cours);
						if(frm.doc.montant) frm.set_value('montant_reference', frm.doc.montant / r.message[0].cours);
					}
					else{
						frm.set_value('cours', 0);
						frm.set_value('montant_reference', 0);
					}
                }
			}
		});
	},
	montant: function(frm) {
		if(frm.doc.cours) frm.set_value('montant_reference', frm.doc.montant / frm.doc.cours);
	},
});

frappe.ui.form.on('Details Operation de Caisse', {
	
    montant_devise(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
        if(row.montant_devise && frm.doc.cours){
			row.montant_devise_ref = row.montant_devise / frm.doc.cours;
		}
		else{
			row.montant_devise_ref = 0;
		}
        frm.refresh_field('montant_devise_ref');
        frm.refresh();
    },
	details_operation_de_caisse_add:(frm, cdt, cdn) =>{
		var total = 0;
		var row = locals[cdt][cdn];

		frm.doc.details_operation_de_caisse.forEach(e => {
			total += e.montant_devise ? e.montant_devise : 0;
		});
		
		if (frm.doc.montant){
			if (frm.doc.montant > total){
				row.montant_devise = frm.doc.montant - total;
				row.montant_devise_ref = frm.doc.montant - total;
			}
			else {
				row.montant_devise = 0;
				row.montant_devise_ref = 0;
			}
			frm.refresh_field('montant_devise');
			frm.refresh_field('montant_devise_ref');
			frm.refresh_field('details_operation_de_caisse');
		}
	},
});
