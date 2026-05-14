// i18n.js - Handles fetching and applying translations dynamically

const SUPPORTED_LANGUAGES = ['en', 'ar', 'fr', 'de'];
const DEFAULT_LANGUAGE = 'en';

let currentTranslations = {};

document.addEventListener('DOMContentLoaded', () => {
    let lang = localStorage.getItem('lang');
    if (!lang || !SUPPORTED_LANGUAGES.includes(lang)) {
        lang = DEFAULT_LANGUAGE;
    }
    setLanguage(lang);

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
        location.reload();
    }
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
        if (lang === 'en') activeLangText.innerHTML = '🇺🇸 EN';
        else if (lang === 'ar') activeLangText.innerHTML = '🇸🇦 AR';
        else if (lang === 'fr') activeLangText.innerHTML = '🇫🇷 FR';
        else if (lang === 'de') activeLangText.innerHTML = '🇩🇪 DE';
    }
}

function applyTranslations() {
    const elements = document.querySelectorAll('[data-i18n], [data-i18n-title]');
    if (!document.body.classList.contains('i18n-transition')) {
        document.body.classList.add('i18n-transition');
    }
    elements.forEach(element => {
        if (element.hasAttribute('data-i18n')) {
            const key = element.getAttribute('data-i18n');
            const translation = getNestedTranslation(currentTranslations, key);
            if (translation) {
                if (element.hasAttribute('placeholder') && (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA')) {
                    element.placeholder = translation;
                } else if (element.tagName === 'INPUT' && (element.type === 'submit' || element.type === 'button')) {
                    element.value = translation;
                } else {
                    element.innerHTML = translation;
                }
            }
        }
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
