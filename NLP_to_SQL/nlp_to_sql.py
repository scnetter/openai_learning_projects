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

