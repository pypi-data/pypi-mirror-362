# clapp - Hafif Komut Satırı Uygulama Paket Yöneticisi

clapp, Python ve Lua uygulamalarını kolayca yükleyip çalıştırmanızı sağlayan, sade ve hızlı bir CLI paket yöneticisidir.

## Özellikler

- 🚀 **Tek Komutla Kurulum ve Çalıştırma**
- 📦 **Çoklu Dil Desteği**: Python ve Lua uygulamaları
- 🔒 **Güvenli ve Şeffaf Paket Sistemi**
- 🛠️ **Geliştirici Araçları**: Doğrulama, yayınlama, kaldırma, güncelleme
- 🌐 **Ayrı Paket Deposu**: [clapp-packages](https://github.com/mburakmmm/clapp-packages) ile iki repo sistemi

## Kurulum

```bash
pip install clapp
```

## Temel Kullanım

```bash
# Paket yükle (uzak depodan)
clapp install hello-world

# Yüklü paketleri listele
clapp list

# Paket çalıştır
clapp run hello-world

# Paket kaldır
clapp uninstall hello-world

# Kendi uygulamanı yayınla (clapp-packages'a otomatik push)
clapp publish ./my-app --push
```

## İki Repo Sistemi

- **clapp:** CLI ve yönetim araçlarını içerir. (Bu repo)
- **clapp-packages:** Sadece paketler ve index.json içerir. Tüm paket işlemleri publish komutu ile otomatik yapılır.

## Manifest Formatı

```json
{
    "name": "my-app",
    "version": "1.0.0",
    "language": "python",
    "entry": "main.py",
    "description": "Açıklama",
    "dependencies": []
}
```

## Katkı ve Destek

- 🐛 Hata bildirimi ve öneriler için: [Issues](https://github.com/mburakmmm/clapp/issues)
- 📦 Paket eklemek için: [clapp-packages](https://github.com/mburakmmm/clapp-packages)
- 📖 Detaylı bilgi ve dokümantasyon: [Wiki](https://github.com/mburakmmm/clapp/wiki)

## Lisans

MIT License 