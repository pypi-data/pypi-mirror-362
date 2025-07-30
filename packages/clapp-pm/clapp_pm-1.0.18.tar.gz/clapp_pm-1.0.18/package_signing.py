#!/usr/bin/env python3
"""
package_signing.py - Paket İmzalama ve Doğrulama Sistemi

Bu modül clapp paketlerinin güvenliğini sağlamak için:
- Paket imzalama
- İmza doğrulama
- Checksum hesaplama
- Güvenlik kontrolü
"""

import os
import json
import hashlib
import hmac
import base64
import tempfile
import zipfile
from pathlib import Path
from typing import Dict, Tuple, Optional
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend

class PackageSigner:
    """Paket imzalama ve doğrulama sınıfı"""
    
    def __init__(self, private_key_path: Optional[str] = None, public_key_path: Optional[str] = None):
        """
        PackageSigner başlatıcısı
        
        Args:
            private_key_path: Özel anahtar dosyası yolu
            public_key_path: Genel anahtar dosyası yolu
        """
        self.private_key_path = private_key_path
        self.public_key_path = public_key_path
        self.private_key = None
        self.public_key = None
        
        if private_key_path and os.path.exists(private_key_path):
            self.load_private_key(private_key_path)
        
        if public_key_path and os.path.exists(public_key_path):
            self.load_public_key(public_key_path)
    
    def generate_key_pair(self, key_size: int = 2048) -> Tuple[str, str]:
        """
        Yeni RSA anahtar çifti oluşturur
        
        Args:
            key_size: Anahtar boyutu (varsayılan: 2048)
            
        Returns:
            (private_key_path, public_key_path)
        """
        # Özel anahtar oluştur
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
            backend=default_backend()
        )
        
        # Genel anahtar al
        public_key = private_key.public_key()
        
        # Anahtarları kaydet
        private_key_path = self._save_private_key(private_key)
        public_key_path = self._save_public_key(public_key)
        
        return private_key_path, public_key_path
    
    def _save_private_key(self, private_key) -> str:
        """Özel anahtarı dosyaya kaydet"""
        key_path = os.path.join(os.path.expanduser("~"), ".clapp", "private_key.pem")
        os.makedirs(os.path.dirname(key_path), exist_ok=True)
        
        with open(key_path, "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        
        return key_path
    
    def _save_public_key(self, public_key) -> str:
        """Genel anahtarı dosyaya kaydet"""
        key_path = os.path.join(os.path.expanduser("~"), ".clapp", "public_key.pem")
        os.makedirs(os.path.dirname(key_path), exist_ok=True)
        
        with open(key_path, "wb") as f:
            f.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))
        
        return key_path
    
    def load_private_key(self, key_path: str):
        """Özel anahtarı dosyadan yükle"""
        with open(key_path, "rb") as f:
            self.private_key = serialization.load_pem_private_key(
                f.read(),
                password=None,
                backend=default_backend()
            )
    
    def load_public_key(self, key_path: str):
        """Genel anahtarı dosyadan yükle"""
        with open(key_path, "rb") as f:
            self.public_key = serialization.load_pem_public_key(
                f.read(),
                backend=default_backend()
            )
    
    def calculate_checksum(self, file_path: str) -> str:
        """
        Dosyanın SHA-256 checksum'unu hesaplar
        
        Args:
            file_path: Dosya yolu
            
        Returns:
            SHA-256 hash (hex formatında)
        """
        sha256_hash = hashlib.sha256()
        
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        
        return sha256_hash.hexdigest()
    
    def calculate_package_checksum(self, package_path: str) -> Dict[str, str]:
        """
        Paket içindeki tüm dosyaların checksum'unu hesaplar
        
        Args:
            package_path: Paket dosyası yolu (.zip)
            
        Returns:
            Dosya yolları ve checksum'ları
        """
        checksums = {}
        
        with zipfile.ZipFile(package_path, 'r') as zip_file:
            for file_info in zip_file.filelist:
                if not file_info.is_dir():
                    file_data = zip_file.read(file_info.filename)
                    checksum = hashlib.sha256(file_data).hexdigest()
                    checksums[file_info.filename] = checksum
        
        return checksums
    
    def sign_package(self, package_path: str) -> Tuple[bool, str, Optional[str]]:
        """
        Paketi imzalar
        
        Args:
            package_path: Paket dosyası yolu
            
        Returns:
            (success, message, signature_path)
        """
        if not self.private_key:
            return False, "Özel anahtar yüklenmedi", None
        
        try:
            # Paket checksum'unu hesapla
            checksum = self.calculate_checksum(package_path)
            
            # Manifest dosyasını oku
            manifest_data = self._extract_manifest_data(package_path)
            if not manifest_data:
                return False, "Manifest dosyası bulunamadı", None
            
            # İmzalanacak veriyi hazırla
            data_to_sign = {
                "checksum": checksum,
                "manifest": manifest_data,
                "package_name": os.path.basename(package_path)
            }
            
            data_string = json.dumps(data_to_sign, sort_keys=True)
            data_bytes = data_string.encode('utf-8')
            
            # İmzala
            signature = self.private_key.sign(
                data_bytes,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            
            # İmzayı kaydet
            signature_path = package_path.replace('.zip', '.sig')
            with open(signature_path, 'wb') as f:
                f.write(base64.b64encode(signature))
            
            return True, "Paket başarıyla imzalandı", signature_path
            
        except Exception as e:
            return False, f"İmzalama hatası: {str(e)}", None
    
    def verify_package(self, package_path: str, signature_path: str) -> Tuple[bool, str]:
        """
        Paket imzasını doğrular
        
        Args:
            package_path: Paket dosyası yolu
            signature_path: İmza dosyası yolu
            
        Returns:
            (is_valid, message)
        """
        if not self.public_key:
            return False, "Genel anahtar yüklenmedi"
        
        try:
            # İmzayı oku
            with open(signature_path, 'rb') as f:
                signature = base64.b64decode(f.read())
            
            # Paket checksum'unu hesapla
            checksum = self.calculate_checksum(package_path)
            
            # Manifest dosyasını oku
            manifest_data = self._extract_manifest_data(package_path)
            if not manifest_data:
                return False, "Manifest dosyası bulunamadı"
            
            # Doğrulanacak veriyi hazırla
            data_to_verify = {
                "checksum": checksum,
                "manifest": manifest_data,
                "package_name": os.path.basename(package_path)
            }
            
            data_string = json.dumps(data_to_verify, sort_keys=True)
            data_bytes = data_string.encode('utf-8')
            
            # İmzayı doğrula
            self.public_key.verify(
                signature,
                data_bytes,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            
            return True, "Paket imzası doğrulandı"
            
        except Exception as e:
            return False, f"İmza doğrulama hatası: {str(e)}"
    
    def _extract_manifest_data(self, package_path: str) -> Optional[Dict]:
        """Paket içinden manifest verilerini çıkarır"""
        try:
            with zipfile.ZipFile(package_path, 'r') as zip_file:
                # packages/ klasörü altındaki manifest.json'u ara
                for file_info in zip_file.filelist:
                    if file_info.filename.endswith('manifest.json'):
                        manifest_data = zip_file.read(file_info.filename)
                        return json.loads(manifest_data.decode('utf-8'))
                
                # Doğrudan manifest.json'u ara
                if 'manifest.json' in zip_file.namelist():
                    manifest_data = zip_file.read('manifest.json')
                    return json.loads(manifest_data.decode('utf-8'))
                
                return None
        except Exception:
            return None
    
    def verify_package_integrity(self, package_path: str) -> Tuple[bool, str]:
        """
        Paket bütünlüğünü kontrol eder
        
        Args:
            package_path: Paket dosyası yolu
            
        Returns:
            (is_valid, message)
        """
        try:
            # ZIP dosyası geçerliliğini kontrol et
            with zipfile.ZipFile(package_path, 'r') as zip_file:
                # Dosya listesini kontrol et
                file_list = zip_file.namelist()
                
                # Manifest dosyası var mı?
                has_manifest = any(f.endswith('manifest.json') for f in file_list)
                if not has_manifest:
                    return False, "Manifest dosyası bulunamadı"
                
                # Dosyaları test et
                zip_file.testzip()
                
                return True, "Paket bütünlüğü doğrulandı"
                
        except zipfile.BadZipFile:
            return False, "Geçersiz ZIP dosyası"
        except Exception as e:
            return False, f"Bütünlük kontrolü hatası: {str(e)}"

# Yardımcı fonksiyonlar
def create_package_signer() -> PackageSigner:
    """Varsayılan ayarlarla PackageSigner oluşturur"""
    clapp_dir = os.path.join(os.path.expanduser("~"), ".clapp")
    private_key_path = os.path.join(clapp_dir, "private_key.pem")
    public_key_path = os.path.join(clapp_dir, "public_key.pem")
    
    return PackageSigner(private_key_path, public_key_path)

def sign_package_file(package_path: str) -> Tuple[bool, str]:
    """Paket dosyasını imzalar"""
    signer = create_package_signer()
    
    # Anahtar yoksa oluştur
    if not signer.private_key:
        print("🔑 Yeni anahtar çifti oluşturuluyor...")
        private_key_path, public_key_path = signer.generate_key_pair()
        signer.load_private_key(private_key_path)
        print(f"✅ Anahtarlar oluşturuldu: {clapp_dir}")
    
    return signer.sign_package(package_path)

def verify_package_file(package_path: str, signature_path: str) -> Tuple[bool, str]:
    """Paket dosyasının imzasını doğrular"""
    signer = create_package_signer()
    return signer.verify_package(package_path, signature_path)

def check_package_security(package_path: str) -> Dict[str, any]:
    """Paket güvenlik kontrolü yapar"""
    signer = create_package_signer()
    
    results = {
        "integrity": False,
        "signature": False,
        "checksum": "",
        "warnings": []
    }
    
    # Bütünlük kontrolü
    integrity_valid, integrity_msg = signer.verify_package_integrity(package_path)
    results["integrity"] = integrity_valid
    
    if not integrity_valid:
        results["warnings"].append(f"Bütünlük hatası: {integrity_msg}")
    
    # Checksum hesapla
    results["checksum"] = signer.calculate_checksum(package_path)
    
    # İmza kontrolü (varsa)
    signature_path = package_path.replace('.zip', '.sig')
    if os.path.exists(signature_path):
        signature_valid, signature_msg = signer.verify_package(package_path, signature_path)
        results["signature"] = signature_valid
        
        if not signature_valid:
            results["warnings"].append(f"İmza hatası: {signature_msg}")
    else:
        results["warnings"].append("İmza dosyası bulunamadı")
    
    return results 