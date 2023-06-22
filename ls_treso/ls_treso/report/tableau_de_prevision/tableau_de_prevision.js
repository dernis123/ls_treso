// Copyright (c) 2023, Kossivi Amouzou and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Tableau de Prevision"] = {
	"filters": [
		{
			fieldname:"date",
			label: __("Date"),
			fieldtype: "Date",
			default: frappe.datetime.get_today(),
			reqd: 1
		},

	]
};
