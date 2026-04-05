"""
PolicyPilot — Backend Server
Helps Indian citizens discover government schemes tailored to their profile.
Includes a natural language parser for conversational queries.
"""

import json
import re
import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "super_secret_policypilot_key_dev")

# Load schemes database (Reloads on start again)
SCHEMES_PATH = os.path.join(os.path.dirname(__file__), "schemes.json")
with open(SCHEMES_PATH, "r", encoding="utf-8") as f:
    SCHEMES = json.load(f)

# -------------------------------------------------------------------
# Indian states list
# -------------------------------------------------------------------
INDIAN_STATES = [
    "andhra pradesh", "arunachal pradesh", "assam", "bihar", "chhattisgarh",
    "goa", "gujarat", "haryana", "himachal pradesh", "jharkhand",
    "karnataka", "kerala", "madhya pradesh", "maharashtra", "manipur",
    "meghalaya", "mizoram", "nagaland", "odisha", "punjab",
    "rajasthan", "sikkim", "tamil nadu", "telangana", "tripura",
    "uttar pradesh", "uttarakhand", "west bengal",
    "andaman and nicobar islands", "chandigarh", "dadra and nagar haveli and daman and diu",
    "delhi", "jammu and kashmir", "ladakh", "lakshadweep", "puducherry"
]

# State abbreviations
STATE_ALIASES = {
    "up": "uttar pradesh", "mp": "madhya pradesh", "hp": "himachal pradesh",
    "ap": "andhra pradesh", "tn": "tamil nadu", "wb": "west bengal",
    "jk": "jammu and kashmir", "uk": "uttarakhand", "j&k": "jammu and kashmir",
    "cg": "chhattisgarh", "jh": "jharkhand", "mh": "maharashtra",
    "ka": "karnataka", "ts": "telangana", "rj": "rajasthan",
    "gj": "gujarat", "hr": "haryana", "pb": "punjab",
    "dl": "delhi", "ncr": "delhi", "mumbai": "maharashtra",
    "bangalore": "karnataka", "bengaluru": "karnataka",
    "chennai": "tamil nadu", "hyderabad": "telangana",
    "kolkata": "west bengal", "lucknow": "uttar pradesh",
    "jaipur": "rajasthan", "ahmedabad": "gujarat",
    "pune": "maharashtra", "bhopal": "madhya pradesh",
    "patna": "bihar", "ranchi": "jharkhand",
    "dehradun": "uttarakhand", "shimla": "himachal pradesh",
    "chandigarh city": "chandigarh", "srinagar": "jammu and kashmir",
    "guwahati": "assam", "bhubaneswar": "odisha",
    "thiruvananthapuram": "kerala", "trivandrum": "kerala",
    "indore": "madhya pradesh", "nagpur": "maharashtra",
    "varanasi": "uttar pradesh", "noida": "uttar pradesh",
    "gurgaon": "haryana", "gurugram": "haryana",
    "faridabad": "haryana", "ghaziabad": "uttar pradesh",
}

# Occupation keywords
OCCUPATION_MAP = {
    "farmer": ["farmer", "kisan", "farming", "agriculture", "kheti", "cultivation", "crop"],
    "student": ["student", "studying", "college", "school", "university", "vidyarthi", "padhai", "education"],
    "self_employed": ["self employed", "self-employed", "freelancer", "small business", "shop", "dukan"],
    "business": ["business", "businessman", "businesswoman", "company", "enterprise", "vyapari", "trading"],
    "entrepreneur": ["entrepreneur", "startup", "founder", "innovator"],
    "laborer": ["laborer", "labourer", "labor", "labour", "mazdoor", "worker", "construction"],
    "daily_wage": ["daily wage", "daily wager", "daily income", "dihadi"],
    "artisan": ["artisan", "craftsman", "craftsperson", "carpenter", "blacksmith", "potter", "tailor",
                "weaver", "goldsmith", "cobbler", "barber", "nai", "kumhar", "lohar", "sunar",
                "darzi", "handicraft", "karigari"],
    "street_vendor": ["street vendor", "hawker", "vendor", "thela", "pheriwala", "rehri"],
    "unemployed": ["unemployed", "jobless", "no job", "berozgar", "looking for work", "job seeker"],
    "government_employee": ["government employee", "sarkari naukri", "govt employee", "government job",
                            "govt job", "psu"],
    "private_employee": ["private job", "private employee", "it professional", "software", "engineer",
                         "private sector", "naukri"],
    "homemaker": ["homemaker", "housewife", "ghar", "home maker"],
}

# Category keywords
CATEGORY_MAP = {
    "sc": ["sc", "scheduled caste", "dalit", "chamar"],
    "st": ["st", "scheduled tribe", "tribal", "adivasi"],
    "obc": ["obc", "other backward class", "backward class", "backward"],
    "general": ["general", "gen", "unreserved", "open category"],
}

# Condition keywords
CONDITION_MAP = {
    "disability": ["disability", "disabled", "handicap", "divyang", "pwd", "physically challenged"],
    "student": ["student", "studying", "college", "school", "padhai"],
    "farmer": ["farmer", "kisan", "farming", "agriculture", "kheti"],
    "senior_citizen": ["senior citizen", "old age", "elderly", "aged", "retired", "buzurg"],
    "widow": ["widow", "vidhwa"],
    "street_vendor": ["street vendor", "hawker", "thela", "pheriwala", "rehri"],
    "artisan": ["artisan", "craftsman", "craftsperson", "carpenter", "blacksmith", "potter",
                "tailor", "weaver", "cobbler", "barber", "handicraft"],
    "rural": ["rural", "village", "gaon", "gram"],
    "parent_of_girl_child": ["daughter", "girl child", "beti", "ladki"],
    "woman_head": ["woman head", "female head", "single mother", "woman-headed"],
}

# Gender keywords
GENDER_MAP = {
    "male": ["male", "man", "boy", "ladka", "purush", "aadmi"],
    "female": ["female", "woman", "girl", "lady", "ladki", "mahila", "aurat", "stree"],
    "other": ["other", "transgender", "third gender"],
}


# -------------------------------------------------------------------
# Natural Language Parser
# -------------------------------------------------------------------
def parse_natural_query(text):
    """
    Parse a natural language query to extract user profile details.
    Returns a dict of extracted fields and a list of missing fields.
    """
    text_lower = text.lower().strip()
    profile = {}
    missing = []

    # --- Extract age ---
    age_patterns = [
        r"(?:i am|i'm|age is|age|aged|umr)\s*[:=]?\s*(\d{1,3})",
        r"(\d{1,3})\s*(?:years?\s*old|yrs?\s*old|sal\b|saal\b|varsh)",
        r"(?:meri umr|mera age|my age)\s*[:=]?\s*(\d{1,3})",
    ]
    for pattern in age_patterns:
        match = re.search(pattern, text_lower)
        if match:
            age = int(match.group(1))
            if 0 < age < 120:
                profile["age"] = age
                break
    if "age" not in profile:
        missing.append("age")

    # --- Extract income ---
    income_patterns = [
        r"(?:income|salary|kamai|aay|kamata|kamati|earn)\s*(?:is|of|[:=])?\s*(?:rs\.?|₹|inr)?\s*([\d,]+)\s*(?:lakh|lac|lpa)?",
        r"(?:rs\.?|₹|inr)\s*([\d,]+)\s*(?:per\s*(?:year|month|annum))?",
        r"(\d[\d,]*)\s*(?:lpa|per\s*annum|per\s*year|sal(?:ana)?)",
        r"(?:income|salary|earn)\s*(?:around|about|approximately)?\s*(?:rs\.?|₹)?\s*([\d,]+)",
        r"(\d+)\s*(?:lakh|lac)\s*(?:per\s*(?:year|month|annum))?",
    ]
    for pattern in income_patterns:
        match = re.search(pattern, text_lower)
        if match:
            income_str = match.group(1).replace(",", "")
            income = int(income_str)
            # Check if "lakh" is mentioned
            if re.search(r"lakh|lac", text_lower[match.start():match.end() + 20]):
                income *= 100000
            elif income < 200:  # Likely in lakhs
                income *= 100000
            profile["income"] = income
            break
    if "income" not in profile:
        # Check for poverty indicators
        if any(w in text_lower for w in ["poor", "garib", "bpl", "below poverty", "no income", "low income"]):
            profile["income"] = 100000
        else:
            missing.append("income")

    # --- Extract state ---
    for alias, state in STATE_ALIASES.items():
        if re.search(r'\b' + re.escape(alias) + r'\b', text_lower):
            profile["state"] = state
            break
    if "state" not in profile:
        for state in sorted(INDIAN_STATES, key=len, reverse=True):
            if state in text_lower:
                profile["state"] = state
                break
    if "state" not in profile:
        missing.append("state")

    # --- Extract category ---
    for cat, keywords in CATEGORY_MAP.items():
        for kw in keywords:
            if re.search(r'\b' + re.escape(kw) + r'\b', text_lower):
                profile["category"] = cat
                break
        if "category" in profile:
            break
    if "category" not in profile:
        missing.append("category")

    # --- Extract gender ---
    # Try explicit mentions first
    for gen, keywords in GENDER_MAP.items():
        for kw in keywords:
            if re.search(r'\b' + re.escape(kw) + r'\b', text_lower):
                profile["gender"] = gen
                break
        if "gender" in profile:
            break
    if "gender" not in profile:
        missing.append("gender")

    # --- Extract occupation ---
    best_occupation = None
    best_len = 0
    for occ, keywords in OCCUPATION_MAP.items():
        for kw in keywords:
            if kw in text_lower and len(kw) > best_len:
                best_occupation = occ
                best_len = len(kw)
    if best_occupation:
        profile["occupation"] = best_occupation
    else:
        missing.append("occupation")

    # --- Extract special conditions ---
    conditions = []
    for cond, keywords in CONDITION_MAP.items():
        for kw in keywords:
            if kw in text_lower:
                conditions.append(cond)
                break
    profile["conditions"] = conditions

    return profile, missing


def generate_followup_question(missing_fields):
    """Generate a friendly follow-up question for missing fields."""
    questions = {
        "age": "How old are you? (आपकी उम्र क्या है?)",
        "income": "What is your approximate annual income? (आपकी सालाना आमदनी कितनी है?)",
        "state": "Which state do you live in? (आप किस राज्य में रहते हैं?)",
        "category": "What is your category — General, OBC, SC, or ST? (आपकी श्रेणी क्या है?)",
        "gender": "What is your gender? (आपका लिंग क्या है?)",
        "occupation": "What do you do for work? (e.g., farmer, student, business, job) (आप क्या काम करते हैं?)",
    }

    if not missing_fields:
        return None

    parts = []
    for field in missing_fields:
        if field in questions:
            parts.append(questions[field])

    if len(parts) == 1:
        return f"To find the best schemes for you, I need one more detail: {parts[0]}"
    else:
        q_text = "\n".join(f"  • {q}" for q in parts)
        return f"To find the best schemes for you, I need a few more details:\n{q_text}\n\nYou can answer in one message, for example: \"I am 30 years old, male, OBC, from Bihar, income 2 lakh\""


# -------------------------------------------------------------------
# Eligibility Engine
# -------------------------------------------------------------------
def check_eligibility(profile, scheme):
    """Check if a user profile matches a scheme's eligibility criteria."""
    elig = scheme["eligibility"]

    # Age check
    age = profile.get("age", 25)
    if age < elig.get("minAge", 0) or age > elig.get("maxAge", 200):
        return False, 0

    # Income check
    income = profile.get("income", 300000)
    if income > elig.get("maxIncome", 999999999):
        return False, 0

    # Category check
    category = profile.get("category", "general")
    if category not in elig.get("categories", []):
        # Check alsoEligibleIf
        also = elig.get("alsoEligibleIf", {})
        if category not in also.get("categories", []):
            return False, 0

    # Gender check
    gender = profile.get("gender", "male")
    eligible_genders = elig.get("gender", ["male", "female", "other"])
    if gender not in eligible_genders:
        # Check alsoEligibleIf
        also = elig.get("alsoEligibleIf", {})
        if gender not in also.get("gender", []):
            return False, 0

    # Occupation check
    occupation = profile.get("occupation", "")
    eligible_occupations = elig.get("occupations", "all")
    if eligible_occupations != "all":
        if occupation not in eligible_occupations:
            return False, 0

    # State check
    state = profile.get("state", "").lower()
    eligible_states = elig.get("states", "all")
    if eligible_states != "all":
        if state not in [s.lower() for s in eligible_states]:
            return False, 0

    # Required conditions check
    conditions = set(profile.get("conditions", []))
    required_conditions = elig.get("conditions", [])
    if required_conditions:
        if not conditions.intersection(set(required_conditions)):
            # Special handling: if condition matches occupation
            if occupation in required_conditions:
                pass  # occupation already serves as condition
            else:
                return False, 0

    # Exclude conditions check
    exclude = elig.get("excludeConditions", [])
    if exclude and conditions.intersection(set(exclude)):
        return False, 0

    # --- Calculate relevance score ---
    score = 10  # Base score for being eligible

    # Benefit value contributes to score
    benefit_value = scheme.get("benefitValue", 0)
    if benefit_value >= 500000:
        score += 30
    elif benefit_value >= 100000:
        score += 20
    elif benefit_value >= 10000:
        score += 10
    else:
        score += 5

    # Occupation match bonus
    if eligible_occupations != "all" and occupation in eligible_occupations:
        score += 15

    # Category priority bonus
    priority = elig.get("priority", [])
    if category in priority:
        score += 10

    # Gender relevance bonus
    if len(eligible_genders) < 3 and gender in eligible_genders:
        score += 10  # Gender-specific scheme that matches

    # Condition match bonus
    if required_conditions and conditions.intersection(set(required_conditions)):
        score += 15

    # Income-sensitivity: lower income gets higher relevance for welfare schemes
    if income < 200000 and scheme["category"] in ["welfare", "health", "pension", "employment"]:
        score += 10

    # Also eligible via special criteria bonus
    also = elig.get("alsoEligibleIf", {})
    if gender in also.get("gender", []):
        score += 8

    return True, score


import copy

def get_recommendations(profile, lang="en"):
    """Get ranked scheme recommendations for a user profile."""
    eligible = []

    for scheme in SCHEMES:
        is_eligible, score = check_eligibility(profile, scheme)
        if is_eligible:
            eligible.append({
                "scheme": copy.deepcopy(scheme),  # Deep copy to prevent modifying global!
                "score": score,
                "whyQualify": _build_why_qualify(profile, scheme)
            })

    # Sort by score descending
    eligible.sort(key=lambda x: x["score"], reverse=True)

    # Split into top 3 and others
    top3 = eligible[:3]
    others = eligible[3:15] # Limit others to 12
    total_eligible = len(eligible)

    # Use pre-translated fields if requested
    if lang == "hi":
        for item in top3:
            s = item["scheme"]
            s["name"] = s.get("nameHi", s.get("name", ""))
            s["shortName"] = s.get("shortNameHi", s.get("shortName", ""))
            s["benefit"] = s.get("benefitHi", s.get("benefit", ""))
            s["simpleExplanation"] = s.get("simpleExplanationHi", s.get("simpleExplanation", ""))
            s["howToApply"] = s.get("howToApplyHi", s.get("howToApply", []))
            s["documentsRequired"] = s.get("documentsRequiredHi", s.get("documentsRequired", []))
            # Translate whyQualify conditionally if we have basic mapping or just leave it
            item["whyQualify"] = item["whyQualify"].replace('Your age', 'आपकी आयु').replace('is within the eligible range', 'पात्रता सीमा के भीतर है').replace('Your income qualifies you', 'आपकी आय आपको पात्र बनाती है').replace('matches this scheme', 'इस योजना से मेल खाता है')
            
        for item in others:
            s = item["scheme"]
            s["name"] = s.get("nameHi", s.get("name", ""))
            s["shortName"] = s.get("shortNameHi", s.get("shortName", ""))
            s["benefit"] = s.get("benefitHi", s.get("benefit", ""))

    # Aggregate documents
    all_docs = set()
    for item in top3 + others:
        for doc in item["scheme"].get("documentsRequired", []):
            all_docs.add(doc)

    return {
        "top3": [{
            "id": item["scheme"]["id"],
            "name": item["scheme"].get("name"),
            "shortName": item["scheme"].get("shortName"),
            "icon": item["scheme"].get("icon"),
            "category": item["scheme"].get("category"),
            "benefit": item["scheme"].get("benefit"),
            "whyQualify": item["whyQualify"],
            "simpleExplanation": item["scheme"].get("simpleExplanation"),
            "howToApply": item["scheme"].get("howToApply"),
            "officialUrl": item["scheme"].get("officialUrl"),
            "documentsRequired": item["scheme"].get("documentsRequired", []),
            "score": item["score"]
        } for item in top3],
        "others": [{
            "id": item["scheme"]["id"],
            "name": item["scheme"].get("name"),
            "shortName": item["scheme"].get("shortName"),
            "icon": item["scheme"].get("icon"),
            "category": item["scheme"].get("category"),
            "benefit": item["scheme"].get("benefit"),
            "officialUrl": item["scheme"].get("officialUrl"),
            "score": item["score"]
        } for item in others],
        "documentsRequired": sorted(list(all_docs)),
        "totalEligible": total_eligible
    }


def _build_why_qualify(profile, scheme):
    """Build personalized 'why you qualify' text."""
    reasons = []
    elig = scheme["eligibility"]

    age = profile.get("age")
    if age and elig.get("minAge") and elig.get("maxAge"):
        if elig["maxAge"] < 100:
            reasons.append(f"Your age ({age}) is within the eligible range of {elig['minAge']}-{elig['maxAge']} years")

    income = profile.get("income")
    if income and elig.get("maxIncome", 999999999) < 50000000:
        reasons.append(f"Your income qualifies you (scheme limit: ₹{elig['maxIncome']:,})")

    category = profile.get("category", "")
    if category in elig.get("categories", []):
        if category != "general":
            reasons.append(f"Your {category.upper()} category makes you eligible")

    occupation = profile.get("occupation", "")
    eligible_occs = elig.get("occupations", "all")
    if eligible_occs != "all" and occupation in eligible_occs:
        reasons.append(f"Your occupation as a {occupation.replace('_', ' ')} matches this scheme")

    gender = profile.get("gender", "")
    if len(elig.get("gender", [])) < 3 and gender in elig.get("gender", []):
        reasons.append(f"This scheme is specifically for {gender}s")

    conditions = profile.get("conditions", [])
    if conditions:
        matching = set(conditions).intersection(set(elig.get("conditions", [])))
        if matching:
            reasons.append(f"Your profile matches: {', '.join(c.replace('_', ' ') for c in matching)}")

    if not reasons:
        reasons.append(scheme.get("whyQualifyTemplate", "You meet the basic eligibility criteria for this scheme"))

    return " • ".join(reasons)


# -------------------------------------------------------------------
# Flask Routes
# -------------------------------------------------------------------
@app.route("/")
def index():
    if "user_name" in session:
        return redirect(url_for("advisor"))
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    name = request.form.get("name", "").strip()
    if name:
        session["user_name"] = name
    return redirect(url_for("advisor"))


@app.route("/logout")
def logout():
    session.pop("user_name", None)
    return redirect(url_for("index"))


@app.route("/advisor")
def advisor():
    user_name = session.get("user_name", "")
    return render_template("index.html", user_name=user_name)


@app.route("/api/recommend", methods=["POST"])
def recommend():
    """Accept user profile and return scheme recommendations."""
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data received"}), 400

    profile = {
        "age": int(data.get("age", 25)),
        "income": int(data.get("income", 300000)),
        "state": data.get("state", "").lower().strip(),
        "category": data.get("category", "general").lower().strip(),
        "occupation": data.get("occupation", "").lower().strip(),
        "gender": data.get("gender", "male").lower().strip(),
        "conditions": data.get("conditions", []),
    }
    
    lang = data.get("lang", "en")

    results = get_recommendations(profile, lang=lang)
    return jsonify(results)


@app.route("/api/chat", methods=["POST"])
def chat():
    """
    Conversational endpoint: parse natural language,
    extract profile, return schemes or ask follow-up questions.
    """
    data = request.get_json()
    message = data.get("message", "")
    existing_profile = data.get("profile", {})

    if not message.strip():
        return jsonify({
            "type": "question",
            "message": "Hello! 👋 I'm PolicyPilot, your personal government scheme advisor.\n\nTell me about yourself, for example:\n\"I am a 28-year-old farmer from UP, SC category, income 2 lakh\"\n\nOr just say what you do and where you're from, and I'll help you find the best schemes! 🇮🇳",
            "profile": existing_profile
        })

    # Parse the new message
    new_profile, missing = parse_natural_query(message)

    # Merge with existing profile (new values override)
    merged = {**existing_profile}
    for key, value in new_profile.items():
        if key == "conditions":
            existing_conds = set(merged.get("conditions", []))
            existing_conds.update(value)
            merged["conditions"] = list(existing_conds)
        elif value:  # Only override if not empty
            merged[key] = value

    # Recalculate missing fields
    truly_missing = []
    required = ["age", "income", "state", "category", "gender", "occupation"]
    for field in required:
        if field not in merged or not merged[field]:
            truly_missing.append(field)

    # If critical fields are still missing, ask follow-up
    critical_missing = [f for f in truly_missing if f in ["age", "state", "occupation"]]

    lang = data.get("lang", "en")

    if len(critical_missing) >= 2:
        followup = generate_followup_question(truly_missing)
        # Build partial summary
        found_parts = []
        if "occupation" in merged:
            found_parts.append(f"occupation: {merged['occupation']}")
        if "state" in merged:
            found_parts.append(f"state: {merged['state'].title()}")
        if "category" in merged:
            found_parts.append(f"category: {merged['category'].upper()}")
        if "gender" in merged:
            found_parts.append(f"gender: {merged['gender']}")
        if "age" in merged:
            found_parts.append(f"age: {merged['age']}")

        understood = ""
        if found_parts:
            understood = f"Got it! I understand you are: {', '.join(found_parts)}.\n\n"

        msg = understood + followup
        
        return jsonify({
            "type": "question",
            "message": msg,
            "profile": merged
        })

    # Fill in reasonable defaults for non-critical missing fields
    if "age" not in merged:
        merged["age"] = 30
    if "income" not in merged:
        merged["income"] = 300000
    if "state" not in merged:
        merged["state"] = ""
    if "category" not in merged:
        merged["category"] = "general"
    if "gender" not in merged:
        merged["gender"] = "male"
    if "occupation" not in merged:
        merged["occupation"] = "private_employee"
    if "conditions" not in merged:
        merged["conditions"] = []

    # Sync occupation with conditions
    occ = merged["occupation"]
    if occ == "farmer" and "farmer" not in merged["conditions"]:
        merged["conditions"].append("farmer")
    if occ == "student" and "student" not in merged["conditions"]:
        merged["conditions"].append("student")
    if occ == "artisan" and "artisan" not in merged["conditions"]:
        merged["conditions"].append("artisan")
    if occ == "street_vendor" and "street_vendor" not in merged["conditions"]:
        merged["conditions"].append("street_vendor")

    # Get recommendations
    results = get_recommendations(merged, lang=lang)

    # Build summary line
    desc_parts = []
    if merged.get("age"):
        desc_parts.append(f"{merged['age']} year old")
    if merged.get("gender"):
        desc_parts.append(merged["gender"])
    if merged.get("category") and merged["category"] != "general":
        desc_parts.append(merged["category"].upper())
    if merged.get("occupation"):
        desc_parts.append(merged["occupation"].replace("_", " "))
    if merged.get("state"):
        desc_parts.append(f"from {merged['state'].title()}")

    summary = " ".join(desc_parts).strip()

    # Note about defaults
    defaults_used = []
    for field in truly_missing:
        if field == "income":
            defaults_used.append("income (assumed ₹3 lakh/year)")
        elif field == "category":
            defaults_used.append("category (assumed General)")
        elif field == "gender":
            defaults_used.append("gender (assumed male)")

    defaults_note = ""
    if defaults_used:
        defaults_note = f"\n\n💡 Note: I assumed some details — {', '.join(defaults_used)}. You can refine your profile for more accurate results."

    final_message = f"Here are the best government schemes for you as a {summary}! 🎯{defaults_note}"

    if lang == "hi":
        if "Here are the best" in final_message:
            final_message = "यहाँ आपके लिए सर्वश्रेष्ठ सरकारी योजनाएं हैं! 🎯"
        
        msg = "मुझे समझ आ गया है कि आप हैं: " + ", ".join(found_parts) + ".\n\n" + followup if 'found_parts' in locals() and found_parts else followup

    return jsonify({
        "type": "results",
        "message": final_message,
        "profile": merged,
        "results": results
    })


@app.route("/api/scheme/<scheme_id>", methods=["GET"])
def scheme_detail(scheme_id):
    """Get full details of a specific scheme."""
    for scheme in SCHEMES:
        if scheme["id"] == scheme_id:
            return jsonify(scheme)
    return jsonify({"error": "Scheme not found"}), 404


if __name__ == "__main__":
    app.run(debug=True, port=5000)
