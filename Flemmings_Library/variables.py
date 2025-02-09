import langchain
import langchain_community

from langchain_community.utilities import SQLDatabase

#   db_path = r"./POC-LangChain/chinook-database-master/ChinookDatabase/DataSources/Chinook_Sqlite.sqlite"
db_path = r"./chinook-database-master/ChinookDatabase/DataSources/Chinook_Sqlite.sqlite"
db = SQLDatabase.from_uri(f"sqlite:///{db_path}")
db_dialect = db.dialect


from langchain import PromptTemplate

prompt_template_sql = PromptTemplate(
    input_variables=["schema_info", "question", "db_dialect"],
    template="""
You are a helpful SQL assistant that provides only SELECT-Statements.
Based on the following database schema, translate a natural language query into an SQL query that is executable in my {db_dialect}-Database.
Make sure to end your SQL query with a semicolon ';'.

Database Schema:
{schema_info}

Using the schema information above, please formulate the appropriate SQL query this question:
Question: {question}

SQL Query:
""".strip()
)

import langchain.prompts

from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

chat_prompt_template_sql = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        "You are a helpful SQL assistant that provides only SELECT-Statements. "
        "Based on the following database schema, translate a natural language query "
        "into an SQL query that is executable in my {db_dialect}-Database.\n\n"
        "Database Schema:\n{schema_info}"
    ),
    HumanMessagePromptTemplate.from_template(
        "Using strictly the schema information above, please formulate the appropriate SQL query for the following question:\n"
        "Question: {question}\n\nSQL Query:"
    )
])


prompt_sql_fix_template = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        "You are a helpful SQL assistant and you will help me to fix my SQL query for my {db_dialect}-Database. I will show you the database schema, the question and the error that I got.\n"
        "Please only answer based on the provided information.\n"
    ),
    HumanMessagePromptTemplate.from_template(
        "User Question: {question}\n"
        "SQL Query: {query}\n"
        "Error: {error}\n"
        "Database-Schema: {schema_info}\n"
    )
])

answer_prompt_template = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        "You are a helpful SQL assistant. Based on the SQL query and its execution result, provide a concise final answer to the user's question."
    ),
    HumanMessagePromptTemplate.from_template(
        "User Question: {question}\n"
        "SQL Query: {query}\n"
        "Execution Result: {execution_result}\n\nPlease provide your final answer:"
    )
])

