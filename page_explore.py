
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 11:54:36 2021

@author: Daisuke Kuwabara & Nesrine Benanteur https://github.com/kwdaisuke/Long-Term-Prognosis-of-Patients-With-Takotsubo-Syndrome
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

# Helper function imports
# These are pre-computed so that they don't slow down the App
from helper_functions import (distr_selectbox_names,
                              stats_options,
                              creating_dictionaries,
                             )


def page_explore():
    """ 
    The first page in this app made with Streamlit is for an interactive 
    exploration of the continuous distributions that are available in SciPy.
    """
    
    def make_expanders(expander_name, sidebar=True):
        """ Set up expanders which contains a set of options. """
        if sidebar:         
            try:
                return st.sidebar.expander(expander_name)
            except:
                return st.sidebar.beta_expander(expander_name)
    
    st.sidebar.subheader("To explore:")

    with make_expanders("Hyperparameter Tuning"):
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


        age="age"
        BMI="BMI"
        age = sliders(age, 0.0, 100.0, 30.0, 1.0)
        BMI = sliders(BMI, 16.0, 40.0, 20.0, 0.5)
        treatment_before = st.selectbox("Treatment before", ("beta_blockers", "IEC", "Antip Py12", "ARA_Ⅱ", "aspirin", "anti_P2Y12", "oral_anticoagulation", "statin", "antidepressant", "anxiolytiques"))
        Anatomy = st.selectbox("Anatomy", ("Apycal", "medio_ventriculaire", "basale", "other"))
        Rhythmic_abnormalities = st.selectbox("Rhythmic_abnormalities", ("ST_positive", "Long_QT", "Tneg_waves"))
        Biomarkers = st.selectbox("Biomarkers", ("entry_troponine", "troponine_peak", "NT_proBNP", "CRP"))