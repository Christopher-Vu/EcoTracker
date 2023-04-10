from matplotlib import pyplot as plt
import matplotlib as mpl
from io import BytesIO

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
    
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, colors=colors, startangle=90, shadow=True, wedgeprops={'edgecolor': 'black', 'width': 0.3})
    ax1.axis('equal')

    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
    buffer.seek(0)

    return buffer.getvalue()
    
footprint_pie(5, 10, 2, 12, 20)