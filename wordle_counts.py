import string
from pathlib import Path
import pandas as pd

#--------------------------------------------------------------------------------------------
# Variables
#--------------------------------------------------------------------------------------------
letters = list(string.ascii_uppercase) #because assumption is that answers are in all caps
vowels = ['A', 'E', 'I', 'O', 'U']

directory = directory = Path(__file__).parent / 'data'
partial_file_name = ('*.txt')

month_names = ['January','February','March','April','May','June','July','August','September','October','November','December']
#--------------------------------------------------------------------------------------------
# Functions
#--------------------------------------------------------------------------------------------
def find_latest_file(dir, partial_file_name):
    files = [f for f in dir.iterdir() if f.is_file()]
    if files:
    # Get the file with the maximum modification time
        latest_file = max(files, key=lambda f: f.stat().st_mtime)
    return latest_file

def get_letter_counts(answers):
    letter_position_counts = [[0 for i in range(0,5)] for letter in letters]
    for word in answers:
        for i, letter in enumerate(word):
            letter_position_counts[letters.index(letter)][i] += 1
    return letter_position_counts

def get_puzzle_num(df, date_str):
    s = date_str.split('-')
    print(s)
    year_val = int(s[0])
    date_val = int(s[2])
    month_val = month_names[int(s[1]) - 1]
    num = df.loc[(df['Year'] == year_val) & (df['Month'] == month_val) & (df['Date'] == date_val), 'Puzzle_Number'].values[0]
    return num

def get_answers_between_dates(df, start_date, end_date):
    num1 = get_puzzle_num(df, start_date)
    num2 = get_puzzle_num(df, end_date)
    custom_df = df.loc[(df['Puzzle_Number'] >= num1) & (df['Puzzle_Number'] <= num2), 'Answer']
    custom_answers = custom_df.tolist()
    return custom_answers


#--------------------------------------------------------------------------------------------
# Actions / calls to functions
#--------------------------------------------------------------------------------------------
text_file_name = find_latest_file(directory, partial_file_name)
df= pd.read_csv(text_file_name)
result_df = df.query('Year == 2026')
answers = result_df['Answer'].tolist()
last_date = str(df['Year'].iloc[-1]) + '-' + str(df['Month'].iloc[-1]) + '-' + str(df['Date'].iloc[-1])
month_name_num = month_names.index(df['Month'].iloc[-1]) + 1
last_date_val = str(df['Year'].iloc[-1]) + '-' + str(month_name_num) + '-' + str(df['Date'].iloc[-1])
