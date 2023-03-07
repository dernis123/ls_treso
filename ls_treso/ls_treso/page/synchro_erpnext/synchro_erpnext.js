frappe.pages['synchro-erpnext'].on_page_load = function(wrapper) {

	new SyncroPage(wrapper);
	/*$("<h3'>TEST</h3>").appendTo(
		page.main
	);

	page.generale_field = page.add_field({
		fieldname: 'generale',
		label: __('Comptabilité Générale'),
		fieldtype:'Check',
		default: 1,
		change: function() {
			page.item_dashboard.start = 0;
			page.item_dashboard.refresh();
		}
	});
	page.analytique_field = page.add_field({
		fieldname: 'analytique',
		label: __('Comptabilité Analytique'),
		fieldtype:'Check',
		default: 1,
		change: function() {
			page.item_dashboard.start = 0;
			page.item_dashboard.refresh();
		}
	});
	page.tiers_field = page.add_field({
		fieldname: 'tiers',
		label: __('Tiers'),
		fieldtype:'Check',
		default: 1,
		change: function() {
			page.item_dashboard.start = 0;
			page.item_dashboard.refresh();
		}
	});
	page.btn_field = page.add_field({
		fieldname: 'btn_synchroniser',
		label: __('Synchroniser'),
		fieldtype:'Button',
		change: function() {
			page.item_dashboard.start = 0;
			page.item_dashboard.refresh();
		}
	});*/
}

SyncroPage = Class.extend({
	init: function(wrapper){
		this.page = frappe.ui.make_app_page({
			parent: wrapper,
			title: 'Synchroniser avec ErpNext',
			single_column: true
		});
		//make page
		this.make();
	},
	
	//Make Page
	make: function(){
		//Grab the class
		let me = $(this);

		//body content
		let total = function(){
			frappe.call('ls_treso.ls_treso.page.synchro_erpnext.synchro_erpnext.get_price')
			.then(r => {
				console.log(r)
				$("#total")[0].innerText = r.message;
			})
		}

		//push dom element to page
		$(frappe.render_template(frappe.ls_treso_page.body, this)).appendTo(this.page.main);

		//execute method 
		total()
	}

	//end of class
})

// HTML Content
let body = `<h1>Hello, World</h1> <br> <div > Total = <span id="total"> Total = <span><div>`;
frappe.ls_treso_page = {
	body : body
}

