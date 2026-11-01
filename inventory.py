from datetime import datetime
from typing import Dict
from models import LibraryItem, Book, Magazine, DigitalMedia

class InventoryManager:
    """Handles object lifecycles, checkouts, returns, and text audits."""
    
    def __init__(self):
        self._inventory: Dict[str, LibraryItem] = {}

    def add_item(self, item: LibraryItem):
        if item.item_id in self._inventory:
            raise KeyError(f"Item ID {item.item_id} already exists in inventory.")
        self._inventory[item.item_id] = item

    def checkout_item(self, item_id: str) -> bool:
        item = self._inventory.get(item_id)
        if not item:
            print(f"Error: Item {item_id} not found.")
            return False
        if item.is_borrowed:
            print(f"Error: '{item.title}' is already checked out.")
            return False
        
        item.is_borrowed = True
        item.borrow_date = datetime.now()
        print(f"Success: '{item.title}' has been checked out.")
        return True

    def return_item(self, item_id: str, days_kept: int = 0, standard_loan_period: int = 14) -> float:
        item = self._inventory.get(item_id)
        if not item or not item.is_borrowed:
            print(f"Error: Item {item_id} is not marked as borrowed.")
            return 0.0

        overdue_days = max(0, days_kept - standard_loan_period)
        fee = item.calculate_fee(overdue_days)
        
        # Reset tracking attributes
        item.is_borrowed = False
        item.borrow_date = None
        
        print(f"Success: '{item.title}' returned. Late fees incurred: ${fee:.2f}")
        return fee

    def generate_audit_report(self):
        """Generates a clean tabular console view of all assets."""
        print("\n" + "="*95)
        print(f"{'ID':<8} | {'Type':<12} | {'Title':<25} | {'Price':<8} | {'Status':<10} | {'Extra Metadata'}")
        print("="*95)
        
        for item in self._inventory.values():
            status = "Borrowed" if item.is_borrowed else "Available"
            type_name = item.__class__.__name__
            print(f"{item.item_id:<8} | {type_name:<12} | {item.title[:23]:<25} | ${item.price:<7.2f} | {status:<10} | {item.display_metadata()}")
        print("="*95 + "\n")


# --- Execution Example ---
if __name__ == "__main__":
    manager = InventoryManager()

    # Create instances showcasing inheritance and explicit type variations
    b1 = Book("B01", "The Clean Coder", "Robert Martin", 35.99, "978-0137081073", 242)
    m1 = Magazine("M01", "Wired Magazine", "Condé Nast", 5.99, 312)
    d1 = DigitalMedia("D01", "Python Design Patterns", "Alex Martelli", 19.99, "PDF", 14)

    # Populate registry
    manager.add_item(b1)
    manager.add_item(m1)
    manager.add_item(d1)

    print("--- Initial System Audit ---")
    manager.generate_audit_report()

    print("--- Simulation of Activity ---")
    manager.checkout_item("B01")
    manager.checkout_item("M01")
    
    print("\n--- State Audit Post-Checkout ---")
    manager.generate_audit_report()

    print("--- Process Returns & Evaluate Polymorphic Overdue Rules ---")
    # Simulating a return after 20 days (6 days overdue)
    manager.return_item("B01", days_kept=20) 
    # Simulating a return after 20 days (6 days overdue)
    manager.return_item("M01", days_kept=20) 
    
    print("\n--- Final Status Audit ---")
    manager.generate_audit_report()
