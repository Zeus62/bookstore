// i18n.js - Handles fetching and applying translations dynamically

const SUPPORTED_LANGUAGES = ['en', 'ar', 'fr', 'de'];
const DEFAULT_LANGUAGE = 'en';

let currentTranslations = {};

document.addEventListener('DOMContentLoaded', () => {
    let lang = localStorage.getItem('lang');
    if (!lang || !SUPPORTED_LANGUAGES.includes(lang)) {
        lang = DEFAULT_LANGUAGE;
        localStorage.setItem('lang', lang);
    }
    
    // Initial load
    loadTranslations(lang);

    const langButtons = document.querySelectorAll('[data-lang-switcher]');
    langButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const selectedLang = e.currentTarget.getAttribute('data-lang-switcher');
            setLanguage(selectedLang);
        });
    });
});

async function setLanguage(lang) {
    if (localStorage.getItem('lang') !== lang) {
        localStorage.setItem('lang', lang);
        // We can either reload or load dynamically. 
        // Dynamically is smoother:
        await loadTranslations(lang);
    }
}

async function loadTranslations(lang) {
    try {
        const response = await fetch(`/static/i18n/${lang}.json`);
        if (!response.ok) throw new Error(`Could not load ${lang} translations`);
        
        currentTranslations = await response.json();
        
        // Apply changes to the page
        applyTranslations();
        updateActiveSwitcher(lang);
        updateDocumentAttributes(lang);
        
    } catch (error) {
        console.error('Error loading translations:', error);
        // Fallback to English if not already trying English
        if (lang !== DEFAULT_LANGUAGE) {
            loadTranslations(DEFAULT_LANGUAGE);
        }
    }
}

function updateDocumentAttributes(lang) {
    document.documentElement.lang = lang;
    document.documentElement.dir = (lang === 'ar' ? 'rtl' : 'ltr');
    
    // Optional: Add a class to body for CSS targeting
    document.body.classList.remove('lang-en', 'lang-ar', 'lang-fr', 'lang-de');
    document.body.classList.add(`lang-${lang}`);
}

function updateActiveSwitcher(lang) {
    const langButtons = document.querySelectorAll('[data-lang-switcher]');
    langButtons.forEach(btn => {
        if (btn.getAttribute('data-lang-switcher') === lang) {
            btn.classList.add('active', 'fw-bold');
        } else {
            btn.classList.remove('active', 'fw-bold');
        }
    });
    
    const activeLangText = document.getElementById('activeLangText');
    if (activeLangText) {
        const flags = {
            'en': '🇺🇸 EN',
            'ar': '🇸🇦 AR',
            'fr': '🇫🇷 FR',
            'de': '🇩🇪 DE'
        };
        activeLangText.innerHTML = flags[lang] || flags[DEFAULT_LANGUAGE];
    }
}

function applyTranslations() {
    const elements = document.querySelectorAll('[data-i18n], [data-i18n-title], [data-i18n-placeholder]');
    
    elements.forEach(element => {
        // Handle standard text content
        if (element.hasAttribute('data-i18n')) {
            const key = element.getAttribute('data-i18n');
            const translation = getNestedTranslation(currentTranslations, key);
            if (translation) {
                if (element.tagName === 'INPUT' && (element.type === 'submit' || element.type === 'button')) {
                    element.value = translation;
                } else {
                    element.innerHTML = translation;
                }
            }
        }
        
        // Handle placeholders
        if (element.hasAttribute('data-i18n-placeholder')) {
            const key = element.getAttribute('data-i18n-placeholder');
            const translation = getNestedTranslation(currentTranslations, key);
            if (translation) {
                element.placeholder = translation;
            }
        } else if (element.hasAttribute('data-i18n') && element.hasAttribute('placeholder')) {
            // Fallback for elements using data-i18n for placeholder (common pattern)
            const key = element.getAttribute('data-i18n');
            const translation = getNestedTranslation(currentTranslations, key);
            if (translation) {
                element.placeholder = translation;
            }
        }

        // Handle titles
        if (element.hasAttribute('data-i18n-title')) {
            const titleKey = element.getAttribute('data-i18n-title');
            const titleTranslation = getNestedTranslation(currentTranslations, titleKey);
            if (titleTranslation) {
                element.title = titleTranslation;
            }
        }
    });
}

function getNestedTranslation(obj, path) {
    return path.split('.').reduce((acc, part) => acc && acc[part], obj);
}

