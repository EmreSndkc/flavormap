import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flavormap.settings')
django.setup()

from restaurants.models import Category, Restaurant, MenuItem, Review

# Temizle
Review.objects.all().delete()
MenuItem.objects.all().delete()
Restaurant.objects.all().delete()
Category.objects.all().delete()

data = {
    "Türk Mutfağı": {
        "restaurants": [
            {
                "name": "Sultanahmet Sofrası",
                "description": "Geleneksel Osmanlı ve Türk mutfağının en güzel örneklerini sunan tarihi bir mekan.",
                "address": "Divan Yolu Cad. No:12, Sultanahmet, İstanbul",
                "phone": "0212 511 22 33",
                "price": "€€",
                "menu": [("Kuzu İncik", 280), ("İskender Kebap", 220), ("Mercimek Çorbası", 80), ("Baklava", 120), ("Ayran", 40)],
                "reviews": [(5, "Harika bir deneyimdi, kebaplar nefisti!"), (4, "Güzel mekan, fiyatlar biraz yüksek ama kalite iyi.")]
            },
            {
                "name": "Karaköy Balıkçısı",
                "description": "Taze balık ve deniz ürünleriyle ünlü İstanbul'un köklü balık restoranı.",
                "address": "Kemankeş Cad. No:45, Karaköy, İstanbul",
                "phone": "0212 244 55 66",
                "price": "€€€",
                "menu": [("Levrek Izgara", 350), ("Balık Çorbası", 95), ("Karides Güveç", 280), ("Midye Dolma", 60), ("Rakı", 150)],
                "reviews": [(5, "En taze balığı burada yedim."), (5, "Manzara ve lezzet mükemmel.")]
            },
            {
                "name": "Beyoğlu Büfesi",
                "description": "Uygun fiyatlı ev yemekleri ve geleneksel Türk lezzetleri.",
                "address": "İstiklal Cad. No:88, Beyoğlu, İstanbul",
                "phone": "0212 293 11 22",
                "price": "€",
                "menu": [("Kuru Fasulye", 75), ("Pilav Üstü Döner", 120), ("Ezogelin Çorbası", 60), ("Kadayıf", 80), ("Çay", 15)],
                "reviews": [(4, "Ev yemeği tadında, çok doyurucu."), (3, "Kalabalık saatlerde biraz yavaş servis.")]
            },
            {
                "name": "Adana Ocakbaşı",
                "description": "Güneyden gelen ustalarımızla gerçek Adana kebabı deneyimi.",
                "address": "Bağcılar Mah. No:7, Fatih, İstanbul",
                "phone": "0212 635 44 55",
                "price": "€€",
                "menu": [("Adana Kebap", 180), ("Urfa Kebap", 175), ("Lahmacun", 45), ("Şalgam", 25), ("Pide", 30)],
                "reviews": [(5, "Gerçek Adana lezzeti İstanbul'da!"), (4, "Acılı sevenler için ideal.")]
            },
            {
                "name": "Boğaz Manzara Restaurant",
                "description": "Boğaz manzarasıyla eşsiz bir ortamda Türk mutfağının incelikleri.",
                "address": "Kuruçeşme Cad. No:22, Beşiktaş, İstanbul",
                "phone": "0212 258 77 88",
                "price": "€€€",
                "menu": [("Çoban Kavurma", 320), ("Hünkar Beğendi", 280), ("Mantı", 160), ("Sütlaç", 90), ("Türk Kahvesi", 45)],
                "reviews": [(5, "Manzara inanılmaz, yemekler harika."), (4, "Özel günler için ideal bir yer.")]
            },
            {
                "name": "Eminönü Pidecisi",
                "description": "Taş fırında pişen geleneksel Türk pidelerinin adresi.",
                "address": "Hasırcılar Cad. No:3, Eminönü, İstanbul",
                "phone": "0212 522 88 99",
                "price": "€",
                "menu": [("Kıymalı Pide", 90), ("Kaşarlı Pide", 80), ("Yumurtalı Pide", 85), ("Çorba", 55), ("Ayran", 30)],
                "reviews": [(4, "Pideleri gerçekten çok lezzetli."), (5, "Fırın kokusu insanı içeri çekiyor.")]
            },
            {
                "name": "Kadıköy Meyhanesi",
                "description": "Geleneksel Türk meyhane kültürünü yaşatan, rakı-balık geleneğinin merkezi.",
                "address": "Moda Cad. No:16, Kadıköy, İstanbul",
                "phone": "0216 336 22 33",
                "price": "€€",
                "menu": [("Meyhane Tabağı (Meze)", 180), ("Balık Tava", 250), ("Rakı (tekil)", 120), ("Fava", 70), ("Cacık", 55)],
                "reviews": [(5, "Asıl İstanbul meyhane kültürü bu!"), (4, "Canlı müzikle güzel bir akşam.")]
            },
            {
                "name": "Çengelköy Köftecisi",
                "description": "50 yıldır aynı lezzeti sunan efsane köfte restoranı.",
                "address": "Çengelköy Cad. No:4, Üsküdar, İstanbul",
                "phone": "0216 422 66 77",
                "price": "€",
                "menu": [("Izgara Köfte", 130), ("İnegöl Köfte", 130), ("Piyaz", 45), ("Patates Kızartması", 50), ("Şerbet", 20)],
                "reviews": [(5, "50 yıllık lezzet bozulmamış."), (5, "İstanbul'un en iyi köftesi burada.")]
            },
            {
                "name": "Nişantaşı Lokantası",
                "description": "Modern Türk mutfağını şık bir ortamda sunan butik restoran.",
                "address": "Teşvikiye Cad. No:34, Nişantaşı, İstanbul",
                "phone": "0212 225 33 44",
                "price": "€€€",
                "menu": [("Modern Meze Tabağı", 220), ("Kuzu Tandır", 380), ("Fıstıklı Baklava", 150), ("Türk Şarabı", 200), ("Künefe", 140)],
                "reviews": [(4, "Şık sunum ve kaliteli malzeme."), (5, "Özel davetler için mükemmel.")]
            },
            {
                "name": "Tarihi Galata Börekçisi",
                "description": "Sabahın erken saatlerinden itibaren taze börek ve simit sunan tarihi dükkân.",
                "address": "Galata Kulesi Yanı No:2, Beyoğlu, İstanbul",
                "phone": "0212 249 11 00",
                "price": "€",
                "menu": [("Su Böreği", 70), ("Sigara Böreği", 55), ("Simit", 15), ("Açma", 20), ("Çay", 15)],
                "reviews": [(5, "Sabah kahvaltısı için harika."), (4, "Börekler her sabah taze.")]
            },
        ]
    },
    "İtalyan Mutfağı": {
        "restaurants": [
            {
                "name": "La Bella Roma",
                "description": "Otantik İtalyan tariflerini İstanbul'a taşıyan, İtalyan şef tarafından yönetilen restoran.",
                "address": "Abdi İpekçi Cad. No:15, Nişantaşı, İstanbul",
                "phone": "0212 231 44 55",
                "price": "€€€",
                "menu": [("Spaghetti Carbonara", 280), ("Pizza Margherita", 220), ("Tiramisu", 150), ("Bruschetta", 120), ("Chianti (kadeh)", 180)],
                "reviews": [(5, "İstanbul'daki en iyi İtalyan restoranı."), (4, "Makarnalar gerçekten İtalya'yı hatırlattı.")]
            },
            {
                "name": "Venezia Ristorante",
                "description": "Venedik usulü deniz ürünleri ve İtalyan klasiklerinin buluşma noktası.",
                "address": "Kuruçeşme Mah. No:8, Beşiktaş, İstanbul",
                "phone": "0212 259 66 77",
                "price": "€€€",
                "menu": [("Risotto ai Frutti di Mare", 320), ("Tagliatelle al Tartufo", 380), ("Panna Cotta", 130), ("Antipasto", 160), ("Prosecco", 200)],
                "reviews": [(5, "Harika deniz ürünleri risottosu!"), (4, "Atmosfer ve lezzet tam İtalya gibi.")]
            },
            {
                "name": "Trattoria Milano",
                "description": "Kuzey İtalya'nın ev yapımı tarifleri ve samimi atmosferi.",
                "address": "Bağdat Cad. No:112, Kadıköy, İstanbul",
                "phone": "0216 355 22 33",
                "price": "€€",
                "menu": [("Lasagne al Forno", 250), ("Penne Arrabbiata", 200), ("Minestrone", 110), ("Gelato", 90), ("Espresso", 60)],
                "reviews": [(4, "Ev yapımı lazanya inanılmaz."), (5, "Her şey taze ve lezzetli.")]
            },
            {
                "name": "Piccolo Napoli",
                "description": "Napoli usulü pizza ustasının açtığı otantik pizza restoranı.",
                "address": "Tarihi Bomonti Mah. No:5, Şişli, İstanbul",
                "phone": "0212 224 88 99",
                "price": "€€",
                "menu": [("Pizza Napoletana", 210), ("Pizza Diavola", 230), ("Calzone", 220), ("Insalata Caprese", 140), ("Limonata", 70)],
                "reviews": [(5, "Gerçek Napoli pizzası!"), (5, "Hamur mükemmel, malzemeler taze.")]
            },
            {
                "name": "Osteria Romana",
                "description": "Roma tarzı makarna ve etin buluştuğu sıcak bir İtalyan lokantası.",
                "address": "Cihangir Mah. No:22, Beyoğlu, İstanbul",
                "phone": "0212 293 55 66",
                "price": "€€",
                "menu": [("Cacio e Pepe", 220), ("Saltimbocca", 290), ("Supplì", 100), ("Crostata", 110), ("Negroni", 160)],
                "reviews": [(4, "Cihangir'in sakin atmosferinde harika İtalyan yemeği."), (4, "Porsiyon büyüklüğü çok iyi.")]
            },
            {
                "name": "Caffè Firenze",
                "description": "Floransa usulü kahve kültürü ve hafif İtalyan atıştırmalıkları.",
                "address": "İstiklal Cad. No:200, Beyoğlu, İstanbul",
                "phone": "0212 244 33 22",
                "price": "€",
                "menu": [("Focaccia", 80), ("Panini Prosciutto", 140), ("Cappuccino", 70), ("Cornetto", 45), ("Cannoli", 85)],
                "reviews": [(5, "En iyi cappuccino İstanbul'da burada!"), (4, "Sandviçler çok doyurucu.")]
            },
            {
                "name": "Sicilia Ristorante",
                "description": "Sicilya adası mutfağının zengin tatlarını sunan aile işletmesi.",
                "address": "Moda Cad. No:33, Kadıköy, İstanbul",
                "phone": "0216 418 77 88",
                "price": "€€",
                "menu": [("Pasta alla Norma", 210), ("Arancini", 90), ("Caponata", 120), ("Cassata", 130), ("Amaro", 100)],
                "reviews": [(5, "Sicilya mutfağını merak edenler için şart."), (4, "Arancini enfes!")]
            },
            {
                "name": "Trevi Restaurant",
                "description": "Modern İtalyan mutfağı anlayışıyla hazırlanan yenilikçi yemekler.",
                "address": "Levent Mah. No:6, Beşiktaş, İstanbul",
                "phone": "0212 270 11 22",
                "price": "€€€",
                "menu": [("Tagliolini al Limone", 270), ("Branzino al Forno", 380), ("Burrata", 180), ("Tartufo", 160), ("Amaretto Sour", 170)],
                "reviews": [(4, "İş yemekleri için ideal."), (5, "Burrata çok tazeydi.")]
            },
            {
                "name": "Da Vinci Pizzeria",
                "description": "Çıtır tabanıyla sevilen, uygun fiyatlı pizza ve makarna restoranı.",
                "address": "Acıbadem Cad. No:44, Kadıköy, İstanbul",
                "phone": "0216 325 99 00",
                "price": "€",
                "menu": [("Pizza Quattro Formaggi", 190), ("Spaghetti Bolognese", 170), ("Caesar Salatası", 120), ("Tiramisu", 100), ("Kola", 30)],
                "reviews": [(4, "Fiyat performans çok iyi."), (3, "Akşam saatlerinde bekleme olabiliyor.")]
            },
            {
                "name": "Toscana Restaurant",
                "description": "Toskana bölgesine ait şarap ve yemek kültürünü İstanbul'a taşıyan şık mekan.",
                "address": "Etiler Mah. No:19, Beşiktaş, İstanbul",
                "phone": "0212 352 44 55",
                "price": "€€€",
                "menu": [("Bistecca alla Fiorentina", 580), ("Ribollita", 160), ("Pappardelle al Cinghiale", 310), ("Biscotti", 80), ("Brunello di Montalcino", 450)],
                "reviews": [(5, "Bistecca mükemmeldi, şarap listesi çok zengin."), (5, "İstanbul'un en iyi İtalyan restoranlarından.")]
            },
        ]
    },
    "Japon Mutfağı": {
        "restaurants": [
            {
                "name": "Sakura Sushi",
                "description": "Japon şef tarafından hazırlanan otantik sushi ve sashimi çeşitleri.",
                "address": "Teşvikiye Cad. No:55, Nişantaşı, İstanbul",
                "phone": "0212 225 11 22",
                "price": "€€€",
                "menu": [("Salmon Nigiri (2 adet)", 120), ("Dragon Roll", 280), ("Miso Çorba", 80), ("Edamame", 90), ("Sake", 200)],
                "reviews": [(5, "İstanbul'un en iyi sushisi!"), (5, "Balık çok taze, sunum mükemmel.")]
            },
            {
                "name": "Tokyo Ramen House",
                "description": "Geleneksel Japon ramen tarifleriyle hazırlanan derin lezzetli çorbalar.",
                "address": "Bağdat Cad. No:78, Kadıköy, İstanbul",
                "phone": "0216 385 33 44",
                "price": "€€",
                "menu": [("Tonkotsu Ramen", 220), ("Shoyu Ramen", 210), ("Gyoza (6 adet)", 130), ("Karaage", 160), ("Matcha Latte", 80)],
                "reviews": [(5, "Eksi derecede soğukta sıcak ramen, mükemmel!"), (4, "Porsiyon büyük ve doyurucu.")]
            },
            {
                "name": "Osaka Izakaya",
                "description": "Japon birahane kültürünü yaşatan, küçük tabaklar ve bira eşliğinde akşam yemeği.",
                "address": "Cihangir Mah. No:8, Beyoğlu, İstanbul",
                "phone": "0212 251 77 88",
                "price": "€€",
                "menu": [("Yakitori (5 şiş)", 180), ("Takoyaki", 140), ("Okonomiyaki", 200), ("Asahi Bira", 100), ("Tofu Salatası", 110)],
                "reviews": [(4, "Canlı atmosfer, lezzetli küçük tabaklar."), (5, "Gerçek izakaya deneyimi.")]
            },
            {
                "name": "Kyoto Kaiseki",
                "description": "Geleneksel Japon çok kurslu kaiseki yemek deneyimi.",
                "address": "Abdi İpekçi Cad. No:30, Nişantaşı, İstanbul",
                "phone": "0212 233 66 77",
                "price": "€€€",
                "menu": [("Kaiseki Menü (7 kurs)", 950), ("Wagyu Sashimi", 480), ("Miso Çorba", 90), ("Matcha Dondurma", 130), ("Japanese Whisky", 300)],
                "reviews": [(5, "Hayatımda yediğim en özel yemek."), (5, "Her kurs bir sanat eseri gibiydi.")]
            },
            {
                "name": "Shibuya Teppanyaki",
                "description": "Gözünüzün önünde pişirilen teppanyaki şovu ve Japon ızgara lezzetleri.",
                "address": "Levent Mah. No:12, Beşiktaş, İstanbul",
                "phone": "0212 280 22 33",
                "price": "€€€",
                "menu": [("Wagyu Teppanyaki", 650), ("Karides Teppanyaki", 380), ("Sebze Teppanyaki", 220), ("Miso Çorba", 80), ("Oolong Çay", 60)],
                "reviews": [(5, "Şov muhteşem, yemek daha da güzel."), (4, "Pahalı ama değer.")]
            },
            {
                "name": "Harajuku Bento",
                "description": "Uygun fiyatlı bento kutuları ve hafif Japon yemekleri.",
                "address": "Kadıköy Çarşısı No:5, Kadıköy, İstanbul",
                "phone": "0216 336 55 66",
                "price": "€",
                "menu": [("Chicken Teriyaki Bento", 150), ("Vegetarian Bento", 130), ("Onigiri", 50), ("Miso Çorba", 55), ("Green Tea", 40)],
                "reviews": [(4, "Hızlı ve lezzetli öğle yemeği."), (4, "Fiyat performans harika.")]
            },
            {
                "name": "Fuji Tempura Bar",
                "description": "Çıtır tempura ve Japon aperatifleri üzerine uzmanlaşmış restoran.",
                "address": "Bomonti Mah. No:17, Şişli, İstanbul",
                "phone": "0212 222 44 55",
                "price": "€€",
                "menu": [("Ebi Tempura", 220), ("Yasai Tempura", 170), ("Tempura Udon", 200), ("Agedashi Tofu", 130), ("Shochu", 140)],
                "reviews": [(5, "Tempura bu kadar çıtır olabilir mi!"), (4, "Her şey tazeliğini koruyor.")]
            },
            {
                "name": "Sapporo Yakiniku",
                "description": "Masada ızgara deneyimi sunan Japon barbekü restoranı.",
                "address": "Etiler Mah. No:9, Beşiktaş, İstanbul",
                "phone": "0212 352 88 99",
                "price": "€€€",
                "menu": [("Wagyu Kalitesi Et (100g)", 350), ("Karışık Et Tabağı", 420), ("Kimchi", 80), ("Garlic Rice", 90), ("Sapporo Bira", 120)],
                "reviews": [(5, "Masada ızgara çok eğlenceli!"), (4, "Et kalitesi mükemmel.")]
            },
            {
                "name": "Matcha Garden",
                "description": "Matcha bazlı içecekler ve Japon tatlılarına adanmış cafe.",
                "address": "Moda Mah. No:28, Kadıköy, İstanbul",
                "phone": "0216 418 11 22",
                "price": "€",
                "menu": [("Matcha Latte", 75), ("Matcha Cheesecake", 110), ("Mochi Dondurma", 90), ("Dorayaki", 65), ("Hojicha Latte", 75)],
                "reviews": [(5, "Matcha sevenler için cennet!"), (4, "Her şey çok taze ve özenle hazırlanmış.")]
            },
            {
                "name": "Nara Udon & Soba",
                "description": "El yapımı udon ve soba erişteleriyle Japonya'nın kuzeyinin lezzetleri.",
                "address": "Yeldeğirmeni Mah. No:3, Kadıköy, İstanbul",
                "phone": "0216 449 33 44",
                "price": "€€",
                "menu": [("Kitsune Udon", 180), ("Zaru Soba", 170), ("Nabeyaki Udon", 220), ("Tempura Soba", 210), ("Yuzu Limonatası", 70)],
                "reviews": [(4, "El yapımı erişte farkı hissediliyor."), (5, "Soba çok lezzetli ve sağlıklı.")]
            },
        ]
    },
    "Meksika Mutfağı": {
        "restaurants": [
            {
                "name": "El Sombrero",
                "description": "Geleneksel Meksika tariflerini modern bir sunumla buluşturan renkli restoran.",
                "address": "İstiklal Cad. No:155, Beyoğlu, İstanbul",
                "phone": "0212 245 66 77",
                "price": "€€",
                "menu": [("Tacos al Pastor (3 adet)", 180), ("Guacamole & Chips", 130), ("Enchilada", 200), ("Churros", 90), ("Margarita", 180)],
                "reviews": [(5, "Gerçek Meksika lezzetleri!"), (4, "Margarita çok güzeldi.")]
            },
            {
                "name": "Taco Fiesta",
                "description": "Uygun fiyatlı cadde taco kültürünü İstanbul'a taşıyan şenlikli mekan.",
                "address": "Bağdat Cad. No:200, Kadıköy, İstanbul",
                "phone": "0216 360 22 33",
                "price": "€",
                "menu": [("Beef Taco", 60), ("Chicken Taco", 55), ("Veggie Taco", 50), ("Nachos", 100), ("Horchata", 50)],
                "reviews": [(4, "Hızlı ve lezzetli."), (5, "Uygun fiyata harika taco!")]
            },
            {
                "name": "Cantina Mexicana",
                "description": "Meksika köy mutfağından ilham alan ev yapımı tarifler ve canlı müzik.",
                "address": "Cihangir Mah. No:14, Beyoğlu, İstanbul",
                "phone": "0212 252 88 99",
                "price": "€€",
                "menu": [("Mole Poblano", 240), ("Chiles Rellenos", 210), ("Pozole", 160), ("Flan", 95), ("Mezcal", 160)],
                "reviews": [(5, "Mole sosu inanılmaz derinlikte."), (4, "Canlı müzikle harika bir akşam.")]
            },
            {
                "name": "Burrito Bros",
                "description": "Dev burritos ve quesadilla çeşitleriyle karın doyuran Meksika fast food.",
                "address": "Kozyatağı Mah. No:6, Kadıköy, İstanbul",
                "phone": "0216 369 44 55",
                "price": "€",
                "menu": [("Beef Burrito", 140), ("Chicken Quesadilla", 130), ("Bean Burrito", 110), ("Salsa Verde", 30), ("Frozen Lemonade", 55)],
                "reviews": [(4, "Çok doyurucu!"), (3, "Biraz yoğun ama lezzetli.")]
            },
            {
                "name": "Hacienda Azul",
                "description": "Tequila ve mezcal koleksiyonuyla ünlü üst segment Meksika restoranı.",
                "address": "Nişantaşı Mah. No:40, Şişli, İstanbul",
                "phone": "0212 227 11 22",
                "price": "€€€",
                "menu": [("Ceviche de Mango", 180), ("Cochinita Pibil", 320), ("Tostadas de Atún", 220), ("Tres Leches", 140), ("Tequila Tasting (3'lü)", 300)],
                "reviews": [(5, "Cochinita Pibil hayatımda yediğim en iyi Meksika yemeği."), (4, "Tequila koleksiyonu muazzam.")]
            },
            {
                "name": "Guadalajara Street Food",
                "description": "Meksika sokak yemeklerini çatı altında toplayan samimi mekan.",
                "address": "Yeldeğirmeni Mah. No:11, Kadıköy, İstanbul",
                "phone": "0216 450 77 88",
                "price": "€",
                "menu": [("Elote (Meksika Mısırı)", 50), ("Torta", 120), ("Sopes", 90), ("Tamale", 80), ("Agua Fresca", 40)],
                "reviews": [(5, "Elote çok lezzetliydi!"), (4, "Samimi atmosfer ve uygun fiyat.")]
            },
            {
                "name": "Verde Cocina",
                "description": "Vegan ve vejetaryen Meksika yemekleri üzerine uzmanlaşmış modern mekan.",
                "address": "Bomonti Mah. No:25, Şişli, İstanbul",
                "phone": "0212 296 33 44",
                "price": "€€",
                "menu": [("Jackfruit Taco", 160), ("Black Bean Enchilada", 170), ("Vegan Guacamole", 100), ("Chia Pudding", 90), ("Agua de Jamaica", 50)],
                "reviews": [(5, "Et yemeden bu kadar doyurucu Meksika yemeği olur mu!"), (4, "Vegan seçenekler çok zengin.")]
            },
            {
                "name": "Azteca Grill",
                "description": "Meksika ızgara kültürünü ön plana çıkaran et ağırlıklı restoran.",
                "address": "Etiler Mah. No:28, Beşiktaş, İstanbul",
                "phone": "0212 351 55 66",
                "price": "€€€",
                "menu": [("Carne Asada", 380), ("Pollo a la Plancha", 260), ("Costillas de Puerco", 340), ("Arroz con Frijoles", 80), ("Michelada", 120)],
                "reviews": [(4, "Et pişirme ustalıkları çok iyi."), (5, "Carne Asada mükemmeldi.")]
            },
            {
                "name": "La Catrina",
                "description": "Dia de los Muertos temalı dekorasyonu ve zengin Meksika mutfağıyla dikkat çeken mekan.",
                "address": "Galata Mah. No:7, Beyoğlu, İstanbul",
                "phone": "0212 243 99 00",
                "price": "€€",
                "menu": [("Birria Tacos", 200), ("Elote en Vaso", 60), ("Sopas Aztecas", 130), ("Churros con Chocolate", 100), ("Paloma Kokteyli", 160)],
                "reviews": [(5, "Birria çorbası muhteşem!"), (5, "Dekorasyon ve yemek ikisi de harika.")]
            },
            {
                "name": "Oaxaca Kitchen",
                "description": "UNESCO mirası Oaxaca mutfağının gizemli tatlarını sunan özel restoran.",
                "address": "Çukurcuma Mah. No:3, Beyoğlu, İstanbul",
                "phone": "0212 244 22 11",
                "price": "€€€",
                "menu": [("Mole Negro", 350), ("Tlayuda", 220), ("Chapulines (Çekirge Atıştırmalık)", 180), ("Nieve de Leche Quemada", 120), ("Tepache", 80)],
                "reviews": [(5, "Oaxaca mutfağı bu kadar kompleks olabilir mi!"), (4, "Cesur tatlar, denemeye değer.")]
            },
        ]
    },
    "Hint Mutfağı": {
        "restaurants": [
            {
                "name": "Maharaja Palace",
                "description": "Hint saray mutfağının ihtişamını modern İstanbul'da yaşatan lüks restoran.",
                "address": "Abdi İpekçi Cad. No:50, Nişantaşı, İstanbul",
                "phone": "0212 240 55 66",
                "price": "€€€",
                "menu": [("Butter Chicken", 280), ("Lamb Biryani", 320), ("Palak Paneer", 220), ("Garlic Naan", 60), ("Mango Lassi", 90)],
                "reviews": [(5, "Butter chicken enfes, naan ekmekleri inanılmaz."), (5, "İstanbul'daki en iyi Hint restoranı.")]
            },
            {
                "name": "Mumbai Street Kitchen",
                "description": "Mumbai'nin kalabalık sokaklarından ilham alan, canlı ve renkli sokak yemeği mekanı.",
                "address": "Kadıköy Mah. No:22, Kadıköy, İstanbul",
                "phone": "0216 337 88 99",
                "price": "€",
                "menu": [("Vada Pav", 60), ("Pav Bhaji", 90), ("Bhel Puri", 70), ("Masala Chai", 40), ("Gulab Jamun", 65)],
                "reviews": [(4, "Uygun fiyata otantik Hint sokak lezzeti!"), (5, "Masala chai mükemmel.")]
            },
            {
                "name": "Delhi Darbar",
                "description": "Kuzey Hindistan mutfağının tandırlı ekmek ve kebaplarına odaklanan restoran.",
                "address": "Bomonti Mah. No:14, Şişli, İstanbul",
                "phone": "0212 230 44 55",
                "price": "€€",
                "menu": [("Seekh Kebab", 200), ("Dal Makhani", 170), ("Chicken Tikka", 220), ("Tandoori Roti", 45), ("Lassi", 75)],
                "reviews": [(4, "Kebaplar inanılmaz lezzetli."), (5, "Dal makhani ev yapımı gibi.")]
            },
            {
                "name": "Spice Garden",
                "description": "Güney Hindistan'ın baharatlı ve eşsiz tatlarını sunan vejetaryen ağırlıklı restoran.",
                "address": "Moda Mah. No:45, Kadıköy, İstanbul",
                "phone": "0216 419 22 33",
                "price": "€€",
                "menu": [("Masala Dosa", 160), ("Idli Sambar", 120), ("Chole Bhature", 170), ("Rasam", 80), ("Filter Kaapi", 55)],
                "reviews": [(5, "Güney Hindistan mutfağını merak ediyorsanız buraya gelin!"), (4, "Masala dosa çok lezzetli.")]
            },
            {
                "name": "Kolkata Curry House",
                "description": "Bengal mutfağının balık ve tatlılarına adanmış özgün restoran.",
                "address": "Yeldeğirmeni Mah. No:8, Kadıköy, İstanbul",
                "phone": "0216 450 66 77",
                "price": "€€",
                "menu": [("Macher Jhol (Balık Köri)", 210), ("Shorshe Ilish", 280), ("Mishti Doi", 75), ("Rasgulla", 60), ("Darjeeling Çayı", 50)],
                "reviews": [(5, "Bengal balık körisini ilk kez denedim, harika!"), (4, "Tatlılar çok özgün.")]
            },
            {
                "name": "Tandoor Express",
                "description": "Özellikle tandır fırınında pişirilen yemekleriyle öne çıkan hızlı Hint lokantası.",
                "address": "Mecidiyeköy Mah. No:3, Şişli, İstanbul",
                "phone": "0212 267 33 44",
                "price": "€",
                "menu": [("Tandoori Chicken", 180), ("Chicken Tikka Masala", 200), ("Plain Naan", 40), ("Samosa (2 adet)", 70), ("Sweet Lassi", 65)],
                "reviews": [(4, "Hızlı servis ve lezzetli yemek."), (4, "Fiyat performans iyi.")]
            },
            {
                "name": "Rajasthan Haveli",
                "description": "Rajasthan bölgesinin renkli kültürünü ve baharatlı mutfağını İstanbul'a taşıyan restoran.",
                "address": "Nişantaşı Mah. No:18, Şişli, İstanbul",
                "phone": "0212 225 77 88",
                "price": "€€€",
                "menu": [("Dal Baati Churma", 240), ("Laal Maas (Kırmızı Et Köri)", 310), ("Ker Sangri", 190), ("Ghevar", 110), ("Thandai", 85)],
                "reviews": [(5, "Rajasthan mutfağını duymamıştım ama harika!"), (4, "Çok derin ve kompleks tatlar.")]
            },
            {
                "name": "Kerala Backwaters",
                "description": "Kerala kıyı mutfağının hindistan cevizi ve baharat ağırlıklı tariflerini sunan mekan.",
                "address": "Cihangir Mah. No:19, Beyoğlu, İstanbul",
                "phone": "0212 293 11 00",
                "price": "€€",
                "menu": [("Kerala Fish Curry", 220), ("Appam & Stew", 180), ("Prawn Moilee", 250), ("Payasam", 85), ("Coconut Water", 55)],
                "reviews": [(5, "Hindistan cevizi bazlı köriler çok eşsiz."), (4, "Appam ekmeği harikaydı.")]
            },
            {
                "name": "Punjab da Dhaba",
                "description": "Punjab eyaletinin doyurucu ve yağlı Hint yolcu lokantası geleneğini yansıtan mekan.",
                "address": "Kadıköy Çarşısı No:14, Kadıköy, İstanbul",
                "phone": "0216 336 99 00",
                "price": "€",
                "menu": [("Sarson da Saag & Makki di Roti", 150), ("Amritsari Kulcha", 90), ("Rajma Chawal", 130), ("Jalebi", 55), ("Lassi (büyük)", 80)],
                "reviews": [(5, "Punjabi ev yemeği gibi, çok doyurucu."), (3, "Biraz yağlı ama lezzetli.")]
            },
            {
                "name": "Goa Beach Bar & Grill",
                "description": "Goa'nın tropikal havası ve deniz ürünleri ağırlıklı menüsüyle öne çıkan şık mekan.",
                "address": "Ortaköy Mah. No:5, Beşiktaş, İstanbul",
                "phone": "0212 261 44 55",
                "price": "€€€",
                "menu": [("Goan Fish Curry", 280), ("Prawn Balchão", 310), ("Bebinca", 130), ("Feni Kokteyli", 180), ("Coconut Lassi", 90)],
                "reviews": [(4, "Ortaköy'de harika bir atmosfer."), (5, "Balık körisi enfes!")]
            },
        ]
    },
    "Çin Mutfağı": {
        "restaurants": [
            {
                "name": "Dragon Palace",
                "description": "Kanton mutfağının en seçkin örneklerini sunan, geleneksel Çin dekorasyonlu restoran.",
                "address": "Levent Mah. No:20, Beşiktaş, İstanbul",
                "phone": "0212 282 33 44",
                "price": "€€€",
                "menu": [("Pekin Ördeği", 420), ("Dim Sum Tabağı", 220), ("Kung Pao Chicken", 240), ("Hot and Sour Soup", 100), ("Jasmine Çayı", 60)],
                "reviews": [(5, "Pekin ördeği için İstanbul'da en iyi adres!"), (4, "Dim sumlar çok lezzetli.")]
            },
            {
                "name": "Sichuan Spice",
                "description": "Sichuanlı usta şefin biber ve baharat ağırlıklı Sichuan mutfağı yorumu.",
                "address": "Bomonti Mah. No:8, Şişli, İstanbul",
                "phone": "0212 219 55 66",
                "price": "€€",
                "menu": [("Mapo Tofu", 180), ("Sichuan Hot Pot (kişi başı)", 250), ("Dan Dan Noodles", 160), ("Scallion Pancake", 90), ("Baijiu Shot", 100)],
                "reviews": [(5, "Acı sevenler için cennet!"), (4, "Sichuan hot pot çok eğlenceli.")]
            },
            {
                "name": "Shanghai Garden",
                "description": "Şangay mutfağının hafif, tatlımsı ve rafine lezzetlerini öne çıkaran modern restoran.",
                "address": "Nişantaşı Mah. No:62, Şişli, İstanbul",
                "phone": "0212 224 77 88",
                "price": "€€€",
                "menu": [("Xiaolongbao (8 adet)", 190), ("Shanghai Braised Pork Belly", 280), ("Smoked Fish", 200), ("Red Bean Pastry", 80), ("Longjing Çayı", 70)],
                "reviews": [(5, "Xiaolongbao hayatımın en iyisi!"), (5, "Her şey çok özenle hazırlanmış.")]
            },
            {
                "name": "Beijing Noodle House",
                "description": "El yapımı noodle ve Pekin usulü yemeklerin ustası.",
                "address": "Kadıköy Mah. No:55, Kadıköy, İstanbul",
                "phone": "0216 338 11 22",
                "price": "€",
                "menu": [("Zha Jiang Mian", 130), ("Hand-Pulled Noodles", 140), ("Wonton Soup", 120), ("Char Siu Bao", 80), ("Bubble Tea", 70)],
                "reviews": [(4, "El yapımı noodleların farkı var."), (5, "Çok uygun fiyat, çok lezzetli.")]
            },
            {
                "name": "Dim Sum Heaven",
                "description": "Yalnızca dim sum ve Kanton içli böreklerine odaklanan uzman restoran.",
                "address": "Cihangir Mah. No:30, Beyoğlu, İstanbul",
                "phone": "0212 292 44 55",
                "price": "€€",
                "menu": [("Har Gow (4 adet)", 130), ("Siu Mai (4 adet)", 120), ("Char Siu Bao (3 adet)", 110), ("Egg Tart", 70), ("Pu-erh Çayı", 55)],
                "reviews": [(5, "Dim sum tutkunu iseniz buraya gelin!"), (4, "Her hafta sonu gidiyorum.")]
            },
            {
                "name": "Canton Street",
                "description": "Hong Kong ilhamıyla hazırlanan Kanton usulü yemekler ve char siu.",
                "address": "Bağdat Cad. No:144, Kadıköy, İstanbul",
                "phone": "0216 360 88 99",
                "price": "€€",
                "menu": [("Char Siu (Barbekü Domuz)", 220), ("Wonton Noodle Soup", 160), ("Fried Rice", 140), ("Mango Pudding", 85), ("Hong Kong Milk Tea", 65)],
                "reviews": [(4, "Hong Kong tarzı milk tea muhteşem."), (5, "Char siu buradaki kadar iyi hiçbir yerde yayimedim.")]
            },
            {
                "name": "Yunnan Kitchen",
                "description": "Çin'in en az bilinen ama en eşsiz bölgesi Yunnan'ın mutfağını sunan keşif restoranı.",
                "address": "Yeldeğirmeni Mah. No:17, Kadıköy, İstanbul",
                "phone": "0216 449 66 77",
                "price": "€€",
                "menu": [("Crossing the Bridge Noodles", 190), ("Steam Pot Chicken", 260), ("Wild Mushroom Stir Fry", 180), ("Rose Cake", 85), ("Pu-erh Çayı", 60)],
                "reviews": [(5, "Yunnan mutfağını ilk kez tattım ve büyülendim."), (4, "Çok farklı ve özgün tatlar.")]
            },
            {
                "name": "Peking Duck House",
                "description": "Yalnızca Pekin ördeği ve eşlikçi yemeklerine odaklanan tek ürün restoranı.",
                "address": "Etiler Mah. No:5, Beşiktaş, İstanbul",
                "phone": "0212 351 22 33",
                "price": "€€€",
                "menu": [("Pekin Ördeği (yarım)", 380), ("Pekin Ördeği (tam)", 680), ("Duck Bone Soup", 120), ("Pancake & Sauce Set", 80), ("Shaoxing Wine", 140)],
                "reviews": [(5, "Tek bir yemek için gidilir, değer!"), (4, "Ördek çok iyi hazırlanmış.")]
            },
            {
                "name": "Chengdu Hot Pot",
                "description": "Sichuan usulü ateşli hot pot kültürünü ailece deneyimlemenizi sağlayan büyük mekan.",
                "address": "Mecidiyeköy Mah. No:18, Şişli, İstanbul",
                "phone": "0212 275 55 66",
                "price": "€€",
                "menu": [("Hot Pot Kişi Başı (malzemeler dahil)", 280), ("Extra Tahini Sos", 30), ("Wagyu Dilim (100g)", 180), ("Frozen Tofu", 60), ("Sour Plum Drink", 55)],
                "reviews": [(5, "Kış aylarının vazgeçilmezi!"), (4, "Gruplarla gitmek çok eğlenceli.")]
            },
            {
                "name": "Hakka Fusion",
                "description": "Hint-Çin Hakka mutfağını modern yorumla sunan benzersiz fusion restoran.",
                "address": "Galata Mah. No:12, Beyoğlu, İstanbul",
                "phone": "0212 244 88 77",
                "price": "€€",
                "menu": [("Hakka Noodles", 170), ("Chilli Chicken", 200), ("Manchurian", 190), ("Spring Roll", 100), ("Lychee Juice", 60)],
                "reviews": [(5, "Hint-Çin mutfağı eşsiz bir kombinasyon!"), (4, "Chilli chicken çok lezzetli.")]
            },
        ]
    },
    "Fransız Mutfağı": {
        "restaurants": [
            {
                "name": "Café de Paris",
                "description": "Otantik Paris bistro atmosferinde klasik Fransız mutfağının en seçkin örnekleri.",
                "address": "Teşvikiye Cad. No:70, Nişantaşı, İstanbul",
                "phone": "0212 219 66 77",
                "price": "€€€",
                "menu": [("Steak Frites", 420), ("Soupe à l'Oignon", 140), ("Crème Brûlée", 160), ("Croissant", 55), ("Bordeaux Rouge", 280)],
                "reviews": [(5, "Paris'te olmak gibi hissettim!"), (5, "Steak mükemmel pişirilmiş.")]
            },
            {
                "name": "Le Petit Bistro",
                "description": "Küçük ve samimi ortamıyla Fransız taşra mutfağını yansıtan mahalle lokantası.",
                "address": "Cihangir Mah. No:6, Beyoğlu, İstanbul",
                "phone": "0212 251 33 44",
                "price": "€€",
                "menu": [("Boeuf Bourguignon", 320), ("Ratatouille", 190), ("Tarte Tatin", 130), ("French Onion Soup", 120), ("Côtes du Rhône", 200)],
                "reviews": [(5, "Boeuf Bourguignon enfes!"), (4, "Samimi ve sıcak atmosfer.")]
            },
            {
                "name": "Boulangerie Istanbul",
                "description": "Fransız unlu mamulleri ve pastacılığına adanmış butik fırın ve kafe.",
                "address": "Nişantaşı Mah. No:8, Şişli, İstanbul",
                "phone": "0212 231 99 00",
                "price": "€",
                "menu": [("Croissant au Beurre", 55), ("Pain au Chocolat", 60), ("Quiche Lorraine", 110), ("Éclair", 75), ("Café au Lait", 65)],
                "reviews": [(5, "Sabah kahvaltısı için en iyi adres!"), (5, "Croissant gerçekten Paris'ten gelmiş gibi.")]
            },
            {
                "name": "Provence Restaurant",
                "description": "Güney Fransa'nın Akdeniz tatlarını ve zeytinyağı kültürünü yansıtan restoran.",
                "address": "Ortaköy Mah. No:15, Beşiktaş, İstanbul",
                "phone": "0212 260 22 33",
                "price": "€€€",
                "menu": [("Bouillabaisse", 380), ("Salade Niçoise", 180), ("Tapenade & Ekmek", 100), ("Lavanta Dondurma", 110), ("Rosé de Provence", 220)],
                "reviews": [(5, "Bouillabaisse inanılmaz derin bir tat!"), (4, "Yaz akşamları için ideal.")]
            },
            {
                "name": "Lyon Bouchon",
                "description": "Lyon usulü geleneksel bouchon lokantası, offal severlerin vazgeçilmezi.",
                "address": "Galata Mah. No:19, Beyoğlu, İstanbul",
                "phone": "0212 250 55 66",
                "price": "€€",
                "menu": [("Quenelles de Brochet", 280), ("Tablier de Sapeur", 260), ("Salade Lyonnaise", 160), ("Tarte à la Praline", 120), ("Beaujolais", 180)],
                "reviews": [(4, "Lyon mutfağı çok cesur ve özgün."), (5, "Gerçek Fransız lezzetleri.")]
            },
            {
                "name": "Alsace Winstub",
                "description": "Alsace bölgesinin Alman-Fransız karışımı mutfağından ilham alan mekan.",
                "address": "Bağdat Cad. No:88, Kadıköy, İstanbul",
                "phone": "0216 356 44 55",
                "price": "€€",
                "menu": [("Choucroute Garnie", 290), ("Tarte Flambée", 200), ("Baeckeoffe", 310), ("Kougelhopf", 100), ("Alsace Riesling", 190)],
                "reviews": [(5, "Choucroute garnie kış aylarının en iyi yemeği!"), (4, "Farklı ve özgün Fransız mutfağı.")]
            },
            {
                "name": "Maison Bretagne",
                "description": "Brittany bölgesinin deniz ürünleri ve krepler üzerine uzmanlaşan mekan.",
                "address": "Moda Mah. No:12, Kadıköy, İstanbul",
                "phone": "0216 418 88 99",
                "price": "€€",
                "menu": [("Galette Complète", 160), ("Crêpe Suzette", 130), ("Moules Marinières", 240), ("Far Breton", 95), ("Cidre Breton", 100)],
                "reviews": [(5, "Galette complète çok lezzetli!"), (4, "Krep çeşitleri harika.")]
            },
            {
                "name": "Burgundy Table",
                "description": "Burgundy şarap bölgesinin mutfağını ve şarap kültürünü buluşturan gastronomi mekanı.",
                "address": "Etiler Mah. No:33, Beşiktaş, İstanbul",
                "phone": "0212 352 11 22",
                "price": "€€€",
                "menu": [("Escargots de Bourgogne", 280), ("Coq au Vin", 360), ("Gougères", 120), ("Époisses Peyniri", 180), ("Pinot Noir de Bourgogne", 400)],
                "reviews": [(5, "Şarap listesi ve yemekler mükemmel uyum içinde."), (5, "Coq au vin inanılmaz lezzetli.")]
            },
            {
                "name": "Brasserie du Marais",
                "description": "Paris'in Marais semtinden ilham alan, canlı ve modern brasserie.",
                "address": "Bebek Mah. No:7, Beşiktaş, İstanbul",
                "phone": "0212 265 33 44",
                "price": "€€€",
                "menu": [("Steak Tartare", 320), ("Moules-Frites", 280), ("Vichyssoise", 130), ("Profiteroles", 140), ("Kir Royal", 160)],
                "reviews": [(4, "Steak tartare çok iyi hazırlanmış."), (5, "Bebek'te Paris brasserie havası.")]
            },
            {
                "name": "Normandie Kitchen",
                "description": "Normandiya'nın elma, krema ve deniz ürünlerine dayalı zengin mutfağından ilham alan restoran.",
                "address": "Arnavutköy Mah. No:4, Beşiktaş, İstanbul",
                "phone": "0212 265 77 88",
                "price": "€€",
                "menu": [("Sole Meunière", 340), ("Poulet Vallée d'Auge", 300), ("Camembert Fırında", 150), ("Tarte Normande", 120), ("Calvados", 130)],
                "reviews": [(5, "Sole meunière hayatımın en iyi balığıydı."), (4, "Normandiya mutfağı gerçekten zengin.")]
            },
        ]
    },
    "Amerikan Mutfağı": {
        "restaurants": [
            {
                "name": "Brooklyn Burger Co.",
                "description": "El yapımı burger ve İstanbul'a özgü malzemelerle hazırlanan Amerikan klasikleri.",
                "address": "Kadıköy Mah. No:34, Kadıköy, İstanbul",
                "phone": "0216 347 55 66",
                "price": "€€",
                "menu": [("Brooklyn Smash Burger", 220), ("BBQ Bacon Burger", 240), ("Crispy Chicken Sandwich", 200), ("Loaded Fries", 110), ("Milkshake", 120)],
                "reviews": [(5, "En iyi burger İstanbul'da burada!"), (5, "Smash burger tekniği mükemmel.")]
            },
            {
                "name": "Texas BBQ House",
                "description": "Texas usulü tütsülenmiş et ve barbekü kültürünü İstanbul'a taşıyan mekan.",
                "address": "Levent Mah. No:44, Beşiktaş, İstanbul",
                "phone": "0212 281 88 99",
                "price": "€€€",
                "menu": [("Beef Brisket (200g)", 350), ("Baby Back Ribs (yarım)", 420), ("Pulled Pork Sandwich", 240), ("Mac & Cheese", 130), ("Sweet Tea", 55)],
                "reviews": [(5, "Beef brisket 12 saat tütsülenmiş, inanılmaz!"), (4, "Gerçek Texas barbekü deneyimi.")]
            },
            {
                "name": "New York Deli",
                "description": "NYC deli kültürünü yansıtan, dev sandviçler ve pastrami ile ünlü mekan.",
                "address": "Nişantaşı Mah. No:25, Şişli, İstanbul",
                "phone": "0212 225 44 55",
                "price": "€€",
                "menu": [("Pastrami on Rye", 210), ("Reuben Sandwich", 220), ("NY Cheesecake", 130), ("Matzo Ball Soup", 110), ("Dr. Brown's Soda", 60)],
                "reviews": [(5, "New York sandviçlerini özleyenler için!"), (4, "Pastrami çok kaliteli.")]
            },
            {
                "name": "Nashville Hot Chicken",
                "description": "Nashville'in meşhur acılı tavuk kültürünü özgün tarifle sunan mekan.",
                "address": "Bomonti Mah. No:31, Şişli, İstanbul",
                "phone": "0212 296 11 22",
                "price": "€",
                "menu": [("Nashville Hot Chicken Sandwich", 170), ("Chicken Tenders (3 adet)", 160), ("Coleslaw", 60), ("Cornbread", 55), ("Arnold Palmer", 65)],
                "reviews": [(4, "Çok acılı ama çok lezzetli!"), (5, "Nashville usulü tavuk burada en iyi.")]
            },
            {
                "name": "Chicago Deep Dish",
                "description": "Chicago'nun meşhur derin tabak pizzasını orijinal tarifiyle yapan restoran.",
                "address": "Bağdat Cad. No:55, Kadıköy, İstanbul",
                "phone": "0216 362 33 44",
                "price": "€€",
                "menu": [("Deep Dish Pizza (kişisel)", 230), ("Chicago Style Hot Dog", 110), ("Italian Beef Sandwich", 190), ("Cheesecake", 120), ("Coca-Cola", 40)],
                "reviews": [(5, "Deep dish pizza çok farklı ve lezzetli!"), (4, "Chicago hot dog da çok güzeldi.")]
            },
            {
                "name": "Southern Comfort Kitchen",
                "description": "ABD'nin güneyinin doyurucu comfort food kültürünü yansıtan sıcak mekan.",
                "address": "Moda Mah. No:7, Kadıköy, İstanbul",
                "phone": "0216 418 55 66",
                "price": "€€",
                "menu": [("Shrimp & Grits", 260), ("Chicken & Waffles", 220), ("Jambalaya", 240), ("Biscuits & Gravy", 150), ("Sweet Potato Pie", 110)],
                "reviews": [(5, "Chicken & Waffles kombinasyonu muhteşem!"), (4, "Güney yemekleri çok doyurucu.")]
            },
            {
                "name": "All-American Diner",
                "description": "1950'ler Amerika'sından ilham alan klasik diner kültürü ve menüsü.",
                "address": "Etiler Mah. No:15, Beşiktaş, İstanbul",
                "phone": "0212 351 77 88",
                "price": "€",
                "menu": [("Classic Cheeseburger", 160), ("Pancakes & Maple Syrup", 130), ("All-Day Breakfast", 170), ("Apple Pie", 90), ("Vanilla Milkshake", 100)],
                "reviews": [(4, "Nostaljik diner atmosferi çok güzel."), (5, "Pancakes inanılmaz kabarık!")]
            },
            {
                "name": "Philly's Best",
                "description": "Philadelphia Cheesesteak ve Doğu Yakası Amerikan mutfağına odaklanan restoran.",
                "address": "Kadıköy Çarşısı No:19, Kadıköy, İstanbul",
                "phone": "0216 337 22 33",
                "price": "€",
                "menu": [("Philly Cheesesteak", 190), ("Hoagie Sandwich", 170), ("Soft Pretzel", 70), ("Tomato Pie", 140), ("Root Beer", 55)],
                "reviews": [(5, "Philly cheesesteak mükemmel!"), (4, "Etin kalitesi çok iyi.")]
            },
            {
                "name": "Kansas City Smokehouse",
                "description": "Kansas City usulü tatlı barbekü sosuyla ünlü, gerçek smokehouse deneyimi.",
                "address": "Bostancı Mah. No:8, Kadıköy, İstanbul",
                "phone": "0216 463 44 55",
                "price": "€€€",
                "menu": [("St. Louis Ribs (tam)", 680), ("Burnt Ends", 320), ("Smoked Turkey", 280), ("BBQ Beans", 80), ("Corn on the Cob", 60)],
                "reviews": [(5, "Burnt ends hayatımın en iyi barbekü lokması!"), (5, "Gerçek smokehouse ustası bu.")]
            },
            {
                "name": "San Francisco Brunch Club",
                "description": "California usulü sağlıklı ve taze malzemeli brunch mekanı.",
                "address": "Bebek Mah. No:22, Beşiktaş, İstanbul",
                "phone": "0212 265 99 00",
                "price": "€€",
                "menu": [("Avocado Toast & Poached Egg", 170), ("Eggs Benedict", 180), ("Acai Bowl", 150), ("Cold Brew Coffee", 80), ("Mimosa", 140)],
                "reviews": [(4, "Hafta sonu brunch için harika bir mekan."), (5, "Avocado toast çok tazeydi.")]
            },
        ]
    },
    "Yunan Mutfağı": {
        "restaurants": [
            {
                "name": "Athena Taverna",
                "description": "Atina'nın geleneksel meyhane kültüründen ilham alan deniz ürünleri ve meze restoranı.",
                "address": "Arnavutköy Mah. No:10, Beşiktaş, İstanbul",
                "phone": "0212 263 44 55",
                "price": "€€",
                "menu": [("Spanakopita", 110), ("Grilled Octopus", 280), ("Moussaka", 200), ("Baklava", 90), ("Ouzo", 100)],
                "reviews": [(5, "Ahtapot ızgara nefisti!"), (4, "Akdeniz atmosferi tam burada.")]
            },
            {
                "name": "Oia Sunset Grill",
                "description": "Santorini'nin mavi-beyaz estetiğinden ilham alan, deniz manzaralı Yunan restoranı.",
                "address": "Bebek Mah. No:14, Beşiktaş, İstanbul",
                "phone": "0212 263 77 88",
                "price": "€€€",
                "menu": [("Grilled Sea Bass", 380), ("Saganaki", 160), ("Greek Salad", 130), ("Tzatziki & Pita", 90), ("Assyrtiko Wine", 220)],
                "reviews": [(5, "Manzara ve yemek ikisi de harika."), (4, "Saganaki enfes!")]
            },
            {
                "name": "Thessaloniki Grill",
                "description": "Kuzey Yunanistan'ın kebap ve ızgara kültürünü yansıtan samimi mekan.",
                "address": "Kadıköy Mah. No:66, Kadıköy, İstanbul",
                "phone": "0216 338 33 44",
                "price": "€",
                "menu": [("Souvlaki (3 şiş)", 130), ("Gyros Sandwich", 110), ("Pita Bread", 30), ("Horiatiki Salata", 100), ("Frappe", 50)],
                "reviews": [(4, "Uygun fiyatlı, lezzetli gyros."), (5, "Souvlaki çok güzeldi.")]
            },
            {
                "name": "Crete Kitchen",
                "description": "Girit adasının zengin ve sağlıklı Akdeniz mutfağına adanmış butik restoran.",
                "address": "Cihangir Mah. No:25, Beyoğlu, İstanbul",
                "phone": "0212 252 55 66",
                "price": "€€",
                "menu": [("Dakos", 120), ("Lamb Stifado", 260), ("Cretan Dakos Rusk Salad", 130), ("Loukoumades", 80), ("Raki", 90)],
                "reviews": [(5, "Girit mutfağı çok sağlıklı ve lezzetli!"), (4, "Loukoumades tatlı mükemmel.")]
            },
            {
                "name": "Meze Bar Hellas",
                "description": "Onlarca farklı meze çeşidiyle tam bir Yunan meyhane deneyimi.",
                "address": "Ortaköy Mah. No:20, Beşiktaş, İstanbul",
                "phone": "0212 261 11 22",
                "price": "€€",
                "menu": [("Mezze Tabağı (10 çeşit)", 280), ("Dolmades", 90), ("Taramasalata", 80), ("Feta & Zeytin Tabağı", 110), ("Retsina", 140)],
                "reviews": [(5, "Meze çeşitliliği inanılmaz!"), (4, "Ortaköy'de güzel akşam.")]
            },
            {
                "name": "Mykonos Fish Tavern",
                "description": "Mykonos balıkçı köyünden ilham alan, taze balık ve deniz ürünleri uzmanı.",
                "address": "Yeniköy Mah. No:3, Sarıyer, İstanbul",
                "phone": "0212 262 88 99",
                "price": "€€€",
                "menu": [("Taze Balık Izgara (günlük)", 350), ("Garides Saganaki", 260), ("Kalamari Tava", 200), ("Greek Salad", 130), ("White Wine", 160)],
                "reviews": [(5, "Boğaz manzarasında taze balık, mükemmel!"), (5, "Her şey çok tazeydi.")]
            },
            {
                "name": "Parthenon Souvlaki",
                "description": "Fast food hızıyla geleneksel souvlaki ve gyros sunan pratik Yunan lokantası.",
                "address": "Beşiktaş Mah. No:5, Beşiktaş, İstanbul",
                "phone": "0212 259 44 55",
                "price": "€",
                "menu": [("Gyros Pita", 100), ("Chicken Souvlaki", 95), ("Pork Souvlaki", 100), ("Tzatziki", 40), ("Mythos Bira", 80)],
                "reviews": [(4, "Hızlı ve lezzetli."), (5, "En iyi gyros burada!")]
            },
            {
                "name": "Corfu Garden",
                "description": "Korfu adasının İtalyan-Yunan füzyon mutfağını sunan özgün mekan.",
                "address": "Moda Mah. No:19, Kadıköy, İstanbul",
                "phone": "0216 418 33 44",
                "price": "€€",
                "menu": [("Pastitsada", 250), ("Sofrito", 270), ("Bianco Fish", 290), ("Mandolato", 95), ("Ginger Beer Mocktail", 70)],
                "reviews": [(5, "Korfu mutfağı çok farklı ve eşsiz!"), (4, "İtalyan-Yunan karışımı harika.")]
            },
            {
                "name": "Zorba's Kitchen",
                "description": "Samimi ve aile sıcaklığında otantik Yunan ev yemekleri.",
                "address": "Yeldeğirmeni Mah. No:21, Kadıköy, İstanbul",
                "phone": "0216 449 55 66",
                "price": "€",
                "menu": [("Pastitsio", 150), ("Gemista (Dolmalık Sebze)", 140), ("Greek Bean Soup", 90), ("Galaktoboureko", 95), ("Greek Coffee", 40)],
                "reviews": [(5, "Yunan ev yemeği tadında, çok doyurucu."), (4, "Fiyat çok uygun.")]
            },
            {
                "name": "Rhodes Seafood",
                "description": "Rodos adasının deniz ürünleri geleneğini ve Akdeniz lezzetlerini sunan balıkçı restoranı.",
                "address": "Sarıyer Mah. No:9, Sarıyer, İstanbul",
                "phone": "0212 242 22 33",
                "price": "€€€",
                "menu": [("Stuffed Squid", 280), ("Shrimp Pilaf", 240), ("Rhodes Salata", 130), ("Loukoumades", 85), ("Muscat Wine", 190)],
                "reviews": [(4, "Sarıyer'de harika Yunan balıkçı restoranı."), (5, "Midye dolma inanılmaz lezzetliydi.")]
            },
        ]
    },
    "Tayland Mutfağı": {
        "restaurants": [
            {
                "name": "Bangkok Street",
                "description": "Bangkok sokak yemeklerinin canlı ve renkli dünyasını İstanbul'a taşıyan mekan.",
                "address": "Kadıköy Mah. No:88, Kadıköy, İstanbul",
                "phone": "0216 337 66 77",
                "price": "€",
                "menu": [("Pad Thai (Chicken)", 150), ("Som Tum", 120), ("Satay (4 şiş)", 140), ("Mango Sticky Rice", 90), ("Thai Iced Tea", 60)],
                "reviews": [(5, "Pad Thai inanılmaz lezzetli!"), (4, "Uygun fiyata otantik Tayland yemeği.")]
            },
            {
                "name": "Chiang Mai Kitchen",
                "description": "Kuzey Tayland'ın dağ mutfağını ve özgün Chiang Mai tariflerini sunan butik restoran.",
                "address": "Cihangir Mah. No:33, Beyoğlu, İstanbul",
                "phone": "0212 251 11 22",
                "price": "€€",
                "menu": [("Khao Soi (Hindistancevizi Köri Çorbası)", 190), ("Sai Ua (Kuzey Tayland Sosisi)", 170), ("Nam Prik Ong", 140), ("Sticky Rice", 50), ("Singha Bira", 90)],
                "reviews": [(5, "Khao Soi hayatımın en iyi çorbası!"), (5, "Chiang Mai mutfağını merak edenler için şart.")]
            },
            {
                "name": "Phuket Seafood Bar",
                "description": "Phuket'in tropik deniz ürünleri kültürünü Boğaz kıyısında sunan restoran.",
                "address": "Ortaköy Mah. No:8, Beşiktaş, İstanbul",
                "phone": "0212 261 55 66",
                "price": "€€€",
                "menu": [("Grilled Tiger Prawn", 380), ("Thai Green Curry with Crab", 320), ("Tom Yum Talay", 220), ("Coconut Ice Cream", 90), ("Lychee Mojito", 150)],
                "reviews": [(5, "Karides çok tazeydi!"), (4, "Tayland deniz ürünleri için en iyi adres.")]
            },
            {
                "name": "Thai Orchid",
                "description": "Şık dekorasyonu ve rafine Tayland mutfağıyla üst segment bir Tayland deneyimi.",
                "address": "Nişantaşı Mah. No:33, Şişli, İstanbul",
                "phone": "0212 225 55 66",
                "price": "€€€",
                "menu": [("Massaman Lamb Curry", 320), ("Tom Kha Gai", 180), ("Miang Kham", 160), ("Tub Tim Grob", 110), ("Butterfly Pea Latte", 85)],
                "reviews": [(5, "Massaman köri inanılmaz!"), (4, "Sunum çok zarif.")]
            },
            {
                "name": "Isaan Grill",
                "description": "Kuzeydoğu Tayland Isaan bölgesinin ızgara ve fermente lezzetlerine adanmış özgün mekan.",
                "address": "Yeldeğirmeni Mah. No:25, Kadıköy, İstanbul",
                "phone": "0216 449 88 99",
                "price": "€€",
                "menu": [("Gai Yang (Izg. Tavuk)", 190), ("Larb Moo", 160), ("Som Tum Thai", 130), ("Khao Niao (Sticky Rice)", 40), ("Chang Bira", 85)],
                "reviews": [(5, "Isaan mutfağını ilk kez denedim, harika!"), (4, "Larb çok aromatik ve lezzetli.")]
            },
            {
                "name": "Ayutthaya Noodle House",
                "description": "Tayland'ın tarihi başkenti Ayutthaya'nın erişte kültüründen ilham alan noodle restoranı.",
                "address": "Bomonti Mah. No:19, Şişli, İstanbul",
                "phone": "0212 224 22 33",
                "price": "€",
                "menu": [("Boat Noodles", 140), ("Pad See Ew", 150), ("Rad Na", 155), ("Thai Fish Cake (4 adet)", 110), ("Nam Manao (Limon Suyu)", 40)],
                "reviews": [(4, "Boat noodles çok farklı bir deneyim."), (5, "Pad See Ew mükemmel!")]
            },
            {
                "name": "Koh Samui Beach Bar",
                "description": "Koh Samui plaj barlarından ilham alan, tropik kokteyl ve hafif Tayland yemekleri.",
                "address": "Bebek Mah. No:18, Beşiktaş, İstanbul",
                "phone": "0212 265 55 66",
                "price": "€€",
                "menu": [("Green Papaya Salad", 130), ("Crying Tiger Steak", 280), ("Fresh Spring Rolls", 120), ("Mango Sorbet", 85), ("Thai Mojito", 150)],
                "reviews": [(4, "Bebek'te tropikal atmosfer çok keyifli."), (5, "Crying tiger steak çok lezzetli.")]
            },
            {
                "name": "Floating Market Kitchen",
                "description": "Tayland yüzen pazarı temasıyla hazırlanmış, renkli ve eğlenceli bir yemek deneyimi.",
                "address": "Galata Mah. No:22, Beyoğlu, İstanbul",
                "phone": "0212 244 66 77",
                "price": "€€",
                "menu": [("Pad Krapow Moo", 170), ("Gaeng Daeng (Kırmızı Köri)", 200), ("Khanom Buang (Tayland Krep)", 80), ("Nam Jim Seafood", 50), ("Cha Yen", 55)],
                "reviews": [(5, "Pad Krapow mükemmel!"), (4, "Dekorasyon çok eğlenceli.")]
            },
            {
                "name": "Sukhothai Spa & Dine",
                "description": "Sukhothai döneminin saray mutfağından ilham alan, huzurlu ve zarif restoran.",
                "address": "Etiler Mah. No:41, Beşiktaş, İstanbul",
                "phone": "0212 352 33 44",
                "price": "€€€",
                "menu": [("Royal Pad Thai", 240), ("Tod Man Pla", 180), ("Kaeng Kari Gai", 260), ("Kluai Buat Chi (Muz Tatlısı)", 100), ("Pandan Latte", 80)],
                "reviews": [(5, "Huzurlu atmosfer ve harika yemekler."), (4, "Tayland saray mutfağı çok sofistike.")]
            },
            {
                "name": "Thai Express",
                "description": "Hızlı ve lezzetli Tayland yemekleri için uygun fiyatlı express lokanta.",
                "address": "Mecidiyeköy Mah. No:25, Şişli, İstanbul",
                "phone": "0212 267 77 88",
                "price": "€",
                "menu": [("Pad Thai Express", 120), ("Green Curry Bowl", 130), ("Thai Fried Rice", 110), ("Spring Roll (2 adet)", 70), ("Coconut Water", 45)],
                "reviews": [(4, "Hızlı öğle yemeği için ideal."), (3, "Standart ama lezzetli.")]
            },
        ]
    },
}

created_count = 0
for cuisine_name, cuisine_data in data.items():
    category = Category.objects.create(name=cuisine_name)
    print(f"[+] Kategori: {cuisine_name}")
    for r in cuisine_data["restaurants"]:
        restaurant = Restaurant.objects.create(
            name=r["name"],
            description=r["description"],
            address=r["address"],
            phone=r["phone"],
            price_range=r["price"],
            category=category,
        )
        for item_name, item_price in r["menu"]:
            MenuItem.objects.create(name=item_name, price=item_price, restaurant=restaurant)
        for stars, comment in r["reviews"]:
            Review.objects.create(stars=stars, comment=comment, restaurant=restaurant)
        created_count += 1

print(f"\nToplam {created_count} restoran olusturuldu!")
print(f"Kategoriler: {Category.objects.count()}")
print(f"Menu Ogesi: {MenuItem.objects.count()}")
print(f"Yorum: {Review.objects.count()}")
