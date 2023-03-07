import frappe

@frappe.whitelist()
def get_price():
    total = frappe.db.sql(
        """
        SELECT 20256.56 AS price
        """, as_dict =1
    )[0].price
    return total