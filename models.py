from abc import ABC, abstractmethod
from datetime import datetime

class LibraryItem(ABC):
    """Abstract Base Class representing a generic item in the system."""
    
    def __init__(self, item_id: str, title: str, author_or_creator: str, price: float):
        self._item_id = item_id
        self._title = title
        self._author_or_creator = author_or_creator
        self.price = price  # Triggers the setter validation
        self._borrow_date = None
        self._is_borrowed = False

    # --- Getters and Setters (Encapsulation) ---
    @property
    def item_id(self) -> str:
        return self._item_id

    @property
    def title(self) -> str:
        return self._title

    @property
    def author_or_creator(self) -> str:
        return self._author_or_creator

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float):
        if value < 0:
            raise ValueError("Price cannot be negative.")
        self._price = value

    @property
    def borrow_date(self) -> datetime:
        return self._borrow_date

    @borrow_date.setter
    def borrow_date(self, value: datetime):
        self._borrow_date = value

    @property
    def is_borrowed(self) -> bool:
        return self._is_borrowed

    @is_borrowed.setter
    def is_borrowed(self, value: bool):
        self._is_borrowed = value

    # --- Abstract Methods ---
    @abstractmethod
    def calculate_fee(self, days_overdue: int) -> float:
        """Calculate late fees based on asset type rules."""
        pass

    @abstractmethod
    def display_metadata(self) -> str:
        """Return a formatted string containing specific type information."""
        pass

    # --- Dunder Methods ---
    def __str__(self) -> str:
        return f"[{self.__class__.__name__}] {self.title} by {self.author_or_creator}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(item_id='{self.item_id}', title='{self.title}', price={self.price})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, LibraryItem):
            return NotImplemented
        return self.item_id == other.item_id


class Book(LibraryItem):
    """Concrete implementation for books."""
    
    def __init__(self, item_id: str, title: str, author_or_creator: str, price: float, isbn: str, page_count: int):
        super().__init__(item_id, title, author_or_creator, price)
        self.isbn = isbn
        self.page_count = page_count

    def calculate_fee(self, days_overdue: int) -> float:
        if days_overdue <= 0:
            return 0.0
        return round(days_overdue * 0.50, 2)  # $0.50 per day

    def display_metadata(self) -> str:
        return f"ISBN: {self.isbn} | Pages: {self.page_count}"

    def __len__(self) -> int:
        return self.page_count


class Magazine(LibraryItem):
    """Concrete implementation for magazines."""
    
    def __init__(self, item_id: str, title: str, author_or_creator: str, price: float, issue_number: int):
        super().__init__(item_id, title, author_or_creator, price)
        self.issue_number = issue_number

    def calculate_fee(self, days_overdue: int) -> float:
        if days_overdue <= 0:
            return 0.0
        return round(days_overdue * 1.00, 2)  # $1.00 per day (higher demand/turnover)

    def display_metadata(self) -> str:
        return f"Issue Number: {self.issue_number}"


class DigitalMedia(LibraryItem):
    """Concrete implementation for digital files/media."""
    
    def __init__(self, item_id: str, title: str, author_or_creator: str, price: float, file_format: str, file_size_mb: int):
        super().__init__(item_id, title, author_or_creator, price)
        self.file_format = file_format
        self.file_size_mb = file_size_mb

    def calculate_fee(self, days_overdue: int) -> float:
        # Digital products typically don't accumulate physical overdue fees, 
        # but could have account block metrics or a flat processing cost.
        return 0.0 

    def display_metadata(self) -> str:
        return f"Format: {self.file_format} | Size: {self.file_size_mb}MB"
