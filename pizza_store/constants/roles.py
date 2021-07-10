from typing import Dict, Final, FrozenSet

from pizza_store.enums.permissions import CategoryPermission, ProductPermission
from pizza_store.enums.role import Role

ROLES: Final[Dict[Role, FrozenSet[str]]] = {
    Role.USER: frozenset({ProductPermission.READ, CategoryPermission.READ}),
    Role.ADMIN: frozenset(
        {
            ProductPermission.CREATE,
            ProductPermission.READ,
            ProductPermission.UPDATE,
            ProductPermission.DELETE,
            CategoryPermission.CREATE,
            CategoryPermission.READ,
            CategoryPermission.UPDATE,
            CategoryPermission.DELETE,
        }
    ),
}
