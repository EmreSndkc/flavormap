// FlavorMap – Final Report Generator
// Produces a .docx with placeholders the user will fill in.
const fs = require('fs');
const path = require('path');

const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, PageOrientation, LevelFormat, ExternalHyperlink,
  TabStopType, TabStopPosition, HeadingLevel, BorderStyle, WidthType, ShadingType,
  PageNumber, PageBreak
} = require('docx');

// -------- helpers --------
const border = { style: BorderStyle.SINGLE, size: 4, color: "BFBFBF" };
const borders = { top: border, bottom: border, left: border, right: border };
const cellMargins = { top: 80, bottom: 80, left: 120, right: 120 };

const P = (text, opts = {}) => new Paragraph({
  spacing: { after: 120 },
  ...opts,
  children: [new TextRun({ text, ...(opts.run || {}) })],
});

const PMulti = (runs, opts = {}) => new Paragraph({
  spacing: { after: 120 },
  ...opts,
  children: runs,
});

const PLACEHOLDER = (label) => new TextRun({
  text: `[${label}]`,
  italics: true,
  color: "B00020",
  highlight: "yellow",
});

const heading = (text, level = HeadingLevel.HEADING_1) => new Paragraph({
  heading: level,
  spacing: { before: 200, after: 120 },
  children: [new TextRun({ text })],
});

const bullet = (text) => new Paragraph({
  numbering: { reference: "bullets", level: 0 },
  spacing: { after: 80 },
  children: [new TextRun(text)],
});

const bulletRuns = (runs) => new Paragraph({
  numbering: { reference: "bullets", level: 0 },
  spacing: { after: 80 },
  children: runs,
});

// Build a table from rows; first row is header
function makeTable(columnWidths, headerCells, dataRows) {
  const totalWidth = columnWidths.reduce((a, b) => a + b, 0);
  const headerRow = new TableRow({
    tableHeader: true,
    children: headerCells.map((text, i) => new TableCell({
      borders, margins: cellMargins,
      width: { size: columnWidths[i], type: WidthType.DXA },
      shading: { fill: "1F3A5F", type: ShadingType.CLEAR },
      children: [new Paragraph({ children: [new TextRun({ text, bold: true, color: "FFFFFF" })] })],
    })),
  });
  const dataRowsObjs = dataRows.map((row, idx) => new TableRow({
    children: row.map((cell, i) => new TableCell({
      borders, margins: cellMargins,
      width: { size: columnWidths[i], type: WidthType.DXA },
      shading: idx % 2 === 1 ? { fill: "F4F6F8", type: ShadingType.CLEAR } : undefined,
      children: Array.isArray(cell) ? cell : [new Paragraph({ children: [new TextRun(String(cell))] })],
    })),
  }));
  return new Table({
    width: { size: totalWidth, type: WidthType.DXA },
    columnWidths,
    rows: [headerRow, ...dataRowsObjs],
  });
}

function placeholderBox(label, heightHint = "≈ 9 cm × 14 cm") {
  // A bordered, single-cell table acting as a screenshot placeholder.
  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [9360],
    rows: [new TableRow({
      children: [new TableCell({
        borders: {
          top: { style: BorderStyle.DASHED, size: 8, color: "888888" },
          bottom: { style: BorderStyle.DASHED, size: 8, color: "888888" },
          left: { style: BorderStyle.DASHED, size: 8, color: "888888" },
          right: { style: BorderStyle.DASHED, size: 8, color: "888888" },
        },
        margins: { top: 600, bottom: 600, left: 200, right: 200 },
        width: { size: 9360, type: WidthType.DXA },
        shading: { fill: "FAFAFA", type: ShadingType.CLEAR },
        children: [
          new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [new TextRun({ text: `[ EKRAN GÖRÜNTÜSÜ: ${label} ]`, bold: true, color: "666666" })],
          }),
          new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [new TextRun({ text: heightHint, italics: true, color: "888888", size: 18 })],
          }),
        ],
      })],
    })],
  });
}

// -------- sections --------
// ========== PAGE 1: COVER ==========
const cover = [
  new Paragraph({ spacing: { before: 1200 }, children: [new TextRun("")] }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 120 },
    children: [new TextRun({ text: "ACIBADEM ÜNİVERSİTESİ", bold: true, size: 32, color: "1F3A5F" })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 600 },
    children: [new TextRun({ text: "CSE 220 – Web Programming", size: 26, color: "555555" })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 240 },
    children: [new TextRun({ text: "FlavorMap", bold: true, size: 72, color: "D35400" })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 120 },
    children: [new TextRun({ text: "Restaurant Review & Discovery Platform", italics: true, size: 28, color: "555555" })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 800 },
    children: [new TextRun({ text: "Discover • Review • Share", size: 22, color: "888888" })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 120 },
    children: [new TextRun({ text: "FINAL REPORT", bold: true, size: 28 })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 480 },
    children: [new TextRun({ text: "Spring 2026", size: 24 })],
  }),

  heading("Group Members", HeadingLevel.HEADING_2),
  bulletRuns([new TextRun("Member 1: "), PLACEHOLDER("Ad Soyad – Öğrenci No")]),
  bulletRuns([new TextRun("Member 2: "), PLACEHOLDER("Ad Soyad – Öğrenci No")]),
  bulletRuns([new TextRun("Member 3: "), PLACEHOLDER("Ad Soyad – Öğrenci No")]),
  bulletRuns([new TextRun("Member 4 (opsiyonel): "), PLACEHOLDER("Ad Soyad – Öğrenci No")]),

  new Paragraph({ spacing: { before: 240 }, children: [new TextRun("")] }),
  PMulti([new TextRun({ text: "GitHub Repository: ", bold: true }), PLACEHOLDER("GitHub repo URL'i")]),
  PMulti([new TextRun({ text: "Submission Date: ", bold: true }), PLACEHOLDER("GG.AA.YYYY")]),
  PMulti([new TextRun({ text: "Instructor: ", bold: true }), PLACEHOLDER("Öğretim Üyesi Adı")]),

  new Paragraph({ children: [new PageBreak()] }),
];

// ========== PAGE 2: PROJECT DESCRIPTION & USER STORIES ==========
const descriptionPage = [
  heading("1. Project Description"),
  new Paragraph({
    spacing: { after: 160 },
    children: [
      new TextRun(
        "FlavorMap, kullanıcıların restoranları keşfettiği, menülerini incelediği, " +
        "1–5 yıldız üzerinden değerlendirme yazdığı ve favori mekânlarını takip ettiği " +
        "bir restoran inceleme ve keşif platformudur. Django 5.2 + SQLite + Bootstrap 5 " +
        "ile geliştirilmiş, çok kullanıcılı, rol bazlı yetkilendirmeye sahip bir web uygulamasıdır."
      ),
    ],
  }),
  new Paragraph({
    spacing: { after: 200 },
    children: [
      new TextRun({ text: "Hedef Kitle: ", bold: true }),
      PLACEHOLDER("Hedef kitle açıklaması – ör. yeme-içme meraklıları, küçük işletme sahipleri"),
    ],
  }),

  heading("2. User Stories", HeadingLevel.HEADING_2),
  bullet("Bir ziyaretçi olarak, kayıt olmadan restoran listesini görebilir ve arama/filtre yapabilirim."),
  bullet("Bir kullanıcı olarak, kayıt olup giriş yapabilir, yorum yazıp puan verebilirim."),
  bullet("Bir kullanıcı olarak, beğendiğim restoranları favori listeme ekleyebilirim."),
  bullet("Bir restoran sahibi olarak, restoranımı kaydedebilir, menü ve çalışma saatlerini yönetebilirim."),
  bullet("Bir kullanıcı olarak, başka bir yoruma cevap verebilirim (1 seviye nesting)."),
  bullet("Bir yönetici olarak, kullanıcı taleplerini (iletişim mesajları, restoran onayları) admin panelinden işleyebilirim."),
  new Paragraph({
    spacing: { after: 80 },
    children: [PLACEHOLDER("Ek bir kullanıcı senaryosu eklemek isterseniz buraya yazın.")],
  }),

  new Paragraph({ children: [new PageBreak()] }),
];

// ========== PAGE 3: ARCHITECTURE + ER ==========
const architecturePage = [
  heading("3. System Architecture (Django MVT)"),
  new Paragraph({
    spacing: { after: 120 },
    children: [new TextRun(
      "FlavorMap, Django'nun Model–View–Template (MVT) mimarisini uygular. " +
      "İstek akışı: Browser → URL Dispatcher (urls.py) → View (views.py) → Model (ORM) → Template → HTML response."
    )],
  }),
  bulletRuns([new TextRun({ text: "URLs: ", bold: true }), new TextRun("restaurants/urls.py – 22 path; restoran CRUD, yorum, menü, favori, profil, auth.")]),
  bulletRuns([new TextRun({ text: "Views: ", bold: true }), new TextRun("Function-based views; @login_required + ownership kontrolleri.")]),
  bulletRuns([new TextRun({ text: "Models: ", bold: true }), new TextRun("6 entity – Category, Restaurant, MenuItem, OpeningHours, Review, ContactMessage.")]),
  bulletRuns([new TextRun({ text: "Templates: ", bold: true }), new TextRun("base.html (Bootstrap 5) + 15 sayfa; template inheritance.")]),
  bulletRuns([new TextRun({ text: "Static: ", bold: true }), new TextRun("static/js/star-rating.js (JS yıldız widget), static/css/star-rating.css.")]),
  bulletRuns([new TextRun({ text: "Media: ", bold: true }), new TextRun("restaurants/ ImageField uploads → MEDIA_ROOT.")]),

  new Paragraph({ spacing: { after: 80 }, children: [new TextRun("")] }),
  PMulti([new TextRun({ text: "Mimari diyagram (kutu-ok şeması) buraya yerleştirin: ", bold: true }),
    PLACEHOLDER("Mimari diyagram görseli – URL → View → Model/Template akışı")]),
  placeholderBox("Mimari Diyagramı (architecture.png)", "≈ 8 cm × 16 cm"),

  heading("4. Database Design (ER Diagram)"),
  new Paragraph({
    spacing: { after: 120 },
    children: [new TextRun(
      "Veritabanı 6 modelden oluşur. Restaurant merkez tablo; Category (1-N), MenuItem (1-N), " +
      "OpeningHours (1-N, unique_together=restaurant+day), Review (1-N, self-FK ile nesting), " +
      "User (M:N favorited_by). ContactMessage bağımsız bir formdan beslenir."
    )],
  }),
  placeholderBox("ER Diyagramı (er_diagram.png) – dbdiagram.io / draw.io ile çizin", "≈ 9 cm × 16 cm"),

  bulletRuns([new TextRun({ text: "Unique constraint: ", bold: true }),
    new TextRun("Review (user, restaurant) WHERE parent IS NULL → bir kullanıcı bir restorana yalnızca bir ana yorum yazabilir.")]),
  bulletRuns([new TextRun({ text: "unique_together: ", bold: true }),
    new TextRun("OpeningHours (restaurant, day_of_week) → her gün için tek kayıt.")]),

  new Paragraph({ children: [new PageBreak()] }),
];

// ========== PAGES 4–5: SCREENSHOTS ==========
const screens = [
  { title: "5.1 Anasayfa", file: "01_home.png",
    caption: "Gradient hero, kategori filtreleri, öne çıkan ve en yüksek puanlı restoranlar. (Mandatory: Popular Ranking)" },
  { title: "5.2 Restoran Listesi + Gelişmiş Filtreler", file: "02_list_filters.png",
    caption: "Arama, kategori/lokasyon/fiyat filtreleri + min_rating ve has_photo (Bonus B4: Advanced Filtering)." },
  { title: "5.3 Restoran Detay", file: "03_detail.png",
    caption: "Foto, ortalama yıldız, menü tablosu, çalışma saatleri, yorumlar + cevaplar, favoriye ekle butonu." },
  { title: "5.4 Restoran Oluştur / Düzenle", file: "04_restaurant_form.png",
    caption: "ModelForm, ImageField yükleme, kategori seçimi. (Mandatory: Restaurant CRUD + Photo)" },
  { title: "5.5 JavaScript Yıldız Widget'ı", file: "05_star_widget.png",
    caption: "Yorum formunda interaktif 5 yıldız widget; mouse hover ve klavye erişimli. (Bonus B1: JavaScript Element)" },
  { title: "5.6 Profil Sayfası", file: "06_profile.png",
    caption: "Kullanıcının yazdığı yorumlar ve oluşturduğu restoranlar listesi. (Mandatory: User Profile)" },
  { title: "5.7 Favorilerim", file: "07_favorites.png",
    caption: "Kullanıcının favori olarak eklediği restoranların kart grid görünümü. (Mandatory: Favorites)" },
  { title: "5.8 Django Admin Paneli", file: "08_admin.png",
    caption: "list_display, list_filter, search_fields ile özelleştirilmiş; ContactMessage ve Restaurant onay yönetimi." },
];

const screenshotPage = [
  heading("5. Key Pages – Screenshots"),
  new Paragraph({
    spacing: { after: 160 },
    children: [new TextRun(
      "Aşağıda uygulamanın 8 anahtar ekranı yer alır. Görselleri report/screenshots/ " +
      "klasöründen yerleştirin (placeholder kutuların yerine sürükle-bırak)."
    )],
  }),
];

screens.forEach((s, i) => {
  screenshotPage.push(new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 200, after: 80 },
    children: [new TextRun(s.title)],
  }));
  screenshotPage.push(placeholderBox(`${s.file}`, "≈ 8 cm × 14 cm"));
  screenshotPage.push(new Paragraph({
    spacing: { after: 160 },
    alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: `Görsel ${i + 1}: ${s.caption}`, italics: true, color: "555555", size: 18 })],
  }));
  // Page break after the 4th screenshot to push remaining to page 5
  if (i === 3) {
    screenshotPage.push(new Paragraph({ children: [new PageBreak()] }));
  }
});
screenshotPage.push(new Paragraph({ children: [new PageBreak()] }));

// ========== PAGE 6: FEATURE CHECKLIST ==========
const featureRows = [
  ["1", "Restaurant CRUD", "✓", "views.restaurant_create/update/delete"],
  ["2", "Category System", "✓", "Category modeli + list filter"],
  ["3", "Location Filter", "✓", "restaurant_list q_location parametresi"],
  ["4", "Price Range Filter", "✓", "PRICE_CHOICES (€/€€/€€€)"],
  ["5", "Reviews & Ratings", "✓", "Review modeli, 1–5 yıldız"],
  ["6", "Average Rating + Sort", "✓", "Restaurant.average_rating, ?order=rating"],
  ["7", "Search", "✓", "name/description __icontains"],
  ["8", "User Authentication", "✓", "Django auth: login/logout/register"],
  ["9", "Menu Management", "✓", "menu_item_create/update/delete"],
  ["10", "Favorites", "✓", "favorited_by M:N + toggle_favorite"],
  ["11", "Restaurant Photo", "✓", "Restaurant.photo ImageField"],
  ["12", "Opening Hours", "✓", "OpeningHours + inlineformset_factory"],
  ["13", "Popular Ranking", "✓", "Anasayfa Öne Çıkan + En Yüksek Puanlılar"],
  ["14", "User Profile", "✓", "/profil/, /kullanici/<user>/"],
  ["15", "Review Replies", "✓", "Review.parent self-FK"],
  ["16", "Atomic Transactions", "✓", "register & toggle_favorite transaction.atomic"],
];

const bonusRows = [
  ["B1", "JavaScript Element", "✓", "static/js/star-rating.js – yıldız widget"],
  ["B4", "Advanced Filtering", "✓", "min_rating + has_photo + multi-combo"],
  ["+", "Restaurant Owner Role", "✓", "creator alanı + status onay süreci"],
  ["+", "Bootstrap Responsive", "✓", "Bootstrap 5.3, mobil uyumlu"],
];

const checklistPage = [
  heading("6. Feature Checklist"),
  new Paragraph({
    spacing: { after: 160 },
    children: [new TextRun("PDF Bölüm 2'deki tüm mandatory özellikler (16/16) ve seçilen bonus özellikler uygulandı.")],
  }),
  new Paragraph({ spacing: { after: 80 }, children: [new TextRun({ text: "Mandatory Features (16/16)", bold: true, size: 24 })] }),
  makeTable([720, 3200, 720, 4720], ["#", "Özellik", "Durum", "Konum / Not"], featureRows),
  new Paragraph({ spacing: { before: 240, after: 80 }, children: [new TextRun({ text: "Bonus & Extras", bold: true, size: 24 })] }),
  makeTable([720, 3200, 720, 4720], ["#", "Özellik", "Durum", "Konum / Not"], bonusRows),
  new Paragraph({
    spacing: { before: 240 },
    children: [PLACEHOLDER("Ek bonus özellik eklediyseniz buraya satır eklemeyi unutmayın.")],
  }),
  new Paragraph({ children: [new PageBreak()] }),
];

// ========== PAGE 7: CHALLENGES & SOLUTIONS ==========
const challengesPage = [
  heading("7. Challenges and Solutions"),

  new Paragraph({ spacing: { before: 80, after: 60 }, children: [
    new TextRun({ text: "7.1 Tek-yorum kısıtı vs. çoklu yanıt", bold: true })] }),
  P("Sorun: Kullanıcı bir restorana yalnızca bir ana yorum yazabilmeli ama yanıt sayısı sınırsız olmalı."),
  P("Çözüm: models.UniqueConstraint(fields=['user','restaurant'], condition=Q(parent__isnull=True)) ile koşullu unique index. Yanıtlarda (parent != NULL) kısıt devre dışı kalır."),

  new Paragraph({ spacing: { before: 160, after: 60 }, children: [
    new TextRun({ text: "7.2 Favori toggle yarış durumu", bold: true })] }),
  P("Sorun: Hızlı çift tıklamada veya paralel isteklerde aynı (user, restaurant) çiftinin iki kez M:N tablosuna eklenmesi riski."),
  P("Çözüm: toggle_favorite view'ında transaction.atomic() + IntegrityError yakalama; idempotent davranış sağlandı."),

  new Paragraph({ spacing: { before: 160, after: 60 }, children: [
    new TextRun({ text: "7.3 OpeningHours – 7 günü tek sayfada yönetme", bold: true })] }),
  P("Sorun: Restoran sahibinin 7 günü tek tek eklemesi UX olarak yorucu, admin'e bağımlılık vardı."),
  P("Çözüm: inlineformset_factory(extra=7, max_num=7) ile dinamik formset; opening_hours_form.html'de tablo görünümü. Admin'de paralel olarak TabularInline korundu."),

  new Paragraph({ spacing: { before: 160, after: 60 }, children: [
    new TextRun({ text: "7.4 Anasayfa görsel hiyerarşi sorunu", bold: true })] }),
  P("Sorun: 'Hoş Geldiniz' başlığı diğer h2 başlıklarıyla aynı görsel ağırlıkta; vurgu kaybediyordu."),
  P("Çözüm: Gradient (linear-gradient #100b09 → #ffffff) hero/jumbotron + display-4 fw-bold; CTA butonları hero içine taşındı."),

  new Paragraph({ spacing: { before: 240 }, children: [
    PLACEHOLDER("Ek bir zorluk yaşadıysanız buraya 3–4 satır olarak ekleyin (örn. ImageField MEDIA_URL setup, Bootstrap CDN entegrasyonu, vb.)")
  ]}),

  new Paragraph({ children: [new PageBreak()] }),
];

// ========== PAGE 8: CONTRIBUTIONS & GITHUB ==========
const contributionsPage = [
  heading("8. Individual Contribution Summary"),
  new Paragraph({
    spacing: { after: 160 },
    children: [new TextRun(
      "Aşağıdaki tablo her grup üyesinin ana sorumluluk alanlarını ve GitHub commit sayılarını özetler. " +
      "Detay için `git shortlog -sn` çıktısına bakılabilir."
    )],
  }),
  makeTable(
    [2400, 5560, 1400],
    ["Grup Üyesi", "Sorumluluk / Yapılan İşler", "Commit Sayısı"],
    [
      [
        [new Paragraph({ children: [PLACEHOLDER("Üye 1 – Ad Soyad")] })],
        [new Paragraph({ children: [PLACEHOLDER("Ör. Model tasarımı, Restaurant CRUD, admin paneli")] })],
        [new Paragraph({ children: [PLACEHOLDER("N")] })],
      ],
      [
        [new Paragraph({ children: [PLACEHOLDER("Üye 2 – Ad Soyad")] })],
        [new Paragraph({ children: [PLACEHOLDER("Ör. Auth, profil, favoriler, JS yıldız widget'ı")] })],
        [new Paragraph({ children: [PLACEHOLDER("N")] })],
      ],
      [
        [new Paragraph({ children: [PLACEHOLDER("Üye 3 – Ad Soyad")] })],
        [new Paragraph({ children: [PLACEHOLDER("Ör. Yorum sistemi, replies, opening hours formset")] })],
        [new Paragraph({ children: [PLACEHOLDER("N")] })],
      ],
      [
        [new Paragraph({ children: [PLACEHOLDER("Üye 4 – Ad Soyad (opsiyonel)")] })],
        [new Paragraph({ children: [PLACEHOLDER("Ör. Template/CSS, hero tasarım, bonus filtreler, dokümantasyon")] })],
        [new Paragraph({ children: [PLACEHOLDER("N")] })],
      ],
    ]
  ),

  heading("9. GitHub Repository", HeadingLevel.HEADING_2),
  PMulti([new TextRun({ text: "Repo URL: ", bold: true }), PLACEHOLDER("https://github.com/<kullanıcı>/<repo>")]),
  PMulti([new TextRun({ text: "Branch: ", bold: true }), PLACEHOLDER("main")]),
  PMulti([new TextRun({ text: "Setup: ", bold: true }), new TextRun("README.md – kurulum ve runserver adımları.")]),

  new Paragraph({
    spacing: { before: 360 },
    alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: "— Son —", italics: true, color: "888888" })],
  }),
];

// -------- assemble document --------
const doc = new Document({
  creator: "FlavorMap Group",
  title: "FlavorMap – Final Report",
  description: "CSE 220 Final Report",
  styles: {
    default: { document: { run: { font: "Calibri", size: 22 } } },
    paragraphStyles: [
      {
        id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 30, bold: true, font: "Calibri", color: "1F3A5F" },
        paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 0 },
      },
      {
        id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 26, bold: true, font: "Calibri", color: "1F3A5F" },
        paragraph: { spacing: { before: 200, after: 100 }, outlineLevel: 1 },
      },
    ],
  },
  numbering: {
    config: [{
      reference: "bullets",
      levels: [{
        level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 540, hanging: 270 } } },
      }],
    }],
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 }, // US Letter
        margin: { top: 1080, right: 1080, bottom: 1080, left: 1080 }, // 0.75 inch margins
      },
    },
    headers: {
      default: new Header({
        children: [new Paragraph({
          alignment: AlignmentType.RIGHT,
          children: [new TextRun({ text: "FlavorMap – CSE 220 Final Report", italics: true, size: 18, color: "888888" })],
        })],
      }),
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({ text: "Page ", size: 18, color: "888888" }),
            new TextRun({ children: [PageNumber.CURRENT], size: 18, color: "888888" }),
            new TextRun({ text: " / ", size: 18, color: "888888" }),
            new TextRun({ children: [PageNumber.TOTAL_PAGES], size: 18, color: "888888" }),
          ],
        })],
      }),
    },
    children: [
      ...cover,
      ...descriptionPage,
      ...architecturePage,
      ...screenshotPage,
      ...checklistPage,
      ...challengesPage,
      ...contributionsPage,
    ],
  }],
});

Packer.toBuffer(doc).then((buffer) => {
  const out = path.join(__dirname, "FlavorMap_Final_Report.docx");
  fs.writeFileSync(out, buffer);
  console.log("Wrote", out);
});
