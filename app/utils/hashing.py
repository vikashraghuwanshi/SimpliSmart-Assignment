import bcrypt

class Hash:
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hashes a plain text password using bcrypt.
        
        Args:
            password (str): The plain text password to hash.
        
        Returns:
            str: The hashed password.
        """
        salt = bcrypt.gensalt()  # Generate a salt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')  # Return hashed password as a string

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verifies if the plain text password matches the hashed password.
        
        Args:
            plain_password (str): The plain text password to verify.
            hashed_password (str): The hashed password to compare against.
        
        Returns:
            bool: True if the passwords match, False otherwise.
        """
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
