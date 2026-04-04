import json, os
schemes = [
# ===== HEALTH SCHEMES =====
("nhm-free-drugs","Free Drugs Service (NHM)","Free Medicines","health","💊","Free essential medicines at all government hospitals and health centres across India",10000,0,100,100000000,["general","obc","sc","st"],["male","female","other"],"all","all",[],[],"https://nhm.gov.in"),
("nhm-free-diagnostics","Free Diagnostics Service (NHM)","Free Lab Tests","health","🔬","Free pathology and radiology tests at government hospitals — blood tests, X-ray, ultrasound",15000,0,100,100000000,["general","obc","sc","st"],["male","female","other"],"all","all",[],[],"https://nhm.gov.in"),
("janani-shishu","Janani Shishu Suraksha Karyakram","Mother Baby Care","health","👩‍🍼","Free delivery + C-section + newborn treatment at government hospitals — zero expense",50000,15,45,100000000,["general","obc","sc","st"],["female"],"all","all",[],[],"https://nhm.gov.in"),
("surakshit-matritva","Surakshit Matritva Abhiyan","Safe Motherhood","health","🤰","Free monthly health checkup on 9th of every month for pregnant women by specialists",5000,15,45,100000000,["general","obc","sc","st"],["female"],"all","all",[],[],"https://pmsma.nhp.gov.in"),
("deaddiction-centres","National Drug De-addiction Programme","De-addiction Help","health","🆘","Free treatment and rehab for drug/alcohol addiction at government de-addiction centres",30000,12,100,100000000,["general","obc","sc","st"],["male","female","other"],"all","all",[],[],"https://nhm.gov.in"),
("nvbdcp-malaria","National Vector Borne Disease Control","Malaria-Dengue Free","health","🦟","Free diagnosis, treatment, and mosquito nets for malaria/dengue/chikungunya",5000,0,100,100000000,["general","obc","sc","st"],["male","female","other"],"all","all",[],[],"https://nvbdcp.gov.in"),
("ntcp-tobacco","National Tobacco Control Programme","Quit Tobacco","health","🚭","Free tobacco cessation clinics and counseling at district hospitals",5000,12,100,100000000,["general","obc","sc","st"],["male","female","other"],"all","all",[],[],"https://ntcp.nhp.gov.in"),
("npcdcs-ncd","NPCDCS (NCD Control)","NCD Screening","health","❤️","Free screening and treatment for diabetes, hypertension, cancer at all health centres",20000,30,100,100000000,["general","obc","sc","st"],["male","female","other"],"all","all",[],[],"https://nhm.gov.in"),
("pradhan-mantri-cancer","National Programme for Cancer","Free Cancer Screen","health","🎗️","Free cancer screening for women (breast, cervical, oral) at health and wellness centres",50000,30,65,100000000,["general","obc","sc","st"],["female"],"all","all",[],[],"https://nhm.gov.in"),
("hiv-art","National AIDS Control (Free ART)","Free HIV Treatment","health","💉","Free lifelong Anti-Retroviral Treatment (ART) for all HIV+ patients at government centres",100000,0,100,100000000,["general","obc","sc","st"],["male","female","other"],"all","all",[],[],"https://naco.gov.in"),
("npcb-eye","National Blindness Control (Free Eye Camp)","Free Eye Surgery","health","👁️","Free cataract surgery, spectacles, and eye treatment through govt eye camps",15000,0,100,100000000,["general","obc","sc","st"],["male","female","other"],"all","all",[],[],"https://nhm.gov.in"),
("nmhp-district","District Mental Health Programme","Free Mental Health","health","🧠","Free psychiatric OPD, medicines, and counseling at all district hospitals",15000,0,100,100000000,["general","obc","sc","st"],["male","female","other"],"all","all",[],[],"https://nhm.gov.in"),
("pm-abhiyan-sickle","National Sickle Cell Anaemia Mission","Sickle Cell Mission","health","🩸","Free screening, treatment, and genetic counseling for sickle cell disease",20000,0,100,100000000,["general","obc","sc","st"],["male","female","other"],"all","all",[],[],"https://nhm.gov.in"),
("school-health-prog","School Health Programme (Ayushman)","School Health","health","🏫","Annual health checkups, spectacles, hearing aids, dental care for all govt school students",10000,5,18,100000000,["general","obc","sc","st"],["male","female","other"],["student"],"all",["student"],[],"https://ab-hwc.nhp.gov.in"),
("health-wellness-centre","Ayushman Bharat Health Wellness Centre","Free Primary Care","health","🏥","Free primary healthcare, teleconsultation, yoga, and 12 types of free services at 1.6L+ centres",10000,0,100,100000000,["general","obc","sc","st"],["male","female","other"],"all","all",[],[],"https://ab-hwc.nhp.gov.in"),
# ===== FINANCE SCHEMES =====
("nps-lite","NPS Lite (Swavalamban)","NPS Lite Pension","finance","📊","Government co-contributes ₹1,000/year to your pension if you save ₹1,000-12,000/year",12000,18,60,200000,["general","obc","sc","st"],["male","female","other"],"all","all",[],["government_employee"],"https://npscra.nsdl.co.in"),
("ppf","Public Provident Fund (PPF)","PPF Savings","finance","🏦","7.1% guaranteed tax-free returns on savings up to ₹1.5 lakh/year — best safe investment",150000,18,100,100000000,["general","obc","sc","st"],["male","female","other"],"all","all",[],[],"https://www.indiapost.gov.in"),
("nsc","National Savings Certificate (NSC)","NSC Savings","finance","📜","7.7% guaranteed interest on postal savings + tax deduction under 80C",0,18,100,100000000,["general","obc","sc","st"],["male","female","other"],"all","all",[],[],"https://www.indiapost.gov.in"),
("mahila-samman-fd","Mahila Samman Fixed Deposit","Women FD","finance","👩","7.5% interest on 2-year FD up to ₹2 lakh — exclusive for women and girls",15000,0,100,100000000,["general","obc","sc","st"],["female"],"all","all",[],[],"https://www.indiapost.gov.in"),
("pm-mudra-shishu","MUDRA Shishu Loan (up to ₹50K)","Mudra Shishu","finance","💳","Loan up to ₹50,000 without collateral for micro businesses — vegetable sellers, tailors, etc.",50000,18,65,500000,["general","obc","sc","st"],["male","female","other"],["self_employed","business"],"all",[],[],"https://mudra.org.in"),
("pm-mudra-kishore","MUDRA Kishore Loan (₹50K-5L)","Mudra Kishore","finance","💰","₹50,000-₹5 lakh loan for growing small businesses without collateral",500000,18,65,1000000,["general","obc","sc","st"],["male","female","other"],["self_employed","business","entrepreneur"],"all",[],[],"https://mudra.org.in"),
("pm-mudra-tarun","MUDRA Tarun Loan (₹5L-10L)","Mudra Tarun","finance","🏭","₹5-₹10 lakh loan for expanding established businesses",1000000,18,65,5000000,["general","obc","sc","st"],["male","female","other"],["self_employed","business","entrepreneur"],"all",[],[],"https://mudra.org.in"),
("gold-monetisation","Gold Monetisation Scheme","Gold Deposit","finance","🥇","Earn interest (up to 2.5%) on your idle gold by depositing it in a bank",0,18,100,100000000,["general","obc","sc","st"],["male","female","other"],"all","all",[],[],"https://rbi.org.in"),
("sovereign-gold","Sovereign Gold Bond","Gold Bond","finance","🪙","Buy govt gold bonds at market rate + earn 2.5%/year interest — safer than physical gold",0,18,100,100000000,["general","obc","sc","st"],["male","female","other"],"all","all",[],[],"https://rbi.org.in"),
("ssy-extension","Sukanya Samriddhi (Extended)","Sukanya SS","finance","👧","8.2% interest savings account for girl child — ₹250 to ₹1.5L/year deposit till age 21",150000,0,10,100000000,["general","obc","sc","st"],["female"],"all","all",[],[],"https://www.indiapost.gov.in"),
("cgfmu","Credit Guarantee for Micro Units","Micro Loan Guarantee","finance","🔐","Government guarantees micro loans up to ₹10 lakh — no collateral needed from borrower",1000000,18,65,500000,["general","obc","sc","st"],["male","female","other"],["self_employed","business"],"all",[],[],"https://mudra.org.in"),
("sie-equity","Startup India Seed Fund","Startup Seed Fund","finance","🚀","Up to ₹50 lakh seed funding for early-stage startups through approved incubators",5000000,18,45,100000000,["general","obc","sc","st"],["male","female","other"],["entrepreneur","self_employed"],"all",[],[],"https://seedfund.startupindia.gov.in"),
("msme-samadhan","MSME Samadhan (Delayed Payment)","MSME Payment Help","finance","⚖️","Online portal to file complaints against buyers who delay payment to MSMEs",0,18,100,100000000,["general","obc","sc","st"],["male","female","other"],["self_employed","business"],"all",[],[],"https://samadhaan.msme.gov.in"),
("gemlot","Government e-Marketplace (GeM)","GeM Seller","finance","🛒","Register as a seller on GeM to supply products/services to government — ₹4.5L+ crore market",500000,18,100,100000000,["general","obc","sc","st"],["male","female","other"],["self_employed","business","entrepreneur","artisan"],"all",[],[],"https://gem.gov.in"),
("zed-certification","ZED Certification for MSMEs","ZED Quality","finance","✅","80% subsidy on quality certification for MSMEs — improves credibility and market access",20000,18,100,100000000,["general","obc","sc","st"],["male","female","other"],["self_employed","business","entrepreneur"],"all",[],[],"https://zed.msme.gov.in"),
]

def build(d):
    return {"id":d[0],"name":d[1],"shortName":d[2],"category":d[3],"icon":d[4],
        "benefit":d[5],"benefitValue":d[6],"simpleExplanation":d[5],
        "eligibility":{"minAge":d[7],"maxAge":d[8],"maxIncome":d[9],
            "categories":d[10],"gender":d[11],
            "occupations":d[12] if isinstance(d[12],list) else "all",
            "states":d[13] if isinstance(d[13],list) else "all",
            "conditions":d[14],"excludeConditions":d[15]},
        "howToApply":["Visit the official portal or nearest government office","Submit required documents","Application verified by authorities","Benefits provided directly"],
        "documentsRequired":["Aadhaar Card","Bank Account Details","Income Certificate (if applicable)"],
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
print(f"Done! Added {added} health+finance schemes. Total: {len(existing)}")
