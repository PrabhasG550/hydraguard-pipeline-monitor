import streamlit as st
import pandas as pd
import numpy as np
from streamlit.components.v1 import html
from testModel import testHydrate
import time as t

st.set_page_config(
    page_title="HydraGuard",
    layout="centered",
    initial_sidebar_state="collapsed",
)

if "pipes" not in st.session_state:
    st.session_state.pipes = {}  

st.title("🧊 Hydrate Detection Challenge")
st.markdown(
    """
    Welcome to the **Hydrate Detection Challenge**! This app helps lease operators quickly identify and predict hydrate formation 
    in pipelines to optimize well production and minimize losses. 🌟
    """
)

tab1, tab2 = st.tabs(["Pipeline Overview", "Add New Pipe"])

with tab2:
    st.header("📈 Add New Pipe")
    
    new_pipe_name = st.text_input("Enter Pipe Name")
    
    uploaded_file = st.file_uploader("Upload your data file (CSV)", type="csv")
    if uploaded_file is not None:
        print('UPLOADED:',uploaded_file.name)
    
    if st.button("Submit Pipe") and uploaded_file and new_pipe_name:
        data = pd.read_csv(uploaded_file)
        data["Time"] = pd.to_datetime(data["Time"])  
        data.set_index("Time", inplace=True)         
        
        data = data.fillna(method='ffill').fillna(method='bfill')

        st.session_state.pipes[new_pipe_name] = {
            "data": data,
            "hydrate_status": False,
            "filename": uploaded_file.name
        }
        
        st.success(f"Pipe '{new_pipe_name}' added successfully!")

with tab1:
    st.header("🔔 Pipe Status and Hydrate Alerts")
    
    selectpipe = []

    if st.session_state.pipes:
        selectpipe = st.selectbox("Select a Pipe", options=list(st.session_state.pipes.keys()))
        
        selected_pipe_data = st.session_state.pipes[selectpipe]
        
        st.write(f"### Graph for '{selectpipe}'")

        df = st.session_state.pipes[new_pipe_name]['data']
        chart_placeholder = st.empty()
        hydrates = np.array(testHydrate(st.session_state.pipes[new_pipe_name]['filename']))
        warning_placeholder = st.empty()

        for i in range(len(df)):
            data_to_plot = df.iloc[:i+1]

            chart_placeholder.line_chart(data_to_plot)
            if hydrates[i] == 1:
                warning_placeholder.warning("⚠️ POTENTIAL HYDRATE DETECTED! ⚠️")
                
            else:
                warning_placeholder.empty()

            t.sleep(0.2)

        st.write(f"### Hydrate Occurrence Data for '{selectpipe}'")
        
        
        print(hydrates)
        

        hydrate_rows = df[hydrates == 1]
        if hydrate_rows.empty:
            st.write('No Hydrates Found!')
        else:
            st.table(hydrate_rows)

    else:
        st.info("No pipes added yet. Please add a new pipe in the 'Add New Pipe' tab.")

st.markdown(
    """
    ---
    *Built for HackUTD: RippleEffect by EOG Resources.*\n
    *Team Members: Devansh Agrawal, Pritam Hegde, Prabhas Gade*  
    """
)