import streamlit as st
from output import generateCommands_JSONStr, generateCommands_JSONToDict

st.title("Cisco IOS - Command Generator")
st.subheader("What would you like to do on the Cisco device?")

# Streamlit App
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
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
        
    st.session_state.messages.append({"role": "assistant", "content": llm_response})
