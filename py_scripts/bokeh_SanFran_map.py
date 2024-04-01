import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.sampledata.periodic_table import elements
from bokeh.transform import dodge, factor_cmap

from utils.distance_funcs import haversine

SAVE_PATH = "./bokeh/sanFran_map.html"
FILENAME = "../data/Police_Department_Incident_Reports__Historical_2003_to_May_2018_20240130.csv"
crime_df = pd.read_csv(FILENAME)
crime_df = crime_df[crime_df["Date"].str.contains("2018") == False]  # Remove 2018 data

print(crime_df.head())

# Filter the data to the only contain points within in the San Francisco peninsula
df_SF = crime_df[(crime_df["Y"] < 50) & (crime_df["X"] < -122)]

# Find the square that encapsulates San Francisco
lat_min = df_SF["Y"].min()
lat_max = df_SF["Y"].max()
lon_min = df_SF["X"].min()
lon_max = df_SF["X"].max()

# now we know we need to get 130 x 125 bins to get 100m x 100m
ROWS = 130
COLS = 125
count, lon, lat = np.histogram2d(df_SF["Y"], df_SF["X"], bins=[ROWS, COLS])

# Just to convince ourselves that what we have done makes sense we plot the counts.
plt.figure(figsize=(10, 10))
plt.title("Number of crimes per $100m^2$ in San Francisco")
plt.imshow(count, cmap="hot", vmax=3000, origin="lower")
plt.colorbar()
plt.savefig(SAVE_PATH + "crime_heatmap_SanFrancisco.png")
plt.show()
