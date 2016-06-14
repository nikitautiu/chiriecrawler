"""Module for the text/tag analyzer"""
import collections
import re
import unicodedata

DEFAULT_TAGS = {
    "manastur": {"manastur"},
    "gheorgheni": {"gheorgheni", "interservisan"},
    "marasti": {"marasti"},
    "grigorescu": {"grigorescu"},
    "cetatutie": {"cetatutie"},
    "coleg": {"coleg(a)?"},
    "hotelier": {"pensiune", "(regim )?hotelier"},
    "camera": {"inchiriez camera", "inchiriez camere"},
    "gruia": {"gruia"},
    "buna ziua": {"buna ziua"},
    "zorilor": {"zorilor"},
    "floresti": {"floresti"},
    "untold": {"untold"},
    "nemobilat": {"nemobilat"},
    "avram iancu": {"avram iancu"},
    "cipariu": {"cipariu"},
    "unirii": {"unirii"},
    "mihai viteazul": {"mihai viteazu(l)?"}
}


def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn')


def sanitize_text(text):
    return strip_accents(text).lower()


class TagExtractor(object):
    def __init__(self, initial_keywords={}):
        self.associations = collections.defaultdict(set)
        for (tag, value) in initial_keywords.items():
            for keyword in value:
                self.add_keyword(tag, keyword)

    def add_keyword(self, tag, keyword):
        self.associations[tag.lower()].add(keyword.lower())

    def extract(self, text):
        tags = set()
        text = sanitize_text(text)
        for (key, value) in self.associations.items():
            if any(re.search(r'{0}'.format(word), text) for word in value):
                tags.add(key)
        return tags


def default_tagger():
    return TagExtractor(DEFAULT_TAGS)