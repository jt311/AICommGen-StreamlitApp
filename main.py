import streamlit as st
from util import (
                generateCommands_JSONStr,
                generateCommands_JSONToDict, 
                ChatMsgStyle,
                clearMsgs)
from prompts import EX_1, EX_2, EX_3


# Streamlit App
st.title("Cisco IOS - Command Generator :link:")
st.subheader(":green[What would you like to do on the Cisco device?]")
intent_str = "**:green[I want to]**"

st.sidebar.title("Menu")

with st.sidebar.expander(label="See examples", expanded=True, icon="📝"):
    with st.container():
        st.markdown(f"{intent_str} {EX_1}")
        st.markdown(f"{intent_str} {EX_2}")
        st.markdown(f"{intent_str} {EX_3}")

st.sidebar.button(
    label="Clear Message History",
    type='primary',
    on_click=clearMsgs)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    if message["role"] == "assistant":
        with st.container(border=True):
            with st.chat_message(message["role"]):
                ChatMsgStyle(
                    comm_flow_name=message['comm_flow_name'],
                    comm_arr=message['comm_arr'],
                    run_id=message['run_id'])
                                    
    else:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


if user_input := st.chat_input("I want to..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    json_str_res, run_id = generateCommands_JSONStr(user_input=user_input)

    if json_str_res:
        commands_object = generateCommands_JSONToDict(json_str_res)
        comm_flow_name = commands_object['flow_name'] + ":"
                                
    with st.container(border=True):
        with st.chat_message("assistant"):
            ChatMsgStyle(
                comm_flow_name=comm_flow_name,
                comm_arr=commands_object['commands'],
                run_id=run_id)
            
    st.session_state.messages.append({"role": "assistant",
                                "comm_flow_name": comm_flow_name,
                                "comm_arr": commands_object['commands'],
                                "run_id": run_id}) 