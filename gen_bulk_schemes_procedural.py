import json
import os

SCHEMES_PATH = os.path.join(os.path.dirname(__file__), "schemes.json")

# 28 States and 8 UTs (Let's use 30 prominent states/UTs for generation)
STATES = [
    ("Andhra Pradesh", "andhra pradesh", "आंध्र प्रदेश"),
    ("Arunachal Pradesh", "arunachal pradesh", "अरुणाचल प्रदेश"),
    ("Assam", "assam", "असम"),
    ("Bihar", "bihar", "बिहार"),
    ("Chhattisgarh", "chhattisgarh", "छत्तीसगढ़"),
    ("Goa", "goa", "गोवा"),
    ("Gujarat", "gujarat", "गुजरात"),
    ("Haryana", "haryana", "हरियाणा"),
    ("Himachal Pradesh", "himachal pradesh", "हिमाचल प्रदेश"),
    ("Jharkhand", "jharkhand", "झारखंड"),
    ("Karnataka", "karnataka", "कर्नाटक"),
    ("Kerala", "kerala", "केरल"),
    ("Madhya Pradesh", "madhya pradesh", "मध्य प्रदेश"),
    ("Maharashtra", "maharashtra", "महाराष्ट्र"),
    ("Manipur", "manipur", "मणिपुर"),
    ("Meghalaya", "meghalaya", "मेघालय"),
    ("Mizoram", "mizoram", "मिजोरम"),
    ("Nagaland", "nagaland", "नागालैंड"),
    ("Odisha", "odisha", "ओडिशा"),
    ("Punjab", "punjab", "पंजाब"),
    ("Rajasthan", "rajasthan", "राजस्थान"),
    ("Sikkim", "sikkim", "सिक्किम"),
    ("Tamil Nadu", "tamil nadu", "तमिलनाडु"),
    ("Telangana", "telangana", "तेलंगाना"),
    ("Tripura", "tripura", "त्रिपुरा"),
    ("Uttar Pradesh", "uttar pradesh", "उत्तर प्रदेश"),
    ("Uttarakhand", "uttarakhand", "उत्तराखंड"),
    ("West Bengal", "west bengal", "पश्चिम बंगाल"),
    ("Delhi", "delhi", "दिल्ली"),
    ("Jammu and Kashmir", "jammu and kashmir", "जम्मू और कश्मीर")
]

BUSINESS_SECTORS = [
    ("IT & Software", "आईटी और सॉफ्टवेयर"),
    ("Textile", "कपड़ा"),
    ("Food Processing", "खाद्य प्रसंस्करण"),
    ("Leather", "चमड़ा"),
    ("Tourism", "पर्यटन"),
    ("Handicrafts", "हस्तशिल्प"),
    ("Export", "निर्यात"),
    ("Pharmaceutical", "फार्मास्युटिकल"),
    ("Electronics", "इलेक्ट्रॉनिक्स"),
    ("Renewable Energy", "नवीकरणीय ऊर्जा")
]

RURAL_SECTORS = [
    ("Dairy", "डेयरी"),
    ("Fisheries", "मत्स्य पालन"),
    ("Beekeeping", "मधुमक्खी पालन"),
    ("Silk Weaving", "रेशम बुनाई"),
    ("Coir", "कयर"),
    ("Bamboo", "बांस"),
    ("Forest Produce", "वन उपज"),
    ("Rural Tourism", "ग्रामीण पर्यटन"),
    ("Agroforestry", "कृषि वानिकी"),
    ("Village Artisans", "ग्राम कारीगर")
]

new_schemes = []

def generate_id(name):
    return name.lower().replace(" ", "-").replace("&", "").replace("  ", " ").strip()

# 1. State-Level Business Schemes (30 * 5 = 150)
for s_name, s_id, s_hi in STATES:
    new_schemes.extend([
        {
            "id": f"{s_id.replace(' ','-')}-msme-subvention",
            "name": f"{s_name} MSME Interest Subvention Scheme",
            "shortName": f"{s_name} MSME Subvention",
            "category": "business",
            "icon": "🏭",
            "benefit": f"Up to 5% interest subvention on term loans for MSMEs in {s_name}",
            "benefitValue": 500000,
            "simpleExplanation": f"This scheme by the {s_name} government provides a 5% interest subsidy on loans taken by MSMEs for setting up or expanding manufacturing or service enterprises in the state.",
            "eligibility": {"minAge": 18, "maxAge": 65, "maxIncome": 999999999, "categories": ["general", "obc", "sc", "st"], "gender": ["male", "female", "other"], "occupations": ["business", "self_employed", "entrepreneur"], "states": [s_id], "conditions": ["business"]},
            "howToApply": [f"Register on the {s_name} MSME portal", "Submit loan sanction letter from bank", "Claim interest subvention quarterly"],
            "documentsRequired": ["Aadhaar", "Udyam Registration", "Bank Loan Documents", "State Domicile"],
            "officialUrl": "https://india.gov.in",
            "whyQualifyTemplate": f"As an entrepreneur in {s_name}, you qualify for this MSME interest subsidy.",
            "nameHi": f"{s_hi} एमएसएमई ब्याज सहायता योजना",
            "shortNameHi": f"{s_hi} एमएसएमई सहायता",
            "benefitHi": f"{s_hi} में एमएसएमई के लिए सावधि ऋण पर 5% तक की ब्याज सहायता",
            "simpleExplanationHi": f"{s_hi} सरकार की यह योजना राज्य में विनिर्माण या सेवा उद्यम स्थापित करने या विस्तार करने के लिए एमएसएमई द्वारा लिए गए ऋण पर 5% ब्याज सब्सिडी प्रदान करती है।",
            "documentsRequiredHi": ["आधार", "उद्यम पंजीकरण", "बैंक ऋण दस्तावेज", "राज्य अधिवास"],
            "howToApplyHi": [f"{s_hi} एमएसएमई पोर्टल पर पंजीकरण करें", "बैंक से ऋण स्वीकृति पत्र जमा करें", "त्रैमासिक ब्याज सहायता का दावा करें"]
        },
        {
            "id": f"{s_id.replace(' ','-')}-startup-seed",
            "name": f"{s_name} Startup Seed Grant Program",
            "shortName": f"{s_name} Startup Seed",
            "category": "business",
            "icon": "🚀",
            "benefit": f"Seed grant of up to ₹10 Lakh for early-stage startups based in {s_name}",
            "benefitValue": 1000000,
            "simpleExplanation": f"The {s_name} Startup Policy offers early-stage startups a seed grant to develop prototypes, conduct market research, and launch their minimal viable product.",
            "eligibility": {"minAge": 18, "maxAge": 50, "maxIncome": 999999999, "categories": ["general", "obc", "sc", "st"], "gender": ["male", "female", "other"], "occupations": ["entrepreneur", "student", "self_employed"], "states": [s_id], "conditions": ["business"]},
            "howToApply": [f"Apply via {s_name} Startup Innovation Portal", "Submit pitch deck and business plan", "Present before the state incubator committee"],
            "documentsRequired": ["DPIIT Registration", "Company Incorporation Certificate", "Pitch Deck", "Bank Details"],
            "officialUrl": "https://startupindia.gov.in",
            "whyQualifyTemplate": f"Your startup in {s_name} can leverage this seed grant for early growth.",
            "nameHi": f"{s_hi} स्टार्टअप सीड ग्रांट प्रोग्राम",
            "shortNameHi": f"{s_hi} स्टार्टअप सीड",
            "benefitHi": f"{s_hi} में शुरुआती चरण के स्टार्टअप के लिए ₹10 लाख तक का सीड ग्रांट",
            "simpleExplanationHi": f"{s_hi} स्टार्टअप नीति शुरुआती चरण के स्टार्टअप को प्रोटोटाइप विकसित करने, बाजार अनुसंधान करने और अपने उत्पाद लॉन्च करने के लिए सीड ग्रांट प्रदान करती है।",
            "documentsRequiredHi": ["डीपीआईआईटी पंजीकरण", "कंपनी निगमन प्रमाणपत्र", "पिच डेक", "बैंक विवरण"],
            "howToApplyHi": [f"{s_hi} स्टार्टअप इनोवेशन पोर्टल के माध्यम से आवेदन करें", "पिच डेक और व्यवसाय योजना प्रस्तुत करें", "राज्य इनक्यूबेटर समिति के समक्ष प्रस्तुत करें"]
        },
        {
            "id": f"{s_id.replace(' ','-')}-women-entrepreneur",
            "name": f"{s_name} Women Entrepreneurship Subsidy",
            "shortName": f"{s_name} Women Business",
            "category": "business",
            "icon": "👩‍💼",
            "benefit": f"20% additional capital subsidy for businesses owned by women in {s_name}",
            "benefitValue": 500000,
            "simpleExplanation": f"To promote female entrepreneurship, {s_name} provides an extra 20% capital investment subsidy for factories or service units started by women.",
            "eligibility": {"minAge": 18, "maxAge": 60, "maxIncome": 999999999, "categories": ["general", "obc", "sc", "st"], "gender": ["female"], "occupations": ["business", "self_employed", "entrepreneur"], "states": [s_id], "conditions": ["business"]},
            "howToApply": ["Apply through the Directorate of Industries", "Submit project report and gender declaration", "Claim subsidy post machinery installation"],
            "documentsRequired": ["Aadhaar", "Project Report", "Machinery Invoices", "Women Ownership Proof"],
            "officialUrl": "https://india.gov.in",
            "whyQualifyTemplate": f"As a female business owner in {s_name}, you are eligible for this special capital subsidy.",
            "nameHi": f"{s_hi} महिला उद्यमिता सब्सिडी",
            "shortNameHi": f"{s_hi} महिला व्यवसाय",
            "benefitHi": f"{s_hi} में महिलाओं के स्वामित्व वाले व्यवसायों के लिए 20% अतिरिक्त पूंजीगत सब्सिडी",
            "simpleExplanationHi": f"महिला उद्यमिता को बढ़ावा देने के लिए, {s_hi} महिलाओं द्वारा शुरू किए गए कारखानों या सेवा इकाइयों के लिए अतिरिक्त 20% पूंजी निवेश सब्सिडी प्रदान करता है।",
            "documentsRequiredHi": ["आधार", "परियोजना रिपोर्ट", "मशीनरी चालान", "महिला स्वामित्व प्रमाण"],
            "howToApplyHi": ["उद्योग निदेशालय के माध्यम से आवेदन करें", "प्रोजेक्ट रिपोर्ट और लिंग घोषणा जमा करें", "मशीनरी स्थापना के बाद सब्सिडी का दावा करें"]
        },
        {
            "id": f"{s_id.replace(' ','-')}-industrial-land",
            "name": f"{s_name} Industrial Land Subsidy",
            "shortName": f"{s_name} Land Subsidy",
            "category": "business",
            "icon": "🏗️",
            "benefit": f"Up to 30% concession on industrial land allotted in state industrial estates",
            "benefitValue": 2000000,
            "simpleExplanation": f"The State Industrial Development Corporation of {s_name} offers a 30% discount on land prime industrial zones for establishing new manufacturing plants.",
            "eligibility": {"minAge": 18, "maxAge": 65, "maxIncome": 999999999, "categories": ["general", "obc", "sc", "st"], "gender": ["male", "female", "other"], "occupations": ["business", "entrepreneur"], "states": [s_id], "conditions": ["business"]},
            "howToApply": ["Apply via State Industrial Development Corp portal", "Deposit earnest money", "Sign lease deed after approval"],
            "documentsRequired": ["Company Registration", "Detailed Project Report", "Financial Projections"],
            "officialUrl": "https://india.gov.in",
            "whyQualifyTemplate": f"Your manufacturing project could receive land subsidies in {s_name}.",
            "nameHi": f"{s_hi} औद्योगिक भूमि सब्सिडी",
            "shortNameHi": f"{s_hi} भूमि सब्सिडी",
            "benefitHi": f"राज्य के औद्योगिक सम्पदा में आवंटित औद्योगिक भूमि पर 30% तक की रियायत",
            "simpleExplanationHi": f"{s_hi} का राज्य औद्योगिक विकास निगम नए विनिर्माण संयंत्र स्थापित करने के लिए भूमि पर 30% छूट प्रदान करता है।",
            "documentsRequiredHi": ["कंपनी पंजीकरण", "विस्तृत परियोजना रिपोर्ट", "वित्तीय अनुमान"],
            "howToApplyHi": ["राज्य औद्योगिक विकास निगम पोर्टल के माध्यम से आवेदन करें", "बयाना राशि जमा करें", "अनुमोदन के बाद पट्टा विलेख पर हस्ताक्षर करें"]
        },
        {
            "id": f"{s_id.replace(' ','-')}-tech-innovation",
            "name": f"{s_name} Tech & Innovation Fund",
            "shortName": f"{s_name} Tech Fund",
            "category": "business",
            "icon": "💻",
            "benefit": f"Grants up to ₹5 Lakh for patent filing, R&D, and tech adoption in {s_name}",
            "benefitValue": 500000,
            "simpleExplanation": f"Aiming to boost IP creation, {s_name} offers financial assistance to businesses and individuals for filing patents, trademarks, and acquiring new technologies.",
            "eligibility": {"minAge": 18, "maxAge": 100, "maxIncome": 999999999, "categories": ["general", "obc", "sc", "st"], "gender": ["male", "female", "other"], "occupations": ["business", "entrepreneur", "student", "self_employed"], "states": [s_id], "conditions": ["business"]},
            "howToApply": ["Apply at the Science & Tech Dept portal", "Submit R&D or Patent application proofs", "Receive reimbursement"],
            "documentsRequired": ["Patent Filing Receipts", "Technology Transfer Agreements", "Aadhaar", "Business PAN"],
            "officialUrl": "https://india.gov.in",
            "whyQualifyTemplate": f"Innovators in {s_name} can get IP and R&D costs reimbursed.",
            "nameHi": f"{s_hi} तकनीकी और नवाचार निधि",
            "shortNameHi": f"{s_hi} तकनीकी निधि",
            "benefitHi": f"{s_hi} में पेटेंट दाखिल करने, आरएंडडी, और तकनीकी अपनाने के लिए ₹5 लाख तक का अनुदान",
            "simpleExplanationHi": f"आईपी निर्माण को बढ़ावा देने के उद्देश्य से, {s_hi} पेटेंट, ट्रेडमार्क दाखिल करने और नई तकनीकों को प्राप्त करने के लिए वित्तीय सहायता प्रदान करता है।",
            "documentsRequiredHi": ["पेटेंट फाइलिंग रसीदें", "प्रौद्योगिकी हस्तांतरण समझौते", "आधार", "बिजनेस पैन"],
            "howToApplyHi": ["विज्ञान और प्रौद्योगिकी विभाग पोर्टल पर आवेदन करें", "आरएंडडी या पेटेंट आवेदन प्रमाण जमा करें", "प्रतिपूर्ति प्राप्त करें"]
        }
    ])

# 2. State-Level Rural Schemes (30 * 5 = 150)
for s_name, s_id, s_hi in STATES:
    new_schemes.extend([
        {
            "id": f"{s_id.replace(' ','-')}-rural-housing",
            "name": f"{s_name} Gramin Awas Scheme (State Supplement)",
            "shortName": f"{s_name} Rural Housing",
            "category": "rural",
            "icon": "🏠",
            "benefit": f"Additional state top-up of ₹50,000 for building a pakka house in rural {s_name}",
            "benefitValue": 50000,
            "simpleExplanation": f"In addition to the central PMAY-G, the {s_name} government offers a special top-up to help rural poor families build stronger houses with modern amenities.",
            "eligibility": {"minAge": 18, "maxAge": 100, "maxIncome": 150000, "categories": ["general", "obc", "sc", "st"], "gender": ["male", "female", "other"], "occupations": ["farmer", "laborer", "daily_wage", "unemployed"], "states": [s_id], "conditions": ["rural"]},
            "howToApply": ["Register your name with the Gram Panchayat", "Get listed in the SECC beneficiary list", "Installments credited as construction progresses"],
            "documentsRequired": ["Aadhaar", "Job Card", "Bank Account", "Land Document"],
            "officialUrl": "https://rural.nic.in",
            "whyQualifyTemplate": f"As a rural resident of {s_name}, you might qualify for housing assistance.",
            "nameHi": f"{s_hi} ग्रामीण आवास योजना (राज्य पूरक)",
            "shortNameHi": f"{s_hi} ग्रामीण आवास",
            "benefitHi": f"ग्रामीण {s_hi} में पक्का घर बनाने के लिए ₹50,000 का अतिरिक्त राज्य टॉप-अप",
            "simpleExplanationHi": f"केंद्रीय PMAY-G के अलावा, {s_hi} सरकार ग्रामीण गरीब परिवारों को आधुनिक सुविधाओं के साथ मजबूत घर बनाने में मदद करने के लिए एक विशेष टॉप-अप प्रदान करती है।",
            "documentsRequiredHi": ["आधार", "जॉब कार्ड", "बैंक खाता", "भूमि दस्तावेज"],
            "howToApplyHi": ["ग्राम पंचायत में अपना नाम दर्ज कराएं", "SECC लाभार्थी सूची में सूचीबद्ध हों", "निर्माण आगे बढ़ने पर किश्तें जमा की जाती हैं"]
        },
        {
            "id": f"{s_id.replace(' ','-')}-rural-water",
            "name": f"{s_name} Jal Jeevan Rural Delivery",
            "shortName": f"{s_name} Clean Water",
            "category": "rural",
            "icon": "🚰",
            "benefit": f"Free individual tap water connection and maintenance in {s_name} villages",
            "benefitValue": 5000,
            "simpleExplanation": f"Ensuring clean drinking water reaches every rural household in {s_name} through functional household tap connections.",
            "eligibility": {"minAge": 18, "maxAge": 100, "maxIncome": 999999999, "categories": ["general", "obc", "sc", "st"], "gender": ["male", "female", "other"], "occupations": ["all"], "states": [s_id], "conditions": ["rural"]},
            "howToApply": ["Apply through the Village Water and Sanitation Committee (VWSC)", "Panchayat approves the connection", "Contractor installs the tap"],
            "documentsRequired": ["Aadhaar", "Residence Proof", "Ration Card"],
            "officialUrl": "https://jaljeevanmission.gov.in",
            "whyQualifyTemplate": f"Get a free tap connection for your home in rural {s_name}.",
            "nameHi": f"{s_hi} जल जीवन ग्रामीण वितरण",
            "shortNameHi": f"{s_hi} स्वच्छ जल",
            "benefitHi": f"{s_hi} के गांवों में मुफ्त व्यक्तिगत नल जल कनेक्शन और रखरखाव",
            "simpleExplanationHi": f"{s_hi} में प्रत्येक ग्रामीण घर तक कार्यात्मक घरेलू नल कनेक्शन के माध्यम से स्वच्छ पेयजल सुनिश्चित करना।",
            "documentsRequiredHi": ["आधार", "निवास प्रमाण", "राशन कार्ड"],
            "howToApplyHi": ["ग्राम जल एवं स्वच्छता समिति (VWSC) के माध्यम से आवेदन करें", "पंचायत कनेक्शन को मंजूरी देती है", "ठेकेदार नल लगाता है"]
        },
        {
            "id": f"{s_id.replace(' ','-')}-livelihood-mission",
            "name": f"{s_name} Rural Livelihood Mission (SRLM)",
            "shortName": f"{s_name} SRLM",
            "category": "rural",
            "icon": "🌾",
            "benefit": f"Training, revolving funds up to ₹25,000, and market linkages for SHGs in {s_name}",
            "benefitValue": 25000,
            "simpleExplanation": f"The State Rural Livelihood Mission in {s_name} empowers rural women by forming Self Help Groups, providing seed capital, and assisting in starting micro-enterprises.",
            "eligibility": {"minAge": 18, "maxAge": 65, "maxIncome": 200000, "categories": ["general", "obc", "sc", "st"], "gender": ["female"], "occupations": ["farmer", "laborer", "homemaker", "self_employed"], "states": [s_id], "conditions": ["rural"]},
            "howToApply": ["Form an SHG in your village", "Register with the Block Mission Management Unit", "Apply for Community Investment Fund"],
            "documentsRequired": ["SHG Resolution", "Members' Aadhaar", "Bank Account passbook"],
            "officialUrl": "https://aajeevika.gov.in",
            "whyQualifyTemplate": f"Rural women in {s_name} can join SHGs to access these livelihood funds.",
            "nameHi": f"{s_hi} राज्य ग्रामीण आजीविका मिशन (SRLM)",
            "shortNameHi": f"{s_hi} SRLM",
            "benefitHi": f"{s_hi} में स्वयं सहायता समूहों के लिए प्रशिक्षण, ₹25,000 तक का रिवॉल्विंग फंड और बाजार संपर्क",
            "simpleExplanationHi": f"{s_hi} में राज्य ग्रामीण आजीविका मिशन स्वयं सहायता समूह बनाकर, बीज पूंजी प्रदान करके और सूक्ष्म उद्यम शुरू करने में सहायता करके ग्रामीण महिलाओं को सशक्त बनाता है।",
            "documentsRequiredHi": ["SHG संकल्प", "सदस्यों का आधार", "बैंक खाता पासबुक"],
            "howToApplyHi": ["अपने गांव में एक स्वयं सहायता समूह (SHG) बनाएं", "ब्लॉक मिशन प्रबंधन इकाई में पंजीकरण करें", "सामुदायिक निवेश कोष के लिए आवेदन करें"]
        },
        {
            "id": f"{s_id.replace(' ','-')}-panchayat-digital",
            "name": f"{s_name} Panchayat Digitalization Scheme",
            "shortName": f"{s_name} Smart Village",
            "category": "rural",
            "icon": "💻",
            "benefit": f"Free WiFi in village squares and digital service centers in every {s_name} panchayat",
            "benefitValue": 0,
            "simpleExplanation": f"Connecting rural {s_name} to the world by establishing free WiFi hotspots and common service centers in all Gram Panchayats.",
            "eligibility": {"minAge": 0, "maxAge": 100, "maxIncome": 999999999, "categories": ["general", "obc", "sc", "st"], "gender": ["male", "female", "other"], "occupations": ["all"], "states": [s_id], "conditions": ["rural"]},
            "howToApply": ["Community-level benefit, no individual application required", "Visit the local Panchayat office to use standard digital services"],
            "documentsRequired": [],
            "officialUrl": "https://panchayat.gov.in",
            "whyQualifyTemplate": f"Your village in {s_name} is being upgraded with free digital infrastructure.",
            "nameHi": f"{s_hi} पंचायत डिजिटलीकरण योजना",
            "shortNameHi": f"{s_hi} स्मार्ट गांव",
            "benefitHi": f"प्रत्येक {s_hi} पंचायत में गांव के चौकों और डिजिटल सेवा केंद्रों में मुफ्त वाईफाई",
            "simpleExplanationHi": f"सभी ग्राम पंचायतों में मुफ्त वाईफाई हॉटस्पॉट और सामान्य सेवा केंद्र स्थापित करके ग्रामीण {s_hi} को दुनिया से जोड़ना।",
            "documentsRequiredHi": [],
            "howToApplyHi": ["सामुदायिक स्तर का लाभ, किसी व्यक्तिगत आवेदन की आवश्यकता नहीं है", "मानक डिजिटल सेवाओं का उपयोग करने के लिए स्थानीय पंचायत कार्यालय जाएं"]
        },
        {
            "id": f"{s_id.replace(' ','-')}-tribal-rural-dev",
            "name": f"{s_name} Tribal Village Development Fund",
            "shortName": f"{s_name} Tribal Village",
            "category": "rural",
            "icon": "🏕️",
            "benefit": f"Special infrastructure grants and livelihood support for tribal-dominated villages in {s_name}",
            "benefitValue": 50000,
            "simpleExplanation": f"Provides comprehensive development—roads, schools, health clinics, and farming tools—specifically for ST majority villages in {s_name}.",
            "eligibility": {"minAge": 18, "maxAge": 100, "maxIncome": 999999999, "categories": ["st"], "gender": ["male", "female", "other"], "occupations": ["all"], "states": [s_id], "conditions": ["rural", "minority"]},
            "howToApply": ["Implemented automatically in notified tribal blocks", "Individuals can apply for livelihood assets via Tribal Development Dept"],
            "documentsRequired": ["ST Certificate", "Aadhaar", "Domicile"],
            "officialUrl": "https://tribal.nic.in",
            "whyQualifyTemplate": f"Tribal communities in {s_name} benefit from this focused rural development scheme.",
            "nameHi": f"{s_hi} जनजातीय ग्राम विकास कोष",
            "shortNameHi": f"{s_hi} जनजातीय गांव",
            "benefitHi": f"{s_hi} में आदिवासी बहुल गांवों के लिए विशेष बुनियादी ढांचा अनुदान और आजीविका सहायता",
            "simpleExplanationHi": f"विशेष रूप से {s_hi} के एसटी बहुसंख्यक गांवों के लिए व्यापक विकास (सड़कें, स्कूल, स्वास्थ्य क्लीनिक और खेती के उपकरण) प्रदान करता है।",
            "documentsRequiredHi": ["एसटी प्रमाणपत्र", "आधार", "अधिवास"],
            "howToApplyHi": ["अधिसूचित आदिवासी ब्लॉकों में स्वचालित रूप से लागू", "व्यक्ति आदिवासी विकास विभाग के माध्यम से आजीविका संपत्ति के लिए आवेदन कर सकते हैं"]
        }
    ])

# 3. State-Level Agriculture Schemes (30 * 4 = 120)
for s_name, s_id, s_hi in STATES:
    new_schemes.extend([
        {
            "id": f"{s_id.replace(' ','-')}-krishi-yantra",
            "name": f"{s_name} Krishi Yantra Subsidy",
            "shortName": f"{s_name} Farm Machinery",
            "category": "agriculture",
            "icon": "🚜",
            "benefit": f"Up to 50% subsidy on buying tractors, rotavators, and farm equipment in {s_name}",
            "benefitValue": 200000,
            "simpleExplanation": f"To promote mechanization, {s_name} provides heavy subsidies to farmers purchasing modern agricultural equipment.",
            "eligibility": {"minAge": 18, "maxAge": 80, "maxIncome": 999999999, "categories": ["general", "obc", "sc", "st"], "gender": ["male", "female", "other"], "occupations": ["farmer"], "states": [s_id], "conditions": ["farmer"]},
            "howToApply": ["Apply on the state agriculture portal", "Get equipment quote from authorized dealer", "Subsidy credited directly to bank/dealer"],
            "documentsRequired": ["Aadhaar", "Land Records (Khasra/Khatauni)", "Bank Passbook", "Dealer Quotation"],
            "officialUrl": "https://agricoop.nic.in",
            "whyQualifyTemplate": f"As a farmer in {s_name}, you can efficiently buy machinery via this subsidy.",
            "nameHi": f"{s_hi} कृषि यंत्र सब्सिडी",
            "shortNameHi": f"{s_hi} कृषि मशीनरी",
            "benefitHi": f"{s_hi} में ट्रैक्टर, रोटावेटर और खेत के उपकरण खरीदने पर 50% तक की सब्सिडी",
            "simpleExplanationHi": f"मशीनीकरण को बढ़ावा देने के लिए, {s_hi} आधुनिक कृषि उपकरण खरीदने वाले किसानों को भारी सब्सिडी प्रदान करता है।",
            "documentsRequiredHi": ["आधार", "भूमि रिकॉर्ड", "बैंक पासबुक", "डीलर कोटेशन"],
            "howToApplyHi": ["राज्य कृषि पोर्टल पर आवेदन करें", "अधिकृत डीलर से उपकरण का कोटेशन प्राप्त करें", "सब्सिडी सीधे बैंक/डीलर के खाते में जमा की जाती है"]
        },
        {
            "id": f"{s_id.replace(' ','-')}-solar-pump",
            "name": f"{s_name} Kisan Solar Pump Scheme",
            "shortName": f"{s_name} Solar Pump",
            "category": "agriculture",
            "icon": "☀️",
            "benefit": f"60% subsidy for installing solar-powered water pumps for irrigation in {s_name}",
            "benefitValue": 100000,
            "simpleExplanation": f"{s_name} implements the PM KUSUM aligned state scheme to help farmers replace diesel pumps with cost-effective solar irrigation pumps.",
            "eligibility": {"minAge": 18, "maxAge": 80, "maxIncome": 999999999, "categories": ["general", "obc", "sc", "st"], "gender": ["male", "female", "other"], "occupations": ["farmer"], "states": [s_id], "conditions": ["farmer", "rural"]},
            "howToApply": ["Register on State Renewable Energy portal", "Pay farmer's share (10-40%) online", "Vendor installs the setup"],
            "documentsRequired": ["Aadhaar", "Land Records", "Irrigation Source Proof", "Photo"],
            "officialUrl": "https://mnre.gov.in",
            "whyQualifyTemplate": f"Farmers in {s_name} can cut energy costs drastically with subsidized solar pumps.",
            "nameHi": f"{s_hi} किसान सोलर पंप योजना",
            "shortNameHi": f"{s_hi} सोलर पंप",
            "benefitHi": f"{s_hi} में सिंचाई के लिए सौर ऊर्जा संचालित पानी पंप स्थापित करने पर 60% सब्सिडी",
            "simpleExplanationHi": f"{s_hi} किसानों को डीजल पंपों को लागत प्रभावी सौर सिंचाई पंपों से बदलने में मदद करने के लिए पीएम कुसुम संरेखित राज्य योजना लागू करता है।",
            "documentsRequiredHi": ["आधार", "भूमि रिकॉर्ड", "सिंचाई स्रोत का प्रमाण", "फोटो"],
            "howToApplyHi": ["राज्य नवीकरणीय ऊर्जा पोर्टल पर पंजीकरण करें", "किसान का हिस्सा (10-40%) ऑनलाइन भुगतान करें", "विक्रेता सेटअप स्थापित करता है"]
        },
        {
            "id": f"{s_id.replace(' ','-')}-organic-farming",
            "name": f"{s_name} Organic Farming Incentive Scheme",
            "shortName": f"{s_name} Organic Farming",
            "category": "agriculture",
            "icon": "🥬",
            "benefit": f"₹50,000 per hectare incentive spread over 3 years for transitioning to organic farming in {s_name}",
            "benefitValue": 50000,
            "simpleExplanation": f"To promote chemical-free crops, {s_name} provides financial and technical support to farmers who adopt organic agricultural practices.",
            "eligibility": {"minAge": 18, "maxAge": 80, "maxIncome": 999999999, "categories": ["general", "obc", "sc", "st"], "gender": ["male", "female", "other"], "occupations": ["farmer"], "states": [s_id], "conditions": ["farmer"]},
            "howToApply": ["Apply at local agriculture office", "Form a cluster with neighboring farmers", "Register for PGS organic certification"],
            "documentsRequired": ["Aadhaar", "Land Records", "Panchayat NOC"],
            "officialUrl": "https://agricoop.nic.in",
            "whyQualifyTemplate": f"Grow organic and earn premium incentives in {s_name}.",
            "nameHi": f"{s_hi} जैविक खेती प्रोत्साहन योजना",
            "shortNameHi": f"{s_hi} जैविक खेती",
            "benefitHi": f"{s_hi} में जैविक खेती अपनाने के लिए 3 वर्षों में प्रति हेक्टेयर ₹50,000 का प्रोत्साहन",
            "simpleExplanationHi": f"रसायन मुक्त फसलों को बढ़ावा देने के लिए, {s_hi} उन किसानों को वित्तीय और तकनीकी सहायता प्रदान करता है जो जैविक कृषि पद्धतियों को अपनाते हैं।",
            "documentsRequiredHi": ["आधार", "भूमि रिकॉर्ड", "पंचायत एनओसी"],
            "howToApplyHi": ["स्थानीय कृषि कार्यालय में आवेदन करें", "पड़ोसी किसानों के साथ एक क्लस्टर बनाएं", "पीजीएस जैविक प्रमाणीकरण के लिए पंजीकरण करें"]
        },
        {
            "id": f"{s_id.replace(' ','-')}-pashudhan-bima",
            "name": f"{s_name} Pashudhan Bima Yojana",
            "shortName": f"{s_name} Livestock Insurance",
            "category": "agriculture",
            "icon": "🐄",
            "benefit": f"Up to 70% premium subsidy for insuring cattle, goats, and poultry in {s_name}",
            "benefitValue": 25000,
            "simpleExplanation": f"Protects {s_name} farmers and cattle rearers from financial loss due to death of their livestock caused by disease or accidents.",
            "eligibility": {"minAge": 18, "maxAge": 80, "maxIncome": 999999999, "categories": ["general", "obc", "sc", "st"], "gender": ["male", "female", "other"], "occupations": ["farmer", "self_employed"], "states": [s_id], "conditions": ["farmer"]},
            "howToApply": ["Contact the nearest Veterinary Doctor/Hospital", "Animal is tagged and health certified", "Pay reduced premium share"],
            "documentsRequired": ["Aadhaar", "Veterinary Health Certificate", "Animal Photo with Tag"],
            "officialUrl": "https://dahd.nic.in",
            "whyQualifyTemplate": f"Insure your livestock in {s_name} against unexpected loss safely.",
            "nameHi": f"{s_hi} पशुधन बीमा योजना",
            "shortNameHi": f"{s_hi} पशुधन बीमा",
            "benefitHi": f"{s_hi} में मवेशियों, बकरियों और मुर्गे-मुर्गियों के बीमा के लिए 70% तक प्रीमियम सब्सिडी",
            "simpleExplanationHi": f"{s_hi} के किसानों और पशुपालकों को बीमारी या दुर्घटनाओं के कारण उनके पशुधन की मृत्यु के कारण होने वाले वित्तीय नुकसान से बचाता है।",
            "documentsRequiredHi": ["आधार", "पशु चिकित्सा स्वास्थ्य प्रमाणपत्र", "टैग के साथ पशु का फोटो"],
            "howToApplyHi": ["निकटतम पशु चिकित्सक/अस्पताल से संपर्क करें", "पशु को टैग किया जाता है और स्वास्थ्य प्रमाणित किया जाता है", "कम प्रीमियम हिस्से का भुगतान करें"]
        }
    ])


# 4. National Business Sectors (10 * 5 = 50)
for sector_en, sector_hi in BUSINESS_SECTORS:
    sec_id = sector_en.lower().replace(" & ", "-").replace(" ", "-")
    new_schemes.extend([
        {
            "id": f"national-{sec_id}-cluster",
            "name": f"National {sector_en} Cluster Development Scheme",
            "shortName": f"{sector_en} Cluster",
            "category": "business",
            "icon": "🏭",
            "benefit": f"Up to ₹20 Crore grant for developing common facility centers for {sector_en} MSMEs",
            "benefitValue": 200000000,
            "simpleExplanation": f"This scheme funds groups of {sector_en} businesses to build shared infrastructure like testing labs, R&D centers, and effluent treatment plants.",
            "eligibility": {"minAge": 21, "maxAge": 100, "maxIncome": 999999999, "categories": ["general", "obc", "sc", "st"], "gender": ["male", "female", "other"], "occupations": ["business"], "states": "all", "conditions": ["business"]},
            "howToApply": ["Form a Special Purpose Vehicle (SPV) with at least 20 enterprises", "Submit a Detailed Project Report (DPR)", "Get State Govt recommendation"],
            "documentsRequired": ["SPV Registration", "DPR", "Land Papers", "State Approval"],
            "officialUrl": "https://msme.gov.in",
            "whyQualifyTemplate": f"If you are in the {sector_en} sector, you can team up to build massive subsidized infrastructure.",
            "nameHi": f"राष्ट्रीय {sector_hi} क्लस्टर विकास योजना",
            "shortNameHi": f"{sector_hi} क्लस्टर",
            "benefitHi": f"{sector_hi} एमएसएमई के लिए सामान्य सुविधा केंद्र विकसित करने के लिए ₹20 करोड़ तक का अनुदान",
            "simpleExplanationHi": f"यह योजना {sector_hi} व्यवसायों के समूहों को परीक्षण प्रयोगशालाओं, आरएंडडी केंद्रों और ऐसे साझा बुनियादी ढांचे के निर्माण के लिए वित्तपोषित करती है।",
            "documentsRequiredHi": ["एसपीवी पंजीकरण", "डीपीआर", "भूमि के कागजात", "राज्य का अनुमोदन"],
            "howToApplyHi": ["कम से कम 20 उद्यमों के साथ एक विशेष प्रयोजन वाहन (एसपीवी) बनाएं", "विस्तृत परियोजना रिपोर्ट (डीपीआर) प्रस्तुत करें", "राज्य सरकार की सिफारिश प्राप्त करें"]
        },
        {
            "id": f"{sec_id}-export-subsidy",
            "name": f"{sector_en} Export Promotion Subsidy",
            "shortName": f"{sector_en} Export Funds",
            "category": "business",
            "icon": "🚢",
            "benefit": f"Freight and marketing assistance to boost international exports in the {sector_en} sector",
            "benefitValue": 500000,
            "simpleExplanation": f"Helps {sector_en} businesses sell globally by reimbursing costs related to international shipping, foreign trade fairs, and export quality certifications.",
            "eligibility": {"minAge": 18, "maxAge": 100, "maxIncome": 999999999, "categories": ["general", "obc", "sc", "st"], "gender": ["male", "female", "other"], "occupations": ["business", "entrepreneur"], "states": "all", "conditions": ["business"]},
            "howToApply": ["Get RCMC from the relevant Export Promotion Council", "Submit claims post-export online on DGFT portal"],
            "documentsRequired": ["IEC Code", "RCMC", "Shipping Bills", "Invoices"],
            "officialUrl": "https://dgft.gov.in",
            "whyQualifyTemplate": f"Take your {sector_en} business global with export reimbursements.",
            "nameHi": f"{sector_hi} निर्यात प्रोत्साहन सब्सिडी",
            "shortNameHi": f"{sector_hi} निर्यात निधि",
            "benefitHi": f"{sector_hi} क्षेत्र में अंतरराष्ट्रीय निर्यात को बढ़ावा देने के लिए माल ढुलाई और विपणन सहायता",
            "simpleExplanationHi": f"अंतरराष्ट्रीय शिपिंग, विदेशी व्यापार मेलों और निर्यात गुणवत्ता प्रमाणपत्रों से संबंधित लागतों की प्रतिपूर्ति करके {sector_hi} व्यवसायों को विश्व स्तर पर बेचने में मदद करता है।",
            "documentsRequiredHi": ["आईईसी कोड", "आरसीएमसी", "शिपिंग बिल", "चालान"],
            "howToApplyHi": ["संबंधित निर्यात संवर्धन परिषद से आरसीएमसी प्राप्त करें", "डीजीएफटी पोर्टल पर निर्यात के बाद दावों को ऑनलाइन जमा करें"]
        },
        {
            "id": f"{sec_id}-tech-upgrade",
            "name": f"{sector_en} Tech Upgradation Fund",
            "shortName": f"{sector_en} Tech Upgrade",
            "category": "business",
            "icon": "⚙️",
            "benefit": f"15% capital subsidy on installing new modern machinery for {sector_en} businesses",
            "benefitValue": 1500000,
            "simpleExplanation": f"Modernize your {sector_en} factory! The government provides a 15% credit-linked subsidy when you take a loan to buy the latest technology equipment.",
            "eligibility": {"minAge": 18, "maxAge": 100, "maxIncome": 999999999, "categories": ["general", "obc", "sc", "st"], "gender": ["male", "female", "other"], "occupations": ["business"], "states": "all", "conditions": ["business"]},
            "howToApply": ["Apply for a term loan from an eligible bank", "Submit supplier invoices", "Bank forwards claim to nodal agency"],
            "documentsRequired": ["Udyam Registration", "Bank Sanction Letter", "Machinery Bills"],
            "officialUrl": "https://msme.gov.in",
            "whyQualifyTemplate": f"Upgrade your {sector_en} equipment using this capital subsidy.",
            "nameHi": f"{sector_hi} प्रौद्योगिकी उन्नयन निधि",
            "shortNameHi": f"{sector_hi} तकनीकी उन्नयन",
            "benefitHi": f"{sector_hi} व्यवसायों के लिए नई आधुनिक मशीनरी स्थापित करने पर 15% पूंजीगत सब्सिडी",
            "simpleExplanationHi": f"अपने {sector_hi} कारखाने का आधुनिकीकरण करें! जब आप नवीनतम तकनीक के उपकरण खरीदने के लिए ऋण लेते हैं तो सरकार 15% क्रेडिट-लिंक्ड सब्सिडी प्रदान करती है।",
            "documentsRequiredHi": ["उद्यम पंजीकरण", "बैंक स्वीकृति पत्र", "मशीनरी बिल"],
            "howToApplyHi": ["एक पात्र बैंक से सावधि ऋण के लिए आवेदन करें", "आपूर्तिकर्ता चालान जमा करें", "बैंक नोडल एजेंसी को दावा अग्रसारित करता है"]
        },
        {
            "id": f"{sec_id}-capacity-building",
            "name": f"{sector_en} Capacity Building Mission",
            "shortName": f"{sector_en} Capacity",
            "category": "employment",
            "icon": "📚",
            "benefit": f"Free advanced management and operations training for {sector_en} executives",
            "benefitValue": 50000,
            "simpleExplanation": f"Upskiling program heavily subsidized by the government tailored to executives and managers working in the {sector_en} sector to learn international best practices.",
            "eligibility": {"minAge": 21, "maxAge": 60, "maxIncome": 999999999, "categories": ["general", "obc", "sc", "st"], "gender": ["male", "female", "other"], "occupations": ["self_employed", "business", "entrepreneur"], "states": "all", "conditions": ["business"]},
            "howToApply": ["Register on national MSME training portal", "Select your sector specific course", "Complete course to get certified"],
            "documentsRequired": ["Aadhaar", "Employment proof/Business registration"],
            "officialUrl": "https://msme.gov.in",
            "whyQualifyTemplate": f"As someone in the {sector_en} industry, level up your skills for free.",
            "nameHi": f"{sector_hi} क्षमता निर्माण मिशन",
            "shortNameHi": f"{sector_hi} क्षमता",
            "benefitHi": f"{sector_hi} अधिकारियों के लिए मुफ्त उन्नत प्रबंधन और संचालन प्रशिक्षण",
            "simpleExplanationHi": f"अंतरराष्ट्रीय सर्वोत्तम प्रथाओं को सीखने के लिए {sector_hi} क्षेत्र में काम करने वाले अधिकारियों और प्रबंधकों के लिए सरकार द्वारा भारी सब्सिडी वाला अपस्किलिंग कार्यक्रम।",
            "documentsRequiredHi": ["आधार", "रोजगार प्रमाण / व्यवसाय पंजीकरण"],
            "howToApplyHi": ["राष्ट्रीय एमएसएमई प्रशिक्षण पोर्टल पर पंजीकरण करें", "अपना क्षेत्र विशिष्ट पाठ्यक्रम चुनें", "प्रमाणित होने के लिए पाठ्यक्रम पूरा करें"]
        },
        {
            "id": f"{sec_id}-skill-initiative",
            "name": f"{sector_en} Skill Development Initiative",
            "shortName": f"{sector_en} Skill",
            "category": "employment",
            "icon": "🛠️",
            "benefit": f"Free skill training and job placement in the {sector_en} industry for youth",
            "benefitValue": 30000,
            "simpleExplanation": f"Provides short-term vocational training to school dropouts and unemployed youth guaranteeing placement in the booming {sector_en} sector.",
            "eligibility": {"minAge": 18, "maxAge": 35, "maxIncome": 500000, "categories": ["general", "obc", "sc", "st"], "gender": ["male", "female", "other"], "occupations": ["unemployed", "student", "laborer", "daily_wage"], "states": "all", "conditions": []},
            "howToApply": ["Enroll at NSDC approved training centers for the sector", "Complete biometric attendance", "Pass final assessment"],
            "documentsRequired": ["Aadhaar", "Education Certificates", "Bank Details"],
            "officialUrl": "https://skillindia.gov.in",
            "whyQualifyTemplate": f"Start a rewarding career in the {sector_en} industry with free training.",
            "nameHi": f"{sector_hi} कौशल विकास पहल",
            "shortNameHi": f"{sector_hi} कौशल",
            "benefitHi": f"युवाओं के लिए {sector_hi} उद्योग में मुफ्त कौशल प्रशिक्षण और नौकरी में प्लेसमेंट",
            "simpleExplanationHi": f"स्कूल छोड़ने वालों और बेरोजगार युवाओं को अल्पकालिक व्यावसायिक प्रशिक्षण प्रदान करता है जो तेजी से बढ़ते {sector_hi} क्षेत्र में प्लेसमेंट की गारंटी देता है।",
            "documentsRequiredHi": ["आधार", "शिक्षा प्रमाण पत्र", "बैंक विवरण"],
            "howToApplyHi": ["क्षेत्र के लिए एनएसडीसी अनुमोदित प्रशिक्षण केंद्रों में नामांकन करें", "बायोमेट्रिक उपस्थिति पूरी करें", "अंतिम मूल्यांकन पास करें"]
        }
    ])

# 5. National Rural Sectors (10 * 5 = 50)
for sector_en, sector_hi in RURAL_SECTORS:
    sec_id = sector_en.lower().replace(" ", "-")
    new_schemes.extend([
        {
            "id": f"rural-{sec_id}-livelihood",
            "name": f"National {sector_en} Livelihood Project",
            "shortName": f"{sector_en} Livelihood",
            "category": "rural",
            "icon": "🌾",
            "benefit": f"Micro-credit and training for rural families engaged in {sector_en}",
            "benefitValue": 50000,
            "simpleExplanation": f"A targeted rural scheme under DAY-NRLM to specifically boost incomes of rural households dependent on {sector_en} by organizing them into producer groups.",
            "eligibility": {"minAge": 18, "maxAge": 65, "maxIncome": 300000, "categories": ["general", "obc", "sc", "st"], "gender": ["male", "female", "other"], "occupations": ["farmer", "laborer", "self_employed", "unemployed", "artisan"], "states": "all", "conditions": ["rural"]},
            "howToApply": ["Join a Producer Group in your village", "Group applies for startup fund", "Access bank credit collectively"],
            "documentsRequired": ["Aadhaar", "BPL/Ration Card", "SHG/PG Membership Proof"],
            "officialUrl": "https://aajeevika.gov.in",
            "whyQualifyTemplate": f"If you work in {sector_en}, this project can multiply your income safely.",
            "nameHi": f"राष्ट्रीय {sector_hi} आजीविका परियोजना",
            "shortNameHi": f"{sector_hi} आजीविका",
            "benefitHi": f"{sector_hi} में लगे ग्रामीण परिवारों के लिए सूक्ष्म ऋण और प्रशिक्षण",
            "simpleExplanationHi": f"डीएवाई-एनआरएलएम के तहत एक लक्षित ग्रामीण योजना, विशेष रूप से {sector_hi} पर निर्भर ग्रामीण परिवारों की आय बढ़ाने के लिए उन्हें उत्पादक समूहों में व्यवस्थित करके।",
            "documentsRequiredHi": ["आधार", "बीपीएल / राशन कार्ड", "एसएचजी / पीजी सदस्यता प्रमाण"],
            "howToApplyHi": ["अपने गांव में एक उत्पादक समूह में शामिल हों", "समूह स्टार्टअप फंड के लिए आवेदन करता है", "सामूहिक रूप से बैंक ऋण तक पहुंचें"]
        },
        {
            "id": f"{sec_id}-infra-fund",
            "name": f"{sector_en} Infrastructure Development Fund",
            "shortName": f"{sector_en} Infra",
            "category": "rural",
            "icon": "🏗️",
            "benefit": f"3% interest subvention for creating cold storage, processing units, etc., for {sector_en}",
            "benefitValue": 1000000,
            "simpleExplanation": f"Private investors, FPOs, and rural entrepreneurs get cheaper loans to build essential infrastructure like warehouses and processing facilities for {sector_en}.",
            "eligibility": {"minAge": 18, "maxAge": 70, "maxIncome": 999999999, "categories": ["general", "obc", "sc", "st"], "gender": ["male", "female", "other"], "occupations": ["farmer", "business", "entrepreneur"], "states": "all", "conditions": ["rural"]},
            "howToApply": ["Submit DPR online on the dedicated national portal", "Get loan sanctioned by scheduled bank", "Interest subvention credited automatically"],
            "documentsRequired": ["Project Report", "Land Docs", "Bank Approval", "Company PAN"],
            "officialUrl": "https://agricoop.nic.in",
            "whyQualifyTemplate": f"Build infrastructure for {sector_en} in rural areas with cheap credit.",
            "nameHi": f"{sector_hi} बुनियादी ढांचा विकास कोष",
            "shortNameHi": f"{sector_hi} इन्फ्रा",
            "benefitHi": f"{sector_hi} के लिए कोल्ड स्टोरेज, प्रसंस्करण इकाइयों आदि के निर्माण के लिए 3% ब्याज सहायता",
            "simpleExplanationHi": f"निजी निवेशकों, एफपीओ और ग्रामीण उद्यमियों को {sector_hi} के लिए गोदामों और प्रसंस्करण सुविधाओं जैसे आवश्यक बुनियादी ढांचे के निर्माण के लिए सस्ते ऋण मिलते हैं।",
            "documentsRequiredHi": ["परियोजना रिपोर्ट", "भूमि के कागजात", "बैंक अनुमोदन", "कंपनी पैन"],
            "howToApplyHi": ["समर्पित राष्ट्रीय पोर्टल पर ऑनलाइन डीपीआर जमा करें", "अनुसूचित बैंक द्वारा ऋण स्वीकृत करवाएं", "ब्याज सहायता स्वचालित रूप से जमा की जाती है"]
        },
        {
            "id": f"{sec_id}-market-linkage",
            "name": f"{sector_en} Market Linkage Scheme",
            "shortName": f"{sector_en} Market",
            "category": "rural",
            "icon": "🚚",
            "benefit": f"Transport subsidy and digital mandis integration to sell {sector_en} products directly",
            "benefitValue": 25000,
            "simpleExplanation": f"Cuts out the middleman. Farmers and artisans producing {sector_en} goods get transport subsidies and guaranteed e-marketplace access to sell directly to buyers nationwide.",
            "eligibility": {"minAge": 18, "maxAge": 100, "maxIncome": 999999999, "categories": ["general", "obc", "sc", "st"], "gender": ["male", "female", "other"], "occupations": ["farmer", "artisan", "self_employed"], "states": "all", "conditions": ["rural"]},
            "howToApply": ["Register on e-NAM or relevant state portal", "Upload product details", "Claim freight subsidy matching e-bills"],
            "documentsRequired": ["Aadhaar", "Bank Account", "Kisan Credit Card / Artisan ID"],
            "officialUrl": "https://enam.gov.in",
            "whyQualifyTemplate": f"Sell your {sector_en} produce nationwide with subsidized transport.",
            "nameHi": f"{sector_hi} बाजार संपर्क योजना",
            "shortNameHi": f"{sector_hi} बाजार",
            "benefitHi": f"{sector_hi} उत्पादों को सीधे बेचने के लिए परिवहन सब्सिडी और डिजिटल मंडियों का एकीकरण",
            "simpleExplanationHi": f"बिचौलियों को खत्म करता है। {sector_hi} माल का उत्पादन करने वाले किसानों और कारीगरों को देश भर में खरीदारों को सीधे बेचने के लिए परिवहन सब्सिडी और गारंटीकृत ई-मार्केटप्लेस पहुंच मिलती है।",
            "documentsRequiredHi": ["आधार", "बैंक खाता", "किसान क्रेडिट कार्ड / कारीगर आईडी"],
            "howToApplyHi": ["ई-नाम या संबंधित राज्य पोर्टल पर पंजीकरण करें", "उत्पाद विवरण अपलोड करें", "ई-बिल से मेल खाने वाली माल ढुलाई सब्सिडी का दावा करें"]
        },
        {
            "id": f"{sec_id}-cooperative-support",
            "name": f"{sector_en} Cooperative Support Project",
            "shortName": f"{sector_en} Co-op",
            "category": "rural",
            "icon": "🤝",
            "benefit": f"Financial aid and admin subsidies for formally registered {sector_en} cooperatives",
            "benefitValue": 200000,
            "simpleExplanation": f"Encourages forming cooperatives in the {sector_en} sector. The government covers initial administrative setup costs and provides matching equity grants to strengthen the cooperative.",
            "eligibility": {"minAge": 18, "maxAge": 100, "maxIncome": 999999999, "categories": ["general", "obc", "sc", "st"], "gender": ["male", "female", "other"], "occupations": ["farmer", "artisan", "business"], "states": "all", "conditions": ["rural"]},
            "howToApply": ["Register Cooperative Society with at least 10 members", "Apply to National Cooperative Development Corporation (NCDC)", "Receive matching share capital"],
            "documentsRequired": ["Cooperative Registration", "Member Details", "Audit Reports"],
            "officialUrl": "https://ncdc.in",
            "whyQualifyTemplate": f"United as a {sector_en} cooperative, you can unlock massive state funding.",
            "nameHi": f"{sector_hi} सहकारी सहायता परियोजना",
            "shortNameHi": f"{sector_hi} को-ऑप",
            "benefitHi": f"औपचारिक रूप से पंजीकृत {sector_hi} सहकारी समितियों के लिए वित्तीय सहायता और प्रशासनिक सब्सिडी",
            "simpleExplanationHi": f"{sector_hi} क्षेत्र में सहकारी समितियों के गठन को प्रोत्साहित करता है। सरकार प्रारंभिक प्रशासनिक स्थापना लागत को कवर करती है और सहकारी को मजबूत करने के लिए मिलान इक्विटी अनुदान प्रदान करती है।",
            "documentsRequiredHi": ["सहकारी पंजीकरण", "सदस्य विवरण", "ऑडिट रिपोर्ट"],
            "howToApplyHi": ["कम से कम 10 सदस्यों के साथ सहकारी समिति पंजीकृत करें", "राष्ट्रीय सहकारी विकास निगम (NCDC) को आवेदन करें", "मिलान शेयर पूंजी प्राप्त करें"]
        },
        {
            "id": f"{sec_id}-quality-cert",
            "name": f"{sector_en} Quality Certification Assistance",
            "shortName": f"{sector_en} Quality Cert",
            "category": "rural",
            "icon": "🏅",
            "benefit": f"100% fee reimbursement for obtaining FSSAI, ISO, or Organic certifications in {sector_en}",
            "benefitValue": 50000,
            "simpleExplanation": f"Quality sells better! The government fully reimburses the testing and certification fees so your {sector_en} products meet national/international standards and fetch better prices.",
            "eligibility": {"minAge": 18, "maxAge": 100, "maxIncome": 999999999, "categories": ["general", "obc", "sc", "st"], "gender": ["male", "female", "other"], "occupations": ["farmer", "artisan", "self_employed", "business"], "states": "all", "conditions": ["rural"]},
            "howToApply": ["Get product tested at NABL accredited labs", "Pay certification fee", "Submit bills online for full reimbursement"],
            "documentsRequired": ["Aadhaar", "Lab Test Reports", "Certification Fee Receipts", "Udyam/Farmer ID"],
            "officialUrl": "https://msme.gov.in",
            "whyQualifyTemplate": f"Upgrade your {sector_en} product's value with free quality certifications.",
            "nameHi": f"{sector_hi} गुणवत्ता प्रमाणन सहायता",
            "shortNameHi": f"{sector_hi} उच्च गुणवत्ता",
            "benefitHi": f"{sector_hi} में FSSAI, ISO, या जैविक प्रमाणपत्र प्राप्त करने के लिए 100% शुल्क प्रतिपूर्ति",
            "simpleExplanationHi": f"गुणवत्ता बेहतर बिकती है! सरकार परीक्षण और प्रमाणन शुल्क की पूरी तरह से प्रतिपूर्ति करती है ताकि आपके {sector_hi} उत्पाद राष्ट्रीय/अंतर्राष्ट्रीय मानकों को पूरा करें और बेहतर मूल्य प्राप्त करें।",
            "documentsRequiredHi": ["आधार", "प्रयोगशाला परीक्षण रिपोर्ट", "प्रमाणन शुल्क रसीदें", "उद्यम/किसान आईडी"],
            "howToApplyHi": ["NABL मान्यता प्राप्त प्रयोगशालाओं में उत्पाद का परीक्षण करवाएं", "प्रमाणन शुल्क का भुगतान करें", "पूर्ण प्रतिपूर्ति के लिए बिल ऑनलाइन जमा करें"]
        }
    ])

# Write back to schemes.json safely
try:
    with open(SCHEMES_PATH, "r", encoding="utf-8") as f:
        existing_schemes = json.load(f)
except Exception:
    existing_schemes = []

existing_ids = {s.get("id") for s in existing_schemes}
added_count = 0

for s in new_schemes:
    if s["id"] not in existing_ids:
        existing_schemes.append(s)
        added_count += 1
        existing_ids.add(s["id"])

with open(SCHEMES_PATH, "w", encoding="utf-8") as f:
    json.dump(existing_schemes, f, indent=4, ensure_ascii=False)

print(f"✅ Generated and added {added_count} new schemes. Total is now {len(existing_schemes)}.")
