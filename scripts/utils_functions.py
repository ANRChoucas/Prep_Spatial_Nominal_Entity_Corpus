import os
from lxml import etree
import json
import pandas as pd
from tqdm import tqdm

import nltk
nltk.download('punkt')  # Download the necessary resources for tokenization
from nltk.tokenize import sent_tokenize


def text_preprocessing(text):
    text = text.replace(' ', ' ')
    text = text.replace('œ', 'oe')
    return text.replace('\n', ' ').strip()


def run_perdido(text, geoparser):
    try :
        return geoparser(text_preprocessing(text))
    except etree.XMLSyntaxError as e:
        return None
    

def process_directory_perdido(input_path, output_path, geoparser):
    for file in tqdm(sorted(os.listdir(input_path))):
        if file.endswith('.txt'):
            filename = file[:-4]
            if os.path.exists(os.path.join(output_path, filename + '.xml')):
                continue
            with open(os.path.join(input_path, file), 'r') as f:
                text = f.read()
                try:
                    doc = run_perdido(text, output_path, filename, geoparser)
                    if doc is not None:
                        doc.to_xml(os.path.join(output_path, filename + '.xml'))
                except:
                    print(filename)
    

def get_term_occurrences_from_ene(filename):
    words = []
    if os.path.exists(filename):
        try:
            tree = etree.parse(filename)
            for term in tree.xpath('.//rs[@type="place" and @subtype="ene"]/term[@type="place"]'):
                phrase = ''
                tokens = term.xpath('.//w[@pos="N" or @pos="PREPDET" or @pos="PREP" or @pos="DET"]')
                for i, w in enumerate(tokens):
                    if len(w.text) > 1:
                        if ('DET' not in w.get('pos') and 'PREP' not in w.get('pos')):
                            phrase += w.text.lower() + ' '
                        if ('DET' in w.get('pos') or 'PREP' in w.get('pos')) and (i > 0 and i < len(tokens)-1):
                            phrase += w.text.lower() + ' '
                words.append(phrase.strip())
        except:
            pass
    return words


def compute_default_pivot_position(ngram_size):
    return (ngram_size // 2) if (ngram_size % 2) == 0 else (ngram_size // 2) + 1


def get_ngrams_wt_term_outside_ene(filename, frequency_dict_geo, ngram_id, label='1', position=None, ngram_size=7):
    json_content = []
    print_content = ''
    if os.path.exists(filename):
        if position is None:
            position = compute_default_pivot_position(ngram_size)
        try:
            tree = etree.parse(filename)
            tokens = tree.xpath('.//w')
            for i, token in enumerate(tokens):
                print_content = ''
                if token.text in frequency_dict_geo:
                    line = {'num':ngram_id, 'class':label, 'id_phrase':'0','pivot':token.text,'occurrence': '0', 'url':filename}
                    phrase = []
                    for j in range(position-1, 0, -1):
                        try:
                            words = {'word':tokens[i-j].text, 'POS':tokens[i-j].get('pos'), 'lemma':tokens[i-j].get('lemma')}
                            print_content += tokens[i-j].text + ' '
                        except IndexError:
                            words = {'word':'_', 'POS':'_', 'lemma':'_'}
                            print_content += '_ '
                        phrase.append(words)
                        
                    phrase.append({'word':token.text, 'POS':token.get('pos') + '+LS', 'lemma':token.get('lemma')})
                    print_content += '[ ' + token.text + ' ] '
                    for j in range(1, ngram_size+1-position):
                        try:
                            words = {'word':tokens[i+j].text, 'POS':tokens[i-j].get('pos'), 'lemma':tokens[i-j].get('lemma')}
                            print_content += tokens[i+j].text + ' '
                        except IndexError:
                            words = {'word':'_', 'POS':'_', 'lemma':'_'}
                            print_content += '_ '
                        phrase.append(words)
                        
                    print(print_content)
                    line['phrase'] = phrase
                    
                    ngram_id += 1
                    json_content.append(line)
        except:
            pass
    
    return json_content


def get_ngrams(input_path, frequency_dicts, position=None, ngram_size=7):
    json_content = []
    if position is None:
        position = compute_default_pivot_position(ngram_size)
    ngram_id = 1
    for file in sorted(os.listdir(input_path)):
        filename = os.path.join(input_path, file)
        json_content.extend(get_ngrams_wt_term_outside_ene(filename, frequency_dicts, ngram_id, position=position, ngram_size=ngram_size))
    print('Number of ngrams:', len(json_content))
    return json_content


def load_json(filename):
    with open(filename) as fp:
        return json.load(fp)
    

def save_json(filename, data):
    with open(filename, 'w') as fp:
        json.dump(data, fp, ensure_ascii=False)


def load_edda_dataframe(edda_dataset_path, domain=None):
    data = pd.read_csv(edda_dataset_path, sep='\t')
    data.rename(columns={'edda-superdomainPred1':'domain'}, inplace=True)
    if domain:
        data = data[data['domain'] == domain]
    return data[['volume', 'numero', 'head', 'author','content', 'domain']]


def segment_sentences(text):
    sentences = sent_tokenize(text_preprocessing(text))
    return sentences


def get_lexicon_occurrences(terms, lexicon=None):
    if lexicon is None:
        lexicon = terms
    return {value: terms.count(value) for value in lexicon}

