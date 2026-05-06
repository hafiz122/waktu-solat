/**
 * Waktu Solat Malaysia - Main JavaScript
 * Features: Location detection, zone search, prayer times display, countdown
 */

// Approximate zone centers for geolocation matching
const ZONE_CENTERS = {
  "JHR01": {lat: 2.45, lon: 104.55},
  "JHR02": {lat: 1.49, lon: 103.74},
  "JHR03": {lat: 1.96, lon: 103.33},
  "JHR04": {lat: 2.04, lon: 102.58},
  "KDH01": {lat: 6.12, lon: 100.37},
  "KDH02": {lat: 5.65, lon: 100.48},
  "KDH03": {lat: 6.25, lon: 100.61},
  "KDH04": {lat: 5.68, lon: 100.92},
  "KDH05": {lat: 5.37, lon: 100.55},
  "KDH06": {lat: 6.35, lon: 99.80},
  "KDH07": {lat: 5.78, lon: 100.43},
  "KTN01": {lat: 6.12, lon: 102.25},
  "KTN03": {lat: 5.05, lon: 101.95},
  "MLK01": {lat: 2.19, lon: 102.25},
  "NGS01": {lat: 2.47, lon: 102.23},
  "NGS02": {lat: 2.73, lon: 101.94},
  "PHG01": {lat: 2.79, lon: 104.17},
  "PHG02": {lat: 3.81, lon: 103.33},
  "PHG03": {lat: 3.48, lon: 102.42},
  "PHG04": {lat: 4.18, lon: 101.85},
  "PHG05": {lat: 3.35, lon: 101.80},
  "PHG06": {lat: 4.47, lon: 101.38},
  "PLS01": {lat: 6.43, lon: 100.20},
  "PNG01": {lat: 5.41, lon: 100.34},
  "PRK01": {lat: 3.95, lon: 101.40},
  "PRK02": {lat: 4.60, lon: 101.07},
  "PRK03": {lat: 5.68, lon: 100.95},
  "PRK04": {lat: 5.35, lon: 101.05},
  "PRK05": {lat: 4.02, lon: 100.93},
  "PRK06": {lat: 4.85, lon: 100.74},
  "PRK07": {lat: 4.85, lon: 100.79},
  "SBH01": {lat: 5.84, lon: 118.12},
  "SBH02": {lat: 5.90, lon: 117.55},
  "SBH03": {lat: 5.03, lon: 118.33},
  "SBH04": {lat: 4.24, lon: 117.89},
  "SBH05": {lat: 6.88, lon: 116.84},
  "SBH06": {lat: 6.08, lon: 116.55},
  "SBH07": {lat: 5.98, lon: 116.10},
  "SBH08": {lat: 5.35, lon: 116.15},
  "SBH09": {lat: 5.35, lon: 115.60},
  "SGR01": {lat: 3.07, lon: 101.52},
  "SGR02": {lat: 3.35, lon: 100.98},
  "SGR03": {lat: 2.99, lon: 101.40},
  "SWK01": {lat: 4.75, lon: 115.40},
  "SWK02": {lat: 4.40, lon: 114.00},
  "SWK03": {lat: 3.27, lon: 113.05},
  "SWK04": {lat: 2.29, lon: 111.83},
  "SWK05": {lat: 2.13, lon: 111.52},
  "SWK06": {lat: 1.25, lon: 111.45},
  "SWK07": {lat: 1.33, lon: 110.58},
  "SWK08": {lat: 1.55, lon: 110.34},
  "SWK09": {lat: 1.55, lon: 110.42},
  "TRG01": {lat: 5.33, lon: 103.13},
  "TRG02": {lat: 5.83, lon: 102.55},
  "TRG03": {lat: 5.05, lon: 102.75},
  "TRG04": {lat: 4.28, lon: 103.43},
  "WLY01": {lat: 3.14, lon: 101.69},
  "WLY02": {lat: 5.28, lon: 115.25}
};

// Ramadan dates (Gregorian ranges) - update yearly
// Format: [start_date_string, end_date_string] YYYY-MM-DD
const RAMADAN_DATES = [
  ["2026-02-18", "2026-03-19"], // Ramadan 1447H (approximate)
  ["2027-02-07", "2027-03-09"], // Ramadan 1448H (approximate)
];

let zonesData = {};
let citiesData = {};
let currentZone = null;
let currentSchedule = [];
let countdownInterval = null;
let lang = 'ms';

// Compute data path prefix based on current URL depth
const DATA_PREFIX = (function() {
  const path = window.location.pathname;
  const depth = path.split('/').filter(Boolean).length;
  // If we're in a subfolder like /en/KDH01.html, depth=2, need ../../data/
  // If we're at /KDH01.html, depth=1, need ./data/
  // If we're at /index.html or /, depth=0 or 1
  if (path.includes('/en/') || path.includes('/zh/') || path.includes('/ta/') || path.includes('/ar/')) {
    return '../data/';
  }
  return 'data/';
})();

const TRANSLATIONS = {
  ms: {
    title: "Waktu Solat Malaysia",
    subtitle: "Jadual Waktu Solat Bagi Semua Zon di Malaysia",
    selectZone: "Pilih Zon",
    searchPlace: "Cari tempat (contoh: Alor Setar, Ipoh)",
    todayPrayer: "Waktu Solat Hari Ini",
    next30Days: "Waktu Solat 30 Hari Akan Datang",
    days: "Hari",
    date: "Tarikh",
    imsak: "Imsak",
    subuh: "Subuh",
    syuruk: "Syuruk",
    zohor: "Zohor",
    asar: "Asar",
    maghrib: "Maghrib",
    isyak: "Isyak",
    nextPrayer: "Solat Seterusnya",
    timeRemaining: "Masa Berbaki",
    fridayNote: "Jumaat",
    ramadanNote: "Buka Puasa",
    home: "Laman Utama",
    currentZone: "Zon Semasa",
    detectedLocation: "Lokasi Dikesan",
    noResults: "Tiada keputusan dijumpai",
    loading: "Memuatkan...",
    friday: "Jumaat",
    disclaimer: "Masa solat adalah anggaran. Sila rujuk JAKIM untuk ketepatan rasmi.",
    seoDesc: "Waktu solat Malaysia mengikut zon JAKIM. Jadual solat harian dan 30 hari akan datang dengan pengesanan lokasi automatik.",
    galleryTitle: "Galeri Masjid Malaysia",
  },
  en: {
    title: "Malaysia Prayer Times",
    subtitle: "Prayer Times for All Zones in Malaysia",
    selectZone: "Select Zone",
    searchPlace: "Search place (e.g. Alor Setar, Ipoh)",
    todayPrayer: "Today's Prayer Times",
    next30Days: "Next 30 Days Prayer Times",
    days: "Day",
    date: "Date",
    imsak: "Imsak",
    subuh: "Fajr",
    syuruk: "Sunrise",
    zohor: "Dhuhr",
    asar: "Asr",
    maghrib: "Maghrib",
    isyak: "Isha",
    nextPrayer: "Next Prayer",
    timeRemaining: "Time Remaining",
    fridayNote: "Friday",
    ramadanNote: "Iftar",
    home: "Home",
    currentZone: "Current Zone",
    detectedLocation: "Detected Location",
    noResults: "No results found",
    loading: "Loading...",
    friday: "Friday",
    disclaimer: "Prayer times are approximate. Please refer to JAKIM for official accuracy.",
    seoDesc: "Malaysia prayer times by JAKIM zone. Daily and 30-day prayer schedules with automatic location detection.",
    galleryTitle: "Malaysian Mosque Gallery",
  },
  zh: {
    title: "马来西亚祈祷时间",
    subtitle: "马来西亚所有地区的祈祷时间",
    selectZone: "选择地区",
    searchPlace: "搜索地点 (例如: 亚罗士打, 怡保)",
    todayPrayer: "今日祈祷时间",
    next30Days: "未来30天祈祷时间",
    days: "日",
    date: "日期",
    imsak: "晨礼前",
    subuh: "晨礼",
    syuruk: "日出",
    zohor: "晌礼",
    asar: "晡礼",
    maghrib: "昏礼",
    isyak: "宵礼",
    nextPrayer: "下一次祈祷",
    timeRemaining: "剩余时间",
    fridayNote: "主麻日",
    ramadanNote: "开斋",
    home: "首页",
    currentZone: "当前地区",
    detectedLocation: "检测到的位置",
    noResults: "未找到结果",
    loading: "加载中...",
    friday: "星期五",
    disclaimer: "祈祷时间为近似值。请参考JAKIM获取官方准确时间。",
    seoDesc: "马来西亚JAKIM分区祈祷时间。每日及未来30天祈祷时间表，支持自动位置检测。",
    galleryTitle: "马来西亚清真寺画廊",
  },
  ta: {
    title: "மலேசியா நமஸ்கார நேரம்",
    subtitle: "மலேசியாவின் அனைத்து மண்டலங்களுக்கான நமஸ்கார நேரம்",
    selectZone: "மண்டலத்தைத் தேர்ந்தெடு",
    searchPlace: "இடத்தைத் தேடு (எ.கா: அலோர் ஸ்டார், இப்போ)",
    todayPrayer: "இன்றைய நமஸ்கார நேரம்",
    next30Days: "அடுத்த 30 நாட்களின் நமஸ்கார நேரம்",
    days: "நாள்",
    date: "தேதி",
    imsak: "இம்சாக்",
    subuh: "சுபு",
    syuruk: "சூர்யோதயம்",
    zohor: "ஜோஹர்",
    asar: "அஸ்ர்",
    maghrib: "மக்ரிப்",
    isyak: "இஷா",
    nextPrayer: "அடுத்த நமஸ்காரம்",
    timeRemaining: "மீதமுள்ள நேரம்",
    fridayNote: "வெள்ளிக்கிழமை",
    ramadanNote: "இஃப்தார்",
    home: "முகப்பு",
    currentZone: "தற்போதைய மண்டலம்",
    detectedLocation: "கண்டறியப்பட்ட இடம்",
    noResults: "முடிவுகள் இல்லை",
    loading: "ஏற்றுகிறது...",
    friday: "வெள்ளிக்கிழமை",
    disclaimer: "நமஸ்கார நேரங்கள் அணுகியதாகும். அதிகாரப்பூர்வ துல்லியத்திற்கு JAKIM-ஐப் பார்க்கவும்.",
    seoDesc: "JAKIM மண்டலத்தின்படி மலேசியா நமஸ்கார நேரம். தானியங்கி இருப்பிடக் கண்டறிதலுடன் தினசரி மற்றும் 30 நாள் அட்டவணை.",
    galleryTitle: "மலேசிய பள்ளிவாசல் காட்சியகம்",
  },
  ar: {
    title: "أوقات الصلاة في ماليزيا",
    subtitle: "أوقات الصلاة لجميع المناطق في ماليزيا",
    selectZone: "اختر المنطقة",
    searchPlace: "ابحث عن مكان (مثال: ألور سيتار، إيبوه)",
    todayPrayer: "أوقات الصلاة اليوم",
    next30Days: "أوقات الصلاة للـ 30 يومًا القادمة",
    days: "يوم",
    date: "التاريخ",
    imsak: "الإمساك",
    subuh: "الفجر",
    syuruk: "الشروق",
    zohor: "الظهر",
    asar: "العصر",
    maghrib: "المغرب",
    isyak: "العشاء",
    nextPrayer: "الصلاة القادمة",
    timeRemaining: "الوقت المتبقي",
    fridayNote: "الجمعة",
    ramadanNote: "الإفطار",
    home: "الرئيسية",
    currentZone: "المنطقة الحالية",
    detectedLocation: "الموقع المكتشف",
    noResults: "لا توجد نتائج",
    loading: "جار التحميل...",
    friday: "الجمعة",
    disclaimer: "أوقات الصلاة تقريبية. يرجى الرجوع إلى JAKIM للدقة الرسمية.",
    seoDesc: "أوقات الصلاة في ماليزيا حسب منطقة JAKIM. جداول الصلاة اليومية ولمدة 30 يومًا مع الكشف التلقائي عن الموقع.",
    galleryTitle: "معرض المساجد الماليزية",
  }
};

const PRAYER_ICONS = {
  imsak: "🌙",
  subuh: "🌅",
  syuruk: "☀️",
  zohor: "🌞",
  asar: "🌤️",
  maghrib: "🌇",
  isyak: "🌃"
};

const PRAYER_ORDER = ["imsak", "subuh", "syuruk", "zohor", "asar", "maghrib", "isyak"];

function t(key) {
  return TRANSLATIONS[lang]?.[key] || TRANSLATIONS['en'][key] || key;
}

function formatDate(dateStr, locale) {
  const d = new Date(dateStr + 'T00:00:00');
  return d.toLocaleDateString(locale, { weekday: 'short', day: 'numeric', month: 'short' });
}

function isRamadan(dateStr) {
  for (const [start, end] of RAMADAN_DATES) {
    if (dateStr >= start && dateStr <= end) return true;
  }
  return false;
}

function isFriday(dateStr) {
  const d = new Date(dateStr + 'T00:00:00');
  return d.getDay() === 5;
}

function haversine(lat1, lon1, lat2, lon2) {
  const R = 6371;
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLon = (lon2 - lon1) * Math.PI / 180;
  const a = Math.sin(dLat/2)**2 + Math.cos(lat1 * Math.PI/180) * Math.cos(lat2 * Math.PI/180) * Math.sin(dLon/2)**2;
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
}

function findNearestZone(lat, lon) {
  let nearest = null;
  let minDist = Infinity;
  for (const [code, center] of Object.entries(ZONE_CENTERS)) {
    const dist = haversine(lat, lon, center.lat, center.lon);
    if (dist < minDist) {
      minDist = dist;
      nearest = code;
    }
  }
  return nearest;
}

async function detectLocation() {
  // Try browser geolocation first
  if (navigator.geolocation) {
    try {
      const pos = await new Promise((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(resolve, reject, {timeout: 8000, maximumAge: 600000});
      });
      const zone = findNearestZone(pos.coords.latitude, pos.coords.longitude);
      if (zone) return zone;
    } catch (e) {
      console.log("Browser geolocation failed:", e);
    }
  }
  
  // Fallback to IP geolocation
  try {
    const res = await fetch("https://ipapi.co/json/", {mode: 'cors'});
    if (res.ok) {
      const data = await res.json();
      if (data.latitude && data.longitude) {
        const zone = findNearestZone(data.latitude, data.longitude);
        if (zone) return zone;
      }
    }
  } catch (e) {
    console.log("IP geolocation failed:", e);
  }
  
  return "WLY01"; // Default to KL
}

async function loadData() {
  const [zonesRes, citiesRes] = await Promise.all([
    fetch(DATA_PREFIX + 'zones.json'),
    fetch(DATA_PREFIX + 'cities.json')
  ]);
  zonesData = await zonesRes.json();
  citiesData = await citiesRes.json();
  populateZoneSelect();
}

function populateZoneSelect() {
  const select = document.getElementById('zoneSelect');
  if (!select) return;
  
  // Sort zones by code
  const sorted = Object.entries(zonesData).sort((a, b) => a[0].localeCompare(b[0]));
  
  select.innerHTML = `<option value="">${t('selectZone')}</option>`;
  for (const [code, name] of sorted) {
    const opt = document.createElement('option');
    opt.value = code;
    opt.textContent = `${code} : ${name}`;
    select.appendChild(opt);
  }
  
  select.addEventListener('change', (e) => {
    if (e.target.value) {
      loadZone(e.target.value);
    }
  });
}

function setupSearch() {
  const input = document.getElementById('searchInput');
  const results = document.getElementById('searchResults');
  if (!input || !results) return;
  
  input.addEventListener('input', (e) => {
    const q = e.target.value.trim().toLowerCase();
    if (!q || q.length < 2) {
      results.classList.remove('active');
      return;
    }
    
    const matches = [];
    
    // Search cities
    for (const [city, code] of Object.entries(citiesData)) {
      if (city.toLowerCase().includes(q)) {
        matches.push({code, name: zonesData[code], city, type: 'city'});
      }
    }
    
    // Search zone codes
    for (const [code, name] of Object.entries(zonesData)) {
      if (code.toLowerCase().includes(q) || name.toLowerCase().includes(q)) {
        matches.push({code, name, type: 'zone'});
      }
    }
    
    // Deduplicate
    const seen = new Set();
    const unique = matches.filter(m => {
      if (seen.has(m.code)) return false;
      seen.add(m.code);
      return true;
    }).slice(0, 10);
    
    if (unique.length === 0) {
      results.innerHTML = `<div class="search-result-item">${t('noResults')}</div>`;
    } else {
      results.innerHTML = unique.map(m => `
        <div class="search-result-item" data-code="${m.code}">
          <span class="code">${m.code}</span>
          <span class="name">${m.name}${m.city ? ` (${m.city})` : ''}</span>
        </div>
      `).join('');
      
      results.querySelectorAll('.search-result-item').forEach(item => {
        item.addEventListener('click', () => {
          loadZone(item.dataset.code);
          input.value = '';
          results.classList.remove('active');
        });
      });
    }
    
    results.classList.add('active');
  });
  
  document.addEventListener('click', (e) => {
    if (!input.contains(e.target) && !results.contains(e.target)) {
      results.classList.remove('active');
    }
  });
}

async function loadZone(zoneCode) {
  currentZone = zoneCode;
  
  const select = document.getElementById('zoneSelect');
  if (select) select.value = zoneCode;
  
  // Update URL without reload
  const params = new URLSearchParams(window.location.search);
  params.set('zone', zoneCode);
  const newUrl = `${window.location.pathname}?${params.toString()}`;
  window.history.replaceState({}, '', newUrl);
  
  // Update zone info
  const infoCode = document.getElementById('zoneCodeDisplay');
  const infoName = document.getElementById('zoneNameDisplay');
  if (infoCode) infoCode.textContent = zoneCode;
  if (infoName) infoName.textContent = zonesData[zoneCode] || '';
  
  // Load schedule
  try {
    const res = await fetch(DATA_PREFIX + zoneCode + '.json');
    const data = await res.json();
    currentSchedule = data.schedule;
    renderPrayerTimes();
    render30Days();
    startCountdown();
  } catch (e) {
    console.error("Failed to load schedule:", e);
    document.getElementById('todayPrayers').innerHTML = `<div class="loading">${t('loading')}</div>`;
  }
}

function renderPrayerTimes() {
  const container = document.getElementById('todayPrayers');
  if (!container || !currentSchedule.length) return;
  
  const now = new Date();
  const todayStr = `${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')}`;
  const todayEntry = currentSchedule.find(s => s.date === todayStr) || currentSchedule[0];
  const ramadan = isRamadan(todayEntry.date);
  const friday = isFriday(todayEntry.date);
  
  let html = '';
  for (const prayer of PRAYER_ORDER) {
    let name = t(prayer);
    let note = '';
    
    if (prayer === 'zohor' && friday) {
      note = `<div class="special-note">${t('fridayNote')}</div>`;
    }
    if (prayer === 'maghrib' && ramadan) {
      note = `<div class="special-note">${t('ramadanNote')}</div>`;
    }
    
    html += `
      <div class="prayer-card" data-prayer="${prayer}">
        <div class="name">
          <span class="icon">${PRAYER_ICONS[prayer]}</span>
          <div>
            <div>${name}</div>
            ${note}
          </div>
        </div>
        <div class="time">${todayEntry[prayer]}</div>
      </div>
    `;
  }
  
  container.innerHTML = html;
}

function render30Days() {
  const container = document.getElementById('days30Table');
  if (!container || !currentSchedule.length) return;
  
  const now = new Date();
  const todayStr = `${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')}`;
  const future = currentSchedule.filter(s => s.date >= todayStr).slice(0, 30);
  
  let html = `
    <table class="days-table">
      <thead>
        <tr>
          <th>${t('days')}</th>
          <th>${t('date')}</th>
          <th>${t('imsak')}</th>
          <th>${t('subuh')}</th>
          <th>${t('syuruk')}</th>
          <th>${t('zohor')}</th>
          <th>${t('asar')}</th>
          <th>${t('maghrib')}</th>
          <th>${t('isyak')}</th>
        </tr>
      </thead>
      <tbody>
  `;
  
  const localeMap = {ms: 'ms-MY', en: 'en-GB', zh: 'zh-CN', ta: 'ta-IN', ar: 'ar-SA'};
  const locale = localeMap[lang] || 'en-GB';
  
  for (const entry of future) {
    const ramadan = isRamadan(entry.date);
    const friday = isFriday(entry.date);
    
    let zohorLabel = t('zohor');
    let maghribLabel = t('maghrib');
    
    if (friday) zohorLabel += ` <span class="badge badge-friday">${t('fridayNote')}</span>`;
    if (ramadan) maghribLabel += ` <span class="badge badge-ramadan">${t('ramadanNote')}</span>`;
    
    html += `
      <tr>
        <td class="day-cell">${entry.day}</td>
        <td class="date-cell">${formatDate(entry.date, locale)}</td>
        <td>${entry.imsak}</td>
        <td>${entry.subuh}</td>
        <td>${entry.syuruk}</td>
        <td>${entry.zohor}${friday ? ' <span class="badge badge-friday">J</span>' : ''}</td>
        <td>${entry.asar}</td>
        <td>${entry.maghrib}${ramadan ? ' <span class="badge badge-ramadan">R</span>' : ''}</td>
        <td>${entry.isyak}</td>
      </tr>
    `;
  }
  
  html += '</tbody></table>';
  container.innerHTML = html;
}

function startCountdown() {
  if (countdownInterval) clearInterval(countdownInterval);
  
  function update() {
    if (!currentSchedule.length) return;
    
    const now = new Date();
    const todayStr = `${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')}`;
    const todayEntry = currentSchedule.find(s => s.date === todayStr);
    if (!todayEntry) return;
    
    let nextPrayer = null;
    let nextTime = null;
    let minDiff = Infinity;
    
    for (const prayer of PRAYER_ORDER) {
      const [h, m] = todayEntry[prayer].split(':').map(Number);
      const prayerTime = new Date(now.getFullYear(), now.getMonth(), now.getDate(), h, m, 0);
      const diff = prayerTime - now;
      
      if (diff > 0 && diff < minDiff) {
        minDiff = diff;
        nextPrayer = prayer;
        nextTime = prayerTime;
      }
    }
    
    // If no prayer left today, get first prayer tomorrow
    if (!nextPrayer) {
      const tomorrow = currentSchedule.find(s => s.date > todayStr);
      if (tomorrow) {
        const [h, m] = tomorrow['imsak'].split(':').map(Number);
        const tDate = new Date(tomorrow.date + 'T00:00:00');
        nextTime = new Date(tDate.getFullYear(), tDate.getMonth(), tDate.getDate(), h, m, 0);
        nextPrayer = 'imsak';
        minDiff = nextTime - now;
      }
    }
    
    const box = document.getElementById('countdownBox');
    if (!box) return;
    
    if (nextPrayer && nextTime) {
      const hrs = Math.floor(minDiff / 3600000);
      const mins = Math.floor((minDiff % 3600000) / 60000);
      const secs = Math.floor((minDiff % 60000) / 1000);
      
      box.innerHTML = `
        <div class="label">${t('nextPrayer')}</div>
        <div class="time-remaining">${String(hrs).padStart(2,'0')}:${String(mins).padStart(2,'0')}:${String(secs).padStart(2,'0')}</div>
        <div class="next-name">${t(nextPrayer)} (${nextTime.toLocaleTimeString(lang === 'ar' ? 'ar-SA' : lang === 'ta' ? 'ta-IN' : lang === 'zh' ? 'zh-CN' : lang === 'ms' ? 'ms-MY' : 'en-GB', {hour:'2-digit', minute:'2-digit'})})</div>
      `;
      
      // Highlight current prayer card
      document.querySelectorAll('.prayer-card').forEach(card => {
        card.classList.remove('highlight');
      });
      const currentCard = document.querySelector(`.prayer-card[data-prayer="${nextPrayer}"]`);
      if (currentCard) currentCard.classList.add('highlight');
    } else {
      box.style.display = 'none';
    }
  }
  
  update();
  countdownInterval = setInterval(update, 1000);
}

function updatePageLanguage() {
  document.querySelectorAll('[data-t]').forEach(el => {
    const key = el.dataset.t;
    if (TRANSLATIONS[lang][key]) {
      el.textContent = TRANSLATIONS[lang][key];
    }
  });
  
  document.querySelectorAll('[data-placeholder]').forEach(el => {
    const key = el.dataset.placeholder;
    if (TRANSLATIONS[lang][key]) {
      el.placeholder = TRANSLATIONS[lang][key];
    }
  });
  
  // Update title
  const titleEl = document.getElementById('pageTitle');
  if (titleEl) titleEl.textContent = t('title');
  
  const subtitleEl = document.getElementById('pageSubtitle');
  if (subtitleEl) subtitleEl.textContent = t('subtitle');
  
  // Update meta description
  const metaDesc = document.querySelector('meta[name="description"]');
  if (metaDesc) metaDesc.content = t('seoDesc');
  
  // Update HTML lang
  document.documentElement.lang = lang === 'zh' ? 'zh-CN' : lang === 'ta' ? 'ta' : lang === 'ar' ? 'ar' : lang === 'ms' ? 'ms' : 'en';
  
  // RTL for Arabic
  if (lang === 'ar') {
    document.body.setAttribute('dir', 'rtl');
  } else {
    document.body.removeAttribute('dir');
  }
}

async function init() {
  // Determine language from URL path
  const path = window.location.pathname;
  if (path.includes('/en/')) lang = 'en';
  else if (path.includes('/zh/')) lang = 'zh';
  else if (path.includes('/ta/')) lang = 'ta';
  else if (path.includes('/ar/')) lang = 'ar';
  else lang = 'ms';
  
  updatePageLanguage();
  
  await loadData();
  setupSearch();
  
  // Check URL params for zone
  const params = new URLSearchParams(window.location.search);
  const zoneParam = params.get('zone');
  
  if (zoneParam && zonesData[zoneParam]) {
    loadZone(zoneParam);
  } else {
    // Auto-detect location
    const detected = await detectLocation();
    if (detected && zonesData[detected]) {
      loadZone(detected);
      const detectMsg = document.getElementById('detectedLocation');
      if (detectMsg) {
        detectMsg.textContent = `${t('detectedLocation')}: ${detected} - ${zonesData[detected]}`;
        detectMsg.style.display = 'block';
      }
    } else {
      loadZone('WLY01');
    }
  }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
