import json, os

# Detailed howToApply and documentsRequired for schemes that have generic data
details = {
    "pm-kisan-maandhan": {
        "simpleExplanation": "Farmers aged 18-40 contribute ₹55-200/month based on age. Government matches your contribution equally. After age 60, you get guaranteed ₹3,000/month pension for life. Register at CSC or PM Kisan portal.",
        "howToApply": ["Visit nearest Common Service Centre (CSC) with Aadhaar and bank details", "Self-register at maandhan.in using mobile number", "Choose monthly contribution based on your age (₹55 for 18 years to ₹200 for 40 years)", "Contribution auto-debited from bank account monthly"],
        "documentsRequired": ["Aadhaar Card", "Savings Bank Account / Jan Dhan Account", "Mobile Number linked to Aadhaar", "Land ownership documents (if available)"]
    },
    "pm-kusum": {
        "simpleExplanation": "Get solar pumps for farm irrigation with 60% government subsidy. Save thousands on diesel and electricity bills every year. Available for individual farmers and farmer groups with agriculture land.",
        "howToApply": ["Apply online at mnre.gov.in or state renewable energy portal", "Submit land documents and water source details", "Get site inspection by state nodal agency", "Pay your 40% share — 30% as bank loan available, 10% farmer contribution"],
        "documentsRequired": ["Aadhaar Card", "Land ownership / lease documents", "Bank Account Details", "Electricity bill (if grid-connected)", "Water source certificate"]
    },
    "nrlm-svep": {
        "simpleExplanation": "Start your own village business with ₹2.5 lakh loan and free training. Get mentoring support, market linkages, and handholding for 3 years. Ideal for rural youth who want to become entrepreneurs.",
        "howToApply": ["Contact your Block Development Office or NRLM District Mission", "Attend Community Enterprise Fund (CEF) meeting", "Submit business proposal with help from Community Resource Person", "Get training and loan disbursement through SHG federation"],
        "documentsRequired": ["Aadhaar Card", "Bank Account Details", "SHG membership proof", "Business proposal document", "Residence proof"]
    },
    "pm-fme": {
        "simpleExplanation": "Get 35% credit-linked subsidy (up to ₹10 lakh) for starting or upgrading a micro food processing unit. Includes free training, branding support, and FSSAI registration help.",
        "howToApply": ["Apply online at pmfme.mofpi.gov.in", "Submit Detailed Project Report (DPR)", "Attend free training at designated institute", "Get bank loan — 35% subsidy credited directly to your loan account"],
        "documentsRequired": ["Aadhaar Card", "PAN Card", "Bank Account Details", "Udyam Registration (or apply simultaneously)", "Detailed Project Report", "Address proof of unit location"]
    },
    "nsa-widow": {
        "simpleExplanation": "Monthly pension of ₹300-500 for widows from BPL families. Amount varies by state — some states add their own top-up. No age limit. Payment directly to bank account via DBT.",
        "howToApply": ["Apply at Gram Panchayat office / Block Development Office", "Or apply online at nsap.nic.in", "Submit documents and verification by local authorities", "Pension starts after approval — credited monthly to bank account"],
        "documentsRequired": ["Aadhaar Card", "Death certificate of husband", "BPL Card / Income Certificate", "Bank Account Details", "Age proof", "Widow status certificate from local authority"]
    },
    "ddugky-urban": {
        "simpleExplanation": "Free skill training for urban poor — learn trades like computer operation, retail sales, hospitality, healthcare, and more. Includes placement support with minimum 50% placement guarantee.",
        "howToApply": ["Visit nearest NULM City Mission Management Unit (CMMU)", "Or contact Urban Local Body / Municipal Corporation", "Enroll in training programme at approved training centre", "Complete training and get placement assistance"],
        "documentsRequired": ["Aadhaar Card", "Address proof (urban area)", "Age proof", "Bank Account Details", "Passport size photographs", "Income certificate / BPL card"]
    },
    "jal-jeevan": {
        "simpleExplanation": "Every rural household gets a functional tap water connection providing 55 litres per person per day of clean drinking water. No application needed — implemented village by village. Check your village status online.",
        "howToApply": ["No individual application needed — implemented at village level", "Check your village status at jaljeevanmission.gov.in", "Contact Gram Panchayat / Block Development Office for status", "Community participation required through Gram Sabha"],
        "documentsRequired": ["No documents required — household-level implementation", "Ration card may be used for beneficiary identification"]
    },
    "ayushman-senior": {
        "simpleExplanation": "All citizens aged 70+ get free health insurance of ₹5 lakh per year regardless of income. Covers 1,929 medical procedures at 29,000+ empanelled hospitals. No premium needed.",
        "howToApply": ["Check eligibility at pmjay.gov.in or call 14555", "Visit nearest Ayushman Mitra at empanelled hospital", "Get Ayushman Card created with Aadhaar authentication", "Show card at any empanelled hospital for cashless treatment"],
        "documentsRequired": ["Aadhaar Card", "Age proof (70+ years)", "Any government photo ID", "Mobile number"]
    },
    "janani-suraksha": {
        "simpleExplanation": "Cash incentive of ₹600-1400 for pregnant women who deliver at a government hospital. Covers transport and post-delivery care. Higher amount in rural areas and low-performing states.",
        "howToApply": ["Register at nearest government health centre during pregnancy", "Get JSY card from ANM / ASHA worker", "Deliver at government or accredited private hospital", "Cash transferred to bank account within 7 days of delivery"],
        "documentsRequired": ["Aadhaar Card", "JSY registration card", "MCH (Mother and Child Health) card", "BPL card / income proof", "Bank Account Details", "Delivery discharge certificate"]
    },
    "pm-tb-mukt": {
        "simpleExplanation": "Complete free TB treatment at any government hospital. Additionally get ₹500/month nutrition support during treatment period (6-9 months). Treatment and medicines are 100% free.",
        "howToApply": ["Visit nearest government hospital or health centre for TB test", "If diagnosed, register on Nikshay portal (done by health worker)", "Start free DOTS treatment", "₹500/month nutrition support credited to bank account automatically"],
        "documentsRequired": ["Aadhaar Card", "Bank Account Details", "Nikshay registration number (assigned by health worker)", "Treatment card from DOTS centre"]
    },
    "cgelcgs": {
        "simpleExplanation": "Get business loans up to ₹5 crore without any collateral or third-party guarantee. Government provides credit guarantee to the bank. Covers manufacturing, service, and retail MSMEs.",
        "howToApply": ["Apply for loan at any scheduled commercial bank, NBFC, or SIDBI", "Submit business plan and financial documents", "Bank processes loan — no collateral required", "CGTMSE guarantee fee (0.37-1.85%) added to loan"],
        "documentsRequired": ["Udyam Registration Certificate", "Business PAN Card", "Last 3 years ITR and balance sheet", "Bank statements (6 months)", "Business plan / project report", "KYC documents of proprietor/partners/directors"]
    },
    "pm-yuva": {
        "simpleExplanation": "Mentoring programme for young authors aged below 30. Selected through national contest. Winners get ₹50,000/month for 6 months and their book is published by National Book Trust.",
        "howToApply": ["Watch for annual contest announcement on innovateindia.mygov.in", "Submit manuscript/book proposal through MyGov portal", "Shortlisted authors go through mentoring phase", "Final selected authors get scholarship and published book"],
        "documentsRequired": ["Age proof (below 30 years)", "Aadhaar Card", "Bank Account Details", "Manuscript or book proposal", "Educational certificates"]
    },
    "ntse": {
        "simpleExplanation": "India's most prestigious scholarship exam for Class 10 students. Win ₹1,250/month (Class 11-12) to ₹2,000/month (UG and above) scholarship that continues till PhD. Tests mental ability and scholastic aptitude.",
        "howToApply": ["Apply through your school for NTSE Stage 1 (state level) in November", "Clear Stage 1 to appear for Stage 2 (national level) in May", "Final selection based on MAT + SAT scores", "Scholarship activated from Class 11 onwards"],
        "documentsRequired": ["School ID card", "Class 9 marksheet", "Aadhaar Card", "Passport size photographs", "Category certificate (if SC/ST)"]
    },
    "gate-scholarship": {
        "simpleExplanation": "GATE-qualified students admitted to M.Tech / M.E. / M.Arch at IITs, NITs, and other AICTE-approved institutions get ₹12,400/month scholarship for 2 years. Must maintain minimum CGPA.",
        "howToApply": ["Qualify GATE exam with valid score", "Get admission to M.Tech programme at recognized institution", "Institution processes MHRD scholarship automatically", "Scholarship credited monthly to bank account"],
        "documentsRequired": ["GATE scorecard", "Admission letter from institution", "Aadhaar Card", "Bank Account Details", "UG degree certificate", "Category certificate (if applicable)"]
    },
    "pm-vidyalakshmi": {
        "simpleExplanation": "Single-window portal to apply for education loans from 38+ banks simultaneously. Compare interest rates, apply to multiple banks with one form. Covers Indian and foreign university courses.",
        "howToApply": ["Register at vidyalakshmi.co.in with email and mobile", "Fill single Common Education Loan Application Form (CELAF)", "Select up to 3 banks and submit application", "Banks process independently — track status on portal"],
        "documentsRequired": ["Admission letter from institution", "Fee structure details", "Aadhaar Card and PAN Card", "Parent/Guardian income proof", "Collateral documents (for loans above ₹7.5 lakh)", "Academic marksheets", "Bank statements of co-borrower"]
    },
    "ugc-net-jrf": {
        "simpleExplanation": "Qualify UGC NET with JRF to get ₹31,000/month (first 2 years) and ₹35,000/month (remaining 3 years) fellowship for pursuing PhD. Also get annual contingency grant of ₹10,000-₹20,500.",
        "howToApply": ["Apply for UGC NET exam conducted by NTA twice a year", "Qualify with JRF rank (top percentile)", "Get PhD admission at any UGC-recognized university", "Submit fellowship form through university to UGC"],
        "documentsRequired": ["UGC NET JRF certificate", "PhD admission letter", "Aadhaar Card", "Bank Account Details", "PG degree certificate and marksheets", "Category certificate (if applicable)"]
    },
    "pm-research-fellowship": {
        "simpleExplanation": "Elite fellowship of ₹70,000-80,000/month for top B.Tech graduates pursuing direct PhD at IITs/IISc. Only for students from NIRF top-100 institutions with CGPA 8.0+. Includes ₹2 lakh/year research grant.",
        "howToApply": ["Apply during May-June at pmrf.in", "Must have B.Tech/Integrated M.Tech from NIRF top-100 institution", "Lateral entry for MTech students at IITs/IISc also eligible", "Selection by national committee — join PhD at IIT/IISc/IISER/IISERs"],
        "documentsRequired": ["B.Tech degree with CGPA 8.0+", "GATE score (recommended but not mandatory)", "Research proposal", "Aadhaar Card", "Bank Account Details", "Recommendation letters from faculty"]
    },
    "swayam-mooc": {
        "simpleExplanation": "Free online courses from India's top professors at IITs, IIMs, and central universities. 3,000+ courses in engineering, humanities, science, commerce. Pay only ₹100-1,000 for exam and certificate.",
        "howToApply": ["Register free at swayam.gov.in", "Browse and enrol in any course", "Watch video lectures, complete assignments", "Optionally pay for proctored exam to get certificate"],
        "documentsRequired": ["Email ID for registration", "No documents needed for learning", "Government ID for proctored exam certificate"]
    },
    "navodaya-school": {
        "simpleExplanation": "Free residential schooling (Class 6-12) at 661 Jawahar Navodaya Vidyalayas across India. CBSE curriculum with free boarding, food, uniforms, textbooks. Selection through JNVST entrance exam in Class 5.",
        "howToApply": ["Apply online at navodaya.gov.in for JNVST exam (Class 5 students)", "Exam held annually in January/April", "Selection based on entrance test (no coaching needed)", "Free admission with complete residential facilities"],
        "documentsRequired": ["Birth certificate", "Class 4/5 marksheet", "Aadhaar Card", "Parent's income certificate", "Domicile certificate of the district", "Passport size photographs"]
    },
    "nhm-free-drugs": {
        "simpleExplanation": "All government hospitals and health centres provide essential medicines completely free through Jan Aushadhi counters. Covers 600+ medicines including antibiotics, painkillers, diabetes, BP, and heart medicines.",
        "howToApply": ["Visit any government hospital / PHC / CHC", "Doctor prescribes from essential drug list", "Collect free medicines from hospital pharmacy counter", "No registration or documents needed"],
        "documentsRequired": ["No documents required", "OPD slip from government hospital doctor"]
    },
    "nhm-free-diagnostics": {
        "simpleExplanation": "Free pathology (blood tests, urine tests) and radiology (X-ray, ultrasound, CT scan) at government hospitals. Covers 63 tests at district hospitals and 15 tests at CHC level.",
        "howToApply": ["Visit government hospital with doctor's prescription", "Get tests done at hospital lab — completely free", "Reports available same day or next day", "No registration needed beyond hospital OPD"],
        "documentsRequired": ["Doctor's prescription / referral", "Hospital OPD slip", "No other documents needed"]
    },
    "janani-shishu": {
        "simpleExplanation": "Complete free delivery services at government hospitals — normal and C-section. Includes free medicines, tests, blood, food, and transport (home to hospital and back). Zero out-of-pocket cost for mother and sick newborn.",
        "howToApply": ["Register at nearest government hospital during pregnancy", "All services are free — no application needed", "Free ambulance available through 102/108 helpline", "Covers treatment up to 30 days for sick newborns"],
        "documentsRequired": ["MCH (Mother and Child Health) card", "Aadhaar Card (if available)", "No documents needed for emergency delivery"]
    },
    "ppf": {
        "simpleExplanation": "Open a PPF account at any post office or bank. Deposit ₹500-₹1.5 lakh per year for 15 years. Get guaranteed 7.1% compound interest — completely tax-free. Best safe long-term investment in India.",
        "howToApply": ["Visit any post office or bank branch", "Fill PPF account opening form", "Minimum deposit ₹500/year, maximum ₹1.5 lakh/year", "Online deposits through internet banking available"],
        "documentsRequired": ["Aadhaar Card", "PAN Card", "Address proof", "Passport size photographs", "Nomination form"]
    },
    "pm-mudra-shishu": {
        "simpleExplanation": "Collateral-free micro business loan up to ₹50,000 under MUDRA Shishu. For small businesses like vegetable vendors, tailors, kirana shops, tea stalls. No guarantee needed. Interest rate 10-12%.",
        "howToApply": ["Visit any bank, NBFC, or Micro Finance Institution", "Fill MUDRA loan application form (available at mudra.org.in)", "Submit business details — no formal project report needed for Shishu", "Loan sanctioned within 7-10 days"],
        "documentsRequired": ["Aadhaar Card", "PAN Card (or Form 60)", "Address proof — utility bill / ration card", "Business proof — licence, GST, shop rent agreement", "Bank statements (3 months)", "2 passport size photographs"]
    },
    "pm-mudra-kishore": {
        "simpleExplanation": "Business loan of ₹50,000-₹5 lakh for growing small businesses under MUDRA Kishore. For established businesses that need working capital or equipment. No collateral required.",
        "howToApply": ["Apply at any bank, NBFC, or MFI branch", "Download application from mudra.org.in", "Submit business plan with projected revenues", "Loan processed within 15-20 days"],
        "documentsRequired": ["Aadhaar Card and PAN Card", "Business registration / Udyam certificate", "Last 2 years ITR / financial statements", "Bank statements (6 months)", "Business plan / Quotation for machinery", "Address proof of business premises"]
    },
    "pm-mudra-tarun": {
        "simpleExplanation": "Business expansion loan of ₹5-10 lakh under MUDRA Tarun for established businesses. Covers working capital, equipment, and expansion needs. Competitive interest rates with flexible repayment.",
        "howToApply": ["Apply at any scheduled commercial bank", "Submit detailed business plan and financial projections", "Bank conducts business assessment", "Loan sanctioned based on business viability"],
        "documentsRequired": ["Udyam Registration", "PAN Card and Aadhaar Card", "Last 3 years ITR and audited balance sheets", "Bank statements (12 months)", "Business plan with projections", "Identity and address proof", "Quotations for assets to be purchased"]
    },
    "sie-equity": {
        "simpleExplanation": "Get up to ₹50 lakh seed funding for your early-stage startup through DPIIT-recognized incubators. Covers proof of concept, prototype development, product trials, and market entry. Grant, not a loan.",
        "howToApply": ["Register your startup at startupindia.gov.in and get DPIIT recognition", "Apply through an approved incubator (list at seedfund.startupindia.gov.in)", "Submit business plan and pitch to incubator", "Incubator evaluates and disburses seed fund in tranches"],
        "documentsRequired": ["DPIIT Startup Recognition certificate", "Company incorporation documents (CIN)", "Business plan / pitch deck", "Bank account of the startup company", "PAN of the company", "Founder Aadhaar and PAN"]
    },
    "ka-gruha-lakshmi": {
        "simpleExplanation": "Women who are heads of households in Karnataka receive ₹2,000 per month directly to their bank account. One woman per household eligible. Must be a Karnataka resident with ration card.",
        "howToApply": ["Apply online at sevasindhuservices.karnataka.gov.in", "Or visit nearest Grama One / Bangalore One centre", "Aadhaar-linked bank account mandatory for DBT", "Application verified by local authorities"],
        "documentsRequired": ["Aadhaar Card", "Ration Card (head of family)", "Bank Account linked to Aadhaar", "Voter ID / Residence proof", "Mobile number linked to Aadhaar"]
    },
    "ka-anna-bhagya": {
        "simpleExplanation": "Every BPL family in Karnataka gets 10 kg of free rice per person per month through the PDS system. Previously 7 kg, now enhanced to 10 kg. Collect from nearest Fair Price Shop.",
        "howToApply": ["Must have BPL / AAY / Priority ration card", "Visit nearest Fair Price Shop with ration card", "Collect free rice using Aadhaar biometric authentication", "Monthly entitlement auto-allocated"],
        "documentsRequired": ["BPL / AAY Ration Card", "Aadhaar Card linked to ration card"]
    },
    "wb-swasthya-sathi": {
        "simpleExplanation": "Every family in West Bengal gets ₹5 lakh cashless health insurance per year. Smart card issued in woman's name. Covers hospitalization at 2,000+ empanelled hospitals. No premium to pay.",
        "howToApply": ["Attend Duare Sarkar camp or visit sub-divisional office", "Apply with family ration card / voter ID", "Smart Health Card issued on the spot with biometric", "Use card at any empanelled hospital for cashless treatment"],
        "documentsRequired": ["Ration Card (family)", "Aadhaar Card of all family members", "Voter ID Card", "Mobile number"]
    },
    "mh-lek-ladki": {
        "simpleExplanation": "Girls born in Maharashtra's economically weaker families receive ₹1,01,000 in instalments: ₹5,000 at birth, ₹4,000 in Class 1, ₹6,000 in Class 6, ₹8,000 in Class 11, and ₹75,000 at age 18.",
        "howToApply": ["Register girl child's birth at hospital / Gram Panchayat", "Apply at nearest Anganwadi centre or Tahsil office", "Submit documents for each instalment at respective stage", "Amount credited to girl's bank / joint account with mother"],
        "documentsRequired": ["Birth Certificate of girl child", "Mother's Aadhaar Card", "Family income certificate (below ₹1 lakh)", "Yellow / Orange ration card", "Bank Account (joint - mother and daughter)", "School enrolment proof (for education instalments)"]
    },
    "ts-rythu-bandhu": {
        "simpleExplanation": "Every farmer in Telangana with registered agricultural land gets ₹10,000 per acre per year (₹5,000 each in Kharif and Rabi season). Money deposited directly into farmer's bank account before each season.",
        "howToApply": ["Automatic — all registered patta (land) holders are beneficiaries", "Verify details at rythubandhu.telangana.gov.in", "Contact Agriculture Extension Officer if not receiving", "Amount credited before each crop season"],
        "documentsRequired": ["Land ownership patta", "Aadhaar Card linked to bank account", "Bank Account Details"]
    },
    "rajasthan-chiranjeevi": {
        "simpleExplanation": "All Rajasthan families get ₹25 lakh health insurance per family per year. Free for government employees, NFSA, small/marginal farmers. Others pay just ₹850/year. Covers 1,597 packages at empanelled hospitals.",
        "howToApply": ["Register at chiranjeevi.rajasthan.gov.in or nearest e-Mitra kiosk", "NFSA/BPL families auto-enrolled — just verify Aadhaar", "Others pay ₹850/year premium through SSO portal", "Download Chiranjeevi card or use Aadhaar at hospital"],
        "documentsRequired": ["Jan Aadhaar Card (Rajasthan family ID)", "Aadhaar Card", "Mobile number", "NFSA / BPL card (for free coverage)"]
    },
    "bihar-student-credit": {
        "simpleExplanation": "Bihar students get up to ₹4 lakh education loan at 0% interest for pursuing higher education (graduation and above). Covers tuition, hostel, books, and laptop. Repayment starts after course completion.",
        "howToApply": ["Apply online at 7nishchay.bihar.gov.in", "Login through Bihar state portal with Aadhaar", "Upload required documents and course details", "District-level committee approves — amount disbursed to institution"],
        "documentsRequired": ["12th marksheet and certificate", "Admission letter from recognized institution", "Aadhaar Card", "Family income certificate", "Domicile certificate of Bihar", "Bank Account Details", "Fee structure of the course"]
    },
    "up-kanya-sumangla": {
        "simpleExplanation": "Girls in UP receive ₹15,000 in 6 instalments from birth to graduation: ₹2,000 at birth, ₹1,000 each at age 1 (vaccination), Class 1, Class 6, Class 9, and ₹5,000 at graduation admission. Family income must be below ₹3 lakh.",
        "howToApply": ["Apply online at mksy.up.gov.in", "Create account and fill application form", "Upload documents for the relevant instalment stage", "Amount credited after verification by District Programme Officer"],
        "documentsRequired": ["Birth Certificate of girl", "Mother-daughter joint photograph", "Aadhaar Card of parent and girl", "Family income certificate (below ₹3 lakh)", "Bank Account Details", "Address proof / Voter ID"]
    },
    "hp-medha-protsahan": {
        "simpleExplanation": "HP students from families earning below ₹2.5 lakh get ₹1 lakh for coaching at Delhi, Chandigarh, or other top coaching centres for UPSC, JEE, NEET, CLAT, and other competitive exams.",
        "howToApply": ["Apply online at himachal.nic.in scholarship portal", "Must have secured admission at approved coaching institute", "Selection based on merit — Class 12 marks", "₹1 lakh disbursed in two instalments to coaching institute"],
        "documentsRequired": ["Class 12 marksheet (for UG coaching)", "Graduation marksheet (for UPSC coaching)", "Admission letter from coaching institute", "Family income certificate", "Aadhaar Card", "HP domicile certificate", "Bank Account Details"]
    },
    "cg-mahtari-vandan": {
        "simpleExplanation": "All married women aged 21-60 in Chhattisgarh get ₹1,000/month (₹12,000/year) directly in their bank account. Registration done through camps and Anganwadi centres. DBT to Aadhaar-linked account.",
        "howToApply": ["Register at Anganwadi centre or Mahtari Vandan camp", "Or apply online at mahtarivandan.cgstate.gov.in", "Aadhaar-linked bank account mandatory", "₹1,000 credited monthly after verification"],
        "documentsRequired": ["Aadhaar Card", "Marriage Certificate or marriage proof", "Bank Account (in woman's name, linked to Aadhaar)", "Age proof", "Chhattisgarh domicile / residence proof"]
    },
    "as-orunodoi": {
        "simpleExplanation": "Women in Assam's BPL/low-income families get ₹1,250/month deposited to their bank account. Covers about 25 lakh families. Amount can be used for any household need — no restriction on usage.",
        "howToApply": ["Apply at Deputy Commissioner's office or Circle office", "Or through Orunodoi portal", "Verification by local authorities and Gram Panchayat", "₹1,250 credited monthly to nominee woman's bank account"],
        "documentsRequired": ["Aadhaar Card", "Bank Account in woman's name", "BPL / income certificate", "Voter ID / Assam domicile proof", "Ration Card"]
    },
    "odisha-kalia": {
        "simpleExplanation": "Small and marginal farmers in Odisha get ₹10,000/year (₹5,000 each in Kharif and Rabi) for crop cultivation. Landless agricultural households get ₹12,500 for livelihood activities. Covers 92% of Odisha's cultivators.",
        "howToApply": ["Check beneficiary status at kalia.odisha.gov.in", "If not listed, apply at Block office or through eModi app", "Gram Panchayat verifies and recommends", "Amount credited directly to Aadhaar-linked bank account"],
        "documentsRequired": ["Aadhaar Card", "Bank Account linked to Aadhaar", "Land records (ROR / Patta) for farmer category", "Address proof for landless category"]
    },
    "tn-kalaignar": {
        "simpleExplanation": "All women who are heads of families in Tamil Nadu aged 21-60 and earning below income threshold get ₹1,000/month to their bank account. Nearly 1 crore women benefit. Can be used for any family need.",
        "howToApply": ["Apply at taluk office or through TN e-Sevai portal", "Aadhaar-linked bank account required", "Application verified by Revenue department", "₹1,000 deposited monthly through DBT"],
        "documentsRequired": ["Aadhaar Card", "Ration Card (family head)", "Bank Passbook (woman's name)", "Family income certificate", "Residence proof"]
    },
    "dl-ladli": {
        "simpleExplanation": "Every girl child born in Delhi gets ₹5,000 at birth and ₹5,000 at admission to Classes 1, 6, 9, 10, and 12 — totalling ₹35,000-₹36,000. Amount kept as fixed deposit, matured at age 18.",
        "howToApply": ["Hospital submits birth registration for institutional delivery", "Parents apply online at wcddel.in within 1 year of birth", "For school-stage benefits, apply through school with class records", "FD matures and becomes accessible when girl turns 18"],
        "documentsRequired": ["Birth Certificate", "Aadhaar Card of parents", "3 years residence proof in Delhi", "Caste certificate (if SC/ST)", "School admission proof (for education instalments)", "Parents' income proof"]
    }
}

f = os.path.join(os.path.dirname(__file__), "schemes.json")
with open(f, "r", encoding="utf-8") as fp:
    schemes = json.load(fp)

updated = 0
for scheme in schemes:
    sid = scheme["id"]
    if sid in details:
        for key, val in details[sid].items():
            scheme[key] = val
        updated += 1

with open(f, "w", encoding="utf-8") as fp:
    json.dump(schemes, fp, indent=2, ensure_ascii=False)

print(f"Updated {updated} schemes with proper details. Total schemes: {len(schemes)}")
