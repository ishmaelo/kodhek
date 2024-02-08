import streamlit as st
from streamlit_modal import Modal

import streamlit.components.v1 as components


def create_modal_widget(title,key,padding,max_width):
    modal = Modal(
        title, 
        key=key,
        # Optional
        padding=padding,    # default value
        max_width=max_width  # default value
    )
    
    return modal