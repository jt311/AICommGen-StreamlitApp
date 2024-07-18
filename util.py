import re
import json
import uuid
import pyperclip
import streamlit as st
from langsmith import Client, traceable, RunTree
from llm import commGen_LLMChain

@traceable(run_type="chain", name="CommGen Chain")
def generateCommands_JSONStr(user_input, run_tree: RunTree):
    if (isinstance(user_input, str)):
        res = commGen_LLMChain.predict(input=user_input)
        json_str = cleanJSONString(res)
        return removeJSON_markdown(json_str), run_tree.id

def cleanJSONString(llm_res):
    newline_pattern = r'\s*\n\s*'
    cleaned_json_str = re.sub(newline_pattern, "", llm_res)
    return cleaned_json_str

def removeJSON_markdown(json):
    md_pattern = r'^```json\s*(.*?)\s*```$'
    output = re.sub(md_pattern, r'\1', json, re.IGNORECASE)
    return output

def generateCommands_JSONToDict(json_str):
    return json.loads(json_str)

# Define uuid -> str function
def UuidStr():
    return str(uuid.uuid4())

# Define ButtonCallbackFn to copy commands to clipboard
def copyCallback(comm_arr):
    comm_str_arr = [comm_object['command'] for comm_object in comm_arr]
    str_to_copy = '\n'.join([*comm_str_arr])
    pyperclip.copy(str_to_copy)

# Define ChatMsgStyleFn to style the elements inside chat message container
def ChatMsgStyle(comm_flow_name, comm_arr, run_id, msg_idx):
    st.markdown(f"**:orange[{comm_flow_name}]**")

    for idx, comm_object in enumerate(comm_arr):
        st.markdown(f"""**{idx+1}. {comm_object['description']}:** 
                    :green-background[{comm_object['command']}]""")
        
    col1, col2, col3 = st.columns([1.5,0.5,4])
    with col1:
        st.button(
            label="Copy Commands",
            type="primary",
            key=UuidStr(),
            help="Copies all commands highlighted in green to clipboard (separated by newline)",
            on_click=copyCallback,
            args=(comm_arr, ))                
    
    with col2:
        st.button(
            label=":thumbsup:",
            help="Good Response",
            key=UuidStr(),
            on_click=handleUserFeedback,
            args=(run_id,1,msg_idx))
        
    with col3:
        st.button(
            label=":thumbsdown:",
            help='Bad Response',
            key=UuidStr(),
            on_click=handleUserFeedback,
            args=(run_id,0,msg_idx))
        

# LangSmith Feedback
def handleUserFeedback(run_id, user_score, msg_idx):
    print("Called Feedback Handler")
    ls_client = Client()
    if run_id:
        score_mappings = {1:"👍", 0:"👎"}

        if user_score is not None:
            feedback_type_str = f"User Feedback: {score_mappings[user_score]}"
            ls_client.create_feedback(
                run_id,
                feedback_type_str,
                score=user_score)
            
            st.session_state.messages[msg_idx]['feedback_submitted'] = True
        else:
            st.warning("Invalid feedback score.")
        
# Clear messages from session state
def clearMsgs():
    st.session_state.messages = []