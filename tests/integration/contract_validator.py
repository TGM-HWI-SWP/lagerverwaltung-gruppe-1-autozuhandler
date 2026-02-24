"""
Contract Validator
Rolle 1 – Projektverantwortung & Schnittstellen

Diese Datei prüft, ob eine Repository-Implementierung
alle erforderlichen Methoden des RepositoryPort besitzt.
"""

REQUIRED_REPOSITORY_METHODS = [
    "save_product",
    "load_product",
    "load_all_products",
    "delete_product",
    "save_movement",
    "load_movements",
]


class ContractViolationError(Exception):
    """Wird geworfen, wenn ein Contract verletzt wird."""
    pass


def validate_repository_contract(repository_instance):
    """
    Prüft, ob die übergebene Repository-Instanz
    alle erforderlichen Methoden implementiert.
    """

    missing_methods = []

    for method in REQUIRED_REPOSITORY_METHODS:
        if not hasattr(repository_instance, method):
            missing_methods.append(method)

    if missing_methods:
        raise ContractViolationError(
            f"Repository verletzt Contract. Fehlende Methoden: {missing_methods}"
        )

    return True


if __name__ == "__main__":
    print("Contract Validator bereit.")