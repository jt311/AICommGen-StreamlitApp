import re
import json
from llm import commGen_LLMChain

def generateCommands_JSONStr(user_input):
    if (isinstance(user_input, str)):
        res = commGen_LLMChain.predict(input=user_input)
        json_str = cleanJSONString(res)
        return removeJSON_markdown(json_str)
    return "Invalid Input"

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
