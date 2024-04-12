let wordDict = {};
export const I18_JSON_URL = "https://jogo9k.s3.sa-east-1.amazonaws.com/Base/base.json";
export const LANG_ZH = 'ZH';
export const LANG_EN = 'EN';
export const LANG_PT = 'PT';

const reVar = /\{\w*\}/g;
const defaultLang = LANG_PT;
const preCache = {};
let currLang = defaultLang;
export const setWordDict = (jsonData) => {
    wordDict = Object.assign(wordDict, jsonData);
}
export async function getOnlineJson() {
    let data = await fetch(I18_JSON_URL).then(response => response.json());

    setWordDict(data);
}

export function setLanguage() {
    localStorage.setItem('language', lang);
    currLang = lang;
}

export function getLanguage() {
    if (currLang === undefined) {
        currLang = localStorage.getItem('language');
        if (currLang === null || !allLangs.includes(currLang)) {
            currLang = defaultLang;
        }
    }
    return currLang;
}

export function tr(key, dict) {
    const lang = getLanguage();
    let temp = getAttrs(preCache, key, lang || '');

    if (temp === undefined) {
        let word = getAttrs(wordDict, key, lang || '');
        if (word === undefined) {
            // console.info(`i18n: [${key}](${lang}) not exist`);
            return key;
        }
        temp = preprocess(word);
        // put cache
        if (!preCache.hasOwnProperty(key)) {
            preCache[key] = {};
        }
        preCache[key][lang] = temp;
    }
    // return key
    if (temp !== undefined) {
        return genStr(temp, dict);
    } else {
        return key;
    }
}

function genStr(temp, dict) {
    if (temp.temp.length === 1) {
        return temp.temp[0];
    } else {
        const newlist = temp.temp.slice();
        for (let k in temp.vars) {
            const pos = temp.vars[k];
            for (let p of pos) {
                newlist[p] = dict[k].toString() || '';
            }
        }
        return newlist.join('');
    }
}
function preprocess(temp) {
    const out = {
        temp: [],
        vars: {},
    };
    const matches = temp.matchAll(reVar);
    let pos = 0;
    for (let match of matches) {
        const find = match[0];
        const key = find.slice(1, -1);
        if (match.index > pos) {
            out.temp.push(temp.slice(pos, match.index));
        }
        pos = match.index + find.length;
        if (out.vars[key] === undefined) {
            out.vars[key] = [];
        }
        out.vars[key].push(out.temp.length);
        out.temp.push('');
    }
    if (pos < temp.length) {
        out.temp.push(temp.slice(pos));
    }
    return out;
}
export function getAttrs(obj, ...keys) {
    let curr = obj;
    for (const k of keys) {
        if (curr.hasOwnProperty(k)) {
            curr = curr[k];
        } else {
            return undefined;
        }
    }
    return curr;
}
