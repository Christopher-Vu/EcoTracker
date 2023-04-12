from matplotlib import pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np
from io import BytesIO
import mplfinance as mpf

# Example dataframe for testing
# date, period, footprint, tpy, comparison, comparison_context, avg_footprint, goods, food, energy, water, transport
example_data = pd.DataFrame({
    'date': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05'],
    'period': ['30', '30', '30', '30', '30'],
    'footprint': [25, 30, 20, 35, 40],
    'tpy': [25, 30, 20, 35, 30],
    'comparison': ['e', 'e', 'e', 'e', 'e'],
    'comparison_context': ['e', 'e', 'e', 'e', 'e'],
    'avg_footprint': [30, 30, 30, 20, 20],
    'goods': [10, 20, 10, 15, 20],
    'food': [5, 5, 5, 10, 10],
    'energy': [5, 5, 5, 5, 5],
    'water': [2, 2, 2, 2, 2],
    'transport': [3, 3, 3, 3, 3]
})

mpl.rcParams['font.family'] = 'Hepta Slab'
mpl.rcParams['font.size'] = 12.0

#Color Pallete
#ECECEC: grey
#BDB76B: yellowish
#1E90FF: blue
#708090: grey blue
#2E8B57: grey green
#00CED1: light blue
#556B2F: muddy green
#87CEFA: light blue
#D2B48C: tan

def footprint_pie(goods, food, water, energy, transport):
    labels = ['Goods', 'Food', 'Water', 'Energy', 'Transport']
    sizes = [goods, food, water, energy, transport]
    colors = ['#BDB76B', '#D2B48C', '#00CED1', '#2E8B57', '#708090']
    
    # Make pie chart
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=colors, startangle=90, shadow=True, wedgeprops={'edgecolor': 'black', 'width': 0.3})
    ax.axis('equal')

    # Convert to bytecode
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
    buffer.seek(0)

    return buffer.getvalue()
    
def footprint_vs_average(data):
    data['date'] = pd.to_datetime(data['date'])
    data.set_index('date', inplace=True)

    fig, ax = plt.subplots()
    ax.plot(data['avg_footprint'], color="white", linewidth="2")
    ax.plot(data['tpy'], color='black', label='Footprint', markersize=5, marker="o")

    # Red/Green above/below average
    ax.fill_between(data.index, data['avg_footprint'], color='green', alpha=.1)
    ax.fill_between(data.index, data['avg_footprint'], ax.get_ylim()[1], color='red', alpha=.1)

    # Labels
    ax.set_xlabel('Date')
    ax.set_xticklabels(data.index.strftime('%Y-%m-%d'), rotation=45, ha='right')
    ax.set_ylabel('Carbon Footprint (tons of CO2 per year)')
    ax.set_ylim(bottom=0)
    ax.legend()

    # Convert to bytecode
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
    buffer.seek(0)

    return buffer.getValue()


def stacked_footprint(data):
    data['date'] = pd.to_datetime(data['date'])
    data.set_index('date', inplace=True)


    colors = ['#BDB76B', '#D2B48C', '#00CED1', '#2E8B57', '#708090']
    multipliers = data.apply(find_multiplier, axis=1).tolist() # multiplier list
    y1, y2, y3, y4, y5 = data['goods'].tolist(), data['food'].tolist(), data['water'].tolist(), data['energy'].tolist(), data['transport'].tolist()
    counts = [0, 1, 2, 3, 4] # stop judging I know it's suboptimal

    for lst in [y1, y2, y3, y4, y5]:
        for val, multiplier, count in zip(lst, multipliers, counts):
            lst[count] = val * multiplier
    
    fig, ax = plt.subplots()
    ax.bar(data.index, y1, color=colors[0], label="goods")
    ax.bar(data.index, y2, bottom=y1, color=colors[1], label="food")
    ax.bar(data.index, y3, bottom=y1+y2, color=colors[2], label="water")
    ax.bar(data.index, y4, bottom=y1+y2+y3, color=colors[3], label="energy")
    ax.bar(data.index, y5, bottom=y1+y2+y3+y4, color=colors[4], label="transport")

    ax.legend(fontsize=10, loc="upper left")
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
    buffer.seek(0)

    return buffer.getValue()

def line_by_category(data):
    data['date'] = pd.to_datetime(data['date'])
    data.set_index('date', inplace=True)

    colors = ['#BDB76B', '#D2B48C', '#00CED1', '#2E8B57', '#708090']
    multipliers = data.apply(find_multiplier, axis=1).tolist() # multiplier list
    lines = [data['goods'], data['food'], data['water'], data['energy'], data['transport']]
    labels = ['goods', 'food', 'water', 'energy', 'transport']
    counts = [0, 1, 2, 3, 4] # stop judging I know it's suboptimal

    for lst in lines:
        for val, multiplier, count in zip(lst, multipliers, counts):
            lst[count] = val * multiplier

    
    fig, ax = plt.subplots()
    for line, color, label in zip(lines, colors, labels):
        ax.plot(line, color=color, label=label, markersize=5, marker="o")
        ax.fill_between(data.index, line, color=color, alpha=.2)

    ax.set_xlabel('Date')
    ax.set_xticklabels(data.index.strftime('%Y-%m-%d'), rotation=45, ha='right')
    ax.set_ylabel('Carbon Footprint (tons of CO2 per year)')
    ax.set_ylim(bottom=0)
    ax.legend(loc="upper left")

    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
    buffer.seek(0)

    return buffer.getValue()

# Standardizes footprints by multipling it by tpy/footprint
def find_multiplier(row):
    return row['tpy'] / row['footprint']
