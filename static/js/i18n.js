// Krushak - Lightweight i18n (EN / MR / HI) - persists in localStorage
const TRANSLATIONS = {
  en: {
    nav_home: "Home",
    nav_about: "About Scheme",
    nav_dashboard: "Dashboard",
    nav_admin: "Admin Panel",
    nav_farmer_login: "Farmer Login",
    nav_farmer_register: "Farmer Register",
    nav_admin_short: "Admin",
    hero_badge: "Government of India • Direct Benefit Transfer",
    hero_title1: "Your Farm is Damaged?",
    hero_title2: "We are with you.",
    hero_desc: "Report crop loss due to <strong>Heavy Monsoon, Flood, Pollution, Drought or Pest</strong> in 2 minutes. Simple form, photo upload, instant tracking. Admin verifies & initiates compensation.",
    btn_report: "Report Damage Now",
    btn_register: "New Farmer? Register",
    check1: "No agents, No fees",
    check2: "24–48h verification",
    check3: "SMS updates",
    help_title: "Toll-Free Help for Farmers",
    help_num: "1800-180-1551",
    help_lang: "| Voice support in Marathi/Hindi",
    trust1: "Verified by Agri Dept",
    trust2: "Aadhaar-safe, Data encrypted",
    trust3: "Works on any phone",
    trust4: "Takes only 2 mins",
    how_title: "How it works — farmer friendly",
    how_sub: "No complicated pages. Big buttons, clear language, photo guidance. Enterprise reliability.",
    how1_t: "1. Register / Login",
    how1_d: "Mobile + Village + District. One-time. Username also works.",
    how1_b: "30 seconds",
    how2_t: "2. Report Damage",
    how2_d: "Select Monsoon / Pollution / Flood. Add crop, farm size, 1 photo.",
    how2_b: "2 minutes",
    how3_t: "3. Track & Get Help",
    how3_d: "Pending → Verified → Approved. SMS + Compensation to account.",
    how3_b: "24–48 hours",
    damage_title: "What damage can you report?",
    dmg_monsoon_t: "Heavy Monsoon",
    dmg_monsoon_d: "Excess rain, waterlogging",
    dmg_flood_t: "Flood",
    dmg_flood_d: "River overflow",
    dmg_drought_t: "Drought",
    dmg_drought_d: "No rain, cracked soil",
    dmg_pollution_t: "Pollution",
    dmg_pollution_d: "Chemical discharge",
    dmg_pest_t: "Pest Attack",
    dmg_pest_d: "Locust, bollworm",
    dmg_hail_t: "Hailstorm",
    dmg_hail_d: "Ice damage",
    recent_title: "Recent Reports (anonymized)",
    cta_title: "Ready to get support for your farm?",
    cta_sub: "Join farmers who already reported. Takes only 2 minutes. Helpline always open.",
    cta_btn: "Create Free Farmer Account",
    cta_login: "Already have account? Login here",
    cta_admin: "Admin login"
  },
  mr: {
    nav_home: "मुख्यपृष्ठ",
    nav_about: "योजनेची माहिती",
    nav_dashboard: "डॅशबोर्ड",
    nav_admin: "प्रशासन पॅनेल",
    nav_farmer_login: "शेतकरी लॉगिन",
    nav_farmer_register: "शेतकरी नोंदणी",
    nav_admin_short: "अॅडमिन",
    hero_badge: "भारत सरकार • थेट लाभ हस्तांतरण",
    hero_title1: "तुमचे शेत खराब झाले आहे का?",
    hero_title2: "आम्ही तुमच्या सोबत आहोत.",
    hero_desc: "<strong>जोरदार पाऊस, पूर, प्रदूषण, दुष्काळ किंवा कीड</strong> मुळे झालेल्या पिकाच्या नुकसानीचा अहवाल २ मिनिटांत द्या. सोपा फॉर्म, फोटो अपलोड, झटपट ट्रॅकिंग. प्रशासन पडताळणी करून भरपाई सुरू करते.",
    btn_report: "आत्ता नुकसान कळवा",
    btn_register: "नवीन शेतकरी? नोंदणी करा",
    check1: "कोणताही दलाल नाही, कोणतीही फी नाही",
    check2: "२४-४८ तासात पडताळणी",
    check3: "SMS अपडेट",
    help_title: "शेतकऱ्यांसाठी टोल-फ्री मदत",
    help_num: "१८००-१८०-१५५१",
    help_lang: "| मराठी/हिंदीत मदत",
    trust1: "कृषी विभागाद्वारे पडताळले",
    trust2: "आधार-सुरक्षित, डेटा एन्क्रिप्टेड",
    trust3: "कोणत्याही फोनवर चालते",
    trust4: "फक्त २ मिनिटे लागतात",
    how_title: "हे कसे कार्य करते — शेतकरी फ्रेंडली",
    how_sub: "कोणतीही गुंतागुंत नाही. मोठी बटणे, सोपी भाषा, फोटो मार्गदर्शन.",
    how1_t: "१. नोंदणी / लॉगिन",
    how1_d: "मोबाइल + गाव + जिल्हा. एकदाच. युजरनेम देखील चालते.",
    how1_b: "३० सेकंद",
    how2_t: "२. नुकसान कळवा",
    how2_d: "पाऊस / प्रदूषण / पूर निवडा. पीक, शेत आकार, १ फोटो जोडा.",
    how2_b: "२ मिनिटे",
    how3_t: "३. ट्रॅक करा व मदत मिळवा",
    how3_d: "प्रलंबित → पडताळले → मंजूर. SMS + खात्यात भरपाई.",
    how3_b: "२४-४८ तास",
    damage_title: "कोणते नुकसान कळवू शकता?",
    dmg_monsoon_t: "जोरदार पाऊस",
    dmg_monsoon_d: "जास्त पाऊस, पाणी साचणे",
    dmg_flood_t: "पूर",
    dmg_flood_d: "नदीला पूर",
    dmg_drought_t: "दुष्काळ",
    dmg_drought_d: "पाऊस नाही, जमीन भेगाळली",
    dmg_pollution_t: "प्रदूषण",
    dmg_pollution_d: "रासायनिक सांडपाणी",
    dmg_pest_t: "कीड हल्ला",
    dmg_pest_d: "टोळधाड, बोंड अळी",
    dmg_hail_t: "गारपीट",
    dmg_hail_d: "बर्फामुळे नुकसान",
    recent_title: "अलीकडील अहवाल",
    cta_title: "तुमच्या शेतासाठी मदत घेण्यास तयार आहात का?",
    cta_sub: "आधीच नोंदणी केलेल्या शेतकऱ्यांमध्ये सामील व्हा. फक्त २ मिनिटे. हेल्पलाइन नेहमी सुरू.",
    cta_btn: "मोफत शेतकरी खाते तयार करा",
    cta_login: "आधीच खाते आहे? लॉगिन करा",
    cta_admin: "अॅडमिन लॉगिन"
  },
  hi: {
    nav_home: "होम",
    nav_about: "योजना के बारे में",
    nav_dashboard: "डैशबोर्ड",
    nav_admin: "एडमिन पैनल",
    nav_farmer_login: "किसान लॉगिन",
    nav_farmer_register: "किसान पंजीकरण",
    nav_admin_short: "एडमिन",
    hero_badge: "भारत सरकार • प्रत्यक्ष लाभ हस्तांतरण",
    hero_title1: "क्या आपका खेत क्षतिग्रस्त है?",
    hero_title2: "हम आपके साथ हैं।",
    hero_desc: "<strong>भारी मानसून, बाढ़, प्रदूषण, सूखा या कीट</strong> से फसल नुकसान की रिपोर्ट 2 मिनट में करें। सरल फॉर्म, फोटो अपलोड, तुरंत ट्रैकिंग। एडमिन सत्यापन कर भरपाई शुरू करता है।",
    btn_report: "अभी नुकसान रिपोर्ट करें",
    btn_register: "नए किसान? पंजीकरण करें",
    check1: "कोई एजेंट नहीं, कोई फीस नहीं",
    check2: "24-48 घंटे में सत्यापन",
    check3: "SMS अपडेट",
    help_title: "किसानों के लिए टोल-फ्री हेल्प",
    help_num: "1800-180-1551",
    help_lang: "| मराठी/हिंदी में सहायता",
    trust1: "कृषि विभाग द्वारा सत्यापित",
    trust2: "आधार-सुरक्षित, एन्क्रिप्टेड",
    trust3: "किसी भी फोन पर काम करता है",
    trust4: "सिर्फ 2 मिनट लगता है",
    how_title: "यह कैसे काम करता है — किसान फ्रेंडली",
    how_sub: "कोई जटिल पेज नहीं। बड़े बटन, सरल भाषा, फोटो गाइड।",
    how1_t: "1. पंजीकरण / लॉगिन",
    how1_d: "मोबाइल + गाँव + जिला। एक बार। यूज़रनेम भी चलता है।",
    how1_b: "30 सेकंड",
    how2_t: "2. नुकसान रिपोर्ट करें",
    how2_d: "मानसून / प्रदूषण / बाढ़ चुनें। फसल, खेत आकार, 1 फोटो जोड़ें।",
    how2_b: "2 मिनट",
    how3_t: "3. ट्रैक करें और मदद लें",
    how3_d: "लंबित → सत्यापित → स्वीकृत। SMS + खाते में भरपाई।",
    how3_b: "24-48 घंटे",
    damage_title: "कौन सा नुकसान रिपोर्ट कर सकते हैं?",
    dmg_monsoon_t: "भारी मानसून",
    dmg_monsoon_d: "अधिक बारिश, जलभराव",
    dmg_flood_t: "बाढ़",
    dmg_flood_d: "नदी में उफान",
    dmg_drought_t: "सूखा",
    dmg_drought_d: "बारिश नहीं, दरारें",
    dmg_pollution_t: "प्रदूषण",
    dmg_pollution_d: "रासायनिक बहाव",
    dmg_pest_t: "कीट हमला",
    dmg_pest_d: "टिड्डी, बॉलवर्म",
    dmg_hail_t: "ओलावृष्टि",
    dmg_hail_d: "बर्फ से नुकसान",
    recent_title: "हाल की रिपोर्ट",
    cta_title: "क्या आप अपने खेत के लिए सहायता चाहते हैं?",
    cta_sub: "पहले से रिपोर्ट करने वाले किसानों से जुड़ें। सिर्फ 2 मिनट। हेल्पलाइन हमेशा खुली।",
    cta_btn: "मुफ्त किसान खाता बनाएं",
    cta_login: "पहले से खाता है? लॉगिन करें",
    cta_admin: "एडमिन लॉगिन"
  }
};

function applyLang(lang){
  const dict = TRANSLATIONS[lang] || TRANSLATIONS.en;
  document.querySelectorAll('[data-i18n]').forEach(el=>{
    const key = el.getAttribute('data-i18n');
    if(dict[key]!==undefined){
      // allow HTML in desc
      if(dict[key].includes('<')) el.innerHTML = dict[key];
      else el.textContent = dict[key];
    }
  });
  document.querySelectorAll('[data-i18n-placeholder]').forEach(el=>{
    const key = el.getAttribute('data-i18n-placeholder');
    if(dict[key]!==undefined) el.placeholder = dict[key];
  });
  localStorage.setItem('ks_lang', lang);
  document.documentElement.lang = lang;
  // update switcher label
  document.querySelectorAll('.lang-label').forEach(l=> l.textContent = lang==='mr'?'मराठी': lang==='hi'?'हिंदी':'EN');
  document.querySelectorAll('.lang-opt').forEach(opt=>{
    opt.classList.toggle('active', opt.dataset.lang===lang);
  });
}

function toggleLang(){
  const cur = localStorage.getItem('ks_lang')||'en';
  const next = cur==='en' ? 'mr' : cur==='mr' ? 'hi' : 'en';
  applyLang(next);
}
function setLang(lang){ applyLang(lang); }

document.addEventListener('DOMContentLoaded', ()=>{
  const saved = localStorage.getItem('ks_lang')||'en';
  applyLang(saved);
});
