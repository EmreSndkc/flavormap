# FlavorMap - Kalan Özellikler ve Yol Haritası (Hafta 10-13)

MS3 aşaması tamamlandıktan sonra proje kılavuzuna göre yapılması gereken **Zorunlu (Mandatory)** özelliklerin listesi aşağıdadır. Kalan bu özellikleri adım adım geliştirmemiz gerekmektedir.

## Zorunlu Özellikler (Mandatory Features)

### 1. Restaurant Photo (Restoran Fotoğrafı)
- `Restaurant` modeline `models.ImageField` eklenmesi.
- Medya (Media) dosyaları ayarlarının `settings.py` üzerinde yapılması (`MEDIA_URL`, `MEDIA_ROOT`).
- Restoran ekleme/düzenleme formlarında dosya yükleme desteği (`enctype="multipart/form-data"`).
- Yüklenen görsellerin arayüzde gösterilmesi.

### 2. Favorites List (Favoriler Listesi)
- Kullanıcı ve Restoran arasında ManyToMany (Çoka Çok) ilişki kuracak bir model veya alan eklenmesi.
- Restoran detay sayfasında (veya liste sayfasında) "Favoriye Ekle" / "Favoriden Çıkar" butonu yapılması.

### 3. User Profile (Kullanıcı Profil Sayfası)
- `/profil/` veya `/kullanici/<username>/` şeklinde bir URL oluşturulması.
- Kullanıcının temel bilgilerinin gösterilmesi.
- Kullanıcının yazdığı **tüm yorumların** listelenmesi.
- Kullanıcının **favoriye eklediği restoranların** listelenmesi.

### 4. Menu Management (Menü Yönetimi)
- Mevcut `MenuItem` modelinin arayüz üzerinden eklenebilmesi için form oluşturulması.
- Yalnızca restoran sahibinin menüye yeni ürün ekleme, ürünü düzenleme ve silme işlemlerini yapabileceği (CRUD) view ve şablonların hazırlanması.

### 5. Review Replies (Yorumlara Cevap Yazma)
- `Review` modeline (kendi içine veya ayrı bir modelle) `reply` veya `parent_review` gibi bir alan eklenerek yoruma cevap verebilme (1 kademe derinlik) özelliğinin kazandırılması.
- Yorumların altında "Cevapla" butonu ve formunun yer alması.

### 6. Opening Hours (Çalışma Saatleri)
- Haftanın 7 günü için açılış ve kapanış saatlerini tutacak yeni bir `OpeningHours` modelinin oluşturulması (Restoran modeli ile ilişkili).
- Restoran detay sayfasında gün gün çalışma saatlerinin listelenmesi.

### 7. Popular Ranking (Popüler ve Yeni Sıralaması)
- Ana sayfada (`home.html`) şu an bulunan "En Yeniler" (Newest) listesinin yanına, veritabanındaki yorumlara göre hesaplanan "En Yüksek Puanlılar" (Top-rated) restoranların çekilip gösterilmesi.

### 8. Atomic Transactions
- Karmaşık veritabanı işlemlerinde (örneğin restoran silindiğinde bağlı görsellerin de silinmesi, yoruma cevap eklenirken oluşabilecek hatalar vb.) `transaction.atomic()` kullanılarak olası `IntegrityError` hatalarının düzgün yönetilmesi.

---

## Bonus Özellikler (İsteğe Bağlı Ekstra Kredi)

- **CSS & Responsive:** Sitenin tasarımının daha profesyonel ve tüm cihazlara (mobil vs.) uyumlu hale getirilmesi.
- **JavaScript Element:** Yıldızlı oylama widget'ı, açılır kapanır modallar veya anlık (sayfa yenilemeden) arama-filtreleme gibi JS ile çalışan interaktif bileşenler eklenmesi.
- **Restaurant Owner Role:** Normal kullanıcılardan ayrı olarak, sisteme "Restoran Sahibi" rolünün getirilmesi ve mevcut restoranları "sahiplenebilme" (claim) başvurusunun yapılması.
- **Map Integration:** Restoran adreslerinin Google Maps iframe'i aracılığıyla sayfaya entegre edilmesi.
- **Photo Gallery:** Her restoran için tek bir resim yerine birden fazla fotoğrafın yüklenebildiği (çoklu upload) bir galeri modeli ve bu görsellerin büyütülebilir (lightbox) olarak sunulması.
- **Advanced Filtering:** Birden fazla filtrenin (örneğin hem kategori hem lokasyon hem de yıldız puanının) aynı anda ve sorunsuz çalıştırılabildiği daha karmaşık sorgu sistemi.
- **Review Likes:** Kullanıcıların yorumları "Faydalı / Beğen" (Like) diyerek oylayabilmesi ve yorumların en çok beğeni alana göre sıralanabilmesi.
