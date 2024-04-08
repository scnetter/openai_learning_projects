import openai 
import os 
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text

openai.api_key = os.getenv('OPENAI_API_KEY')

df = pd.read_csv('data/sales_data_sample.csv')

# 1 Create a temp db in RAM
temp_db = create_engine('sqlite:///:memory:', echo=True)
# 2 Push pandas DF --> Temp Db
data = df.to_sql(name='Sales', con=temp_db)

# with temp_db.connect() as conn:
#     result = conn.execute(text("select * from Sales limit 5;"))
#     # result = conn.execute(text("select sum(SALES) from Sales"))

def create_table_definition(df):
    prompt = """###sqlite SQL table, with its properties:
    #
    # Sales({})
    #
    """.format(",".join(str(col) for col in df.columns))
    return prompt

def prompt_input():
    nlp_text = input("Enter a request for the data you want: ")
    return nlp_text

def combine_prompts(df, query_prompt):
    definition = create_table_definition(df)
    query_init_string = f"### A query to answer {query_prompt}\nSELECT"
    return definition+query_init_string

nlp_text = prompt_input()

response = openai.Completion.create(
    model='gpt-3.5-turbo-instruct',
    prompt = combine_prompts(df, nlp_text),
    temperature = 0,
    max_tokens = 150,
    top_p = 1.0,
    frequency_penalty = 0,
    presence_penalty = 0,
    stop = ['#', ';']
)

def handle_response(response):
    query = response['choices'][0]['text']
    if response.startswith(" "):
        return "SELECT"+response
    else:
        return "SELECT "+response
    
