import streamlit as st
import os
import math
import pandas as pd
import matplotlib.pyplot as plt

# ----- Page Configuration & Branding -----
st.set_page_config(layout="wide", page_title="SMART CVD Risk Reduction")

# ----- Logo -----
col1, col2, col3 = st.columns([1, 6, 1])
with col3:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=1000)
    else:
        st.warning("⚠️ Logo not found — please upload 'logo.png' into the app directory.")

# ----- Risk Functions -----
def estimate_smart_risk(age, sex, sbp, tc, hdl, smoke, dm, egfr, crp, vasc):
    sex_v = 1 if sex == "Male" else 0
    smoke_v = 1 if smoke else 0
    dm_v = 1 if dm else 0
    crp_l = math.log(crp + 1)
    lp = (0.064 * age + 0.34 * sex_v + 0.02 * sbp + 0.25 * tc
          - 0.25 * hdl + 0.44 * smoke_v + 0.51 * dm_v
          - 0.2 * (egfr / 10) + 0.25 * crp_l + 0.4 * vasc)
    r10 = 1 - 0.900**math.exp(lp - 5.8)
    return round(r10 * 100, 1)

def convert_5yr(r10):
    p = r10 / 100
    return round((1 - (1 - p)**0.5) * 100, 1)

# ----- Sidebar: Risk Profile -----
st.sidebar.markdown("### 🔹 Risk Profile")
age = st.sidebar.slider("Age (years)", 30, 90, 60)
sex = st.sidebar.radio("Sex", ["Male", "Female"])
weight = st.sidebar.number_input("Weight (kg)", 40.0, 200.0, 75.0)
height = st.sidebar.number_input("Height (cm)", 140.0, 210.0, 170.0)
bmi = weight / ((height / 100)**2)
st.sidebar.markdown(f"**BMI:** {bmi:.1f} kg/m²")
smoker = st.sidebar.checkbox("Current smoker")
diabetes = st.sidebar.checkbox("Diabetes")
egfr = st.sidebar.slider("eGFR (mL/min/1.73 m²)", 15, 120, 90)
st.sidebar.markdown("**Vascular Disease (tick all that apply)**")
vasc1 = st.sidebar.checkbox("Coronary artery disease")
vasc2 = st.sidebar.checkbox("Cerebrovascular disease")
vasc3 = st.sidebar.checkbox("Peripheral artery disease")
vasc_count = sum([vasc1, vasc2, vasc3])

# ----- Main Page: Step 1 -----
st.title("SMART CVD Risk Reduction Calculator")
st.markdown("### Step 1: Lab Results")
total_chol = st.number_input("Total Cholesterol (mmol/L)", 2.0, 10.0, 5.2, 0.1)
hdl = st.number_input("HDL‑C (mmol/L)", 0.5, 3.0, 1.3, 0.1)
baseline_ldl = st.number_input("Baseline LDL‑C (mmol/L)", 0.5, 6.0, 3.0, 0.1)
crp = st.number_input("hs‑CRP (mg/L) — Baseline (not during acute MI)", 0.1, 20.0, 2.5, 0.1)
hba1c = st.number_input("Latest HbA₁c (%)", 4.5, 15.0, 7.0, 0.1)
tg = st.number_input("Fasting Triglycerides (mmol/L)", 0.5, 5.0, 1.5, 0.1)
st.markdown("---")

# ----- Main Page: Step 2 -----
st.markdown("### Step 2: Therapies")

st.subheader("Pre-admission Lipid-lowering Therapy")
statin = st.selectbox("Statin", ["None", "Atorvastatin 80 mg", "Rosuvastatin 20 mg"])
ez = st.checkbox("Ezetimibe 10 mg")
bemp = st.checkbox("Bempedoic acid")
# Anticipated LDL after current therapy
adj_ldl = baseline_ldl
if statin != "None":
    adj_ldl *= (1 - {"Atorvastatin 80 mg":0.50, "Rosuvastatin 20 mg":0.55}[statin])
if ez: adj_ldl *= 0.80
adj_ldl = max(adj_ldl, 1.0)
st.write(f"**Anticipated LDL‑C:** {adj_ldl:.2f} mmol/L")

st.subheader("Add-on Lipid-lowering Therapy")
if adj_ldl > 1.8:
    pcsk9 = st.checkbox("PCSK9 inhibitor")
    incl = st.checkbox("Inclisiran (siRNA)")
else:
    st.info("PCSK9i/Inclisiran only if LDL‑C >1.8 mmol/L")

st.markdown("**Lifestyle Changes**")
smoke_iv = st.checkbox("Smoking cessation", disabled=not smoker)
semaglutide = st.checkbox("GLP‑1 RA (Semaglutide)", disabled=(bmi < 30))
med_iv = st.checkbox("Mediterranean diet")
act_iv = st.checkbox("Physical activity")
alc_iv = st.checkbox("Alcohol moderation (>14 units/week)")
str_iv = st.checkbox("Stress reduction")

st.markdown("**Other Therapies**")
asa_iv = st.checkbox("Antiplatelet (ASA or Clopidogrel)")
bp_iv = st.checkbox("BP control (target <130 mmHg)")
sglt2iv = st.checkbox("SGLT2 inhibitor")
if tg > 1.7:
    ico_iv = st.checkbox("Icosapent ethyl")
else:
    st.info("Icosapent ethyl only if TG >1.7 mmol/L")
st.markdown("---")

# ----- Main Page: Step 3 -----
st.markdown("### Step 3: Results & Summary")
r10 = estimate_smart_risk(age, sex, sbp if 'sbp' in locals() else 130, total_chol, hdl, smoker, diabetes, egfr, crp, vasc_count)
r5 = convert_5yr(r10)
base = r5
enabled=base
st.write(f"Baseline 5yr risk: {base}%")
st.markdown("(Full ARR/RRR calculation to be inserted here)")
st.markdown("---")
st.markdown("Created by Samuel Panday — 21/04/2025")
st.markdown("Created by PRIME team (Prevention Recurrent Ischaemic Myocardial Events)")
st.markdown("King's College Hospital, London")
st.markdown("This tool is provided for informational purposes and designed to support discussions with your healthcare provider—it’s not a substitute for professional medical advice.")'''


Path("/mnt/data/cvd_risk_app.py").write_text(final_complete_code)
