# -*- coding: utf-8 -*-
#
# These are the master permissions set
# 1. Any change to this must be cascaded in the following permission dicts
#

# 1. Print Partner: Account Admin (PP_ADMIN)
# # - Register the Company
#  edit_company, Edit Company Profile
#  create_printer, Create Printing Equipment
#  add_user, Create Print Operators (Users)
#  invite_partners, Invite Partners (Clients)
#  edit_workorder, View & Edit Work Orders
#  view_billing_reports, View Billing Reports

# 2. Print Partner: Printer Operator (PO)
#  #- Use the QA App
#  #- Scan & Submit Codes
#  view_workorder, View Work Orders
#  edit_workorder_results, Edit Work Order (Results Only)

# 3. Brand Owner: Acount Admin (BO_ADMIN)
#  #Register the Company
#  edit_company, Edit Company Profile
#  create_brand, edit_brand, Create Brands
#  create_product, edit_product, Create Products
#  add_user, Create Brand Managers (Users)
#  invite_partners, Invite Partners (Printing Partners)
#  create_workorder, Create Work Orders
#  view_workorder_results, View Work Order Results
#  view_billing_reports, View Billing Reports
#  view_dashboard, View Dashboard

# 4. Brand Owner: Brand Manager (BM)
#  create_product, edit_products, Create Products
#  create_workorder, Create Work Orders
#  view_workorder_results, View Work Order Results
#  view_dashboard, View Dashboard


# 6. beer: Support Engineer (SSE)
#  approve_company, Approve Companies
#  invite_company, Invite Companies
#  edit_user, Edit Users
#  edit_workorder, Edit Work Orders
#  view_dashboard, View Dashboard

GRANULAR_PERMISSIONS = (
    ('brand_create', u'Can create brands'),
    ('brand_view', u'Can view brands'),
    ('brand_edit', u'Can edit  brands'),
    ('brand_delete', u'Can delete brands'),

    ('product_create', u'Can create products'),
    ('product_view', u'Can view product'),
    ('product_edit', u'Can edit  product'),
    ('product_delete', u'Can delete product'),

    ('workorder_create', u'Can create product batch workorders'),
    ('workorder_view', u'Can view product batch workorders'),
    ('workorder_edit', u'Can edit product batch workorders'),
    ('workorder_delete', u'Can delete product batch workorders'),

    ('proofsheet_create', u'Can create proof-sheets'),
    ('proofsheet_view', u'Can view proof-sheets'),
    ('proofsheet_edit', u'Can edit proof-sheets'),
    ('proofsheet_delete', u'Can delete proof-sheets'),

    ('batch_create', u'Can create batches'),
    ('batch_view', u'Can view product batches'),
    ('batch_edit', u'Can manage can edit product batches'),
    ('batch_delete', u'Can delete product batches'),

    #
    # Scans - cannot create scans but can enable editing and deleting
    #
    # ('scan_edit', u'Can edit Scan details'),
    # ('scan_delete', u'Can delete Scans'),

    #
    # Printers
    #
    ('printer_view', u'Can view Printers'),
    ('printer_create', u'Can create Printers'),
    ('printer_edit', u'Can edit Printers'),
    ('printer_delete', u'Can delete Printers'),

    #
    # Helper setting, when True will allow CRUD on all user-types
    #
    ('manage_participants', u'Can manage participants'),  # if True can do all to participants
    ('view_participants', u'Can view participants'),  # if True can view the participants
    #
    # User classes - relate to the roles.ROLES file
    #
    ('customer_user_create', u'Can create Customers'),
    ('customer_user_edit', u'Can edit Customer details'),
    ('customer_user_delete', u'Can delete Customers'),

    ('qa_user_create', u'Can create Q.A Users'),
    ('qa_user_edit', u'Can edit Q.A Users'),
    ('qa_user_delete', u'Can delete Q.A Users'),

    ('portal_user_create', u'Can create Portal Users'),
    ('portal_user_edit', u'Can edit Portal Users'),
    ('portal_user_delete', u'Can delete Portal Users'),

    ('inspector_user_create', u'Can create Inspector Users'),
    ('inspector_user_edit', u'Can edit Inspector Users'),
    ('inspector_user_delete', u'Can delete Inspector Users'),

    #
    # Misc permissions, dont confuse these with things like
    # recieve_email_notifications which is a user settings not a permission
    #
    ('dashboard_view', u'Can view Dashboard Overview'),
    ('billing_reports_view', u'Can view Billing Reports'),
    ('billing_reports_edit', u'Can edit Billing Reports'),
)
#
# Owners of a brand
#
OWNER_PERMISSIONS = dict.fromkeys([key for key, value in GRANULAR_PERMISSIONS], True)  # Grant the owner all permissions by default
#
# Privileged users permission template
#
PRIVILEGED_USER_PERMISSIONS = {
    'manage_participants': True,
    'printer_create': True,
    'printer_edit': True,
    'printer_delete': True,
    'batch_create': True,
    'batch_view': True,
    'batch_edit': True,
    'batch_delete': True,
    'workorder_create': True,
    'workorder_view': True,
    'workorder_edit': True,
    'workorder_delete': True,
    'scan_edit': False,
    'scan_delete': True,
    'printer_create': True,
    'printer_edit': True,
    'printer_delete': True,
}
#
# Standard users permission template
#
UNPRIVILEGED_USER_PERMISSIONS = {
    'manage_participants': False,
    'view_participants': True,
    'printer_view': True,
    'batch_view': True,
    'workorder_view': True,
    'scan_edit': False,
    'scan_delete': False,
    'printer_view': True,
}
#
# Not logged in or random user permissions
#
ANONYMOUS_USER_PERMISSIONS = dict.fromkeys([key for key, value in GRANULAR_PERMISSIONS], False)
