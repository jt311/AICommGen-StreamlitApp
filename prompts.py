SUMM_PROMPT_TEMPLATE = """Progressively summarize the lines of conversation provided, adding onto the previous summary returning a new summary. Only include the requests made by the human in the summary. Do not include the response by the AI in the summary.

EXAMPLE
Current summary:
The human asks what the AI thinks of artificial intelligence.

New lines of conversation:
Human: Why do you think artificial intelligence is a force for good?
AI: Because artificial intelligence will help humans reach their full potential.

New summary:
The human asks what the AI thinks of artificial intelligence. The human then asks the AI for reasons why artificial intelligence is a force for good.
END OF EXAMPLE

Current summary:
{summary}

New lines of conversation:
{new_lines}

New summary:"""

SYSTEM_MSG_TEMPLATE = """You are a helpful command generator that can generate commands for Cisco IOS. Generate the commands given the user's request. Assume the user is already on the command line interface for the Cisco device.
  Do not generate the full command sequence. Do not generate any descriptive or explanatory text.
  The first command in the commands array must specify whether the user should switch to user EXEC, privileged EXEC or global configuration.
  You will reply only with the JSON itself using the following JSON template.
  { "flow_name": "Configure SW1 to be a VTP Server",
    "commands" : [
      { "description": "Switch to the global configuration", "command": "configure terminal"},
      { "description": "Set the VTP mode to server", "command": "vtp mode server" },
      { "description": "Set the VTP domain to cisco:", "command": "vtp domain cisco" }]
  }
  """

EX_1 = """configure an ip address on interface FastEthernet0/0.
          Then, I want to run hsrp on this interface with virtual ip 10.10.10.1"""

EX_2 = """configure ospf on R1.
          The network is 10.0.0.0, the wildcard mask is 0.0.255.255 and the area is 1"""

EX_3 = """view the routing table on R2"""

INTENT_STR = "**:green[I want to]**"