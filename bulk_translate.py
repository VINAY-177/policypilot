import json
import os
import time
from deep_translator import GoogleTranslator

# Note: this script uses threading/batching internally inside the deep-translator,
# or we can do chunked translated to avoid hitting limits.

SCHEMES_PATH = os.path.join(os.path.dirname(__file__), "schemes.json")
with open(SCHEMES_PATH, "r", encoding="utf-8") as f:
    schemes = json.load(f)

translator = GoogleTranslator(source='en', target='hi')
delimiter = " ~|~ "

def bulk_translate(texts):
    if not texts:
        return []
    
    # We do chunks of 50 strings
    chunk_size = 50
    final_res = []
    
    for i in range(0, len(texts), chunk_size):
        chunk = texts[i:i+chunk_size]
        joined = delimiter.join(chunk)
        
        try:
            res = translator.translate(joined)
            if not res:
                final_res.extend(chunk)
                continue
            
            res_parts = res.replace(" ~| ~ ", delimiter).replace(" ~ | ~ ", delimiter).replace("~|~", delimiter).split(delimiter)
            
            for j in range(len(chunk)):
                if j < len(res_parts) and res_parts[j]:
                    final_res.append(res_parts[j].strip())
                else:
                    final_res.append(chunk[j])
        except Exception as e:
            print(f"Error chunk {i}: {e}")
            final_res.extend(chunk)
            
        time.sleep(1) # slight delay to avoid rate limit
        
    return final_res

print("Starting bulk translation for Schemes...")

# 1. Collect all english texts
all_texts = []
mapping = [] # (scheme_index, field_name, is_list, list_index)

for idx, s in enumerate(schemes):
    # Only translate if we haven't already
    if "nameHi" not in s:
        all_texts.append(s.get("name", ""))
        mapping.append((idx, "nameHi", False, 0))
        
        all_texts.append(s.get("shortName", ""))
        mapping.append((idx, "shortNameHi", False, 0))
        
        all_texts.append(s.get("benefit", ""))
        mapping.append((idx, "benefitHi", False, 0))
        
        all_texts.append(s.get("simpleExplanation", ""))
        mapping.append((idx, "simpleExplanationHi", False, 0))
        
        docs = s.get("documentsRequired", [])
        for di, doc in enumerate(docs):
            all_texts.append(doc)
            mapping.append((idx, "documentsRequiredHi", True, di))
            
        Applys = s.get("howToApply", [])
        for api, app in enumerate(Applys):
            all_texts.append(app)
            mapping.append((idx, "howToApplyHi", True, api))

print(f"Total texts to translate: {len(all_texts)}")

if all_texts:
    # 2. Translate bulk
    translated_texts = bulk_translate(all_texts)
    
    # 3. Apply back to schemes
    for k in range(len(mapping)):
        idx, field, is_list, list_index = mapping[k]
        val = translated_texts[k] if k < len(translated_texts) else all_texts[k]
        
        if is_list:
            if field not in schemes[idx]:
                if "documentsRequired" in field:
                    schemes[idx][field] = [""] * len(schemes[idx].get("documentsRequired", []))
                else:
                    schemes[idx][field] = [""] * len(schemes[idx].get("howToApply", []))
            if list_index < len(schemes[idx][field]):
                schemes[idx][field][list_index] = val
        else:
            schemes[idx][field] = val

    # 4. Save
    with open(SCHEMES_PATH, "w", encoding="utf-8") as f:
        json.dump(schemes, f, indent=4, ensure_ascii=False)
        
    print("Saved translations successfully.")
else:
    print("Already translated everything.")
