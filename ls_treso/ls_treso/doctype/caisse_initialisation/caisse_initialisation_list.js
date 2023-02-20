frappe.listview_settings['Caisse Initialisation'] = {

    onload: function (listview) {

        // Add a button for doing something useful.
        listview.page.add_inner_button(__("Ouverture"), function () {
                        frappe.call({
                                doc: frm.doc,
                                method: 'print_msg',
                                freeze: true,
                                callback: function() {
                                        frm.reload_doc();
                                }
                        });  // change to your function's name
        }).addClass("btn-warning").css({'background-color':'#2490EF','color':'white','font-weight': 'normal'});
        // The .addClass above is optional.  It just adds styles to the button.
    }
};