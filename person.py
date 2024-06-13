class Person:
    def __init__(self, ID: None, name: str, phone: str, email: str, created_at: str, modified_at: str) -> None:
        self.name = name
        self.phone = phone
        self.email = email
        self.created_at = created_at
        self.modified_at = modified_at
        self.ID = ID
        
    