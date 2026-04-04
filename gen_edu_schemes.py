import json, os
edu_schemes = [
("ugc-net-jrf","UGC NET JRF Fellowship","UGC NET JRF","education","🎓","₹31,000-35,000/month fellowship for NET-JRF qualified candidates pursuing PhD",420000,22,40,100000000,["general","obc","sc","st"],["male","female","other"],["student"],"all",["student"],[],"https://ugcnetonline.in"),
("gate-scholarship","GATE Scholarship for M.Tech","GATE Scholar","education","⚙️","₹12,400/month scholarship for GATE-qualified students admitted to IITs/NITs for M.Tech",148800,20,30,100000000,["general","obc","sc","st"],["male","female","other"],["student"],"all",["student"],[],"https://gate.iitd.ac.in"),
("pm-vidyalakshmi","PM Vidya Lakshmi (Education Loan)","Vidya Lakshmi Loan","education","🏦","Education loans from multiple banks at subsidized interest — covers tuition, hostel, books",1000000,17,35,100000000,["general","obc","sc","st"],["male","female","other"],["student"],"all",["student"],[],"https://vidyalakshmi.co.in"),
("interest-subsidy-edu","Central Sector Interest Subsidy","Edu Interest Subsidy","education","📉","Full interest subsidy during moratorium period on education loans for EWS students",200000,17,30,450000,["general","obc","sc","st"],["male","female","other"],["student"],"all",["student"],[],"https://vidyalakshmi.co.in"),
("pgcil-scholarship","PGCIL Scholarship for Engineering","PGCIL Scholar","education","⚡","₹45,000/year for engineering students from SC/ST/PwD category by Power Grid",45000,17,25,100000000,["sc","st"],["male","female","other"],["student"],"all",["student"],[],"https://powergrid.in"),
("ntse","National Talent Search Examination","NTSE","education","🧠","₹1,250-₹2,000/month scholarship for Class 10 toppers till PhD — India's most prestigious exam",24000,14,30,100000000,["general","obc","sc","st"],["male","female","other"],["student"],"all",["student"],[],"https://ncert.nic.in"),
("kvpy-kishore","KVPY Kishore Vaigyanik","KVPY Science","education","🔬","₹5,000-₹7,000/month + annual contingency for students pursuing basic sciences",84000,16,25,100000000,["general","obc","sc","st"],["male","female","other"],["student"],"all",["student"],[],"https://kvpy.iisc.ac.in"),
("aicte-saksham","AICTE Saksham Scholarship","Saksham PwD","education","♿","₹50,000/year for differently-abled students in AICTE-approved technical institutions",50000,17,30,800000,["general","obc","sc","st"],["male","female","other"],["student"],"all",["student","disability"],[],"https://aicte-india.org"),
("aicte-pragati","AICTE Pragati Scholarship (Girls)","Pragati Girls Tech","education","👩‍💻","₹50,000/year for girls in AICTE-approved degree/diploma technical courses",50000,17,25,800000,["general","obc","sc","st"],["female"],["student"],"all",["student"],[],"https://aicte-india.org"),
("aicte-swanath","AICTE Swanath Scholarship","Swanath Orphan","education","🤝","₹50,000/year for orphans/wards of armed forces/COVID victims in technical courses",50000,17,25,800000,["general","obc","sc","st"],["male","female","other"],["student"],"all",["student"],[],"https://aicte-india.org"),
("sitaram-jindal","Sitaram Jindal Foundation Scholarship","Jindal Scholar","education","📘","₹1,000-₹12,000/year for underprivileged students from Class 1 to post-graduation",12000,5,30,200000,["general","obc","sc","st"],["male","female","other"],["student"],"all",["student"],[],"https://sitaramjindalfoundation.org"),
("dn-merit","Dr. Ambedkar Merit Scholarship","Ambedkar Merit","education","📕","₹10,000-₹25,000/year for SC/ST students scoring 80%+ in Class 12",25000,16,25,100000000,["sc","st"],["male","female","other"],["student"],"all",["student"],[],"https://socialjustice.gov.in"),
("nsp-disability-scholar","Scholarship for PwD Students","PwD Scholarship","education","♿","Maintenance + tuition for students with 40%+ disability from pre-matric to PhD",30000,5,35,350000,["general","obc","sc","st"],["male","female","other"],["student"],"all",["student","disability"],[],"https://scholarships.gov.in"),
("ignou-fee-waiver","IGNOU Fee Waiver for SC/ST","IGNOU Free","education","🏫","Full fee waiver for SC/ST students in all IGNOU programmes",30000,18,60,100000000,["sc","st"],["male","female","other"],["student"],"all",["student"],[],"https://ignou.ac.in"),
("iti-free-training","Free ITI Training","Free ITI","education","🔧","Free training in 100+ trades at government ITIs — electrician, fitter, mechanic, etc.",50000,14,40,100000000,["general","obc","sc","st"],["male","female","other"],["student","unemployed"],"all",[],[],"https://ncvtmis.gov.in"),
("nios-open-school","NIOS Open Schooling","NIOS Open School","education","📖","Secondary/Senior Secondary education through open schooling for dropouts and working adults",5000,14,100,100000000,["general","obc","sc","st"],["male","female","other"],"all","all",[],[],"https://nios.ac.in"),
("pm-usp","PM USP (Universities Social Programme)","PM USP","education","🏛️","Research internships and industry exposure for undergraduate students in top universities",50000,18,25,100000000,["general","obc","sc","st"],["male","female","other"],["student"],"all",["student"],[],"https://ugc.gov.in"),
("swayam-mooc","SWAYAM Free Online Courses","SWAYAM Free","education","💻","Free online courses from IITs/IIMs/Central Universities — earn certificates for free",0,15,100,100000000,["general","obc","sc","st"],["male","female","other"],"all","all",[],[],"https://swayam.gov.in"),
("diksha-digital","DIKSHA Digital Learning","DIKSHA Platform","education","📱","Free digital textbooks, video lessons, quizzes for school students on mobile app",0,5,18,100000000,["general","obc","sc","st"],["male","female","other"],["student"],"all",["student"],[],"https://diksha.gov.in"),
("ndl-library","National Digital Library","Digital Library","education","📚","Free access to 9 crore+ books, journals, thesis, videos from India's digital library",0,0,100,100000000,["general","obc","sc","st"],["male","female","other"],"all","all",[],[],"https://ndl.iitkgp.ac.in"),
("vtf-vocational","Vocational Training for Women","Women Vocational","education","👩‍🍳","Free vocational training (tailoring, beauty, computers, nursing) for women + stipend",20000,18,45,300000,["general","obc","sc","st"],["female"],["homemaker","unemployed"],"all",[],[],"https://wcd.nic.in"),
("remedial-coaching-obc","Remedial Coaching for OBC","OBC Coaching","education","📝","Free coaching for OBC students preparing for NET/GATE/civil services/bank exams",50000,18,30,600000,["obc"],["male","female","other"],["student"],"all",["student"],[],"https://ugc.gov.in"),
("coaching-minority","Free Coaching for Minorities","Minority Coaching","education","📋","Free coaching for minority students for UPSC/SSC/Bank/Medical/Engineering entrance exams",80000,18,30,600000,["general","obc"],["male","female","other"],["student"],"all",["student","minority"],[],"https://minorityaffairs.gov.in"),
("navodaya-school","Jawahar Navodaya Vidyalaya","Navodaya School","education","🏫","Free residential schooling (Class 6-12) with CBSE education for talented rural students",100000,10,18,100000000,["general","obc","sc","st"],["male","female","other"],["student"],"all",["student","rural"],[],"https://navodaya.gov.in"),
("kv-admission","Kendriya Vidyalaya Admission","KV Admission","education","🏫","Quality CBSE education at nominal fees at 1,200+ Kendriya Vidyalayas across India",10000,5,18,100000000,["general","obc","sc","st"],["male","female","other"],["student"],"all",["student"],[],"https://kvsangathan.nic.in"),
("pm-research-fellowship","PM Research Fellowship","PM Research","education","🔬","₹70,000-80,000/month for top B.Tech students pursuing PhD at IITs/IISc directly",960000,20,30,100000000,["general","obc","sc","st"],["male","female","other"],["student"],"all",["student"],[],"https://pmrf.in"),
("nmmss-arts","National Fellowship for OBC (NFOBC)","OBC PhD Fellowship","education","📜","₹31,000-35,000/month for OBC students pursuing M.Phil/PhD in universities",420000,22,40,800000,["obc"],["male","female","other"],["student"],"all",["student"],[],"https://ugc.gov.in"),
("dst-inspire-faculty","DST INSPIRE Faculty Award","INSPIRE Faculty","education","🔬","₹80,000-1,25,000/month + ₹7 lakh/year research grant for young scientists",1500000,27,40,100000000,["general","obc","sc","st"],["male","female","other"],["student"],"all",[],[],"https://online-inspire.gov.in"),
("skill-india-digital","Skill India Digital Hub","Skill India Digital","education","🖥️","Free online skill courses with certificates — 600+ courses in digital skills",0,15,45,100000000,["general","obc","sc","st"],["male","female","other"],"all","all",[],[],"https://skillindiadigital.gov.in"),
("unnat-bharat","Unnat Bharat Abhiyan (University Social)","Unnat Bharat","education","🏘️","Higher education institutions adopt villages — students do real-world projects",0,17,25,100000000,["general","obc","sc","st"],["male","female","other"],["student"],"all",["student"],[],"https://unnatbharatabhiyan.gov.in"),
]

def build(d):
    return {"id":d[0],"name":d[1],"shortName":d[2],"category":d[3],"icon":d[4],
        "benefit":d[5],"benefitValue":d[6],"simpleExplanation":d[5],
        "eligibility":{"minAge":d[7],"maxAge":d[8],"maxIncome":d[9],
            "categories":d[10],"gender":d[11],
            "occupations":d[12] if isinstance(d[12],list) else "all",
            "states":d[13] if isinstance(d[13],list) else "all",
            "conditions":d[14],"excludeConditions":d[15]},
        "howToApply":["Visit the official portal or National Scholarship Portal","Register and submit your application online","Upload required documents","Scholarship/benefit credited to bank account after verification"],
        "documentsRequired":["Aadhaar Card","Bank Account Details","Marksheets/Academic Records","Income Certificate (if applicable)","Institution Admission Proof"],
        "officialUrl":d[16],
        "whyQualifyTemplate":"Based on your educational profile, you meet the eligibility criteria for this scheme."}

f = os.path.join(os.path.dirname(__file__),"schemes.json")
with open(f,"r",encoding="utf-8") as fp:
    existing = json.load(fp)
ids = {s["id"] for s in existing}
added = 0
for d in edu_schemes:
    if d[0] not in ids:
        existing.append(build(d))
        added += 1
with open(f,"w",encoding="utf-8") as fp:
    json.dump(existing, fp, indent=2, ensure_ascii=False)
print(f"Done! Added {added} education schemes. Total: {len(existing)}")
