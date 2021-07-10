
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 14:25:33 2021

@author: Daisuke Kuwabara&Nesrine Benanteur  https://github.com/kwdaisuke/Takotsubo-Syndrome-Prediction-of-Hospitalization-Outcomes
"""


def page_introduction():
    
  import streamlit as st

  from matplotlib.backends.backend_agg import RendererAgg
  _lock = RendererAgg.lock
  import numpy as np
  import pandas as pd
  import altair as alt
  import matplotlib.pyplot as plt
  import seaborn as sns
  import streamlit as st
  sns.set_theme(style="ticks")
  sns.set_style("whitegrid")
  
  path_dk = "/content/drive/MyDrive/Takotsubo_Prognosis/Tako Final Nes.xlsx"
  path = "/content/Tako Final Nes.xlsx"
  df = pd.read_excel(path_dk)
  PATIENT_WITHNAN = [106, 119, 120, 122,124] 
  df_nonfill = df[df.index.isin(PATIENT_WITHNAN)]
  df=df[~df.index.isin(PATIENT_WITHNAN)]
  df.rename(columns=
                  {"DDN": "birthdate", 
                  "âge": "age",
                   "Date hospit initiale": "hospitalisation_date",
                   "Homme": "sex", 
                   "poids": "weight", 
                   "taille": "height",
                   "IMC ( kg/ cm2)": "BMI",
                   "ATCD dépression/axiété": "depression_anxiety_history", 
                   "ATCD psychiatrique": "mental_illness_history", 
                   "patho neurologiques": "neurological_pathologies",
                   "HTA": "hypertension",
                   "Dyslipidémie": "dyslipidemia", 
                   "Tabac": "smoking", 
                   "Diabète": "diabetes",
                   "IRC": "chronic_kidney_disease", 
                   "AVC/AIT": "stroke_TIA", 
                   "ATCD Cancer": "cancer_history", 
                   "Cancer actif": "cancer",
                   "BPCO/asthme": "COPD_asthma", 
                   "Facteurs de stress": "stress_trigger",
                   "Stress émotionnel": "emotional_stress", 
                   "stress physique": "physical_stress", 
                   "type stress physique":"physical_stress_type",
                   "ICM Code":"ICM_Code",
                   "BB": "beta_blockers", 
                   "ARA II": "ARA_II",
                   "Aspirine": "aspirin",                   
                   "anti P2Y12": "anti_P2Y12",
                   "Anticoagulation orale": "oral_anticoagulation", 
                   "statines": "statin",
                   "antidépresseur / anxiolytiques": "antidepressant", 
                   "Forme apicale": "apical_type", 
                   "médio-ventriculaire": "mid_ventricular",
                   "autre": "other", 
                  "FEVG admission": "entry_LVEF",
                   "FEVG suivi": "out_LVEF", 
                   "atteinte VD": "RV_harm",
                   "ST +": "ST_positive", 
                   "QT long": "Long_QT", 
                   "ondes T -": "Tneg_waves",
                   "tropo entrée": "entry_troponin",                   
                   "pic tropo": "troponin_peak",
                   "NT pro-BNP": "NT_proBNP", 
                   "Coronarographie": "coronarography",
                   "Lésions coronariennes sign": "coronary_disease", 
                   "Coronaires lisses": "healthy_coronary", 
                   " Insuffisance cardiaque": "heart_failure",
                   "Aythmies atriales": "atrium_arrhythmia",
                    "arythmies ventriculaires": "ventricle_arrhythmia",
                   "thrombus VG": "thrombus_LV",
                    "choc cardio": "cardiogenic_shock",
                   "décès hospit": "hospital_death", 
                   "BB sortie": "beta_blockers", 
                   "IEC sortie": "IEC",
                   "ARA II sortie": "ARA_II",
                    "aspirine": "aspirin",
                   "Anti P2Y12": "anti_P2Y12",
                    "Anticoag": "oral_anticoagulation",
                   "statines.1": "statin", 
                   "antidepresseur": "antidepressant" 
                   ,"COVID +": "Covid_positive", 
                   "ATCD Cardio": "Cardio_history", 
                   "alcoolisme": "alcoolism"
                   }, inplace=True)

  

  #st.set_page_config(layout="wide")

  with st.beta_container():
    st.title("**TAKOTSUBO CARDIOMYOPATHY: PREDICTIVE MODEL**")
    st.write("**Takotsubo cardiomyopathy (TTC) or « broken heart » syndrome** is a condition mostly triggered by \
              physical or emotional stress. It happens when the left ventricule, which is the heart’s largest cavity,\
              responsible for pumping the blood to the whole body through the aorta, swells and changes shape, \
              impairing the heart function by reducing the blood flow coming out of the heart.  \
              The symptoms are similar to a classic myocardium infarction, but intrinsically different,\
              because in the latter, it’s most of the time because of a stenosis of the coronary arteries \
              (the one feeding the myocardium) provocking ischemia and necrosis of the heart muscle, \
              and impairing its pump function. In TTC, there’s a temporary deformation of the myocardium, \
              leading to the same consequences than an acutal heart infarction.")
    st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTtrDcEEvdSPDiKyg4FiTsxIgyMb-klnNGP2Q&usqp=CAU")

  with st.beta_container():
    st.subheader("Take a look at our data")
    st.write(df.head())

  with st.beta_container():
    st.subheader("1. Demographics")
  ################################
  st.write("")
  row1, row2, row3, row4= st.beta_columns(4)

  with row1, _lock:
    def age_box():
      fig,ax = plt.subplots()
      sns.boxplot(x="age", hue="sex", data=df, width=.6)
      plt.title("Patient's age", fontsize=14, fontname="Times New Roman Bold", fontweight="bold")
      return fig

    plot=age_box()
    st.pyplot(plot, clear_figure=True)

  with row2, _lock:
    def patient_Age():
      fig2,ax = plt.subplots()
      patient_description = df.loc[:, "birthdate": "BMI"] # Make a dataframe with the patient description
      patient_description.BMI = patient_description.BMI.replace("#DIV/0!", np.nan) # replace by 0 Note that inplace=True doesn't work(regex problem)
      sns.histplot(data=patient_description, x = "age", hue="sex",  multiple="stack")  
      plt.title("Patient's age distribution", fontsize=12, fontweight="bold")
      return fig2
    plot=patient_Age()
    st.pyplot(plot, clear_figure=True)
    
  with row3, _lock:
    def BMI_hist():
      fig2,ax = plt.subplots()
      patient_description = df.loc[:, "birthdate": "BMI"] # Make a dataframe with the patient description
      patient_description.BMI = patient_description.BMI.replace("#DIV/0!", np.nan) # replace by 0 Note that inplace=True doesn't work(regex problem)
      sns.histplot(x="BMI",data=patient_description, kde=True)
      plt.title("Patient's BMI", fontsize=14, fontname="Times New Roman Bold", fontweight="bold")
      return fig2
    plot=BMI_hist()
    st.pyplot(plot, clear_figure=True)

  with row4, _lock:
    def age_BMI():
      fig,ax = plt.subplots()
      patient_description = df.loc[:, "birthdate": "BMI"] # Make a dataframe with the patient description
      patient_description.BMI = patient_description.BMI.replace("#DIV/0!", np.nan) # replace by 0 Note that inplace=True doesn't work(regex problem)
      bins = [-np.inf, 16, 18, 25, 30, np.inf] # Set lower and upper bound as infinity
      BMI_range = pd.cut(patient_description.BMI, bins, labels = "1 2 3 4 5".split(" "))
      patient_description["BMI_range"]  = BMI_range 
      sns.scatterplot(data=patient_description, x = "age", y = "BMI", hue="BMI_range", s=50, edgecolor="black", markers="BMI_range")
      L=plt.legend(loc="best")#, labels=['BMI: ~16', 'BMI: 16-18', 'BMI: 18-25', "BMI: 25-30","BMI: 30 ~"])
      L.get_texts()[0].set_text("BMI: ~16") ; L.get_texts()[1].set_text("BMI: 16-18") ; L.get_texts()[2].set_text("BMI: 18-25") ; L.get_texts()[3].set_text("BMI: 25-30") ; L.get_texts()[4].set_text("BMI: 30 ~")
      plt.title("Patient's BMI vs age in each BMI group", fontsize=13, fontweight="bold")
      return fig
    st.pyplot(age_BMI(), clear_figure=True)
  ############################################

  # with st.beta_container():
  # st.write("")
  row1, row2, row3 = st.beta_columns(3)

  with row1, _lock:
    st.subheader("2. Medical History")
    cardio_history_alcoolisme = df.iloc[:, -2:].fillna(0)
    medical_history = pd.concat([df.loc[:, "depression_anxiety_history":"COPD_asthma"], cardio_history_alcoolisme], axis=1)
    dff = medical_history.sum().sort_values().reset_index().rename(columns={"index": "col", 0:"values"})
    dff.sort_values("values", inplace=True, ascending=False)
    def medical_hist_sum():
      fig,ax = plt.subplots()
      sns.barplot(x="col", y="values", data=dff, order=dff["col"])
      plt.xticks(rotation=90)
      return fig
    st.pyplot(medical_hist_sum(), clear_figure=True)

  with row2, _lock:
    st.subheader("3. Treatment")
    treatment_before = df.iloc[: , 25: 33].replace(np.nan, 0) # Exclude ttt entrée = ttt antérieur
    treatment_after = df.iloc[:,  56:65].replace(np.nan, 0)
    treatment_before["anxiolytiques"] =0.0 # Add anxiolytiques for treatment_before
    sum_treatment = pd.concat([treatment_before.sum(axis=0), treatment_after.sum(axis=0)], axis=1)
    sum_treatment.rename(columns = {0:"Total_Sum_Before ", 1:"Total_Sum_After"}, inplace=True)
    def Treatment_count():
      fig,ax = plt.subplots()
      axe = sum_treatment.plot.bar(figsize=(20, 12), rot=30, ax=ax)
      for p in ax.patches:
        axe.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
        plt.title("Comparison of total count of respective treatment before and after the hospitalization", fontsize=14, fontweight="bold")
      return fig
    plot=Treatment_count()
    st.pyplot(plot, clear_figure=True)

    with row3, _lock:
      st.subheader("4. Treatment's Correlation")
      treatment_before = df.iloc[: , 25: 33].replace(np.nan, 0) # Exclude ttt entrée = ttt antérieur
      treatment_after = df.iloc[:,  56:65].replace(np.nan, 0)
      treatment_before["anxiolytiques"] =0.0 # Add anxiolytiques for treatment_before
      sum_treatment = pd.concat([treatment_before.sum(axis=0), treatment_after.sum(axis=0)], axis=1)

      from PIL import Image
      image1 = Image.open('Image/BEFORE.png')
      image2 = Image.open('Image/AFTER.png')
      st.image(image1, caption='Correlation Before Inhospitalization',width=None)
      st.image(image2, caption='Correlation After Inhospitalization',width=None)
      #st.pyplot(treatment_after.corr(method="kendall").style.background_gradient(cmap="coolwarm"), clear_figure=True)

  #with st.beta_container(): 
  ################################
  #st.write("")
  row1, row2, row3, row4= st.beta_columns(4)

  with row1, _lock:
    st.subheader("5. LVEF")
    LVEF = df.loc[:, "entry_LVEF":"out_LVEF"]; LVEF = LVEF.astype("float") ; LVEF.out_LVEF =LVEF.out_LVEF.replace("NaN", np.nan)
    bin = [-np.inf, 40, 50, 55, np.inf]
    LVEF["entry_LVEF_category"] = pd.cut(LVEF.entry_LVEF, bin, labels = "1 2 3 4".split(" ")) ; LVEF.notnull().sum()
    diff = LVEF.dropna().out_LVEF - LVEF.dropna().entry_LVEF ; diff[diff <0]
    
    def LVEF_diff():
      fig,ax = plt.subplots()
      diff.plot.hist() 
      plt.title("Difference of LVEF", fontsize=14, fontname="Times New Roman Bold", fontweight="bold")
      return fig
    plot=LVEF_diff()
    st.pyplot(plot, clear_figure=True)

  with row2, _lock:
    st.subheader("6. Biomarkers")
    biomarkers = pd.concat([df.loc[:, "entry_troponin": "NT_proBNP"], df.iloc[:, 65]], axis=1) 
    biomarkers["NT_proBNP"] = biomarkers["NT_proBNP"].replace("23 289", "23289")  # Fill the blank 
    
    def Biomarker():
      fig,ax = plt.subplots()
      #biomarkers.troponin_peak.clip(biomarkers.troponin_peak.min(), upper_bound).plot.box()
      biomarkers.NT_proBNP.astype("float").plot.box(figsize=(8, 6))
      plt.title("Biomarker", fontsize=14, fontname="Times New Roman Bold", fontweight="bold")
      return fig
    plot=Biomarker()
    st.pyplot(plot, clear_figure=True)

  with row3, _lock:
    st.subheader("7.Coronarography")
    coronarography = df.loc[:, "coronarography": "healthy_coronary"]
    not_examined = coronarography[coronarography.coronarography == 0]
    yes_examined = coronarography[coronarography.coronarography == 1]
    yes_examined_disease = yes_examined[yes_examined.coronary_disease ==1]
    yes_examined_healthy = yes_examined[yes_examined.healthy_coronary ==1]
    not_examined["coronarography_status"] = "not_examined"
    yes_examined_disease["coronarography_status"] = "coronary_disease"
    yes_examined_healthy["coronarography_status"] = "healthy"
    coronarography_with_status = pd.concat([not_examined, yes_examined_disease, yes_examined_healthy], axis=0).sort_index()
    a = pd.DataFrame(coronarography_with_status.coronarography_status.value_counts()).T.not_examined
    b = pd.DataFrame(coronarography_with_status.coronarography_status.value_counts()).T[["healthy", "coronary_disease"]]

    def coronarography():
      fig,ax = plt.subplots()
      axe=pd.concat([pd.DataFrame(a), b], axis=0).plot(kind="bar", stacked=True, ax=ax)
      axe.set_xticklabels(["non_examined", "examined"], rotation=30)   
      plt.title("Coronarography", fontsize=14, fontname="Times New Roman Bold", fontweight="bold")
      return fig
    st.pyplot(coronarography(), clear_figure=True)

  with row4, _lock:
    st.subheader("8. Inhospital Consequences")
    from PIL import Image
    image = Image.open('Image/inhospital_consequences.png')
    st.image(image, caption='Total Count of respective Inhospital Consequences',width=None)
  ############################################