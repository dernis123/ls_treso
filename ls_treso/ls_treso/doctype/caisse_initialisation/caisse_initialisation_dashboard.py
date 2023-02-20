from frappe import _


def get_data():
	return {
		"heatmap": False,
		"heatmap_message": _("This is based on the Time Sheets created against this project"),
		"fieldname": "initialisation",
		"transactions": [
			{
				"label": _("Opérations"),
				"items": ["Operation de Caisse"],
			},
		],
	}
