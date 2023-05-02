// Copyright (c) 2023, Kossivi Amouzou and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Export Sage X3"] = {
	"filters": [
		{
			fieldname:"societe",
			label: __("Société"),
			fieldtype: "Link",
			options: "Societe",
			reqd: 1
		},
		{
			fieldname:"caisse",
			label: __("Caisse"),
			fieldtype: "Link",
			options: "Caisse",
			reqd: 0
		},
		{
			fieldname:"date_debut",
			label: __("Date Début"),
			fieldtype: "Date",
			default: frappe.datetime.month_start(),
			reqd: 0
		},
		{
			fieldname:"date_fin",
			label: __("Date Fin"),
			fieldtype: "Date",
			default: frappe.datetime.month_end(),
			reqd: 1
		},
	]
};
