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
		{
			fieldname: "site",
			label: __("Site"),
			fieldtype: "Link",
			options: "Branch",
			reqd: 1,
		},

	]
};
