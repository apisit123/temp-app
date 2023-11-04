# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
import pandas as pd
from streamlit.logger import get_logger

import psycopg2
import datetime
import time


LOGGER = get_logger(__name__)

def convert_df(df):
      return df.to_csv(index=False).encode('utf-8')

def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    st.write("# Welcome to Streamlit! 👋")

    st.sidebar.success("Select a demo above.")

    today = datetime.datetime.now()
    next_year = today.year
    jan_1 = datetime.date(next_year, 1, 1)
    dec_31 = datetime.date(next_year, 12, 31)
    

    noww = datetime.date(today.year, today.month, today.day)
    # st.write(type(jan_1))
    
    
    
    d = st.date_input(
        "Select your vacation for next year",
        (noww, noww),
        jan_1,
        dec_31,
        format="MM.DD.YYYY",
    )
    
    if len(d) == 2:
      unixtime0 = time.mktime(d[0].timetuple())
      unixtime1 = time.mktime(d[1].timetuple())

      # Initialize connection.
      conn = st.connection("postgresql", type="sql")
      df = conn.query(f'SELECT * FROM mobiles WHERE created_at > {unixtime0} AND created_at < {unixtime1};', ttl="10m")
      with st.expander("See explanation Data"):
        st.write(df)
      
      

      df['time_stamp'] = pd.to_datetime(df['created_at'],unit='s')
      df1 = df[['time_stamp', 'temp', 'unit_temp', 'sku', 'area', 'plant']]
      st.write(df1)
      csv = convert_df(df1)


      st.download_button(
        "Press to Download",
        csv,
        "file.csv",
        "text/csv",
        key='download-csv'
      )

if __name__ == "__main__":
    run()
