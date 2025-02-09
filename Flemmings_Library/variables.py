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

Database Schema:
{schema_info}

Using the schema information above, please formulate the appropriate SQL query this question:
Question: {question}

SQL Query:
""".strip()
)

