import streamlit as st
from output import generateCommands_JSONStr, generateCommands_JSONToDict

st.title("Cisco IOS - Command Generator")
st.subheader("What would you like to do on the Cisco device?")
user_input = st.text_input("EG: I want to configure an ip address on interface fa0/0")

if st.button("Generate Commands") and user_input:
    with st.spinner("Generating commands..."):
        json_str_res = generateCommands_JSONStr(user_input=user_input)
    if (json_str_res != "Invalid Input"):
        commands_object = generateCommands_JSONToDict(json_str=json_str_res)
        comm_flow_str = f"{commands_object['flow_name']}"
        st.write(comm_flow_str)
        for elem in commands_object['commands']:
            comm_str = f"{elem['description']}: {elem['command']}"
            st.write(comm_str)
    else: 
        st.write(json_str_res)