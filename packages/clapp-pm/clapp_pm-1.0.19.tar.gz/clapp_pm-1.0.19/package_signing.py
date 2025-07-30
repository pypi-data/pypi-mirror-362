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
import base64
import zipfile
from typing import Dict, Tuple, Optional, Any
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend


class PackageSigner:
    """Paket bütünlüğü ve checksum sınıfı (imzalama geçici olarak devre dışı)"""

    def __init__(self):
        pass

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
                has_manifest = any(
                    f.endswith('manifest.json')
                    for f in file_list
                )
                if not has_manifest:
                    return False, "Manifest dosyası bulunamadı"

                # Dosyaları test et
                zip_file.testzip()

                return True, "Paket bütünlüğü doğrulandı"

        except zipfile.BadZipFile:
            return False, "Geçersiz ZIP dosyası"
        except Exception as e:
            return False, f"Bütünlük kontrolü hatası: {str(e)}"


def check_package_security(package_path: str) -> Dict[str, Any]:
    """Paket güvenlik kontrolü yapar (imza kontrolü geçici olarak devre dışı)"""
    signer = PackageSigner()

    results = {
        "integrity": False,
        "signature": None,
        "checksum": "",
        "warnings": []
    }

    # Bütünlük kontrolü
    integrity_valid, integrity_msg = signer.verify_package_integrity(
        package_path
    )
    results["integrity"] = integrity_valid

    if not integrity_valid:
        results["warnings"].append(f"Bütünlük hatası: {integrity_msg}")

    # Checksum hesapla
    results["checksum"] = signer.calculate_checksum(package_path)

    # İmza kontrolü kaldırıldı
    results["signature"] = None

    return results