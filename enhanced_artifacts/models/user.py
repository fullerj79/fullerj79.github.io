"""
models/user.py

Author: Jason Fuller
Date: 2026-01-25

Responsibilities (Model layer):
- Connects to the MongoDB "users" collection via an injected collection handle.
- Performs database operations ONLY (CRUD-style reads/writes).
- Returns raw user documents (dict-like objects) to the controller layer.

Non-responsibilities (kept OUT of this file on purpose):
- Password hashing / verification (belongs in models/auth.py)
- Session management / login state (controller responsibility)
- UI rendering (view responsibility)

Typical usage:
    # app startup (composition root)
    users_col = db["users"]
    user_model = UserModel(users_col)

    # controller
    user = user_model.get_by_email(email)
"""

from typing import Optional, Dict, Any


class UserModel:
    """
    Model layer: responsible ONLY for database reads/writes.
    No password checking here. No UI stuff here.
    """

    def __init__(self, users_collection):
        # users_collection = db["users"]
        self.users = users_collection

    def get_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Return the user document if it exists, otherwise None.
        """
        return self.users.find_one({"email": email.lower().strip()})

    def create_user(self, display_name: str, email: str, password_hash: str) -> str:
        """
        Insert a new user doc and return the inserted id as string.
        """
        doc = {
            "display_name": display_name.strip(),
            "email": email.lower().strip(),
            "password_hash": password_hash,
        }
        result = self.users.insert_one(doc)
        return str(result.inserted_id)
