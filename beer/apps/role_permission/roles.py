# -*- coding: utf-8 -*-
from beer.utils.app import get_namedtuple_choices


COMPANY_ROLES = get_namedtuple_choices('COMPANY_ROLES', (
    (1, 'brand_owner', 'Brand Owner'),
    (2, 'printing_partner', 'Printing Partner'),
))

ROLES = get_namedtuple_choices('ROLES', (
    (0, 'noone', 'No Access'),
    (1, 'brand_account_admin', 'Account Admin (brand)'),  # used by both COMPANY_ROLES.brand_account_admin and COMPANY_ROLES.printing_partner
    (2, 'printer_account_admin', 'Account Admin (print)'),  # used by both COMPANY_ROLES.brand_account_admin and COMPANY_ROLES.printing_partner
    (3, 'brand_manager', 'Brand Manager'),  # used by COMPANY_ROLES.brand_account_admin
    (4, 'printer_operator', 'Print Operator'),  # used by both COMPANY_ROLES.printing_partner
))
