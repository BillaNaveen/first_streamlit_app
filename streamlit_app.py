import streamlit 
import pandas
import requests
import snowflake.connector
from urllib.error import URLError
streamlit.title('My Parents New Healthy Diner')
streamlit.header(' Break fast menu')
streamlit.text(' 🥣 omega3 & blueberry oatmeal ')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie ')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avacado toast')


streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')



my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
streamlit.dataframe(my_fruit_list)

# Let's put a pick list here so they can pick the fruit they want to include 
streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/kiwi")

# write your own comment -what does the next line do? 
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# write your own comment - what does this do?
streamlit.dataframe(fruityvice_normalized)
def get_fruityvice_data(this_fruit_choice):
       fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
       fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
       return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice!")

try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')

    if not fruit_choice:
       streamlit.error('please select a fruit to get info')
    else:
       back_from_function= get_fruityvice_data(fruit_choice)   
       streamlit.dataframe(back_from_function)
  
  
except URLError as e:
    streamlit.error()

streamlit.write('The user entered ', fruit_choice)


def get_fruit_load_list():
       with  my_cnx.cursor() as my_cur:
           my_cur.execute("SELECT *from fruit_load_list")
           return my_cur.fetchall()
 
if streamlit.button('get fruit load list'):
      my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
      my_data_rows=get_fruit_load_list()
      my_cnx.close()
      streamlit.dataframe(my_data_rows)

def insert_row_snowflake(new_fruit):
       with my_cnx.cursor() as my_cur:
         my_cur.execute("insert into fruit_load_list values ('from streamlit')")
         return"Thanks for entering  your fruit" +new_fruit
add_my_fruit= streamlit.text_input('what friut would you like to add?')
if streamlit.button('add a fruit to the list'):
      my_cnx=snowflake.connector.connect(**streamlit.secrets["snowflake"])
      back_from_function=insert_row_snowflake(add_my_fruit)
      streamlit.text(back_from_function)
