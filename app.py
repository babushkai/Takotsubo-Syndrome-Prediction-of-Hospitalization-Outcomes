
# -*- coding: utf-8 -*-
"""
Created on Wed July 10  11:54:36 2021

@author: Daisuke Kuwabara&Nesrine Benanteur  https://github.com/kwdaisuke
"""
# Awesome Streamlit
import streamlit as st

# Add pages -- see those files for deatils within
from page_introduction import page_introduction
from page_explore import page_explore
# Use random seed
import numpy as np
np.random.seed(1)


# Set the default elements on the sidebar
st.set_page_config(page_title='Takotsubo-Syndrome-Prediction-of-Hospitalization-Outcomes')

logo, name = st.sidebar.beta_columns(2)
with logo:
    image =   "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTtrDcEEvdSPDiKyg4FiTsxIgyMb-klnNGP2Q&usqp=CAU"
    st.image(image, use_column_width=True)
with name:
    st.markdown("<h1 style='text-align: left; color: grey;'> \
                Takotsubo Syndrome Prediction of Hospitalization Outcomes </h1>", unsafe_allow_html=True)

st.sidebar.write(" ")


def main():
    """
    Register pages to Explore and Fit:
        page_introduction - contains page with images and brief explanations
        page_explore - contains various functions that allows exploration of
                        continuous distribution; plotting class and export
    """
    try:
        import googleclouddebugger
        googleclouddebugger.enable(
            breakpoint_enable_canary=True
        )
    except ImportError:
        pass

    pages = {
        "Visualization": page_introduction,
        "Data Analyze": page_explore,
    }

    st.sidebar.title("Main options")

    # Radio buttons to select desired option
    page = st.sidebar.radio("Select:", tuple(pages.keys()))
                                
    # Display the selected page with the session state
    pages[page]()

    # Write About
    st.sidebar.header("About")
    st.sidebar.warning(
            """
            Takotsubo Analysis app is created and maintained by 
            **Daisuke Kuwabara&Nesrine Benanteur**. If you like this app please star its
            [**GitHub**](https://github.com/kwdaisuke/Takotsubo-Syndrome-Prediction-of-Hospitalization-Outcomes)
            repo, share it and feel free to open an issue if you find a bug 
            or if you want some additional features.
            """
    )


if __name__ == "__main__":
    main()