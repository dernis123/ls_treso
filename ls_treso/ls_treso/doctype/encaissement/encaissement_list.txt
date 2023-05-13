frappe.listview_settings['Encaissement'] = {
    onload: function(listview) {
        listview.page.btn_primary.hide();
        listview.page.btn_secondary.hide();
    }
};