import streamlit as st
import pandas as pd
import numpy as np
from streamlit.components.v1 import html
from testModel import getHydrates

# Set page configuration
st.set_page_config(
    page_title="Hydrate Detection Challenge",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Initialize session state for pipe data and hydrate status
if "pipes" not in st.session_state:
    st.session_state.pipes = {}  # Dictionary to store pipe data and statuses

if "alert_active" not in st.session_state:
    st.session_state.alert_active = False  # To control global alert popup

# Function to toggle hydrate status for a specific pipe
def toggle_hydrate(pipe_name):
    st.session_state.pipes[pipe_name]["hydrate_status"] = not st.session_state.pipes[pipe_name]["hydrate_status"]
    if st.session_state.pipes[pipe_name]["hydrate_status"]:
        st.session_state.alert_active = True  # Activate global alert if any pipe has hydrate

# Function to dismiss the alert popup
def dismiss_alert():
    st.session_state.alert_active = False

# Header and Introduction
st.title("🧊 Hydrate Detection Challenge")
st.markdown(
    """
    Welcome to the **Hydrate Detection Challenge**! This app helps lease operators quickly identify and predict hydrate formation 
    in pipelines to optimize well production and minimize losses. 🌟
    """
)

# Main Tab Layout
tab1, tab2 = st.tabs(["Pipeline Overview", "Add New Pipe"])


# --- Tab 2: Add New Pipe ---
with tab2:
    st.header("📈 Add New Pipe")
    
    # Input field for naming the new pipe
    new_pipe_name = st.text_input("Enter Pipe Name")
    
    # File uploader for uploading CSV data for the new pipe
    uploaded_file = st.file_uploader("Upload your data file (CSV)", type="csv")
    
    
    if st.button("Submit Pipe") and uploaded_file and new_pipe_name:
        # Load and process the uploaded CSV file
        data = pd.read_csv(uploaded_file)
        data["Time"] = pd.to_datetime(data["Time"])  # Convert Time column to datetime
        data.set_index("Time", inplace=True)         # Set Time as index
        
        # Store data in session state under the given pipe name
        st.session_state.pipes[new_pipe_name] = {
            "data": data,
            "hydrate_status": False   # Default hydrate status is False (no hydrate detected)
        }
        
        st.success(f"Pipe '{new_pipe_name}' added successfully!")

# --- Tab 1: Pipeline Overview ---
with tab1:
    st.header("🔔 Pipe Status and Hydrate Alerts")
    
    selectpipe = []

    # Display Drop Down Menu of all Pipes
    if st.session_state.pipes:
        selectpipe = st.selectbox("Select a Pipe", options=list(st.session_state.pipes.keys()))
        
        # Get the data for the selected pipe
        selected_pipe_data = st.session_state.pipes[selectpipe]
        
        # Plot a graph for the selected pipe's data
        st.write(f"### Graph for '{selectpipe}'")
        st.line_chart(selected_pipe_data["data"])  # This will plot the entire dataframe

        st.write(f"### Hydrate Probability Data for '{selectpipe}'")


    else:
        st.info("No pipes added yet. Please add a new pipe in the 'Add New Pipe' tab.")

    # # Display uploaded data and graphs for this new pipe
    # st.write(f"### Data for '{new_pipe_name}'")
    # st.dataframe(data)
    
    # # Graph visualization of key metrics from uploaded data
    # st.write(f"### Key Metrics Visualization for '{new_pipe_name}'")
    # st.line_chart(data)
    
    # # Button to simulate hydrate detection for this specific pipe
    # if st.button(f"Simulate Hydrate Detection for '{new_pipe_name}'"):
    #     toggle_hydrate(new_pipe_name)


    # # If any alert is active, show the fullscreen blinking popup with dismiss button
    # if st.session_state.alert_active:
    #     st.markdown(
    #         """
    #         <style>
    #             @keyframes blink {
    #                 0% {background-color: rgba(255, 0, 0, 0.9);}
    #                 50% {background-color: rgba(255, 0, 0, 0.5);}
    #                 100% {background-color: rgba(255, 0, 0, 0.9);}
    #             }
    #             .alert-popup {
    #                 position: fixed;
    #                 top: 0;
    #                 left: 0;
    #                 width: 100%;
    #                 height: 100%;
    #                 animation: blink 1s infinite;
    #                 color: white;
    #                 display: flex;
    #                 flex-direction: column;
    #                 align-items: center;
    #                 justify-content: center;
    #                 font-size: 1.5rem;
    #                 text-align: center;
    #                 z-index: 9999;
    #             }
    #             .alert-button {
    #                 margin-top: 20px;
    #                 padding: 10px 20px;
    #                 font-size: 1rem;
    #                 background: white;
    #                 color: red;
    #                 border: none;
    #                 border-radius: 5px;
    #                 cursor: pointer;
    #             }
    #         </style>
    #         <div class="alert-popup">
    #             ⚠️ **Hydrate Detected! Immediate Action Required!**  
    #             <button class="alert-button" onclick="window.location.reload();">Dismiss Alert</button>
    #         </div>
    #         """,
    #         unsafe_allow_html=True,
    #     )

        

# Footer section with credits
st.markdown(
    """
    ---
    *Built for HackUTD: RippleEffect by EOG Resources.*  
    """
)