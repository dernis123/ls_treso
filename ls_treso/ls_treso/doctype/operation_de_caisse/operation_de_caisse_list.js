frappe.listview_settings['Operation de Caisse'] = {

    /*onload: function (listview) {

        // Add a button for doing something useful.
        listview.page.add_inner_button(__("Décaissement"), function () {
                        frappe.new_doc("Decaissement", true);  // change to your function's name
        }).addClass("btn-warning")
          .css({'background-color':'#2490EF','color':'white','font-weight': 'normal'});
        
        // Add a button for doing something useful.
        listview.page.add_inner_button(__("Encaissement"), function () {
            frappe.new_doc("Encaissement", true);  // change to your function's name
        }).addClass("btn-warning")
          .css({'background-color':'#2490EF','color':'white','font-weight': 'normal'});
    },*/
    refresh: function (listview){
        listview.page.btn_primary.hide();
    }
};