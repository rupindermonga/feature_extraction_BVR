import spacy
import sys
import glob
import json
import os
import csv

nlp = spacy.load('en_core_web_sm')

# in_slug = sys.argv[1]
path_to_json = '/media/rupinder/C49A5A1B9A5A0A76/Users/Rupinder/Desktop/BVR/feature_analysis-master/electric-kettles'
texts = []
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
count = 0
# for f in glob.iglob('/media/rupinder/C49A5A1B9A5A0A76/Users/Rupinder/Desktop/BVR/Warning_code/feature_analysis-master/electric-kettles*.json'.format(in_slug)):
# for f in glob.iglob('/media/rupinder/C49A5A1B9A5A0A76/Users/Rupinder/Desktop/BVR/Warning_code/feature_analysis-master/electric-kettles*.json'):
for filename in json_files:
    with open(os.path.join(path_to_json, filename)) as f:
        data = json.load(f)
        try:
            for r in data['reviews']:
                count += 1
                if count == 5:
                    break   
                text = r.get('reviewText','').strip()
                if text != '':
                    texts.append(text)
        except:
            pass
docs = nlp.pipe(texts)

freq = {}

for doc in docs:
    for chunk in doc.noun_chunks:
        tokens = [t.lemma_ for t in chunk if not t.is_stop and t.lemma_ not in ['-PRON-']]
        lemma = ' '.join(tokens).strip()
        if lemma not in ['-PRON-','']:
            freq[lemma] = freq.get(lemma,0) + 1

# out = csv.writer(open('/media/rupinder/C49A5A1B9A5A0A76/Users/Rupinder/Desktop/BVR/Warning_code/feature_analysis-master/electric-kettles/ek.csv'.format(in_slug),'w'))
out = csv.writer(open('/media/rupinder/C49A5A1B9A5A0A76/Users/Rupinder/Desktop/BVR/feature_analysis-master/electric-kettles/ek.csv','w'))

sort = sorted(freq, key=lambda k:freq[k], reverse=True)
for s in sort:
    out.writerow([s,freq[s]])
    
        
    
