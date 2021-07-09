
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 14:25:33 2021

@author: Daisuke Kuwabara&Nesrine Benanteur  https://github.com/kwdaisuke/Long-Term-Prognosis-of-Patients-With-Takotsubo-Syndrome
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
  
  path_dk = "/content/drive/MyDrive/Takotsubo_Prognosis/Data/modified_data.csv"
  df = pd.read_csv(path_dk)
  

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
    st.header("1. Demographics")
  ################################
  st.write("")
  row1, row2, row3 = st.beta_columns(3)

  with row1, _lock:
    st.write("We can observe many patients are at age of around 60 to 80")
    def age_box():
      fig,ax = plt.subplots()
      with st.echo(): 
        sns.boxplot(x="age", hue="sex", data=df)
        plt.title("Patient's age", fontsize=14, fontname="Times New Roman Bold", fontweight="bold")
      return fig

    plot=age_box()
    st.pyplot(plot, clear_figure=True)

  with row2, _lock:
    st.write("We can observe BMI value is around 20 to 30")
    def BMI_hist():
      fig2,ax = plt.subplots()
      with st.echo(): 
        sns.histplot(x="BMI",data=df, kde=True)
        plt.title("Patient's BMI", fontsize=14, fontname="Times New Roman Bold", fontweight="bold")
      return fig2
    plot=BMI_hist()
    st.pyplot(plot, clear_figure=True)

  with row3, _lock:
    st.write("We can observe BMI value is around 20 to 30")
    def BMI_hist():
      fig,ax = plt.subplots()
      with st.echo(): 
        sns.scatterplot(x="age", y="BMI",data=df[df.BMI.notnull()],  s=50, edgecolor="black", linewidth=0.5,legend=False)    
        plt.title("age vs BMI", fontsize=14, fontname="Times New Roman Bold", fontweight="bold")
      return fig
    st.pyplot(BMI_hist(), clear_figure=True)
  ############################################

  with st.beta_container():
    st.header("2. Medical History")
  st.write("")
  row1, row2, row3 = st.beta_columns(3)

  with row1, _lock:
    cardio_history_alcoolisme = df.iloc[:, -2:].fillna(0)
    medical_history = pd.concat([df.loc[:, "depression_anxiety_history":"COPD_asthma"], cardio_history_alcoolisme], axis=1)
    dff = medical_history.sum().sort_values().reset_index().rename(columns={"index": "col", 0:"values"})
    dff.sort_values("values", inplace=True, ascending=False)
    def medical_hist_sum():
      fig,ax = plt.subplots()
      with st.echo():
        sns.barplot(x="col", y="values", data=dff, order=dff["col"])
        plt.xticks(rotation=90)
      return fig
    st.pyplot(medical_hist_sum(), clear_figure=True)

  with row2, _lock:
    st.header("3. Treatment")
    df.columns.get_loc("ttt entrée = ttt antérieur") # Get the integer index of the specified column
    treatment_before = df.iloc[: , 25: 33].replace(np.nan, 0) # Exclude ttt entrée = ttt antérieur
    treatment_after = df.iloc[:,  56:65].replace(np.nan, 0)
    treatment_before["anxiolytiques"] =0.0 # Add anxiolytiques for treatment_before
    sum_treatment = pd.concat([treatment_before.sum(axis=0), treatment_after.sum(axis=0)], axis=1)
    sum_treatment.rename(columns = {0:"Total_Sum_Before ", 1:"Total_Sum_After"}, inplace=True)
    def Treatment_count():
      fig2,ax = plt.subplots()
      with st.echo(): 
        ax = sum_treatment.plot.bar(figsize=(12, 7), rot=30)
        for p in ax.patches:
          ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
        plt.title("Comparison of total count of respective treatment before and after the hospitalization", fontsize=14, fontweight="bold")
      return fig2
    st.pyplot(Treatment_count(), clear_figure=True)

    with row3, _rock:
      def correlation():
        fig, ax = plt.subplots()
        with st.echo():
          treatment_before.iloc[:, :8].corr(method="kendall").style.background_gradient(cmap="coolwarm")
          treatment_after.corr(method="kendall").style.background_gradient(cmap="coolwarm")
        return fig
      st.pyplot(corr_before(), clear_figure=True)




  with st.beta_container():
    st.header("4. LVEF")
  ################################
  st.write("")
  row1, row2, row3 = st.beta_columns(3)

  with row1, _lock:
    LVEF = df.loc[:, "entry_LVEF":"out_LVEF"]; LVEF = LVEF.astype("float") ; LVEF.out_LVEF =LVEF.out_LVEF.replace("NaN", np.nan)
    bin = [-np.inf, 40, 50, 55, np.inf]
    LVEF["entry_LVEF_category"] = pd.cut(LVEF.entry_LVEF, bin, labels = "1 2 3 4".split(" ")) ; LVEF.notnull().sum()
    diff = LVEF.dropna().out_LVEF - LVEF.dropna().entry_LVEF ; diff[diff <0]
    
    def LVEF_diff():
      fig,ax = plt.subplots()
      with st.echo(): 
        diff.plot.hist() 
        plt.title("Difference of LVEF", fontsize=14, fontname="Times New Roman Bold", fontweight="bold")
      return fig
    plot=LVEF_diff()
    st.pyplot(plot, clear_figure=True)

  with row2, _lock:
    biomarkers = pd.concat([df.loc[:, "entry_troponin": "NT_proBNP"], df.iloc[:, 65]], axis=1) 
    biomarkers["NT_proBNP"] = biomarkers["NT_proBNP"].replace("23 289", "23289")  # Fill the blank 
    def Biomarker():
      fig2  ,ax = plt.subplots()
      with st.echo(): 
        biomarkers.troponin_peak.clip(biomarkers.troponin_peak.min(), upper_bound).plot.box()
        biomarkers.NT_proBNP.astype("float").plot.box(figsize=(8, 6))
        plt.title("Biomarker", fontsize=14, fontname="Times New Roman Bold", fontweight="bold")
      return fig2
    plot=Biomarker()
    st.pyplot(plot, clear_figure=True)

  with row3, _lock:
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
      with st.echo(): 
        ax = pd.concat([pd.DataFrame(a), b], axis=0).plot(kind="bar", stacked=True)
        ax.set_xticklabels(["non_examined", "examined"], rotation=30)   
        plt.title("Coronarography", fontsize=14, fontname="Times New Roman Bold", fontweight="bold")
      return fig
    st.pyplot(coronarography(), clear_figure=True)
  ############################################




  # avriable = st.selectbox('box', df.columns)
  # st.area_chart(df[variable])

  # selected_col2=st.multiselect('Choose variables', df.columns)
  # st.bar_chart(df[selected_col2])

  # st.dataframe(df.describe().T)
  # st.dataframe(df.style.highlight_null())

  # st.sidebar.markdown("## Select Data Time and Detector")

  # select_event = st.sidebar.selectbox("Which variables you want to see?",
  #                                     list(df.columns))

  # st.sidebar.markdown('## Set Plot Parameters')
  # dtboth = st.sidebar.slider('Time Range (seconds)', 0.1, 18.0, 1.0)  # min, max, default
  # dt = dtboth / 2.0
  # st.bar_chart(df[select_event])
  return 


##################################################################


# def page_introduction():
    
#     # Space so that 'About' box-text is lower
#     st.sidebar.write("")
#     st.sidebar.write("")
#     st.sidebar.write("")
#     st.sidebar.write("")
#     st.sidebar.write("")
#     st.sidebar.write("")
#     st.sidebar.write("")
#     st.sidebar.write("")
    
#     st.markdown("<h2 style='text-align: center;'> Welcome To </h2>", 
#                 unsafe_allow_html=True)
#     st.markdown("<h1 style='text-align: center;'> Distribution Analyser</h1>", 
#                 unsafe_allow_html=True)
     

#     st.info("""
#             There are two main features: \n
#             - Explore distributions 
#             - Fit distributions  
#             $←$ To start playing with the app, select an option on the 
#             left sidebar.
#             """)
#     st.info("""
#             - Here is a youtube link to the [Distribution Analyser walkthrough](https://www.youtube.com/watch?v=6S0b7gFY36I&t=3s).
#             - App snippets and brief descriptions ⮧
#             """)


#     image1 = "https://raw.githubusercontent.com/rdzudzar/DistributionAnalyser/main/images/Dist1.png?token=AIAWV2ZQOGWADUFWZM3ZWBLAN3CD6"
#     image2 = "https://raw.githubusercontent.com/rdzudzar/DistributionAnalyser/main/images/Dist2.png?token=AIAWV27IFN4ZLN3EAONHMVLAN3BNS"
#     image3 = "https://raw.githubusercontent.com/rdzudzar/DistributionAnalyser/main/images/Dist3.png?token=AIAWV25DCGRPJRFLDPQIWN3AN3BPA"
#     image4 = "https://raw.githubusercontent.com/rdzudzar/DistributionAnalyser/main/images/Fit1.png?token=AIAWV2ZVPX4HJL77ZQRTIBDAN3BQK"
#     image5 = "https://raw.githubusercontent.com/rdzudzar/DistributionAnalyser/main/images/Fit2.png?token=AIAWV27QFQIAEOQSRDQVC3DAN3BRQ"
#     image6 = "https://raw.githubusercontent.com/rdzudzar/DistributionAnalyser/main/images/Fit3.png?token=AIAWV265V2EQ24SLCTLEHOTAN3BSQ"


    
#     def make_line():
#         """ Line divider between images. """
            
#         line = st.markdown('<hr style="border:1px solid gray"> </hr>',
#                 unsafe_allow_html=True)

#         return line    


#     # Images and brief explanations.
#     st.error('Explore distributions')
#     feature1, feature2 = st.beta_columns([0.5,0.4])
#     with feature1:
#         st.image(image1, use_column_width=True)
#     with feature2:
#         st.warning('Select Distribution')
#         st.info("""
#                 - Select distribution from Dropdown Menu (or type its name)
#                 - Change distribution parameters on sliders and see the change. 
#                 - Check created hyperlink to **SciPy** official documentation at the bottom of the sidebar.
#                 """)
    
#     make_line()
    
#     feature3, feature4 = st.beta_columns([0.6,0.4])
#     with feature3:        
#         st.image(image2, use_column_width=True)
#     with feature4:
#         st.warning('Tweak Display')
#         st.info("""
#                 - Pick *Dark/Light Theme*
#                 - Select **on/off** each option: Histogram, PDF, CDF, SF,
#                 boxplot, quantiles, or shade 1/2/3 $\sigma$.
#                 - Get Table with descriptive statistics.
#                 """)
#     make_line()
    
#     feature5, feature6 = st.beta_columns([0.6,0.4])
#     with feature5:
#         st.image(image3, use_column_width=True)
#     with feature6:
#         st.warning('Export')
#         st.info("""
#                 - Generate a Python code with selected distribution and 
#                 parameters
#                 - Save .py file or copy to clipboard to take it home.
#                 """)
    
#     make_line()
    
#     st.error('Fit distributions')
#     feature7, feature8 = st.beta_columns([0.4,0.6])
#     with feature7:
#         st.warning('Import')
#         st.info("""
#                 - Import a **.csv** file with your own data (or get a sample).
#                 - Plot your data with or without basic statistical information.
#                 """)
#     with feature8:
#         st.image(image4, use_column_width=True)
    
#     make_line()
    
#     feature9, feature10 = st.beta_columns([0.4,0.6])
#     with feature9:
#         st.warning('Fit')
#         st.info("""
#                 - Multiselectbox: pick any number of distributions
#                 - **'All_distributions'** - select all
#                 - Fit distribution(s) to your data
#                 """)
#     with feature10:
#         st.image(image5, use_column_width=True)        
    
#     make_line()
    
#     feature10, feature11 = st.beta_columns([0.4,0.6])
#     with feature10:
#         st.warning('Results & Export')
#         st.info("""
#                 - Interactive **Figures**
#                 - **Table** with all fitted distribution(s) 
#                 - Generate **Python code** with best fit distribution 
#                 """)
#     with feature11:
#         st.image(image6, use_column_width=True)      
    
#     make_line()
    
#     st.info('There are 100 continuous distribution functions  \
#                 from **SciPy v1.6.1** available to play with.')
        
#     st.markdown("""
                
#                 - Abriviations:
                
#                     - PDF - Probability Density Function
                
#                     - CDF - Cumulative Density Function
                
#                     - SF - Survival Function
                
#                     - P(X<=x) - Probability of obtaining a value smaller than 
#                                 x for selected x.
                
#                     - Empirical quantiles for a data array: 
#                         Q1, Q2, Q3 respectively 0.25, 0.50, 0.75
                              
#                     - $\sigma$ (Standard Deviation). On plot shades: 
#                         mean$\pm x\sigma$
                        
#                     - SSE - Sum of squared estimate of errors
                
#                 """)
    
#     return