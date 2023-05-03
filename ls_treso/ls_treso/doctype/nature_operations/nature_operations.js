// Copyright (c) 2022, Kossivi Amouzou and contributors
// For license information, please see license.txt

frappe.ui.form.on('Nature Operations', {
	refresh: function(frm) {
		frm.set_query("compte_comptable", function() {
			return {
				"filters": {
					"societe": frm.doc.societe ? frm.doc.societe : ''
				}
			};
		});
		frm.set_query("famille", function() {
			return {
				"filters": {
					"societe": frm.doc.societe ? frm.doc.societe : ''
				}
			};
		});
	}
});
