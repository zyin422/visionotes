from enum import unique
from keybert import KeyBERT
from nltk.stem import PorterStemmer
import spacy

kw_model = KeyBERT()
nlp = spacy.load('en_core_web_sm')

def deduplicate_keywords(keywords):
    seen = []
    for word, score in keywords:
        if any(word in existing for existing in seen):
            continue
        seen.append(word)
    return [(kw, score) for kw, score in keywords if kw in seen]

def stem_filter(keywords):
    ps = PorterStemmer()
    stems = {}
    for kw, score in keywords:
        stem = ps.stem(kw.split()[0])  # just stem first word
        if stem not in stems or score > stems[stem][1]:
            stems[stem] = (kw, score)
    return list(stems.values())

def lemmatize_text(text):
    doc = nlp(text)
    return " ".join([token.lemma_ for token in doc])


def filter_keywords_with_spacy(keywords):
    nlp = spacy.load('en_core_web_sm')
    filtered_keywords = []

    for keyword in keywords:
        doc = nlp(keyword)
        for token in doc:
            if token.pos_ in ['NOUN', 'PROPN'] or token.ent_type_:
                filtered_keywords.append(keyword)
                break

    return filtered_keywords

def keyword_extraction(notes_raw, knum):
    notes_str = lemmatize_text(notes_raw)

    top_num = max(5, knum * 4)

    keywords_1_1 = kw_model.extract_keywords(
        notes_str,
        keyphrase_ngram_range=(1, 1),
        stop_words='english',
        top_n=top_num
    )

    keywords_1_2 = kw_model.extract_keywords(
        notes_str,
        keyphrase_ngram_range=(1, 2),
        stop_words='english',
        top_n=top_num
    )

    keywords_1_3 = kw_model.extract_keywords(
        notes_str,
        keyphrase_ngram_range=(1, 3),
        stop_words='english',
        top_n=top_num
    )

    keywords = []
    for (kw, score) in keywords_1_1:
        keywords.append(kw)

    combined_keywords = keywords_1_2 + keywords_1_3
    combined_keywords = sorted(combined_keywords, key=lambda x: x[1], reverse=True)

    unique_keywords = []
    for (kw_str, score) in combined_keywords:
        add = False
        for kw in kw_str.split(" "):
            if kw in keywords:
                keywords.remove(kw)
                add = True
                break
        if add:
            unique_keywords.append((kw_str, score))

    deduped = deduplicate_keywords(unique_keywords)
    final_keywords = stem_filter(deduped)

    keywords = [kw for kw, score in final_keywords]
    filtered_keywords = filter_keywords_with_spacy(keywords)

    return filtered_keywords