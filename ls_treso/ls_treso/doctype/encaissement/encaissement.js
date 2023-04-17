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

		frm.set_value('type_operation', 'Encaissement');
	},
	refresh(frm) {
		// Clear the existing breadcrumbs. Set custom breadcrumbs will not do this automatically
		frappe.breadcrumbs.clear();
		
		// Now add breadcrumb for the 'parent' document
		frappe.breadcrumbs.set_custom_breadcrumbs({
			label: 'Opérations de Caisse', //the name of the field in Doc 2 that points to Doc 1
			route: '/app/operation-de-caisse/',
		});

		// Finally add the breadcrumb for this document  
		frappe.breadcrumbs.set_custom_breadcrumbs({
			label: frm.doc.name,
			route: '/app/operation-de-caisse/' + frm.doc.name,
		});

		if(frappe.has_route_options()){
			frm.set_value('caisse', frappe.route_options.caisse);
			frm.set_value('date', frappe.route_options.date_initialisation);
			frm.set_value('devise_caisse', frappe.route_options.devise);
			frm.set_value('devise', frappe.route_options.devise);
			frm.set_value('initialisation', frappe.route_options.initialisation);
		}

	},
	devise: function(frm) {
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

	after_insert: function(frm){
		if(! frm.is_new()) return;
		frappe.call({
			method: "ls_treso.ls_treso.doctype.operation_de_caisse.operation_de_caisse.insert_operation",
			args: {
				doc: frm.doc,
				type: 1,
			},
			callback: function (r) {
				frappe.set_route("Form", "Operation de Caisse", frm.doc.name);
			}
		});
	},
	after_save: function(frm){
		if(frm.is_new()) return;
		frappe.call({
			method: "ls_treso.ls_treso.doctype.operation_de_caisse.operation_de_caisse.insert_operation",
			args: {
				doc: frm.doc,
				type: 2,
			},
			callback: function (r) {
				frappe.set_route("Form", "Operation de Caisse", frm.doc.name);
			}
		});
	},

	before_insert: function(frm){
		frm.doc.details_operation_de_caisse.forEach(e => {
			frappe.db.get_value("Nature Operations", e.nature_operations, "justifiable", (r) => {
				if(r.justifiable == 'Oui'){
					if(!e.imputation_analytique) frappe.throw(_("Ligne {0}: Veuillez renseigner la nature analytique").format(e.idx))
				}
			});
			
			frappe.db.get_value("Nature Operations", e.nature_operations, "tiers", (r) => {
				if(r.tiers == 'Oui'){
					if(!e.tiers) frappe.throw(_("Ligne {0}: Veuillez renseigner le tiers").format(e.idx))
				}
			});
		});
	},
	before_save: function(frm){
		frm.doc.details_operation_de_caisse.forEach(e => {
			frappe.db.get_value("Nature Operations", e.nature_operations, "justifiable", (r) => {
				if(r.justifiable == 'Oui'){
					if(!e.imputation_analytique) frappe.throw(_("Ligne {0}: Veuillez renseigner la nature analytique").format(e.idx))
				}
			});
			
			frappe.db.get_value("Nature Operations", e.nature_operations, "tiers", (r) => {
				if(r.tiers == 'Oui'){
					if(!e.tiers) frappe.throw(_("Ligne {0}: Veuillez renseigner le tiers").format(e.idx))
				}
			});
		});
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
