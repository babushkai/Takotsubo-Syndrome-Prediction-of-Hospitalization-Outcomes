
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 11:54:36 2021

@author: Daisuke Kuwabara & Nesrine Benanteur https://github.com/kwdaisuke/Takotsubo-Syndrome-Prediction-of-Hospitalization-Outcomes
"""
# Package imports
import streamlit as st
from scipy import stats
from scipy.stats.mstats import mquantiles
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import base64
from typing import List

def flatten(list2d):
  ls=[]
  for i in list2d:
    if isinstance(i, list):
      for j in i:
        ls.append(j)
        continue
    else:   
      ls.append(i)
  return ls

def page_explore():
    """ 
    The first page in this app made with Streamlit is for an interactive 
    exploration of the continuous distributions that are available in SciPy.
    """
    import numpy as np
    df_imputed=pd.read_csv("data/imputed_data.csv")
    Cardio_History_Alcoholism = df_imputed[["alcoolism", "Cardio_history"]].fillna(0) # NaN is 0 for the binary value?
    medical_history = pd.concat([df_imputed.loc[:, "depression_anxiety_history":"COPD_asthma" ], Cardio_History_Alcoholism], axis=1).columns.to_numpy()  
    stress_factor = df_imputed.loc[:, "stress_trigger": "ICM_Code"].columns.to_numpy()
    # without_stress = stress_factor[stress_factor["stress_trigger"] == 0]
    # with_stress = stress_factor[stress_factor["stress_trigger"] == 1]
    #with_stress["physical_stress_type"] = with_stress["physical_stress_type"].replace(np.nan, "emotional")
    treatment_before = df_imputed.iloc[: , 27: 34].replace(np.nan, 0) # Exclude ttt entrée = ttt antérieur
    treatment_before["anxiolytiques"] =0.0; treatment_before = treatment_before.columns.to_numpy()
    anatomy = df_imputed.loc[:, "apical_type":"other"].columns.to_numpy()
    LVEF = df_imputed.loc[:, "entry_LVEF":"out_LVEF"].columns.to_numpy()
    rythmic_abnormality =df_imputed.loc[:, "ST_positive": "Tneg_waves"].columns.to_numpy()
    biomarkers = pd.concat([df_imputed.loc[:, "entry_troponin": "CRP"], df_imputed.iloc[:, 65]], axis=1) 
    biomarkers["NT_proBNP"] = biomarkers["NT_proBNP"].replace("23 289", "23289")
    biomarkers =biomarkers.columns.to_numpy()  # Fill the blank 
    coronarography = df_imputed.loc[:, "coronarography": "healthy_coronary"].columns.to_numpy()
    inhospital_consequences = pd.concat([df_imputed.loc[:, "heart_failure": "hospital_death"], df_imputed.loc[:, "RV_harm"]], axis=1).columns.to_numpy()


    new_patient=[]
    def make_expanders(expander_name, sidebar=True):
        """ Set up expanders which contains a set of options. """
        if sidebar:         
            try:
                return st.sidebar.expander(expander_name)
            except:
                return st.sidebar.beta_expander(expander_name)
    
    st.sidebar.subheader("To explore:")

    with make_expanders("Parameters"):
        st.markdown("**Parameters**")
                  
        def sliders(param, min, max, default_value, step_value):
            """
            Function that defines a slider. It's going to be
            initiated with the default value as defined in SciPy.
            Slider min value of 0.01; max value of 10 - are added
            arbitrary.
            """

            slider_i = st.slider('Default value: '+'{}'.format(param)+' = '+f'{default_value}',
                      min_value = min,
                      value = float("{:.2f}".format(default_value)),
                      max_value = max,
                      step = step_value)
            
            return slider_i

        sex = st.radio("SEX", ("Male", "Female"))
        if sex=="Female":
          sex=0
        elif sex=="Male":
          sex=1
        age = sliders("age", 0.0, 100.0, 30.0, 1.0)
        BMI = sliders("BMI", 16.0, 40.0, 20.0, 0.5)
        LVEF_entry = sliders("entry_LVEF",1.0, 80.0, 50.0, 1.0)
        
        Medical_History = st.selectbox("Medical History", ('depression_anxiety_history', 'mental_illness_history',
       'neurological_pathologies', 'hypertension', 'dyslipidemia',
       'smoking', 'diabetes', 'chronic_kidney_disease', 'stroke_TIA',
       'cancer_history', 'cancer', 'COPD_asthma', 'RV_harm', 'alcoolism',
       'Cardio_history'))
        Stress_Factor = st.selectbox("Stress Factor", ( 'emotional_stress', 'physical_stress', ))
        Treatment = st.selectbox("Treatment", ('beta_blockers_in', 'IEC_in',
       'ARA_II_in', 'aspirin_in', 'anti_P2Y12_in',
       'oral_anticoagulation_in', 'statin_in','antidepressant_in', 'anxiolytiques_in','anxiolytiques'))
        Anatomy = st.selectbox("Anatomy", ('apical_type', 'mid_ventricular', 'basale', 'other'))
        Rhythmic_Abnormality = st.selectbox("Rhythmic Abnormality", ('ST_positive', 'Long_QT', 'Tneg_waves'))
        Biomarkers = st.selectbox("Biomarkers", ('entry_troponin', 'troponin_peak', 'NT_proBNP', 'CRP','thrombus_LV'))
        Coronarography = st.selectbox("Coronarography", ('coronarography', 'coronary_disease', 'healthy_coronary'))
        Inhospital_Consequences = st.selectbox("Inhospital Consequences", ('heart_failure', 'atrium_arrhythmia', 'ventricle_arrhythmia',
        'thrombus_LV', 'cardiogenic_shock', 'ECMO','hospital_death','RV_harm'))

        Medical_History = np.array(medical_history == Medical_History).astype(float).tolist()
        Stress_Factor = np.array(stress_factor == Stress_Factor).astype(float).tolist()
        Treatment = np.array(treatment_before == Treatment).astype(float).tolist()
        Anatomy = np.array(anatomy == Anatomy).astype(float).tolist()
        Rhythmic_Abnormality = np.array(rythmic_abnormality == Rhythmic_Abnormality).astype(float).tolist()
        Biomarkers = np.array(biomarkers == Biomarkers).astype(float).tolist()
        Coronarography = np.array(coronarography == Coronarography).astype(float).tolist()
        Inhospital_Consequences = np.array(inhospital_consequences ==Inhospital_Consequences).astype(float).tolist()
        new_patient.extend([sex, age, BMI, LVEF_entry, Medical_History,  Stress_Factor, Treatment, Anatomy, Rhythmic_Abnormality, Biomarkers, Coronarography,Inhospital_Consequences])
    with make_expanders("Machine Learning"):
        st.markdown("**Target**")
        target= st.selectbox("Target variable", ("Inhospital Consequences", "Heart Failure"))
        st.markdown("**Model Engine**")
        engine = st.selectbox("Background Algorithm", ("Pycaret", "LightGBM with Optuna"))
    
    if engine=="Pycaret":
      st.header("Sorry, This page is under construction...")
      return False
      # df_imputed[["age", "sex", "inhospital_consequences_encoded"]] = df_imputed.select_dtypes(np.number).astype(float)[["age", "sex", "inhospital_consequences_encoded"]]
      # from pycaret.classification import *

      # if target=="Heart Failure":
      #   target=""
      # reg_experiment = setup(df_imputed.drop("inhospital_consequences_encoded", axis=1), 
      #                 target = 'heart_failure', 
      #                 #imputation_type='iterative',
      #                 log_experiment=True)   
      # best_model = compare_models(fold=5)
      # predictions = predict_model(best_model, data = new_patient)

      # elif target=="Inhospital Consequences":
      #   target="inhospital_consequences_encoded"

    elif engine=="LightGBM with Optuna":
      import lightgbm as lgb
      import numpy as np
      import sklearn.metrics
      from sklearn.model_selection import train_test_split
      X = df_imputed["anxiolytiques"] =0.0;
      X = df_imputed[['sex', 'age', 'BMI', 'entry_LVEF', 'depression_anxiety_history', 'mental_illness_history',
            'neurological_pathologies', 'hypertension', 'dyslipidemia',
            'smoking', 'diabetes', 'chronic_kidney_disease', 'stroke_TIA',
            'cancer_history', 'cancer', 'COPD_asthma', 'RV_harm', 'alcoolism',
            'Cardio_history',
            'emotional_stress', 'physical_stress',
            'beta_blockers_in', 'IEC_in',
            'ARA_II_in', 'aspirin_in', 'anti_P2Y12_in',
            'oral_anticoagulation_in','statin_in',
            'antidepressant_in', 'anxiolytiques_in', 'anxiolytiques',
            'apical_type', 'mid_ventricular', 'basale', 'other',
            'ST_positive', 'Long_QT', 'Tneg_waves',
            'entry_troponin', 'troponin_peak', 'NT_proBNP', 'CRP','thrombus_LV',
            'coronarography', 'coronary_disease', 'healthy_coronary',
            'heart_failure', 'atrium_arrhythmia', 'ventricle_arrhythmia',
            'thrombus_LV', 'cardiogenic_shock', 'ECMO', 'hospital_death',
            'RV_harm']]

      if target=="Heart Failure":
        target=X["heart_failure"]
        
        y = target
        train_x, valid_x, train_y, valid_y = train_test_split(X, y, test_size=0.25)
        dtrain = lgb.Dataset(train_x, label=train_y)
        param = { # Parameters Tuned with Optuna
            "objective": "binary",
            "metric": "binary_logloss",
            "verbosity": -1,
            "boosting_type": "gbdt",
            "lambda_l1": 0.02793865122821334,
            "lambda_l2": 6.826747702500326e-07,
            "num_leaves": 153,
            "feature_fraction": 0.5928088789054791,
            "bagging_fraction": 0.47214401792490684,
            "bagging_freq": 5,
            "min_child_samples": 71,}

        st.text("Prediction has initiated")
        from sklearn.ensemble import RandomForestClassifier
        regressor= RandomForestClassifier() 
        regressor.fit(train_x, train_y)
        preds=regressor.predict(valid_x)
        new_patient = flatten(new_patient)
        st.write(f"Your input status: ")
        st.code(f"{new_patient}")
        preds_newpatient=regressor.predict(np.expand_dims(new_patient, axis=0))
        from PIL import Image       
        st.write(f"Your result is: ")
        if preds_newpatient<0.5:
          st.subheader("You have no heart failure")
        elif preds_newpatient>0.5:
          st.subheader("You might have heart failure")

      elif target=="Inhospital Consequences":
        target="inhospital_consequences_encoded"
        inhospital_consequences = pd.concat([df_imputed.loc[:, "heart_failure": "hospital_death"], df_imputed.loc[:, "RV_harm"]], axis=1)

        from itertools import chain, combinations
        def all_subsets(ss):
            return chain(*map(lambda x: combinations(ss, x), range(0, len(ss)+1)))
        consequence_subset = list(list(i) for i in all_subsets(inhospital_consequences.columns))
        indexed_subset={}
        for index, subset in enumerate(consequence_subset):
          indexed_subset[index] =list(subset)

        

        y = df_imputed[target]
        train_x, valid_x, train_y, valid_y = train_test_split(X, y, test_size=0.25)
        dtrain = lgb.Dataset(train_x, label=train_y)
        param = { # Parameters Tuned with Optuna
            "objective": "multiclass",
            "metric": "multi_logloss",
            "num_class": 254,
            "verbosity": -1,
            "boosting_type": "gbdt",
            "lambda_l1": 0.02793865122821334,
            "lambda_l2": 6.826747702500326e-07,
            "num_leaves": 153,
            "feature_fraction": 0.5928088789054791,
            "bagging_fraction": 0.47214401792490684,
            "bagging_freq": 5,
            "min_child_samples": 71,}

        from sklearn.ensemble import RandomForestRegressor

        regressor= RandomForestRegressor() 
        regressor.fit(train_x, train_y)
        preds=regressor.predict(valid_x)
        new_patient = flatten(new_patient)
        st.write(f"Your input status: ")
        st.code(f"{new_patient}")
        preds_newpatient=regressor.predict(np.expand_dims(new_patient, axis=0))
        st.subheader(f"Your complication might be...{indexed_subset[int(preds_newpatient)]}")
        # st.text("Prediction has initiated")
        # gbm = lgb.train(param, dtrain, 10)
        # preds = gbm.predict(valid_x)
        # st.write(f"{preds}")
        # st.write(f"{[np.argmax(line) for line in preds]}")
        # pred_labels = np.rint(preds)
        # new_patient = flatten(new_patient)
        # st.write(f"Your status: {new_patient}")
        # st.write(f"{np.expand_dims(new_patient, axis=0)}")
        # pred_newpatient=gbm.predict(np.expand_dims(new_patient, axis=0))
        # st.write('Prediction has finished')
        # st.write("Your consequence might be: ")
        # st.write(f"{np.argmax(pred_newpatient)}")