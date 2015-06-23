from .roles import ROLES
from .permissions import (OWNER_PERMISSIONS,
                          PRIVILEGED_USER_PERMISSIONS,
                          UNPRIVILEGED_USER_PERMISSIONS,
                          ANONYMOUS_USER_PERMISSIONS,)


class PermissionProviderMixin(object):
    ROLES = ROLES
    PERMISSIONS = OWNER_PERMISSIONS.keys()  # get a list of keys
    OWNER_PERMISSIONS = OWNER_PERMISSIONS  # as the OWNER_PERMISSIONS always has ALL of them
    PRIVILEGED_USER_PERMISSIONS = PRIVILEGED_USER_PERMISSIONS
    UNPRIVILEGED_USER_PERMISSIONS = UNPRIVILEGED_USER_PERMISSIONS
    ANONYMOUS_USER_PERMISSIONS = ANONYMOUS_USER_PERMISSIONS

    OWNER_PERMISSIONS_USERCLASS = ['brand_account_admin', 'printer_account_admin']
    PRIVILEGED_PERMISSIONS_USERCLASS = ['brand_manager']
    UNPRIVILEGED_PERMISSIONS_USERCLASS = ['printer_operator']

    @staticmethod
    def permissions_by_role(role):
        """
        """
        if role in PermissionProviderMixin.OWNER_PERMISSIONS_USERCLASS:
            return PermissionProviderMixin.OWNER_PERMISSIONS

        if role in PermissionProviderMixin.PRIVILEGED_PERMISSIONS_USERCLASS:
            # Lawyers currently can do everything the owner can except clients and participants
            return PermissionProviderMixin.PRIVILEGED_USER_PERMISSIONS

        elif role in PermissionProviderMixin.UNPRIVILEGED_PERMISSIONS_USERCLASS:
            # Clients by default can currently see all items (allow by default)
            return PermissionProviderMixin.UNPRIVILEGED_USER_PERMISSIONS

        # Anon permissions, for anyone else that does not match
        return PermissionProviderMixin.ANONYMOUS_USER_PERMISSIONS
