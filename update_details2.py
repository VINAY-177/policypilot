import json, os

details2 = {
    "pm-gram-sadak": {
        "simpleExplanation": "All-weather road connectivity to habitations with 500+ population (250+ in hilly/tribal areas). Not an individual benefit — improves your village's connectivity to markets, hospitals, and schools.",
        "howToApply": ["No individual application — Block/District administration identifies habitations", "Check road status at pmgsy.nic.in with your habitation name", "Raise demand through Gram Panchayat / Gram Sabha", "Construction by state PWD / rural development department"],
        "documentsRequired": ["No individual documents needed"]
    },
    "amrut-water": {
        "simpleExplanation": "Clean tap water and proper sewerage for all urban households. Covers 500 cities/towns. If your city is listed, you'll get piped water supply and underground drainage system.",
        "howToApply": ["No individual application — city-level implementation", "Check if your city is covered at amrut.gov.in", "New water/sewer connections through Municipal Corporation", "Contact local ward office for connection status"],
        "documentsRequired": ["Property ownership / tenancy proof for new connection", "Aadhaar Card", "Application to Municipal Corporation"]
    },
    "rashtriya-swasthya": {
        "simpleExplanation": "BPL families get smart card-based health insurance covering hospitalization up to ₹30,000 per year. Covers family of 5. Now largely merged into Ayushman Bharat PM-JAY with ₹5 lakh coverage.",
        "howToApply": ["Check if your family is on SECC/BPL list", "Visit nearest Ayushman Bharat centre or call 14555", "Get smart card / Ayushman card created", "Use at any empanelled hospital for cashless treatment"],
        "documentsRequired": ["BPL card / SECC list", "Aadhaar Card of family members", "Ration Card"]
    },
    "rashtriya-bal": {
        "simpleExplanation": "Free health screening for 30 conditions (heart defects, hearing, vision, dental, learning disabilities) for all children 0-18. If any condition found, free treatment provided at district hospital or tertiary centre.",
        "howToApply": ["Automatic — mobile health teams visit government schools and Anganwadis", "No application needed — screening done at school", "Children needing treatment referred to District Early Intervention Centre", "Free treatment including surgery at tertiary hospitals"],
        "documentsRequired": ["No documents needed — school/Anganwadi records used", "Aadhaar Card for referral treatment"]
    },
    "mission-indradhanush": {
        "simpleExplanation": "Free vaccination against 12 diseases for all children under 2 and pregnant women. Covers BCG, OPV, Hepatitis B, DPT, Measles, Rubella, JE, Rotavirus, PCV, IPV, and TD. Sessions at Anganwadi/health centres.",
        "howToApply": ["Visit nearest Anganwadi or government health centre", "ASHA/ANM worker visits homes in campaign mode", "No appointment needed during Mission Indradhanush campaigns", "Get complete vaccination as per National Immunization Schedule"],
        "documentsRequired": ["Mother and Child Protection (MCP) card", "No other documents mandatory", "Aadhaar (optional, for digital record)"]
    },
    "iay-housing": {
        "simpleExplanation": "₹1.2 lakh (plain areas) to ₹1.3 lakh (hilly areas) for building a pucca house. Now known as PM Awaas Yojana Gramin. Beneficiary can add own design. 90 days MGNREGA wages also provided for construction labour.",
        "howToApply": ["Identified through SECC-2011 housing deprivation data", "Verification by Gram Sabha", "If eligible but not listed, apply at Block Development Office", "Money released in 3 instalments tracked through AwaasSoft app"],
        "documentsRequired": ["SECC deprivation data listing", "Aadhaar Card", "Bank Account Details", "Land ownership / NOC from Gram Panchayat", "Photograph of house site", "MGNREGA Job Card"]
    },
    "dic-scheme": {
        "simpleExplanation": "District Industries Centre provides subsidized loans up to ₹5 lakh and free training for starting small industries. Each district has a DIC that helps with registration, raw materials, and marketing support.",
        "howToApply": ["Visit your District Industries Centre (DIC) office", "Discuss business idea with General Manager DIC", "Submit Project Report and application form", "DIC recommends to bank for subsidized loan"],
        "documentsRequired": ["Aadhaar Card and PAN Card", "Project Report / Business Plan", "Educational certificates", "Caste certificate (for additional subsidy)", "Bank Account Details", "Land/premises documents"]
    },
    "aspire": {
        "simpleExplanation": "ASPIRE promotes innovation through Livelihood Business Incubators (LBI) and Technology Business Incubators (TBI) in rural areas. Get mentoring, workspace, prototyping support, and seed funding for innovative ideas.",
        "howToApply": ["Find nearest LBI/TBI at msme.gov.in/aspire", "Apply with innovative business idea", "Get selected through incubator's evaluation process", "Receive mentoring, workspace, and seed funding support"],
        "documentsRequired": ["Business idea / innovation proposal", "Aadhaar Card", "Educational certificates", "Bank Account Details"]
    },
    "cbse-merit": {
        "simpleExplanation": "Single girl child who scored 60%+ in CBSE Class 10 gets ₹500/month for Class 11 and 12. Renewable for 2 years. Must continue studying in CBSE-affiliated school. Tuition fee waiver at KVs and government schools.",
        "howToApply": ["Apply online at cbse.gov.in scholarship portal after Class 10 results", "School verifies single girl child status", "CBSE processes and announces scholarships", "Amount transferred directly to student's bank account"],
        "documentsRequired": ["CBSE Class 10 marksheet", "Affidavit declaring single girl child", "School enrollment proof for Class 11", "Aadhaar Card", "Bank Account Details"]
    },
    "tsp-scholarship": {
        "simpleExplanation": "Full scholarship for ST students from pre-matric to PhD. Covers tuition fees(full reimbursement), maintenance allowance ₹150-1,200/month, and book allowance. For family income below ₹2-2.5 lakh/year.",
        "howToApply": ["Apply on National Scholarship Portal (scholarships.gov.in)", "Login with Aadhaar and fill application", "Institute verifies and forwards to state tribal department", "Scholarship credited to bank account in instalments"],
        "documentsRequired": ["ST certificate", "Family income certificate", "Aadhaar Card", "Bank Account Details", "Previous year marksheet", "Institute enrollment proof", "Fee receipt"]
    },
    "sugamya-bharat": {
        "simpleExplanation": "Making India accessible for persons with disabilities — ramps, tactile paths, accessible toilets in government buildings. Sign language interpreters, accessible websites, and public transport modifications.",
        "howToApply": ["No individual application for infrastructure — government implements", "Report inaccessible government buildings at accessibleindia.gov.in", "Request accessible facilities at District Disability Rehabilitation Centre", "Apply for assistive devices separately through ADIP scheme"],
        "documentsRequired": ["Disability certificate (UDID) for related individual benefits", "No documents for reporting accessibility issues"]
    },
    "adip": {
        "simpleExplanation": "Free or heavily subsidized assistive devices — motorized wheelchair ₹25,000, hearing aid ₹15,000, artificial limbs, Braille kits, crutches, smart cane. For persons with 40%+ disability and income below ₹30,000/month.",
        "howToApply": ["Apply at District Disability Rehabilitation Centre (DDRC)", "Or apply during ADIP camps organized in districts", "Medical assessment done at camp/DDRC", "Device fitted and provided on the spot or within weeks"],
        "documentsRequired": ["Disability certificate (40%+ disability)", "Aadhaar Card", "Income certificate (below ₹30,000/month)", "Passport size photograph", "Prescription from medical specialist"]
    },
    "niramaya": {
        "simpleExplanation": "₹1 lakh health insurance for persons with disabilities (autism, cerebral palsy, mental retardation, multiple disabilities) at just ₹250/year (₹50 for BPL). Covers OPD, hospitalization, therapy, and medicines.",
        "howToApply": ["Apply through registered organization or Local Level Committee", "Or apply online at thenationaltrust.gov.in", "Submit disability certificate and application form", "Insurance card issued — covers all family members on policy"],
        "documentsRequired": ["Disability certificate (any of 4 covered disabilities)", "Aadhaar Card", "Photograph", "BPL card (for reduced premium)", "Bank Account Details"]
    },
    "nsfdc-loan": {
        "simpleExplanation": "Low-interest loans for SC families: ₹15 lakh for business, ₹10 lakh for education, ₹5 lakh for housing. Interest rate as low as 5% per annum. Available through state channelizing agencies.",
        "howToApply": ["Contact State Channelizing Agency (SCA) of your state", "Or visit nsfdc.nic.in for state-wise SCA list", "Submit loan application with project report", "SCA processes and disburses loan after approval"],
        "documentsRequired": ["SC caste certificate", "Income certificate (below ₹3 lakh/year)", "Aadhaar Card and PAN Card", "Project Report / Business Plan", "Quotation for machinery/equipment", "Educational admission letter (for education loan)", "Bank Account Details"]
    },
    "pm-aasha": {
        "simpleExplanation": "If market price falls below MSP, government buys your crops at MSP through procurement centres. Covers 23 crops including pulses, oilseeds, and copra. Check MSP rates at farmer.gov.in.",
        "howToApply": ["Register at nearest APMC mandi or procurement centre", "Bring crop to designated procurement centre during season", "Crop graded and weighed — payment at MSP within 72 hours", "Amount credited directly to bank account"],
        "documentsRequired": ["Land records / Kisan Credit Card", "Aadhaar Card", "Bank Account Details", "Crop details / sowing declaration"]
    },
    "e-nam": {
        "simpleExplanation": "Sell your produce at the best price across India through online auction. 1,361 mandis connected. Register once, sell anywhere. See real-time prices from all markets before deciding where to sell.",
        "howToApply": ["Register at any e-NAM mandi with Aadhaar and bank details", "Bring produce to e-NAM enabled mandi", "Produce quality tested, uploaded online for bidding", "Best bid accepted — payment to bank within 24-48 hours"],
        "documentsRequired": ["Aadhaar Card", "Bank Account Details", "Land records / tenant farmer proof", "Mobile number"]
    },
    "pm-krishi-sichai": {
        "simpleExplanation": "55% subsidy (for small/marginal farmers) and 45% (for others) on drip/sprinkler micro-irrigation systems. Save 40-50% water and increase crop yield by 20-30%. Per drop more crop.",
        "howToApply": ["Apply online at pmksy.gov.in or state agriculture portal", "Select equipment from approved list", "Get work order from state agriculture department", "Pay your share — subsidy credited after installation and verification"],
        "documentsRequired": ["Land records / 7/12 extract", "Aadhaar Card", "Bank Account Details", "Water source proof", "Quotation from approved company", "Caste certificate (for additional subsidy)"]
    },
    "national-beekeeping": {
        "simpleExplanation": "Start beekeeping with government support — free bee colonies, boxes, equipment, and training. Earn ₹30,000-50,000 per year from honey, beeswax, and pollination services. Technical support included.",
        "howToApply": ["Contact District Agriculture / Horticulture Officer", "Or apply through National Bee Board at nbb.gov.in", "Attend free beekeeping training programme", "Receive bee colonies, boxes, and equipment with subsidy"],
        "documentsRequired": ["Aadhaar Card", "Land / farm ownership proof", "Bank Account Details", "Passport size photographs", "Training completion certificate (if already trained)"]
    },
    "khadi-gramodyog": {
        "simpleExplanation": "KVIC provides raw materials, equipment, training, and marketing support to khadi weavers and village artisans. Subsidies on looms, charkha, and workspace. Products sold through Khadi Gramodyog Bhawan showrooms.",
        "howToApply": ["Visit nearest KVIC office or Khadi institution", "Apply for artisan registration", "Get raw materials at subsidized rates", "Products marketed through KVIC retail network and exhibitions"],
        "documentsRequired": ["Aadhaar Card", "Artisan / craft skill proof", "Bank Account Details", "Photographs of work samples"]
    },
    "aicte-pragati": {
        "simpleExplanation": "₹50,000/year for girls pursuing degree/diploma in AICTE-approved technical institutions (engineering, pharmacy, architecture, etc.). Up to 4,000 scholarships per year. Family income must be below ₹8 lakh.",
        "howToApply": ["Apply on National Scholarship Portal (scholarships.gov.in) after admission", "Or apply through AICTE portal at aicte-india.org", "Institute verifies and forwards application", "Scholarship credited directly to student's bank account"],
        "documentsRequired": ["Admission letter from AICTE-approved institution", "10th and 12th marksheets", "Family income certificate (below ₹8 lakh)", "Aadhaar Card", "Bank Account in student's name", "Caste certificate (if applicable)", "Fee receipt"]
    },
    "aicte-saksham": {
        "simpleExplanation": "₹50,000/year for differently-abled students (40%+ disability) in AICTE-approved degree/diploma programmes. No income limit. Covers tuition, books, and equipment. Up to 1,000 scholarships.",
        "howToApply": ["Apply on AICTE portal or National Scholarship Portal", "Submit disability certificate (UDID preferred)", "Institute verification required", "Amount credited to bank account in two instalments"],
        "documentsRequired": ["UDID / Disability certificate (40%+ disability)", "Admission proof at AICTE institution", "Aadhaar Card", "Bank Account Details", "Previous marksheets"]
    },
    "nsp-central-sector": {
        "simpleExplanation": "Top 82nd percentile scorers in Class 12 boards get ₹10,000/year (UG) and ₹20,000/year (PG). Based purely on board marks — no entrance exam. 82,000 scholarships per year. Family income below ₹8 lakh.",
        "howToApply": ["Apply on National Scholarship Portal after Class 12 results", "Board percentile verified automatically", "Institute verifies enrollment", "Renewed annually with 50%+ marks in college"],
        "documentsRequired": ["Class 12 marksheet", "College admission proof", "Aadhaar Card", "Family income certificate (below ₹8 lakh)", "Bank Account in student's name", "Caste certificate (for SC/ST quota)"]
    },
    "free-legal-aid": {
        "simpleExplanation": "Free lawyer, court fees, and legal help for: SC/ST persons, women, children, disabled, industrial workers, victims of trafficking, disaster victims, and anyone earning below ₹3 lakh/year. Available in every district.",
        "howToApply": ["Visit District Legal Services Authority (DLSA) office in your district court", "Or call NALSA helpline: 15100", "Or apply online at nalsa.gov.in", "Free lawyer assigned within 24 hours for urgent cases"],
        "documentsRequired": ["Any identity proof", "Income proof (if applying on economic ground)", "SC/ST certificate (if applying on category ground)", "Disability certificate (if applicable)", "Case details / FIR copy (if any)"]
    },
    "digital-saksharata": {
        "simpleExplanation": "Free digital literacy training for one person per household in rural areas. Learn to operate smartphones, email, internet, digital payments (UPI/Paytm), and access government services online. 10-20 hour course.",
        "howToApply": ["Enrol at nearest CSC (Common Service Centre)", "Or register at pmgdisha.in", "Attend 10-20 hours of training at training centre", "Get digital literacy certificate after completing assessment"],
        "documentsRequired": ["Aadhaar Card", "Mobile number", "No age limit (priority to 14-60 age group)"]
    },
    "iti-free-training": {
        "simpleExplanation": "Free vocational training in 130+ trades at 15,000+ government ITIs. Courses: 1-2 years. Trades include electrician, fitter, welder, plumber, mechanic, COPA (computer), stenography, and more. 80%+ placement rate.",
        "howToApply": ["Apply online at admission portal of your state's DTE/DGET", "Or apply at ncvtmis.gov.in during admission season (June-August)", "Merit-based selection from Class 8th/10th marks", "Free tuition at government ITIs — hostel may have nominal fees"],
        "documentsRequired": ["Class 8th or 10th marksheet (trade-dependent)", "Aadhaar Card", "Category certificate (if SC/ST/OBC)", "Domicile certificate", "Medical fitness certificate", "Transfer certificate from school"]
    },
    "health-wellness-centre": {
        "simpleExplanation": "1.6 lakh+ Health and Wellness Centres (HWCs) across India provide 12 types of free services: teleconsultation, medicines, maternal care, child health, NCD screening, dental, eye, mental health, ENT, and geriatric care.",
        "howToApply": ["Visit nearest Health and Wellness Centre / Sub Health Centre", "No registration or appointment needed", "All services free including medicines and consultations", "Teleconsultation with specialist available via e-Sanjeevani"],
        "documentsRequired": ["Aadhaar Card (optional, for medical records)", "No documents mandatory for treatment"]
    },
    "hiv-art": {
        "simpleExplanation": "Lifelong free Anti-Retroviral Treatment (ART) for all HIV+ patients at 650+ ART centres and 1,200+ Link ART centres. Includes free CD4 testing, viral load testing, and opportunistic infection treatment.",
        "howToApply": ["Get tested at any ICTC (Integrated Counselling and Testing Centre)", "If HIV+, register at nearest ART centre", "Start lifelong free ART medication", "Monthly medicine pickup with counselling support"],
        "documentsRequired": ["HIV test report", "Aadhaar Card (optional)", "Any photo ID for registration", "Referred by ICTC"]
    },
    "npcdcs-ncd": {
        "simpleExplanation": "Free screening for diabetes, hypertension/BP, and 3 types of cancer (oral, breast, cervical) for adults 30+ at all Health and Wellness Centres. Free medicines for BP and diabetes provided at HWC. Early detection saves lives.",
        "howToApply": ["Visit nearest Health and Wellness Centre after age 30", "ASHA/ANM may visit home for population-based screening", "Free blood sugar, BP check, and cancer screening", "If condition found, free treatment and monthly medicines at HWC"],
        "documentsRequired": ["No documents needed", "Aadhaar Card (optional, for ABHA health record)"]
    }
}

f = os.path.join(os.path.dirname(__file__), "schemes.json")
with open(f, "r", encoding="utf-8") as fp:
    schemes = json.load(fp)

updated = 0
for scheme in schemes:
    if scheme["id"] in details2:
        for key, val in details2[scheme["id"]].items():
            scheme[key] = val
        updated += 1

with open(f, "w", encoding="utf-8") as fp:
    json.dump(schemes, fp, indent=2, ensure_ascii=False)
print(f"Updated {updated} more schemes. Total: {len(schemes)}")
