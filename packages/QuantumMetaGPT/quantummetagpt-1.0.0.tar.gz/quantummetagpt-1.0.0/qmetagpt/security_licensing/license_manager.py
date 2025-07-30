from cryptography.fernet import Fernet
import hashlib
import uuid
import json
from datetime import datetime, timedelta
from ..utils.logger import get_logger

logger = get_logger(__name__)

class LicenseManager:
    def __init__(self, secret_key=None):
        self.secret_key = secret_key or Fernet.generate_key()
        self.cipher = Fernet(self.secret_key)
    
    def generate_license(self, customer_info, duration_days=365):
        hw_id = self.get_hardware_id()
        expiry = (datetime.now() + timedelta(days=duration_days)).isoformat()
        
        license_data = {
            "customer": customer_info,
            "hw_id": hw_id,
            "expiry": expiry,
            "features": ["full_access"]
        }
        
        json_data = json.dumps(license_data).encode()
        return self.cipher.encrypt(json_data)
    
    def validate_license(self, license_key):
        try:
            decrypted = self.cipher.decrypt(license_key).decode()
            license_data = json.loads(decrypted)
            
            current_hw_id = self.get_hardware_id()
            expiry_date = datetime.fromisoformat(license_data['expiry'])
            
            if license_data['hw_id'] != current_hw_id:
                logger.error("Hardware ID mismatch")
                return False
            
            if datetime.now() > expiry_date:
                logger.error("License expired")
                return False
                
            logger.info("License validation successful")
            return True
        except Exception as e:
            logger.error(f"License validation failed: {e}")
            return False
    
    def get_hardware_id(self):
        return hashlib.sha256(str(uuid.getnode()).encode()).hexdigest()