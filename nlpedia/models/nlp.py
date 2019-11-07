# coding=utf-8

# This is disabled while using Heroku's free tier
"""
from textacy.preprocess import preprocess_text
from textacy.keyterms import sgrank
import textacy

def extract_tags(txt):
    txt = preprocess_text(txt, lowercase=True, no_accents=True, no_contractions=True, fix_unicode=True)
    doc = textacy.Doc(txt)
    sg  = sgrank(doc)
    string = ''

    for term, score in sg:
        if score > 0.02:
            string = string + ',' + term

    return string
"""