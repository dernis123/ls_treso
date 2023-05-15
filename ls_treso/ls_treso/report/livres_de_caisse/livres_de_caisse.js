// Copyright (c) 2023, Kossivi Amouzou and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Livres de Caisse"] = {
	"filters": [
		{
			fieldname:"date_debut",
			label: __("Date Début"),
			fieldtype: "Date",
			default: frappe.datetime.month_start(),
			reqd: 1
		},
		{
			fieldname:"date_fin",
			label: __("Date Fin"),
			fieldtype: "Date",
			default: frappe.datetime.month_end(),
			reqd: 1
		},
		{
			fieldname: "caisse",
			label: __("Caisse"),
			fieldtype: "Link",
			options: "Caisse",
			reqd: 1
		},
		{
			fieldname: "valide",
			label: __("Validées"),
			fieldtype: "Check",
		},
	]
};
