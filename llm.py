from langchain_openai import ChatOpenAI, OpenAI
from langchain.prompts import ChatPromptTemplate, PromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage
from langchain.chains import LLMChain
from langchain.memory import ConversationSummaryMemory
from dotenv import load_dotenv
import os
from prompts import SUMM_PROMPT_TEMPLATE, SYSTEM_MSG_TEMPLATE

load_dotenv()
API_KEY = os.environ["OPENAI_API_KEY"]

llm = ChatOpenAI(model='gpt-4o', api_key=API_KEY, temperature=0.0)
llm.bind(response_format={"type":"json_object"})

promptTemplate = ChatPromptTemplate.from_messages([
    SystemMessage(content=SYSTEM_MSG_TEMPLATE),
    MessagesPlaceholder(variable_name='history'),
    HumanMessagePromptTemplate.from_template('{input}')
])

summaryPromptTemplate = PromptTemplate.from_template(SUMM_PROMPT_TEMPLATE)
summary_memory = ConversationSummaryMemory(
    llm=OpenAI(temperature=0.0),
    memory_key='history',
    prompt=summaryPromptTemplate,
    return_messages=True)

commGen_LLMChain = LLMChain(
    llm=llm,
    prompt=promptTemplate,
    verbose=True,
    memory=summary_memory
)
