import json, os
# State-specific schemes - format: (id, name, shortName, category, icon, benefit, benefitValue, minAge, maxAge, maxIncome, categories, gender, occupations, states, conditions, excludeConditions, officialUrl)
state_schemes = [
# --- UTTARAKHAND ---
("uk-gaura-devi","Gaura Devi Kanya Dhan (Uttarakhand)","UK Kanya Dhan","education","👧","₹50,000 fixed deposit for BPL girls passing Class 12 in Uttarakhand",50000,16,20,300000,["general","obc","sc","st"],["female"],["student"],["uttarakhand"],["student"],[],"https://escholarship.uk.gov.in"),
("uk-vatsalya","Mukhyamantri Vatsalya Yojana (UK)","UK Vatsalya","welfare","🤗","₹3,000/month + free education for orphan children who lost parents to COVID in Uttarakhand",36000,0,21,100000000,["general","obc","sc","st"],["male","female","other"],["student"],["uttarakhand"],[],[],"https://uk.gov.in"),

# --- MAHARASHTRA ---
("mh-majhi-kanya","Majhi Kanya Bhagyashree (Maharashtra)","MH Kanya Bhagyashree","welfare","👧","₹50,000 for girl child birth + insurance in Maharashtra for BPL families",50000,0,18,750000,["general","obc","sc","st"],["female"],"all",["maharashtra"],[],[],"https://maharashtra.gov.in"),
("mh-lek-ladki","Lek Ladki Yojana (Maharashtra)","MH Lek Ladki","welfare","🎀","₹1,01,000 total in instalments from birth to 18 years for girls in Maharashtra",101000,0,18,100000,["general","obc","sc","st"],["female"],"all",["maharashtra"],[],[],"https://maharashtra.gov.in"),
("mh-shetkari","Namo Shetkari Maha Sanman (MH)","MH Farmer Support","agriculture","🌾","₹6,000/year additional support for Maharashtra farmers (on top of PM-KISAN)",6000,18,100,10000000,["general","obc","sc","st"],["male","female","other"],["farmer"],["maharashtra"],["farmer"],[],"https://maharashtra.gov.in"),

# --- KARNATAKA ---
("ka-gruha-lakshmi","Gruha Lakshmi (Karnataka)","KA Gruha Lakshmi","welfare","🏠","₹2,000/month for women heads of households in Karnataka",24000,18,65,500000,["general","obc","sc","st"],["female"],["homemaker","self_employed","farmer","laborer"],["karnataka"],[],[],"https://sevasindhuservices.karnataka.gov.in"),
("ka-anna-bhagya","Anna Bhagya (Karnataka)","KA Anna Bhagya","welfare","🍚","10 kg free rice per person per month for BPL families in Karnataka",12000,0,100,200000,["general","obc","sc","st"],["male","female","other"],"all",["karnataka"],[],[],"https://ahara.kar.nic.in"),
("ka-yuva-nidhi","Yuva Nidhi (Karnataka)","KA Yuva Nidhi","employment","💼","₹3,000-₹1,500/month for unemployed graduates in Karnataka while job searching",36000,18,25,300000,["general","obc","sc","st"],["male","female","other"],["unemployed","student"],["karnataka"],[],[],"https://sevasindhuservices.karnataka.gov.in"),
("ka-bhagya-jyothi","Bhagya Jyothi (Karnataka)","KA Free Power","welfare","💡","Free electricity up to 200 units/month for SC/ST families in Karnataka",12000,18,100,500000,["sc","st"],["male","female","other"],"all",["karnataka"],[],[],"https://bescom.karnataka.gov.in"),

# --- TAMIL NADU ---
("tn-kalaignar","Kalaignar Magalir Urimai Thogai (TN)","TN Women ₹1000","welfare","👩","₹1,000/month for women heads of families in Tamil Nadu",12000,21,60,250000,["general","obc","sc","st"],["female"],"all",["tamil nadu"],[],[],"https://tn.gov.in"),
("tn-free-laptop","TN Free Laptop Scheme","TN Free Laptop","education","💻","Free laptop for all 11th and 12th government school students in Tamil Nadu",25000,15,18,100000000,["general","obc","sc","st"],["male","female","other"],["student"],["tamil nadu"],["student"],[],"https://tn.gov.in"),
("tn-marriage-assist","Moovalur Ramamirtham Marriage Aid (TN)","TN Marriage Aid","welfare","💍","₹25,000 + 8g gold for marriage of women from poor families in Tamil Nadu",25000,18,35,300000,["general","obc","sc","st"],["female"],"all",["tamil nadu"],[],[],"https://tn.gov.in"),

# --- WEST BENGAL ---
("wb-lakshmir-bhandar","Lakshmir Bhandar (West Bengal)","WB Lakshmir Bhandar","welfare","💰","₹500-1,000/month for women aged 25-60 in West Bengal",12000,25,60,300000,["general","obc","sc","st"],["female"],"all",["west bengal"],[],[],"https://wb.gov.in"),
("wb-swasthya-sathi","Swasthya Sathi (West Bengal)","WB Health Card","health","🏥","₹5 lakh cashless health insurance for all WB families — issued in women's name",500000,0,100,100000000,["general","obc","sc","st"],["male","female","other"],"all",["west bengal"],[],[],"https://swasthyasathi.gov.in"),
("wb-rupashree","Rupashree (West Bengal)","WB Rupashree","welfare","💐","₹25,000 one-time grant for marriage of girls from economically weaker families in WB",25000,18,40,150000,["general","obc","sc","st"],["female"],"all",["west bengal"],[],[],"https://wb.gov.in"),

# --- PUNJAB ---
("pb-aashirwad","Aashirwad Scheme (Punjab)","PB Aashirwad","welfare","🎊","₹51,000 shagun for marriage of SC/BC/EWS girls in Punjab",51000,18,40,300000,["sc","obc"],["female"],"all",["punjab"],[],[],"https://punjab.gov.in"),
("pb-bhagat-puran","Bhagat Puran Singh Sehat Bima (PB)","PB Health Insurance","health","💊","₹5 lakh health insurance for all Punjab families — cashless treatment at empanelled hospitals",500000,0,100,100000000,["general","obc","sc","st"],["male","female","other"],"all",["punjab"],[],[],"https://sha.punjab.gov.in"),

# --- HARYANA ---
("hr-ladli","Ladli Scheme (Haryana)","HR Ladli","welfare","👶","₹5,000/year for second daughter from birth — ₹1 lakh total at age 18",100000,0,18,100000000,["general","obc","sc","st"],["female"],"all",["haryana"],[],[],"https://haryana.gov.in"),
("hr-chirayu","Chirayu Yojana (Haryana)","HR Chirayu","health","🏥","₹5 lakh health insurance for families earning less than ₹1.8L/year in Haryana",500000,0,100,180000,["general","obc","sc","st"],["male","female","other"],"all",["haryana"],[],[],"https://haryana.gov.in"),

# --- RAJASTHAN ---
("rj-palanhar","Palanhar Yojana (Rajasthan)","RJ Palanhar","welfare","🤱","₹1,500/month for orphan/destitute children's guardians in Rajasthan",18000,0,18,120000,["general","obc","sc","st"],["male","female","other"],"all",["rajasthan"],[],[],"https://sje.rajasthan.gov.in"),
("rj-indira-rasoi","Indira Rasoi (Rajasthan)","RJ Indira Rasoi","welfare","🍛","Full meal at just ₹8 at government-run kitchens across Rajasthan",3000,0,100,100000000,["general","obc","sc","st"],["male","female","other"],"all",["rajasthan"],[],[],"https://indirarasoi.rajasthan.gov.in"),

# --- GUJARAT ---
("gj-vahali-dikri","Vahali Dikri Yojana (Gujarat)","GJ Vahali Dikri","education","👧","₹1,10,000 total for girls at Class 1, 9, 12 and marriage in Gujarat",110000,0,25,200000,["general","obc","sc","st"],["female"],"all",["gujarat"],[],[],"https://gujaratindia.gov.in"),
("gj-manav-garima","Manav Garima Yojana (Gujarat)","GJ Manav Garima","employment","🛠️","₹4,000-₹25,000 equipment/tools kit for SC families for self-employment in Gujarat",25000,18,60,47000,["sc"],["male","female","other"],["self_employed","unemployed"],["gujarat"],[],[],"https://sje.gujarat.gov.in"),

# --- MADHYA PRADESH ---
("mp-mukhyamantri-kanya","Mukhyamantri Kanya Vivah Yojana (MP)","MP Kanya Vivah","welfare","💍","₹55,000 for marriage of BPL/destitute/widow's daughters in Madhya Pradesh",55000,18,35,200000,["general","obc","sc","st"],["female"],"all",["madhya pradesh"],[],[],"https://mpvivahportal.nic.in"),
("mp-medhavi-vidyarthi","Mukhyamantri Medhavi Vidyarthi (MP)","MP Merit Scholar","education","🏅","Full tuition fees for students scoring 70%+ in MP Board 12th (85% for CBSE)",200000,16,25,600000,["general","obc","sc","st"],["male","female","other"],["student"],["madhya pradesh"],["student"],[],"https://scholarshipportal.mp.nic.in"),

# --- CHHATTISGARH ---
("cg-mahtari-vandan","Mahtari Vandan Yojana (Chhattisgarh)","CG Mahtari Vandan","welfare","🤰","₹1,000/month for married women aged 21-60 in Chhattisgarh",12000,21,60,300000,["general","obc","sc","st"],["female"],"all",["chhattisgarh"],[],[],"https://mahtarivandan.cgstate.gov.in"),
("cg-godhan-nyay","Godhan Nyay Yojana (CG)","CG Godhan Nyay","agriculture","🐄","Government buys cow dung at ₹2/kg from cattle owners for vermicompost in CG",10000,18,100,10000000,["general","obc","sc","st"],["male","female","other"],["farmer"],["chhattisgarh"],["farmer"],[],"https://cgstate.gov.in"),

# --- JHARKHAND ---
("jh-mukhyamantri-kanya","Mukhyamantri Kanya Utthan (Jharkhand)","JH Kanya Utthan","welfare","👧","₹40,000 for unmarried girls completing graduation in Jharkhand",40000,18,25,72000,["general","obc","sc","st"],["female"],["student"],["jharkhand"],["student"],[],"https://jharkhand.gov.in"),
("jh-savitribai-phule","Savitribai Phule Fellowship (JH)","JH Women PhD","education","📚","₹60,000/year fellowship for women pursuing higher education in Jharkhand",60000,20,35,300000,["general","obc","sc","st"],["female"],["student"],["jharkhand"],["student"],[],"https://jharkhand.gov.in"),

# --- ASSAM ---
("as-orunodoi","Orunodoi Scheme (Assam)","AS Orunodoi","welfare","🌅","₹1,250/month for women in low-income families in Assam",15000,18,60,200000,["general","obc","sc","st"],["female"],"all",["assam"],[],[],"https://orunodoi.assam.gov.in"),
("as-arundhati","Arundhati Gold Scheme (Assam)","AS Arundhati Gold","welfare","💍","10g gold (worth ~₹60,000) for brides in registered marriages in Assam",60000,18,40,500000,["general","obc","sc","st"],["female"],"all",["assam"],[],[],"https://assam.gov.in"),

# --- KERALA ---
("kl-snehapoorvam","Snehapoorvam Scheme (Kerala)","KL Snehapoorvam","welfare","🤝","₹300-500/month for orphans and children of widows in Kerala for education",6000,3,18,100000000,["general","obc","sc","st"],["male","female","other"],["student"],["kerala"],["student"],[],"https://sjd.kerala.gov.in"),
("kl-ksheerasagaram","Ksheerasagaram (Kerala Dairy)","KL Dairy Subsidy","agriculture","🐄","Subsidy for dairy farming: cattle purchase, shed construction, equipment in Kerala",100000,18,65,500000,["general","obc","sc","st"],["male","female","other"],["farmer","self_employed"],["kerala"],[],[],"https://dairy.kerala.gov.in"),

# --- ANDHRA PRADESH ---
("ap-amma-odi","Jagananna Vidya Deevena (AP)","AP Fee Reimbursement","education","🎓","Full fee reimbursement for students from families earning <₹2.5L in Andhra Pradesh",150000,16,30,250000,["general","obc","sc","st"],["male","female","other"],["student"],["andhra pradesh"],["student"],[],"https://jnanabhumi.ap.gov.in"),
("ap-vasathi-deevena","Jagananna Vasathi Deevena (AP)","AP Hostel Fee","education","🏨","₹10,000-20,000/year hostel/mess fee for students in AP hostels",20000,16,30,250000,["general","obc","sc","st"],["male","female","other"],["student"],["andhra pradesh"],["student"],[],"https://jnanabhumi.ap.gov.in"),

# --- TELANGANA ---
("ts-kalyana-lakshmi","Kalyana Lakshmi (Telangana)","TS Kalyana Lakshmi","welfare","💐","₹1,00,116 for marriage of SC/ST/BC/EBC/minority girls in Telangana",100116,18,40,200000,["sc","st","obc"],["female"],"all",["telangana"],[],[],"https://telanganaepass.cgg.gov.in"),
("ts-aasara","Aasara Pension (Telangana)","TS Aasara Pension","pension","🧓","₹2,016/month pension for elderly/disabled/widows in Telangana",24192,57,100,300000,["general","obc","sc","st"],["male","female","other"],"all",["telangana"],["senior_citizen","disability","widow"],[],"https://finance.telangana.gov.in"),

# --- ODISHA ---
("od-mamata","Mamata Scheme (Odisha)","OD Mamata","welfare","🤰","₹5,000 for pregnant/lactating women in Odisha for nutrition (2 instalments)",5000,19,45,300000,["general","obc","sc","st"],["female"],"all",["odisha"],[],[],"https://wcdodisha.gov.in"),
("od-madhu-babu","Madhu Babu Pension (Odisha)","OD Pension","pension","🧓","₹500-700/month pension for elderly/disabled/widows in Odisha",8400,60,100,300000,["general","obc","sc","st"],["male","female","other"],"all",["odisha"],["senior_citizen","disability","widow"],[],"https://ssepd.odisha.gov.in"),

# --- DELHI ---
("dl-ladli","Ladli Yojana (Delhi)","DL Ladli","welfare","👧","₹5,000-₹11,000 at different stages from birth to Class 12 for girls in Delhi",36000,0,18,100000000,["general","obc","sc","st"],["female"],"all",["delhi"],[],[],"https://wcddel.in"),
("dl-ration","One Nation One Ration Card (Delhi)","DL Free Ration","welfare","🍚","Free ration (5kg grain + 1kg dal) per person per month for NFSA cardholders in Delhi",6000,0,100,200000,["general","obc","sc","st"],["male","female","other"],"all",["delhi"],[],[],"https://nfs.delhi.gov.in"),

# --- HIMACHAL PRADESH ---
("hp-sahara","Sahara Yojana (Himachal)","HP Sahara","health","💊","₹3,000/month financial aid for patients with serious diseases (cancer, kidney, etc.) in HP",36000,0,100,400000,["general","obc","sc","st"],["male","female","other"],"all",["himachal pradesh"],[],[],"https://himachal.nic.in"),
("hp-medha-protsahan","Medha Protsahan (HP)","HP Merit Coaching","education","📖","₹1 lakh for coaching for competitive exams (UPSC/JEE/NEET) for HP students",100000,18,30,250000,["general","obc","sc","st"],["male","female","other"],["student"],["himachal pradesh"],["student"],[],"https://himachal.nic.in"),

# --- GOA ---
("ga-laadli-laxmi","Laadli Laxmi Yojana (Goa)","GA Laadli Laxmi","welfare","🎀","₹1 lakh insurance for girl child in Goa, matured at 18",100000,0,18,300000,["general","obc","sc","st"],["female"],"all",["goa"],[],[],"https://goa.gov.in"),
("ga-griha-aadhar","Griha Aadhar (Goa)","GA Griha Aadhar","welfare","🏠","₹1,500/month for women homemakers in Goa households",18000,18,60,300000,["general","obc","sc","st"],["female"],["homemaker"],["goa"],[],[],"https://goa.gov.in"),

# --- MANIPUR ---
("mn-lairik","CM Lairik Yojana (Manipur)","MN Free Textbook","education","📚","Free textbooks and uniforms for all government school students in Manipur",3000,5,18,100000000,["general","obc","sc","st"],["male","female","other"],["student"],["manipur"],["student"],[],"https://manipur.gov.in"),

# --- MEGHALAYA ---
("ml-chief-minister","CM Scholarship (Meghalaya)","ML CM Scholarship","education","🎓","₹10,000-20,000/year scholarship for meritorious students in Meghalaya",20000,15,25,300000,["general","obc","sc","st"],["male","female","other"],["student"],["meghalaya"],["student"],[],"https://meghalaya.gov.in"),

# --- MIZORAM ---
("mz-socio-economic","Socio-Economic Development Policy (Mizoram)","MZ SEDP","finance","🏗️","Subsidized loans for small enterprises and self-employment in Mizoram",200000,18,55,300000,["general","obc","sc","st"],["male","female","other"],["self_employed","unemployed","entrepreneur"],["mizoram"],[],[],"https://mizoram.gov.in"),

# --- NAGALAND ---
("nl-chief-minister","CM Health Insurance (Nagaland)","NL Health","health","🏥","Health insurance coverage for BPL families in Nagaland",300000,0,100,200000,["general","obc","sc","st"],["male","female","other"],"all",["nagaland"],[],[],"https://nagaland.gov.in"),

# --- TRIPURA ---
("tr-lakhi","Lakhi Bhandar (Tripura)","TR Lakhi Bhandar","welfare","💰","₹1,000/month for women aged 21-60 in Tripura",12000,21,60,300000,["general","obc","sc","st"],["female"],"all",["tripura"],[],[],"https://tripura.gov.in"),

# --- ARUNACHAL PRADESH ---
("ar-deen-dayal","Deen Dayal Upadhyaya Buniyadi Yojana (AR)","AR Basic Services","welfare","🏘️","Basic infrastructure support: roads, water, electricity for remote villages in Arunachal",0,0,100,100000000,["general","obc","sc","st"],["male","female","other"],"all",["arunachal pradesh"],["rural"],[],"https://arunachalpradesh.gov.in"),

# --- SIKKIM ---
("sk-one-family","One Family One Job (Sikkim)","SK Govt Job","employment","💼","Government job guaranteed for at least one member of every Sikkimese family",250000,18,40,300000,["general","obc","sc","st"],["male","female","other"],["unemployed"],["sikkim"],[],[],"https://sikkim.gov.in"),

# --- JAMMU & KASHMIR (more) ---
("jk-mumkin","Mumkin Scheme (J&K)","JK Mumkin","employment","🚗","Subsidized commercial vehicle for youth self-employment in J&K",500000,18,35,400000,["general","obc","sc","st"],["male","female","other"],["unemployed"],["jammu and kashmir"],[],[],"https://jk.gov.in"),

# --- UTTARAKHAND (more) ---
("uk-mukhyamantri","Mukhyamantri Swarojgar Yojana (UK)","UK Self-Employment","finance","🏭","25% subsidy (up to ₹6.25 lakh) on loans for self-employment projects in Uttarakhand",625000,18,45,100000000,["general","obc","sc","st"],["male","female","other"],["self_employed","unemployed","entrepreneur"],["uttarakhand"],[],[],"https://msy.uk.gov.in"),
]

def build(d):
    return {"id":d[0],"name":d[1],"shortName":d[2],"category":d[3],"icon":d[4],
        "benefit":d[5],"benefitValue":d[6],"simpleExplanation":d[5],
        "eligibility":{"minAge":d[7],"maxAge":d[8],"maxIncome":d[9],
            "categories":d[10],"gender":d[11],
            "occupations":d[12] if isinstance(d[12],list) else "all",
            "states":d[13] if isinstance(d[13],list) else "all",
            "conditions":d[14],"excludeConditions":d[15]},
        "howToApply":["Visit the official state portal or nearest CSC/e-Seva centre","Submit required documents with application form","Application will be verified by authorities","Benefits credited to your bank account"],
        "documentsRequired":["Aadhaar Card","Bank Account Details","State Domicile/Residence Certificate","Income Certificate (if applicable)"],
        "officialUrl":d[16],
        "whyQualifyTemplate":"Based on your state and profile, you meet the eligibility criteria for this scheme."}

f = os.path.join(os.path.dirname(__file__),"schemes.json")
with open(f,"r",encoding="utf-8") as fp:
    existing = json.load(fp)
ids = {s["id"] for s in existing}
added = 0
for d in state_schemes:
    if d[0] not in ids:
        existing.append(build(d))
        added += 1
with open(f,"w",encoding="utf-8") as fp:
    json.dump(existing, fp, indent=2, ensure_ascii=False)
print(f"Done! Added {added} state schemes. Total: {len(existing)}")
