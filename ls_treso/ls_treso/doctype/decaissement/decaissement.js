// Copyright (c) 2023, Kossivi Amouzou and contributors
// For license information, please see license.txt

frappe.ui.form.on('Decaissement', {
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

		frm.set_value('type_operation', 'Decaissement');
	},
	refresh(frm) {
		/*if(frm.doc.docstatus === 1){
			frm.page.btn_primary.hide();
			frm.page.btn_secondary.hide();
			frm.page.clear_primary_action();
			
		}
		frappe.db.get_doc("Caisse Initialisation", cur_frm.doc.initialisation).then(d => {
			if(d.docstatus === 1){
				frm.page.btn_primary.hide();
				frm.page.btn_secondary.hide();
				frm.page.clear_primary_action();

				var span;
				var a;
				var li;
				span = document.querySelector('[data-label="New%20Decaissement"]');
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
			if(d.docstatus === 0){
				if(frm.is_new()){
					if(frm.doc.initialisation == ""){
						frm.set_value('initialisation', d.name);
					}
				}
			}
		});*/
		if (!frm.customFlag){
			var grid = frm.get_field('details_operation_de_caisse');
			// Add a new empty row to the grid
			grid.grid.add_new_row();
			frm.customFlag = true;
		}
		

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
	/*after_insert: function(frm){
		if(! frm.is_new()) return;
		frappe.set_route("Form", "Operation de Caisse", frm.doc.name);
	},
	/*after_save: function(frm){
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
					if(!e.imputation_analytique) frappe.throw("Ligne " + e.idx +  ": Veuillez renseigner la nature analytique");
				}
			});
			
			frappe.db.get_value("Nature Operations", e.nature_operations, "tiers", (r) => {
				if(r.tiers == 'Oui'){
					if(!e.tiers) frappe.throw("Ligne " + e.idx +  ": Veuillez renseigner le tiers");
				}
			});
		});
	},
	before_save: function(frm){
		frm.doc.details_operation_de_caisse.forEach(e => {
			frappe.db.get_value("Nature Operations", e.nature_operations, "justifiable", (r) => {
				if(r.justifiable == 'Oui'){
					if(!e.imputation_analytique) frappe.throw("Ligne " + e.idx +  ": Veuillez renseigner la nature analytique");
				}
			});
			
			frappe.db.get_value("Nature Operations", e.nature_operations, "tiers", (r) => {
				if(r.tiers == 'Oui'){
					if(!e.tiers) frappe.throw("Ligne " + e.idx +  ": Veuillez renseigner le tiers");
				}
			});
		});
	},*/
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

frappe.ui.form.on("Decaissement","refresh", function(frm, cdt, cdn) { 
	var df_axe_1 = frappe.meta.get_docfield("Details Operation de Caisse","imputation_analytique", cur_frm.doc.name);
	frappe.db.get_value("Axe Analytique", {"type": "Axe 1"}, "name").then(r=>{
		df_axe_1.label = r.message.name;
		div = document.querySelector('[data-fieldname="imputation_analytique"]');
		div.children[1].innerText = r.message.name;
	});
	/*df = frappe.meta.get_docfield("Details Operation de Caisse","imputation_analytique_2", cur_frm.doc.name);
    df.read_only = 1;
	df = frappe.meta.get_docfield("Details Operation de Caisse","imputation_analytique_3", cur_frm.doc.name);
    df.read_only = 1;
    var df = frappe.meta.get_docfield("Details Operation de Caisse","imputation_analytique_4", cur_frm.doc.name);
    df.read_only = 1;
	df = frappe.meta.get_docfield("Details Operation de Caisse","imputation_analytique_5", cur_frm.doc.name);
    df.read_only = 1;
	//df.hidden = 1;
	df = frappe.meta.get_docfield("Details Operation de Caisse","reste", cur_frm.doc.name);
    df.read_only = 1;
	//df.hidden = 1; */

});
