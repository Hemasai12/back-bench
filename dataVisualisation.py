import pandas as pd
import numpy as np
import csv
from datetime import datetime
import matplotlib.pyplot as plt
% matplotlib inline

tmdb_data=pd.read_csv('tmdb-movies.csv')
print(type(tmdb_data))
x=tmdb_data.shape
print(x)
tmdb_data.head(3)

#creating a list of columns to be deleted 
del_col=['id', 'imdb_id', 'popularity', 'budget_adj', 'revenue_adj', 'homepage', 'keywords', 'overview', 'production_companies', 'vote_count', 'vote_average']

#deleting the colums
tmdb_data=tmdb_data.drop(del_col,1)#1 is for column and 0 is for row

#previewing the new dataset
tmdb_data.head(3)

tmdb_data.drop_duplicates(keep='first', inplace=True)
x =tmdb_data.shape
print(x)
#printing the wous
tmdb_data.head(10)

#creating a seperate list of revenue and dudget column
temp_list=['budget', 'revenue', 'runtime']
temp_list1=['budget', 'revenue']

#this will replace all the value from '0' to NAN in the temp_list
tmdb_data[temp_list] = tmdb_data[temp_list].replace(0, np.NAN)

#removing all the row which has NaN value in the temp_list1
tmdb_data.dropna(subset =temp_list1, inplace=True)
tmdb_data.head()

tmdb_data.release_date=pd.to_datetime(tmdb_data['release_date'])
#priting  
tmdb_data.head(3)

print(type(tmdb_data.budget[0]))
change_type=['budget', 'revenue']
#changing data type
tmdb_data[change_type]=tmdb_data[change_type].applymap(np.int64)
#pinting  te changed indo
tmdb_data.dtypes

#inserting func
tmdb_data.insert(2, 'profit_earned', tmdb_data['revenue']-tmdb_data['budget'])

def finding(column):
    #for highest earned profit
    high=tmdb_data[column].idxmax()
    high_details=pd.DataFrame(tmdb_data.loc[high])
    
    #for lowest earned profit
    low=tmdb_data[column].idxmin()
    low_details=pd.DataFrame(tmdb_data.loc[low])
        
    #collection data in one place
    info=pd.concat([high_details, low_details], axis=1)
    return info
finding('profit_earned')
#finding the highest and lowest budget 
finding('budget')

top = tmdb_data['budget'].sort_values(ascending=False).head(10)
bottom = tmdb_data['budget'].sort_values(ascending=False).tail(10)
pdf = pd.DataFrame(top)
ax=pdf.plot.bar()
ax.set_xlabel("amount")
ax.set_ylabel("frequency")
ax.set_title("graph of top 10 budget")
pdf = pd.DataFrame(bottom)
ax=pdf.plot.bar()
ax.set_xlabel("amount")
ax.set_ylabel("frequency")
ax.set_title("graph of bottom 10 budget")

profits_year = tmdb_data.groupby('release_year')['profit_earned'].sum()
#To find that which year made the highest profit?
print(profits_year.head(5))
profits_year.idxmax()

#selecting the movies having profit
profit_data=tmdb_data[tmdb_data['profit_earned'] >= 60000000]

#reindexing new data
profit_data.index = range(len(profit_data))
#we will start from 1 instead 0
profit_data.index = profit_data.index+1

#printing the changed database
profit_data.head(3)

#function which will take any coulmn as argument from and keep its track
def data(column):
    #will take the column, and separate the string by '|'
    data=profit_data[column].str.cat(sep='|')
    #print(data)
    #giving pandas seroies and storing the values separately
    data=pd.Series(data.split('|'))
    #print (data)
    #arranging in decending order
    count=data.value_counts(ascending=False)
    print(count.head(3))
    return count
#variable to store the retrured value
count=data("genres")
#printing
count.head()

#
df= pd.DataFrame(count)

ax=df.plot(kind='pie', subplots=True, figsize=(20,20), title="pie plot on genres", fontsize=15)

#variable to store 
count = data('cast')
#priting top 5 values
count.head()

dta = count.head(10)

dta.sort_values(ascending = True, inplace = True)

#plotig 
lt= dta.plot.barh(color = '#00FF00', fontsize =13)

#title
lt.set(title = 'Frequent Used cast in profitabel movies')

# on x axis 
lt.set_xlabel('NOs od movies in the dataset', color='black', fontsize='13')
lt.set_xlabel('Cast', color='black', fontsize='13')
#figure size(width, height)
lt.figure.set_size_inches(12,6)
#ploting the graph
plt.show()
