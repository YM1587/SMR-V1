import sys
import os

# Add backend to path
sys.path.append('backend')
from auth import get_password_hash, verify_password

def test_auth():
    password = "MySecurePassword123"
    print(f"Testing with password: {password}")
    
    hashed = get_password_hash(password)
    print(f"Hashed password: {hashed}")
    
    print("Verifying correct password...")
    if verify_password(password, hashed):
        print("SUCCESS: Correct password verified.")
    else:
        print("FAILURE: Correct password failed verification.")
        
    print("Verifying incorrect password...")
    if not verify_password("WrongPassword", hashed):
        print("SUCCESS: Incorrect password rejected.")
    else:
        print("FAILURE: Incorrect password accepted.")

if __name__ == "__main__":
    try:
        test_auth()
    except Exception as e:
        print(f"ERROR: {e}")
