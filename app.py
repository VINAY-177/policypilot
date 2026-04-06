"""
Yojana Mitra — Backend Server
Helps Indian citizens discover government schemes tailored to their profile.
Includes a natural language parser for conversational queries.
"""

import json
import re
import os
import sqlite3
import psycopg2
import psycopg2.extras
from datetime import timedelta
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "super_secret_yojanamitra_key_dev")
app.permanent_session_lifetime = timedelta(days=30)

DATABASE_URL = os.environ.get("DATABASE_URL")

if os.environ.get("VERCEL") and not DATABASE_URL:
    DB_PATH = "/tmp/database.db"
else:
    DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")

def get_db_connection():
    if DATABASE_URL:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    else:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

def init_db():
    conn = get_db_connection()
    if DATABASE_URL:
        with conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    phone TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL
                )
            ''')
            cur.execute('''
                CREATE TABLE IF NOT EXISTS saved_schemes (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    scheme_id TEXT NOT NULL,
                    scheme_name TEXT NOT NULL,
                    scheme_icon TEXT DEFAULT '',
                    scheme_benefit TEXT DEFAULT '',
                    saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(user_id, scheme_id)
                )
            ''')
        conn.commit()
    else:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS saved_schemes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                scheme_id TEXT NOT NULL,
                scheme_name TEXT NOT NULL,
                scheme_icon TEXT DEFAULT '',
                scheme_benefit TEXT DEFAULT '',
                saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, scheme_id)
            )
        ''')
        conn.commit()
    conn.close()

def create_user(name, phone, password_hash):
    conn = get_db_connection()
    try:
        if DATABASE_URL:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO users (name, phone, password_hash) VALUES (%s, %s, %s)",
                    (name, phone, password_hash)
                )
        else:
            conn.execute(
                "INSERT INTO users (name, phone, password_hash) VALUES (?, ?, ?)",
                (name, phone, password_hash)
            )
        conn.commit()
        return True
    except Exception as e:
        return False
    finally:
        conn.close()

def get_user_by_phone(phone):
    conn = get_db_connection()
    user = None
    if DATABASE_URL:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT id, name, phone, password_hash FROM users WHERE phone = %s", (phone,))
            user = cur.fetchone()
    else:
        user = conn.execute("SELECT id, name, phone, password_hash FROM users WHERE phone = ?", (phone,)).fetchone()
    conn.close()
    return user

def save_scheme(user_id, scheme_id, scheme_name, scheme_icon, scheme_benefit):
    conn = get_db_connection()
    try:
        if DATABASE_URL:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO saved_schemes (user_id, scheme_id, scheme_name, scheme_icon, scheme_benefit) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (user_id, scheme_id) DO NOTHING",
                    (user_id, scheme_id, scheme_name, scheme_icon, scheme_benefit)
                )
        else:
            conn.execute(
                "INSERT OR IGNORE INTO saved_schemes (user_id, scheme_id, scheme_name, scheme_icon, scheme_benefit) VALUES (?, ?, ?, ?, ?)",
                (user_id, scheme_id, scheme_name, scheme_icon, scheme_benefit)
            )
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()

def unsave_scheme(user_id, scheme_id):
    conn = get_db_connection()
    try:
        if DATABASE_URL:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM saved_schemes WHERE user_id = %s AND scheme_id = %s", (user_id, scheme_id))
        else:
            conn.execute("DELETE FROM saved_schemes WHERE user_id = ? AND scheme_id = ?", (user_id, scheme_id))
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()

def get_saved_schemes(user_id):
    conn = get_db_connection()
    schemes = []
    if DATABASE_URL:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT scheme_id, scheme_name, scheme_icon, scheme_benefit FROM saved_schemes WHERE user_id = %s ORDER BY saved_at DESC", (user_id,))
            schemes = cur.fetchall()
    else:
        rows = conn.execute("SELECT scheme_id, scheme_name, scheme_icon, scheme_benefit FROM saved_schemes WHERE user_id = ? ORDER BY saved_at DESC", (user_id,)).fetchall()
        schemes = [dict(r) for r in rows]
    conn.close()
    return schemes

with app.app_context():
    init_db()

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


def generate_followup_question(missing_fields, lang="en"):
    """Generate a friendly follow-up question for missing fields."""
    questions_en = {
        "age": "How old are you?",
        "income": "What is your approximate annual income?",
        "state": "Which state do you live in?",
        "category": "What is your category — General, OBC, SC, or ST?",
        "gender": "What is your gender?",
        "occupation": "What do you do for work? (e.g., farmer, student, business, job)",
    }
    questions_hi = {
        "age": "आपकी उम्र क्या है?",
        "income": "आपकी अनुमानित सालाना आमदनी कितनी है?",
        "state": "आप किस राज्य में रहते हैं?",
        "category": "आपकी श्रेणी क्या है — सामान्य, OBC, SC, या ST?",
        "gender": "आपका लिंग क्या है?",
        "occupation": "आप क्या काम करते हैं? (जैसे: किसान, विद्यार्थी, व्यापार, नौकरी)",
    }
    questions = questions_hi if lang == "hi" else questions_en

    if not missing_fields:
        return None

    parts = []
    for field in missing_fields:
        if field in questions:
            parts.append(questions[field])

    if lang == "hi":
        if len(parts) == 1:
            return f"आपके लिए सर्वोत्तम योजनाएं खोजने के लिए, मुझे एक और जानकारी चाहिए: {parts[0]}"
        else:
            q_text = "\n".join(f"  • {q}" for q in parts)
            return f"आपके लिए सर्वोत्तम योजनाएं खोजने के लिए, मुझे कुछ और जानकारी चाहिए:\n{q_text}\n\nआप एक ही संदेश में जवाब दे सकते हैं, जैसे: \"मैं 30 साल का हूं, पुरुष, OBC, बिहार से, आय 2 लाख\""
    else:
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

    # Show ALL valid schemes instead of just the top 3
    top3 = eligible
    others = []
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
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("index"))
        return f(*args, **kwargs)
    return decorated_function


@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("home"))
    return render_template("login.html")


@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name", "").strip()
    phone = request.form.get("phone", "").strip()
    password = request.form.get("password", "")
    
    if not name or not phone or not password:
        flash("All fields are required")
        return redirect(url_for("index"))
        
    success = create_user(name, phone, generate_password_hash(password))
    
    if not success:
        flash("Phone number already registered. Please sign in.")
        return redirect(url_for("index"))
        
    user = get_user_by_phone(phone)
    
    session.permanent = True
    session["user_id"] = user["id"]
    session["user_name"] = user["name"]
    session["user_phone"] = phone
    return redirect(url_for("home"))


@app.route("/login", methods=["POST"])
def login():
    phone = request.form.get("phone", "").strip()
    password = request.form.get("password", "")
    
    user = get_user_by_phone(phone)
    
    if user and check_password_hash(user["password_hash"], password):
        session.permanent = True
        session["user_id"] = user["id"]
        session["user_name"] = user["name"]
        session["user_phone"] = user["phone"]
        return redirect(url_for("home"))
    else:
        flash("Invalid phone number or password")
        return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/home")
@login_required
def home():
    saved = get_saved_schemes(session.get("user_id"))
    return render_template("home.html", user_name=session.get("user_name"), user_phone=session.get("user_phone"), saved_schemes=saved)


@app.route("/dashboard")
@login_required
def dashboard():
    saved = get_saved_schemes(session.get("user_id"))
    return render_template("dashboard.html", user_name=session.get("user_name"), user_phone=session.get("user_phone"), saved_schemes=saved)


@app.route("/api/save-scheme", methods=["POST"])
@login_required
def api_save_scheme():
    data = request.get_json()
    scheme_id = data.get("scheme_id", "")
    scheme_name = data.get("scheme_name", "")
    scheme_icon = data.get("scheme_icon", "")
    scheme_benefit = data.get("scheme_benefit", "")
    if not scheme_id:
        return jsonify({"error": "Missing scheme_id"}), 400
    success = save_scheme(session["user_id"], scheme_id, scheme_name, scheme_icon, scheme_benefit)
    return jsonify({"saved": success})


@app.route("/api/unsave-scheme", methods=["POST"])
@login_required
def api_unsave_scheme():
    data = request.get_json()
    scheme_id = data.get("scheme_id", "")
    if not scheme_id:
        return jsonify({"error": "Missing scheme_id"}), 400
    success = unsave_scheme(session["user_id"], scheme_id)
    return jsonify({"unsaved": success})


@app.route("/api/saved-schemes")
@login_required
def api_saved_schemes():
    saved = get_saved_schemes(session.get("user_id"))
    return jsonify({"schemes": saved})


@app.route("/advisor")
@login_required
def advisor():
    return render_template("index.html", user_name=session.get("user_name"))


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

    lang = data.get("lang", "en")

    if not message.strip():
        if lang == "hi":
            greeting = "नमस्ते! 👋 मैं योजना मित्र हूं, आपका सरकारी योजना सलाहकार।\n\nमुझे अपने बारे में बताइए, जैसे:\n\"मैं 28 साल का किसान हूं, UP से, SC श्रेणी, आय 2 लाख\"\n\nया बस बताइए आप क्या करते हैं और कहां से हैं, मैं आपके लिए सबसे अच्छी योजनाएं खोजूंगा!"
        else:
            greeting = "Hello! 👋 I'm Yojana Mitra, your personal government scheme advisor.\n\nTell me about yourself, for example:\n\"I am a 28-year-old farmer from UP, SC category, income 2 lakh\"\n\nOr just say what you do and where you're from, and I'll help you find the best schemes!"
        return jsonify({
            "type": "question",
            "message": greeting,
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
        followup = generate_followup_question(truly_missing, lang=lang)
        # Build partial summary
        found_parts = []
        if lang == "hi":
            if "occupation" in merged:
                found_parts.append(f"पेशा: {merged['occupation']}")
            if "state" in merged:
                found_parts.append(f"राज्य: {merged['state'].title()}")
            if "category" in merged:
                found_parts.append(f"श्रेणी: {merged['category'].upper()}")
            if "gender" in merged:
                found_parts.append(f"लिंग: {merged['gender']}")
            if "age" in merged:
                found_parts.append(f"आयु: {merged['age']}")
            understood = ""
            if found_parts:
                understood = f"समझ गया! आप हैं: {', '.join(found_parts)}।\n\n"
        else:
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
    if lang == "hi":
        defaults_used = []
        for field in truly_missing:
            if field == "income":
                defaults_used.append("आय (अनुमानित ₹3 लाख/वर्ष)")
            elif field == "category":
                defaults_used.append("श्रेणी (अनुमानित सामान्य)")
            elif field == "gender":
                defaults_used.append("लिंग (अनुमानित पुरुष)")

        defaults_note = ""
        if defaults_used:
            defaults_note = f"\n\n💡 नोट: मैंने कुछ जानकारी अनुमानित की है — {', '.join(defaults_used)}। अधिक सटीक परिणामों के लिए अपनी प्रोफ़ाइल परिष्कृत करें।"

        final_message = f"यहाँ आपके लिए सर्वश्रेष्ठ सरकारी योजनाएं हैं! 🎯{defaults_note}"
    else:
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


# -------------------------------------------------------------------
# Scheme Discussion / Q&A
# -------------------------------------------------------------------
def find_schemes_by_keyword(query):
    """Search schemes by keyword in name, benefit, or category."""
    query_lower = query.lower().strip()
    matches = []
    for scheme in SCHEMES:
        searchable = " ".join([
            scheme.get("name", ""),
            scheme.get("shortName", ""),
            scheme.get("benefit", ""),
            scheme.get("category", ""),
            scheme.get("simpleExplanation", ""),
            scheme.get("id", "")
        ]).lower()
        if query_lower in searchable:
            matches.append(scheme)
    return matches[:10]  # Limit to 10 results


def build_scheme_answer(scheme, question, lang="en"):
    """Build a detailed answer about a scheme based on the user's question."""
    q = question.lower()
    parts = []

    # Use Hindi fields if available
    name = scheme.get("nameHi", scheme.get("name", "")) if lang == "hi" else scheme.get("name", "")
    benefit = scheme.get("benefitHi", scheme.get("benefit", "")) if lang == "hi" else scheme.get("benefit", "N/A")
    explanation = scheme.get("simpleExplanationHi", scheme.get("simpleExplanation", "")) if lang == "hi" else scheme.get("simpleExplanation", "")
    how_steps = scheme.get("howToApplyHi", scheme.get("howToApply", [])) if lang == "hi" else scheme.get("howToApply", [])
    docs = scheme.get("documentsRequiredHi", scheme.get("documentsRequired", [])) if lang == "hi" else scheme.get("documentsRequired", [])

    # Header
    parts.append(f"**{scheme.get('icon','')} {name}**")
    parts.append("")

    # Determine what the user is asking about
    asks_docs = any(w in q for w in ["document", "docs", "paper", "kagaz", "dastavez", "proof", "certificate"])
    asks_apply = any(w in q for w in ["apply", "how to", "register", "aavedan", "kaise", "process", "step"])
    asks_eligible = any(w in q for w in ["eligible", "qualify", "patra", "yogya", "who can", "kaun", "criteria"])
    asks_benefit = any(w in q for w in ["benefit", "amount", "money", "kitna", "labh", "paisa", "value", "how much"])
    asks_general = not (asks_docs or asks_apply or asks_eligible or asks_benefit)

    lbl_benefit = "लाभ" if lang == "hi" else "Benefit"
    lbl_elig = "पात्रता" if lang == "hi" else "Eligibility"
    lbl_apply = "आवेदन कैसे करें" if lang == "hi" else "How to Apply"
    lbl_docs = "आवश्यक दस्तावेज़" if lang == "hi" else "Documents Required"
    lbl_website = "आधिकारिक वेबसाइट" if lang == "hi" else "Official Website"
    lbl_age = "आयु" if lang == "hi" else "Age"
    lbl_income = "अधिकतम आय" if lang == "hi" else "Max Income"
    lbl_cats = "श्रेणियां" if lang == "hi" else "Categories"
    lbl_gender = "लिंग" if lang == "hi" else "Gender"
    lbl_states = "राज्य" if lang == "hi" else "States"
    lbl_years = "वर्ष" if lang == "hi" else "years"

    if asks_general or asks_benefit:
        parts.append(f"💰 **{lbl_benefit}:** {benefit}")
        parts.append(f"📝 {explanation}")
        parts.append("")

    if asks_eligible or asks_general:
        elig = scheme.get("eligibility", {})
        parts.append(f"✅ **{lbl_elig}:**")
        if elig.get("minAge") and elig.get("maxAge"):
            parts.append(f"  • {lbl_age}: {elig['minAge']}–{elig['maxAge']} {lbl_years}")
        if elig.get("maxIncome") and elig["maxIncome"] < 999999990:
            parts.append(f"  • {lbl_income}: ₹{elig['maxIncome']:,}/{lbl_years}")
        cats = elig.get("categories", [])
        if cats:
            parts.append(f"  • {lbl_cats}: {', '.join(c.upper() for c in cats)}")
        genders = elig.get("gender", [])
        if len(genders) < 3:
            parts.append(f"  • {lbl_gender}: {', '.join(genders)}")
        states = elig.get("states", "all")
        if states != "all" and isinstance(states, list):
            parts.append(f"  • {lbl_states}: {', '.join(s.title() for s in states[:5])}{'...' if len(states) > 5 else ''}")
        parts.append("")

    if asks_apply or asks_general:
        if how_steps:
            parts.append(f"📋 **{lbl_apply}:**")
            for i, step in enumerate(how_steps, 1):
                parts.append(f"  {i}. {step}")
            parts.append("")

    if asks_docs or asks_general:
        if docs:
            parts.append(f"🧾 **{lbl_docs}:**")
            for doc in docs:
                parts.append(f"  • {doc}")
            parts.append("")

    url = scheme.get("officialUrl", "")
    if url:
        parts.append(f"🌐 **{lbl_website}:** {url}")

    return "\n".join(parts)


@app.route("/api/discuss", methods=["POST"])
def discuss():
    """
    Discuss specific schemes with the user.
    Accepts a question and optional scheme_id or search keywords.
    """
    data = request.get_json()
    question = data.get("question", "").strip()
    scheme_id = data.get("scheme_id", "")
    lang = data.get("lang", "en")

    if not question:
        msg = "कृपया किसी सरकारी योजना के बारे में पूछें! जैसे: 'PM-KISAN के बारे में बताओ' या 'आयुष्मान भारत के लिए कौन से दस्तावेज़ चाहिए?'" if lang == "hi" else "Please ask a question about a government scheme! For example: 'Tell me about PM-KISAN' or 'What documents do I need for Ayushman Bharat?'"
        return jsonify({"answer": msg})

    # If a specific scheme_id is provided, answer about that scheme
    if scheme_id:
        for scheme in SCHEMES:
            if scheme["id"] == scheme_id:
                answer = build_scheme_answer(scheme, question, lang)
                return jsonify({"answer": answer, "scheme_id": scheme_id})
        msg = "क्षमा करें, मुझे वह योजना नहीं मिली।" if lang == "hi" else "Sorry, I couldn't find that scheme."
        return jsonify({"answer": msg})

    # Otherwise, search by keywords in the question
    stop_words = {"tell", "me", "about", "what", "is", "the", "how", "to", "can", "i",
                  "do", "does", "get", "for", "in", "of", "a", "an", "are", "this",
                  "which", "who", "need", "mujhe", "batao", "kya", "hai", "ke", "ka",
                  "ki", "se", "ko", "ye", "wo", "yeh", "scheme", "yojana"}
    words = question.lower().split()
    search_terms = [w for w in words if w not in stop_words and len(w) > 2]

    found_schemes = []
    for term in search_terms:
        found_schemes.extend(find_schemes_by_keyword(term))

    # Deduplicate
    seen_ids = set()
    unique_schemes = []
    for s in found_schemes:
        if s["id"] not in seen_ids:
            seen_ids.add(s["id"])
            unique_schemes.append(s)

    if unique_schemes:
        if len(unique_schemes) == 1:
            answer = build_scheme_answer(unique_schemes[0], question, lang)
            return jsonify({"answer": answer, "scheme_id": unique_schemes[0]["id"]})

        # List matches
        if lang == "hi":
            answer_parts = [f"आपकी खोज से **{len(unique_schemes)}** योजनाएं मिलीं:\n"]
            for i, s in enumerate(unique_schemes[:8], 1):
                sname = s.get('nameHi', s.get('name', ''))
                sbenefit = s.get('benefitHi', s.get('benefit', ''))[:80]
                answer_parts.append(f"{i}. {s.get('icon','')} **{sname}** — {sbenefit}")
            if len(unique_schemes) > 8:
                answer_parts.append(f"\n...और {len(unique_schemes)-8} और योजनाएं।")
            answer_parts.append("\nकिसी विशेष योजना के बारे में पूछें, जैसे *\"पहली वाली के बारे में बताओ\"* या नाम बताएं!")
        else:
            answer_parts = [f"I found **{len(unique_schemes)}** schemes matching your query:\n"]
            for i, s in enumerate(unique_schemes[:8], 1):
                answer_parts.append(f"{i}. {s.get('icon','')} **{s.get('name','')}** — {s.get('benefit','')[:80]}")
            if len(unique_schemes) > 8:
                answer_parts.append(f"\n...and {len(unique_schemes)-8} more.")
            answer_parts.append("\nAsk me about any specific one, e.g. *\"Tell me about the first one\"* or mention its name!")
        return jsonify({"answer": "\n".join(answer_parts), "matches": len(unique_schemes)})

    not_found = "मुझे आपकी खोज से मिलती-जुलती कोई योजना नहीं मिली। 'शिक्षा छात्रवृत्ति', 'आवास योजना', 'किसान ऋण' जैसे विषय पूछें!" if lang == "hi" else "I couldn't find a scheme matching your query. Try asking about a specific topic like 'education scholarships', 'housing scheme', 'farmer loan', or mention a scheme by name!"
    return jsonify({"answer": not_found})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
