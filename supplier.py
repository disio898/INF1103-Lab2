from typing import Any


class Supplier:
    """Who supplies a product. Associated with Product, owned by neither side."""

    def __init__(self, supplier_id: str, name: str, contact_email: str) -> None:
        self.supplier_id: str = str(supplier_id)
        self.name: str = name
        self.contact_email: str = contact_email

    def display_information(self) -> None:
        print(
            f"Supplier: {self.name}, "
            f"Supplier ID: {self.supplier_id}, "
            f"Email: {self.contact_email}"
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "supplier_id": self.supplier_id,
            "name": self.name,
            "contact_email": self.contact_email,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Supplier":
        return cls(data["supplier_id"], data["name"], data["contact_email"])