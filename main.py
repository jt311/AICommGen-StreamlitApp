import streamlit as st
from util import generateCommands_JSONStr, generateCommands_JSONToDict, UuidStr, copyCallback
from prompts import EX_1, EX_2, EX_3


# Streamlit App
st.title("Cisco IOS - Command Generator :link:")
st.subheader(":green[What would you like to do on the Cisco device?]")
intent_str = "**:green[I want to]**"

with st.sidebar.expander("See examples"):
    with st.container():
        st.markdown(f"{intent_str} {EX_1}")
        st.markdown(f"{intent_str} {EX_2}")
        st.markdown(f"{intent_str} {EX_3}")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    if message["role"] == "assistant":
        with st.container(border=True):
            with st.chat_message(message["role"]):
                comm_fn = message["comm_flow_name"]
                st.markdown(f"**:orange[{comm_fn}]**")

                for idx, comm_object in enumerate(message['comm_arr']):
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
                        args=(message['comm_arr'], ))                
                
                with col2:
                    st.button(label=":thumbsup:", help="Good Response", key=UuidStr())
                with col3:
                    st.button(label=":thumbsdown:", help='Bad Response', key=UuidStr())
                                    
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
    
    with st.container(border=True):
        with st.chat_message("assistant"):
            st.markdown(f"**:orange[{comm_flow_name}]**")

            for idx, comm_object in enumerate(commands_object['commands']):
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
                    args=(commands_object['commands'], ))
                                
            with col2:
                    st.button(label=":thumbsup:", help="Good Response", key=UuidStr())
            with col3:
                st.button(label=":thumbsdown:", help='Bad Response', key=UuidStr())

    st.session_state.messages.append({"role": "assistant",
                                      "comm_flow_name": comm_flow_name,
                                      "comm_arr": commands_object['commands']})