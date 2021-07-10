import enum


class ProductPermission(str, enum.Enum):
    """Permissions for product endpoint."""

    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"


class CategoryPermission(str, enum.Enum):
    """Permissions for category endpoint."""

    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
