import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as plticker

# df = pd.DataFrame([[5.1, 3.5, 0], [4.9, 3.0, 0], [7.0, 3.2, 1],[6.4, 3.2, 1], [5.9, 3.0, 2]],columns=['length', 'width', 'species'])



data = [
     {"target":{"ingestion_time":"2021-11-12T15:29:44.800Z","icao_address":"4A09AD","timestamp":"2021-11-12T15:29:41Z","latitude":44.655899,"longitude":20.361328,"altitude_baro":40000,"heading":230.0,"speed":418.4,"vertical_rate":-30,"squawk":"7355","on_ground":False,"callsign":"BLA2915","collection_type":"terrestrial"}},
 {"target":{"ingestion_time":"2021-11-12T15:29:44.777Z","icao_address":"3C656F","timestamp":"2021-11-12T15:29:41Z","latitude":43.303543,"longitude":19.643555,"altitude_baro":38000,"heading":300.0,"speed":475.0,"vertical_rate":0,"squawk":"7213","on_ground":False,"callsign":"DLH705","collection_type":"terrestrial"}}
]

df = pd.DataFrame([d["target"] for d in data])

a4_dims = (11, 8)

fig, ax = plt.subplots()
# df.plot(kind='scatter', ax=ax, x='latitude', y='longitude')
fig.set_size_inches(*a4_dims)


# ax1 = df.plot.scatter(x='latitude', y='longitude', hue='icao_address')
ax = sns.scatterplot(x='latitude', y='longitude', data=df, hue='icao_address')

def get_axis_interval(resolution = 0.1):
    return plticker.MultipleLocator(base=resolution) # this locator puts ticks at regular intervals


ax.xaxis.set_major_locator(get_axis_interval())
ax.yaxis.set_major_locator(get_axis_interval())

# plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

plt.show()
