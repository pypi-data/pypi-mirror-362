# clapp-packages - Resmi clapp Paket Deposu

Bu repo, [clapp](https://github.com/mburakmmm/clapp) paket yöneticisinin resmi ve merkezi paket deposudur.

## Yapı ve Kullanım

- Her paket kendi klasöründe bulunur (ör: `hello-world/`)
- Her pakette en az bir `manifest.json` ve giriş dosyası (`main.py` veya benzeri) bulunur
- Tüm paketler ve sürümler `index.json` dosyasında listelenir
- Paketler doğrudan elle eklenmez, sadece `clapp publish` komutu ile eklenir/güncellenir

## Paket Yükleme

Kullanıcılar paketleri doğrudan CLI ile yükler:
```bash
clapp install hello-world
```
clapp, bu repodaki `index.json` üzerinden paketleri bulur ve indirir.

## Paket Yayınlama

Kendi uygulamanızı eklemek için:
1. Uygulamanızın klasöründe geçerli bir `manifest.json` ve giriş dosyası olmalı
2. `clapp publish ./my-app --push` komutunu kullanın
   - Bu komut, paketi zipler, bu repoya ekler ve `index.json`'u günceller
   - Tüm işlemler otomatik yapılır, manuel ekleme yapılmaz

## index.json

- Tüm paketlerin adı, sürümü, açıklaması ve indirme bağlantısı burada tutulur
- clapp CLI, paket arama ve yükleme işlemlerinde bu dosyayı kullanır

## Katkı ve Güvenlik

- Paketler sadece `clapp publish` ile eklenir/güncellenir
- Her paket için geçerli manifest ve çalışır giriş dosyası zorunludur
- Zararlı veya uygunsuz içerik tespit edilirse paket kaldırılır

## Lisans

Bu repodaki paketler kendi lisanslarına sahiptir. Genel repo MIT lisansı altındadır.

## Destek

- 🐛 Hata bildirimi ve öneriler: [Issues](https://github.com/mburakmmm/clapp-packages/issues)
- 📖 Ana proje: [clapp](https://github.com/mburakmmm/clapp) 