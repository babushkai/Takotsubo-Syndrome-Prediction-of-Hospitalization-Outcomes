
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 11:54:36 2021

@author: Daisuke Kuwabara & Nesrine Benanteur https://github.com/kwdaisuke/Long-Term-Prognosis-of-Patients-With-Takotsubo-Syndrome
"""
# Package imports
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import cmasher as cmr
import numpy as np
#from scipy import stats
import scipy.stats
import math

from bokeh.plotting import figure
from bokeh.models import Legend
#from bokeh.io import curdoc

# Helper function imports
# These are pre-computed so that they don't slow down the App
from helper_functions import distr_selectbox_names,creating_dictionaries

import time
import base64
import collections


def page_fit():
    """
    The fit page in this app made with Streamlit is for a fitting a selected
    distribution(s) to the User imported data.
    """
    name_docstring_dict, name_eq_dict, name_proper_dict, \
        all_dist_params_dict, name_url_dict = creating_dictionaries()
    
    st.sidebar.info("""
                Import your data as a **.csv** file 
                and follow instructions to fit a
                continuous distribution(s) to your data.
                """)
                
    # Add a bit empy space before showing About
    st.sidebar.text("")

    st.sidebar.markdown("**Select Figure Mode:**")
    plot_mode = st.sidebar.radio("Options", ('Dark Mode', 'Light Mode'))   

    st.sidebar.text("")
    st.sidebar.text("")

    st.markdown("<h1 style='text-align: center;'> Fit distribution(s) </h1>", 
                unsafe_allow_html=True)

    
    #Streamlit Sharing if you set the config option in .streamlit/config.toml:
    #[server]
    #maxUploadSize=2

    st.number_input("Enter a number")