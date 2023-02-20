// Copyright (c) 2022, Kossivi Amouzou and contributors
// For license information, please see license.txt

frappe.ui.form.on('Caisse', {
	setup: function(frm) {
        //frm.toggle_enable(['status', 'priority'], is_allowed);
		//frm.get_field("billetage").grid.only_sortable();
	},
	devise: function(frm) {
        /*frappe.call({
			method: "ls_treso.ls_treso.doctype.devise.devise.get_cours",
			args: {
				reference: frm.doc.devise_caisse,
				devise: frm.doc.devise,
			},
			callback: function (r) {
				if (r.message) {
                    if(r.message.length > 0) {
						frm.set_value('cours', r.message[0].cours);
						//if(frm.doc.montant) frm.set_value('montant_reference', frm.doc.montant / r.message[0].cours);
						//frm.refresh_field('cours'); 
					}
					else{
						frm.set_value('cours', 0);
						//frm.set_value('montant_reference', 0);
					}
                }
			}
		});*/
		frappe.call({
			method: "ls_treso.ls_treso.doctype.devise.devise.get_billetage",
			args: {
				devise: frm.doc.devise,
			},
			callback: function (r) {
				if (r.message) {
                    frm.clear_table("billetage");
					console.log(r.message);
                    r.message.forEach(e => {
                        var row = frm.add_child('billetage');
						row.image = e.image,
                        row.nom = e.nom,
						row.unite = e.unite;
                        row.nombre_initial = 0;
                        row.valeur_initiale = 0;
                        row.nombre_final = 0;
                        row.valeur_finale = 0;
                    });

                    frm.refresh_field('billetage');
                    frm.dirty();
                    //frm.refresh();
                }
			}
		});
	},
	refresh: function(frm) {
        if (cur_frm.doc.__unsaved != 1) {
            if(frm.doc.total != frm.doc.solde_initial) $('.primary-action').prop('disabled', true);
            else $('.primary-action').prop('disabled', false);
        }
        else $('.primary-action').prop('disabled', false);
	}
});

frappe.ui.form.on('Billetage', {
	
    nombre_final(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
        const old_value =  row.valeur_finale;
        if(row.nombre_final){
			row.valeur_finale = row.nombre_final * row.nom / (row.unite == "Centime" ? 100 : 1);
		}
		else{
			row.valeur_finale = 0;
		}
        frm.doc.total = frm.doc.total - old_value + row.valeur_finale;
        frm.refresh_field('billetage');
        frm.refresh_field('total');
        frm.refresh();
    }
});

frappe.ui.form.on("Caisse","onload", function(frm, cdt, cdn) {
    var df = frappe.meta.get_docfield("Billetage","nom", cur_frm.doc.name);
    df.read_only = 1;
    df = frappe.meta.get_docfield("Billetage","image", cur_frm.doc.name);
    df.read_only = 1;
    df = frappe.meta.get_docfield("Billetage","nombre_initial", cur_frm.doc.name);
    df.read_only = 1;
    df = frappe.meta.get_docfield("Billetage","valeur_initiale", cur_frm.doc.name);
    df.read_only = 1;
    df = frappe.meta.get_docfield("Billetage","unite", cur_frm.doc.name);
    df.read_only = 1;
});
