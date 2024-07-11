import streamlit as st
from util import generateCommands_JSONStr, generateCommands_JSONToDict, UuidStr
from prompts import EX_1, EX_2, EX_3


# Streamlit App
st.title("Cisco IOS - Command Generator :link:")
st.subheader(":green[What would you like to do on the Cisco device?]")
intent_str = "**:green[I want to]**"
with st.expander("See examples"):
    with st.container():
        st.markdown(f"{intent_str} {EX_1}")
        st.markdown(f"{intent_str} {EX_2}")
        st.markdown(f"{intent_str} {EX_3}")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    if message["role"] == "assistant":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            st.button(label="Copy Commands", type="primary", key=UuidStr())
    else:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


if user_input := st.chat_input("I want to..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    json_str_res = generateCommands_JSONStr(user_input=user_input)
    if (json_str_res != "Invalid Data"):
        commands_object = generateCommands_JSONToDict(json_str_res)
        comm_flow_name = commands_object['flow_name'] + ":"
        comm_arr = [f"{idx+1}. {comm_object['description']}: {comm_object['command']}" 
                    for idx, comm_object in enumerate(commands_object['commands'])]
        
        llm_response = "\n".join([comm_flow_name, *comm_arr])
    else:
        llm_response = json_str_res
     
    with st.chat_message("assistant"):
        st.markdown(f"{llm_response}")
        st.button(label="Copy Commands", type="primary", key=UuidStr())

    st.session_state.messages.append({"role": "assistant", "content": llm_response})
