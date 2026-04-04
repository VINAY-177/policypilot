import json, os

schemes = [
# ===== SCHOLARSHIP SCHEMES =====
("moma-scholarship-pre","Pre-Matric Scholarship for Minorities","Minority Pre-Matric","education","📗",
 "₹4,500-7,700/year for minority students (Muslim, Christian, Sikh, Buddhist, Jain, Parsi) studying in Class 1-10. Covers admission, tuition, and maintenance allowance.",
 7700,6,16,200000,["general","obc"],["male","female","other"],["student"],"all",["student","minority"],[],
 "https://scholarships.gov.in",
 ["Apply on National Scholarship Portal (scholarships.gov.in) during July-October","Login with Aadhaar, fill academic and bank details","Institute verifies enrollment and minority status","Scholarship credited to student's bank account in instalments"],
 ["Minority community certificate","Previous year marksheet","Income certificate (below ₹2 lakh)","Aadhaar Card","Bank Account (student or parent)","Bonafide certificate from school"]),

("moma-scholarship-post","Post-Matric Scholarship for Minorities","Minority Post-Matric","education","📘",
 "₹7,000-16,500/year for minority students (Class 11 to PhD). Covers tuition fee reimbursement + maintenance allowance. Family income below ₹2 lakh/year.",
 16500,16,35,200000,["general","obc"],["male","female","other"],["student"],"all",["student","minority"],[],
 "https://scholarships.gov.in",
 ["Apply on National Scholarship Portal during October-December window","Select Post-Matric Scholarship for Minorities scheme","Institute verifies and forwards to state minority department","Scholarship credited to bank account after approval"],
 ["Minority community certificate","Class 10/12 marksheet","College/university enrollment proof","Income certificate (below ₹2 lakh)","Aadhaar Card","Bank Account in student's name","Fee receipt from institution"]),

("maulana-azad-fellowship","Maulana Azad National Fellowship (Minorities)","Maulana Azad PhD","education","🎓",
 "₹31,000-35,000/month fellowship for minority students pursuing M.Phil/PhD. 5-year duration. Includes ₹10,000-₹20,500/year contingency grant. 756 fellowships annually.",
 420000,22,40,100000000,["general","obc"],["male","female","other"],["student"],"all",["student","minority"],[],
 "https://minorityaffairs.gov.in",
 ["Clear UGC NET JRF or CSIR NET JRF exam","Get PhD admission at UGC-recognized university","Apply through university to Ministry of Minority Affairs","Fellowship activated after admission verification"],
 ["UGC NET JRF / CSIR NET JRF certificate","PhD admission letter","Minority community certificate","Aadhaar Card","Bank Account Details","PG degree certificate"]),

("nsp-sc-postmatric","Post-Matric Scholarship for SC Students","SC Post-Matric","education","📕",
 "Full tuition + ₹230-1,200/month maintenance for SC students (Class 11 to PhD). Family income below ₹2.5 lakh. India's largest scholarship — 56 lakh+ beneficiaries.",
 50000,16,35,250000,["sc"],["male","female","other"],["student"],"all",["student"],[],
 "https://scholarships.gov.in",
 ["Apply on National Scholarship Portal (scholarships.gov.in)","Institute verifies caste and enrollment","State Social Welfare department approves","Full fee reimbursement + monthly maintenance to bank account"],
 ["SC caste certificate","Previous year marksheet","Family income certificate (below ₹2.5 lakh)","Aadhaar Card","Bank Account in student's name","Fee receipt","Institute bonafide certificate"]),

("nsp-st-postmatric","Post-Matric Scholarship for ST Students","ST Post-Matric","education","📗",
 "Full tuition + ₹230-1,200/month for ST students (Class 11 to PhD). Family income below ₹2.5 lakh. No limit on number of scholarships — all eligible ST students get it.",
 50000,16,35,250000,["st"],["male","female","other"],["student"],"all",["student"],[],
 "https://scholarships.gov.in",
 ["Apply on National Scholarship Portal","Select Post-Matric Scholarship for ST scheme","Institute and tribal welfare department verify","Tuition paid to institute, maintenance to student's bank"],
 ["ST certificate","Marksheets","Income certificate (below ₹2.5 lakh)","Aadhaar Card","Bank Account","Fee receipt from institution"]),

("nsp-obc-postmatric","Post-Matric Scholarship for OBC Students","OBC Post-Matric","education","📒",
 "Full tuition + ₹230-750/month maintenance for OBC students (Class 11 to PhD). Family income must be below ₹1 lakh/year (non-creamy layer). Covers 10 lakh+ students annually.",
 25000,16,35,100000,["obc"],["male","female","other"],["student"],"all",["student"],[],
 "https://scholarships.gov.in",
 ["Apply on National Scholarship Portal","Submit OBC non-creamy layer certificate","Institute verifies enrollment","Tuition + maintenance credited to bank account"],
 ["OBC non-creamy layer certificate","Income certificate (below ₹1 lakh)","Previous marksheets","Aadhaar Card","Bank Account","Institute enrollment proof"]),

("begum-hazrat-mahal","Begum Hazrat Mahal Scholarship (Minority Girls)","BHM Girls Scholar","education","👩‍🎓",
 "₹5,000 (Class 9-10) and ₹6,000 (Class 11-12) for minority girls scoring 50%+ marks. Family income below ₹2 lakh. Covers 60,000+ girls annually across India.",
 6000,13,19,200000,["general","obc"],["female"],["student"],"all",["student","minority"],[],
 "https://bhmnsmaef.org",
 ["Apply online at bhmnsmaef.org during scholarship window","School verifies minority status and marks","Maulana Azad Education Foundation processes","Amount transferred to girl's bank account"],
 ["Minority community certificate","Marksheet (50%+ marks required)","Income certificate (below ₹2 lakh)","Aadhaar Card","Bank Account","School bonafide certificate"]),

("ishan-uday","Ishan Uday Scholarship (North East)","NE Students Scholar","education","🏔️",
 "₹5,400/month (technical) or ₹3,800/month (general) for NE state students pursuing UG courses. 10,000 scholarships/year. Must join college outside NE region also eligible.",
 64800,17,25,450000,["general","obc","sc","st"],["male","female","other"],["student"],
 ["assam","arunachal pradesh","manipur","meghalaya","mizoram","nagaland","sikkim","tripura"],
 ["student"],[],
 "https://ugc.gov.in",
 ["Apply through UGC portal after getting admission to recognized UG programme","University verifies NE domicile status","UGC selects based on merit and family income","Scholarship credited monthly for duration of course"],
 ["NE state domicile certificate","UG admission letter","Family income certificate (below ₹4.5 lakh)","Aadhaar Card","Bank Account","Class 12 marksheet"]),

("inspire-scholarship","DST INSPIRE SHE Scholarship","INSPIRE SHE","education","🔭",
 "₹80,000/year (₹5,000/month + ₹20,000 summer research) for top 1% performers in Class 12 boards pursuing BSc/BS/Integrated MSc in natural and basic sciences.",
 80000,17,23,100000000,["general","obc","sc","st"],["male","female","other"],["student"],"all",["student"],[],
 "https://online-inspire.gov.in",
 ["Top 1% rankers in Class 12 boards automatically eligible","Or KVPY/JEE/NEET qualified students eligible","Apply online at online-inspire.gov.in after BSc admission","₹5,000/month + ₹20,000 summer project credited to bank"],
 ["Class 12 marksheet (top 1% proof)","BSc/Integrated MSc admission letter","Aadhaar Card","Bank Account","KVPY/JEE/NEET scorecard (if applicable)"]),

("kishore-vaigyanik","KVPY Fellowship","KVPY Fellow","education","🧪",
 "₹5,000/month (UG) or ₹7,000/month (PG) + annual contingency ₹20,000-28,000 for students in basic sciences. One of India's most prestigious science fellowships. Valid till PhD.",
 84000,16,25,100000000,["general","obc","sc","st"],["male","female","other"],["student"],"all",["student"],[],
 "https://kvpy.iisc.ac.in",
 ["Apply online at kvpy.iisc.ac.in (November-December)","Clear aptitude test held in January","Shortlisted candidates attend interview","Final selection — fellowship starts from UG 1st year"],
 ["Class 10/12 marksheets","Aadhaar Card","Bank Account Details","Passport size photograph","UG/PG enrollment proof (if already studying)"]),

("pm-scholarship-rpf","PM Scholarship for RPF/CISF Wards","PM Scholar Forces","education","🎖️",
 "₹3,000/month (boys) and ₹3,250/month (girls) for children of RPF/RPSF/CISF personnel pursuing professional courses. Covers engineering, medicine, MBA, law. 150 scholarships/year.",
 39000,17,25,100000000,["general","obc","sc","st"],["male","female","other"],["student"],"all",["student"],[],
 "https://scholarships.gov.in",
 ["Apply on National Scholarship Portal during admission year","RPF/CISF HQ verifies parent's service record","Selection based on Class 12 marks","Scholarship for full duration of professional course"],
 ["Parent's RPF/CISF service certificate","Class 12 marksheet","Professional course admission proof","Aadhaar Card","Bank Account in student's name"]),

("warb-scholarship","WARB Scholarship (ex-servicemen wards)","Ex-Servicemen Scholar","education","🎖️",
 "₹2,500-3,000/month for children/widows of ex-servicemen, war widows pursuing professional courses (engineering, medical, MBA). 5,500 scholarships per year.",
 36000,17,25,100000000,["general","obc","sc","st"],["male","female","other"],["student"],"all",["student"],[],
 "https://aborads.gov.in",
 ["Apply on KSB portal online","Ex-serviceman's Zila Sainik Board verifies","Selection based on marks and service record of parent","Monthly scholarship for course duration"],
 ["Ex-serviceman's discharge certificate","Dependent certificate from record office","Class 12 marksheet","Course admission proof","Aadhaar Card","Bank Account"]),

# ===== INTERNSHIP SCHEMES =====
("pm-internship","PM Internship Scheme 2024","PM Internship","employment","💼",
 "₹5,000/month stipend + ₹6,000 one-time grant for youth 21-24 years. 12-month internship at top 500 companies in India. 1 crore internships over 5 years. Real work experience at corporate offices.",
 66000,21,24,800000,["general","obc","sc","st"],["male","female","other"],["student","unemployed"],"all",[],["government_employee"],
 "https://pminternship.mca.gov.in",
 ["Register at pminternship.mca.gov.in with Aadhaar","Browse and apply to internship opportunities","Company shortlists and selects candidates","12-month internship begins with ₹5,000/month stipend"],
 ["Aadhaar Card","Educational certificates (ITI/Diploma/Degree)","Bank Account Details","Resume/CV","PAN Card","Medical fitness certificate"]),

("niti-internship","NITI Aayog Internship","NITI Intern","employment","🏛️",
 "Prestigious internship at NITI Aayog for students and researchers. Work on national policy research. No stipend but certificate from NITI Aayog. Duration: 6 weeks to 6 months. Apply any time.",
 0,18,28,100000000,["general","obc","sc","st"],["male","female","other"],["student"],"all",["student"],[],
 "https://niti.gov.in/internship",
 ["Apply online at niti.gov.in/internship","Submit SOP (Statement of Purpose) and resume","Selection by NITI Aayog verticals based on research interest","Intern works on policy research projects for 6 weeks-6 months"],
 ["Resume/CV","Academic transcripts","Statement of Purpose (SOP)","Letter from university (if student)","Aadhaar Card","Passport size photograph"]),

("icar-internship","ICAR Student READY Internship","ICAR Agri Intern","employment","🌾",
 "Mandatory 6-month internship for agriculture university students. ₹3,000/month stipend. Work at KVK, ICAR institutes, agri-tech companies. Hands-on experience in farming technology and rural development.",
 18000,20,28,100000000,["general","obc","sc","st"],["male","female","other"],["student"],"all",["student"],[],
 "https://icar.org.in",
 ["Enroll through your agriculture university","University assigns KVK/ICAR institute placement","Complete 6-month hands-on training programme","Receive certificate and ₹3,000/month stipend"],
 ["Agriculture university enrollment proof","Aadhaar Card","Bank Account Details","University forwarding letter"]),

("csir-summer-training","CSIR Summer Research Training","CSIR Summer Intern","education","🔬",
 "Work with top scientists at CSIR labs for 2 months (May-July). Stipend of ₹5,000-10,000/month. Open to BSc/BTech/MSc students. 38 CSIR labs across India covering chemistry, physics, biology, engineering.",
 20000,18,28,100000000,["general","obc","sc","st"],["male","female","other"],["student"],"all",["student"],[],
 "https://csir.res.in",
 ["Check individual CSIR lab websites for summer training notifications","Apply directly to lab of interest with resume and SOP","Scientist evaluates and selects students","Selected students join for May-July summer training"],
 ["UG/PG enrollment proof","Academic transcripts","CV/Resume","Statement of Purpose","Recommendation letter from faculty","Aadhaar Card"]),

("indian-academy-summer","IAS-INSA-NASI Summer Fellowship","Science Summer Fellow","education","🧬",
 "₹5,000/month for 2 months + travel for BSc/MSc/BTech students to work with top scientists at IISc/IITs/national labs. India's most prestigious summer research programme. 3,000+ positions.",
 10000,17,25,100000000,["general","obc","sc","st"],["male","female","other"],["student"],"all",["student"],[],
 "https://web-japps.ias.ac.in",
 ["Apply online at web-japps.ias.ac.in during November-December","Select up to 3 research guides/topics","Guide selects students based on profile","2-month fellowship at guide's institution during May-July"],
 ["Academic transcripts and marksheets","CV/Resume with research interests","Recommendation from faculty member","Aadhaar Card","Bank Account Details"]),

("tulip-internship","TULIP Urban Internship","TULIP Urban","employment","🏙️",
 "Internships for fresh graduates with Urban Local Bodies (Municipal Corporations). Work on smart city projects, urban planning, GIS mapping, data analytics. Stipend varies ₹5,000-15,000/month.",
 15000,18,30,100000000,["general","obc","sc","st"],["male","female","other"],["student","unemployed"],"all",[],[],
 "https://tulip.mohua.gov.in",
 ["Register at tulip.mohua.gov.in as a student/graduate","Browse internship opportunities in your city","Apply to ULB/Smart City internships of interest","Municipal body selects and assigns projects"],
 ["Graduation/degree certificate","Aadhaar Card","Resume/CV","Bank Account Details","College ID (if current student)"]),

("startup-india-intern","Startup India Learning Programme","Startup India Learn","employment","🚀",
 "Free online courses and mentoring for aspiring entrepreneurs. Learn from successful founders, VCs, and industry experts. Certificate from DPIIT on completion. Self-paced 4-week modules.",
 0,18,45,100000000,["general","obc","sc","st"],["male","female","other"],"all","all",[],[],
 "https://www.startupindia.gov.in/content/sih/en/learning-and-development.html",
 ["Register free at startupindia.gov.in","Browse learning modules under 'Learning Programme'","Complete self-paced courses on entrepreneurship topics","Earn certificate from DPIIT on completion"],
 ["Email ID for registration","No documents needed for online learning"]),

("msme-internship","MSME Internship through Tool Rooms","MSME Tool Room","employment","🔧",
 "6-month internship at MSME Tool Rooms and Technology Development Centres. Learn CNC, CAD/CAM, plastics, electronics. Stipend ₹5,000/month. 18 centres across India.",
 30000,18,35,100000000,["general","obc","sc","st"],["male","female","other"],["student","unemployed"],"all",[],[],
 "https://msme.gov.in",
 ["Contact nearest MSME Tool Room / Technology Development Centre","Apply for internship during admission cycle","Selection based on qualification and aptitude test","6-month hands-on training with ₹5,000/month stipend"],
 ["ITI/Diploma/Engineering certificate","Aadhaar Card","Bank Account Details","Passport photographs"]),

("drdo-internship","DRDO Internship for Engineering Students","DRDO Intern","employment","🛡️",
 "Work at DRDO labs on defence R&D projects. For BTech/MTech/PhD students. Duration: 2-6 months. Stipend ₹10,000-25,000/month. Top performers may get pre-placement offers.",
 150000,20,30,100000000,["general","obc","sc","st"],["male","female","other"],["student"],"all",["student"],[],
 "https://rac.gov.in",
 ["Check DRDO lab websites for internship notifications","Apply with resume, transcripts, and research proposal","Lab Director selects based on project requirements","Join lab for 2-6 months with stipend"],
 ["BTech/MTech enrollment proof","Academic transcripts (7.5+ CGPA preferred)","Research proposal aligned with lab work","Aadhaar Card","NOC from university","Security clearance form"]),

("isro-internship","ISRO Internship (IIRS/SAC)","ISRO Intern","employment","🚀",
 "Work at ISRO centres on space technology projects. Open to BTech/MSc/PhD students. IIRS Dehradun and SAC Ahmedabad regularly offer summer/semester internships. Certificate from ISRO.",
 0,20,30,100000000,["general","obc","sc","st"],["male","female","other"],["student"],"all",["student"],[],
 "https://isro.gov.in",
 ["Check ISRO centre websites for internship announcements","Apply to specific centre (IIRS/SAC/VSSC etc) directly","Selection based on academic profile and research interest","Intern works on ongoing ISRO projects for 1-6 months"],
 ["BTech/MSc enrollment proof with good CGPA","Research proposal","University NOC","Aadhaar Card","CV/Resume"]),

("rbi-internship","RBI Research Internship","RBI Research Intern","employment","🏦",
 "Work with RBI economists on monetary policy, banking, financial inclusion research. For post-graduate students and PhD scholars. Stipend ₹35,000/month. Duration: 2-4 months.",
 140000,22,30,100000000,["general","obc","sc","st"],["male","female","other"],["student"],"all",["student"],[],
 "https://rbi.org.in",
 ["Check RBI website for research internship notifications (annual)","Apply online with research proposal and CV","Academic credentials and research aptitude evaluated","Selected interns work at RBI offices for 2-4 months"],
 ["PG/PhD enrollment proof (Economics/Statistics/Finance)","CV with publications (if any)","Research proposal","Academic transcripts","Aadhaar Card","University recommendation letter"]),
]

def build(d):
    return {"id":d[0],"name":d[1],"shortName":d[2],"category":d[3],"icon":d[4],
        "benefit":d[5],"benefitValue":d[6],"simpleExplanation":d[5],
        "eligibility":{"minAge":d[7],"maxAge":d[8],"maxIncome":d[9],
            "categories":d[10],"gender":d[11],
            "occupations":d[12] if isinstance(d[12],list) else "all",
            "states":d[13] if isinstance(d[13],list) else "all",
            "conditions":d[14],"excludeConditions":d[15]},
        "howToApply":d[17],
        "documentsRequired":d[18],
        "officialUrl":d[16],
        "whyQualifyTemplate":"Based on your profile, you meet the eligibility criteria for this scheme."}

f = os.path.join(os.path.dirname(__file__),"schemes.json")
with open(f,"r",encoding="utf-8") as fp:
    existing = json.load(fp)
ids = {s["id"] for s in existing}
added = 0
for d in schemes:
    if d[0] not in ids:
        existing.append(build(d))
        added += 1
with open(f,"w",encoding="utf-8") as fp:
    json.dump(existing, fp, indent=2, ensure_ascii=False)
print(f"Done! Added {added} scholarship+internship schemes. Total: {len(existing)}")
