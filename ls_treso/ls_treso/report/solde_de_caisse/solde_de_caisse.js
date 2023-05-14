// Copyright (c) 2023, Kossivi Amouzou and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Solde de Caisse"] = {
	"filters": [
		{
			fieldname: "name",
			label: __("Caisse"),
			fieldtype: "Link",
			options: "Caisse",
		},
	]
};
