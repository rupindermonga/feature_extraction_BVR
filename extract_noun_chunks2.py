import spacy
import sys
import glob
import json
import os
import csv
import time
import pandas as pd

start_time = time.time()
nlp = spacy.load('en_core_web_sm')

# in_slug = sys.argv[1]
path_to_json = '/media/rupinder/C49A5A1B9A5A0A76/Users/Rupinder/Desktop/BVR/feature_analysis-master/coffee-grinder'
texts = []
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]

# for f in glob.iglob('/media/rupinder/C49A5A1B9A5A0A76/Users/Rupinder/Desktop/BVR/Warning_code/feature_analysis-master/electric-kettles*.json'.format(in_slug)):
# for f in glob.iglob('/media/rupinder/C49A5A1B9A5A0A76/Users/Rupinder/Desktop/BVR/Warning_code/feature_analysis-master/electric-kettles*.json'):
final_dict = {}
new_count = 0
count = 0
for filename in json_files:        
    with open(os.path.join(path_to_json, filename)) as f:
        data = json.load(f)
        try:
            if len(data['reviews']) < 50:
                break
            else:
                count += 1
                if count <= 5:
                    for r in data['reviews']:
                        # count += 1
                        # if count == 5:
                        #     break   
                        text = r.get('reviewText','').lower().strip() #lowered all chunks
                        if text != '':
                            texts.append(text)
                else:
                    break
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
    final_dict[filename] = freq
    new_count += 1
    print(filename)
    print(new_count)
    print(time.time()- start_time)
# docs = nlp.pipe(texts)

# freq = {}

# for doc in docs:
#     for chunk in doc.noun_chunks:
#         tokens = [t.lemma_ for t in chunk if not t.is_stop and t.lemma_ not in ['-PRON-']]
#         lemma = ' '.join(tokens).strip()
#         if lemma not in ['-PRON-','']:
#             freq[lemma] = freq.get(lemma,0) + 1



# out = csv.writer(open('/media/rupinder/C49A5A1B9A5A0A76/Users/Rupinder/Desktop/BVR/Warning_code/feature_analysis-master/electric-kettles/ek.csv'.format(in_slug),'w'))
out = csv.writer(open(os.path.join(path_to_json, "ek.csv"),'w'))
# out2 = csv.writer(open(os.path.join(path_to_json, "ek2.csv"),'w'))


# out = csv.writer(open('/media/rupinder/C49A5A1B9A5A0A76/Users/Rupinder/Desktop/BVR/feature_analysis-master/electric-kettles/ek1.csv','w'))
# out2 = csv.writer(open('/media/rupinder/C49A5A1B9A5A0A76/Users/Rupinder/Desktop/BVR/feature_analysis-master/electric-kettles/ek2.csv','w'))

# with open(os.path.join(path_to_json, 'ek1.json'), 'w') as outfile:
#     json.dump(final_dict, outfile)


for k, v in final_dict.items():
    sort = sorted(v, key=lambda k1:v[k1], reverse=True)
    for s in sort:
        out.writerow([s,k,v[s]])


# for k, v in final_dict.items():
#     sort = sorted(v, key=lambda k1:v[k1], reverse=True)
#     for s in sort:
#         if v[s] > 100:
#             out2.writerow([s,k,v[s]])

updated_data = pd.read_csv(os.path.join(path_to_json, "ek.csv"))
# sort = sorted(freq, key=lambda k:freq[k], reverse=True)
# for s in sort:
#     out.writerow([s,freq[s]])

print(type(updated_data))
# updated_data['']

updated_data.columns = ['noun_chunk', 'product', 'freq']

updated_data['overall_freq'] = updated_data.groupby('noun_chunk').freq.transform('sum')

updated_data["Rank"] = updated_data["overall_freq"].rank( ascending = False, method = "dense")

updated_data.sort_values("Rank", inplace = True)

updated_data.to_csv(os.path.join(path_to_json, "cg_final.csv"))
print(time.time()-start_time)
    
