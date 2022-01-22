#scraping modules
from urllib.request import urlopen
from bs4 import BeautifulSoup

#data manipulation modules
import pandas as pd
import numpy as np

#data visualization modules
import matplotlib as mpl
import matplotlib.pyplot as plt

#set target url
url = 'https://www.pro-football-reference.com/years/2020/rushing.htm'

#open url, this is the reason for urllib
html = urlopen(url)
stats_page = BeautifulSoup(html, 'lxml')

column_headers = stats_page.findAll('tr')[1]
column_headers = [i.getText() for i in
                  column_headers.findAll('th')]

#grabbing data rows is 2 because rb has extra before
rows = stats_page.findAll('tr')[2:] #!

#get stats from each row
rb_stats = []
for i in range(len(rows)):
    rb_stats.append([col.getText() for col in rows[i].findAll('td')]) #?

#create dataframe from scraped data
data = pd.DataFrame(rb_stats, columns=column_headers[1:])
categories = ['Att', 'GS', 'Yds', 'TD', 'Y/A']

#test
new_columns = data.columns.values
data.columns = new_columns
print(data.columns)
#https://www.youtube.com/watch?v=dcqPhpY7tWk 3:20
#choose visualization stats



data = data.drop(['Pos','Age', 'G', 'Fmb', '1D', 'Y/G', 'Lng'], axis = 1)


for i in categories:
  data[i] = pd.to_numeric(data[i])

data = data[data['GS'] > 7]
data = data[data['Yds'] > 1000]
 
for i in categories:
  data[i + '_Rank'] = data[i].rank(pct=True)
  
data['GS_Rank'] = data['GS'] / 16

mpl.rcParams['font.size'] = 16
mpl.rcParams['axes.linewidth'] = 0
mpl.rcParams['xtick.major.pad'] = 15

team_colors = {'ARI':'#97233f', 'ATL':'#a71930', 'BAL':'#241773', 'BUF':'#00338d', 'CAR':'#0085ca', 'CHI':'#0b162a', 'CIN':'#fb4f14', 'CLE':'#311d00', 'DAL':'#041e42', 'DEN':'#002244', 'DET':'#0076b6', 'GNB':'#203731', 'HOU':'#03202f', 'IND':'#002c5f', 'JAX':'#006778', 'KAN':'#e31837', 'LAC':'#002a5e', 'LAR':'#003594', 'MIA':'#008e97', 'MIN':'#4f2683', 'NWE':'#002244', 'NOR':'#d3bc8d', 'NYG':'#0b2265', 'NYJ':'#125740', 'LVR':'#000000', 'PHI':'#004c54', 'PIT':'#ffb612', 'SFO':'#aa0000', 'SEA':'#002244', 'TAM':'#d50a0a', 'TEN':'#0c2340', 'WAS':'#773141'}

def create_radar_chart(ax, angles, player_data, color='blue'):
  ax.plot(angles, np.append(player_data[-(len(angles)-1):], player_data[-(len(angles)-1)]), color=color, linewidth=2)
  ax.fill(angles, np.append(player_data[-(len(angles)-1):], player_data[-(len(angles)-1)]), color=color, alpha=0.2)
  ax.set_xticks(angles[:-1])
  ax.set_xticklabels(categories)
  ax.set_yticklabels([])
  ax.text(np.pi/2, 1.7, player_data[0], ha='center', va='center', size=18, color=color)
  ax.set(xlim=(0, 2*np.pi), ylim=(0, 1))

  return ax
  
def get_rb_data(data, team):
  return np.asarray(data[data['Tm'] == team])[0]
  
#Not sure
offset = np.pi/6
angles = np.linspace(0, 2*np.pi, len(categories) + 1) + offset

# Create figure
fig = plt.figure(figsize=(8, 8), facecolor='white')

# Add subplots
ax1 = fig.add_subplot(221, projection='polar', facecolor='#ededed')
ax2 = fig.add_subplot(222, projection='polar', facecolor='#ededed')
ax3 = fig.add_subplot(223, projection='polar', facecolor='#ededed')
ax4 = fig.add_subplot(224, projection='polar', facecolor='#ededed')

# Adjust space between subplots
plt.subplots_adjust(hspace=0.8, wspace=0.5)

# Get rb data
ind_data = get_rb_data(data, 'IND')
cle_data = get_rb_data(data, 'CLE')
ten_data = get_rb_data(data, 'TEN')
min_data = get_rb_data(data, 'MIN')

# Plot rb data
ax1 = create_radar_chart(ax1, angles, ind_data, team_colors['IND'])
ax2 = create_radar_chart(ax2, angles, cle_data, team_colors['CLE'])
ax3 = create_radar_chart(ax3, angles, ten_data, team_colors['TEN'])
ax4 = create_radar_chart(ax4, angles, min_data, team_colors['MIN'])

#create CSV file to manually check data
data.to_csv('rushing_t.csv', encoding='utf-8', index=False)

plt.show()
