
# coding: utf-8

# In[1]:

from lxml import etree
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.collections import PatchCollection
from mpl_toolkits.basemap import Basemap
from shapely.geometry import Point, Polygon, MultiPoint, MultiPolygon
from shapely.prepared import prep
from pysal.esda.mapclassify import Natural_Breaks as nb
from descartes import PolygonPatch
import fiona
from itertools import chain
import csv
import time
import datetime
from __future__ import division


# In[2]:

reader = csv.DictReader(open('/Users/xiaoxiaowang/CitiBike/one_for_all.csv'))
#reader = csv.DictReader(open('/Users/xiaoxiaowang/CitiBike/sorted_pop_annual_start_am_weekday.csv'))
#reader = csv.DictReader(open('/Users/xiaoxiaowang/CitiBike/sorted_pop_annual_end_am_weekday.csv'))
#reader2 = csv.DictReader(open('/Users/xiaoxiaowang/CitiBike/sorted_pop_customer_start_weekend.csv'))
result = {}
result2= {}
for row in reader:
    #print row['station']
    for column, value in row.items():
        result.setdefault(column, []).append(value)

#for row in reader2:
#    #print row['station']
#    for column, value in row.items():
#        result2.setdefault(column, []).append(value)


# In[3]:

output = dict()
#output2 = dict()

#output['raw'] = result['incl_annual_start_weekday'] #result['station']

output['raw'] = result['incl_annual_start_am_weekday']
#output['raw'] = result['incl_annual_end_am_weekday']

#output['raw'] = result['incl_annual_start_pm_weekday']
#output['raw'] = result['incl_annual_end_pm_weekday']

#output['raw'] = result['incl_annual_start_weekday']
#output['raw'] = result['incl_annual_end_weekday']

#output['raw'] = result['incl_annual_start_weekend']
#output['raw'] = result['incl_annual_end_weekend']

#output['raw'] = result['incl_customer_start_weekday']
#output['raw'] = result['incl_customer_end_weekday']

#output['raw'] = result['incl_customer_start_weekend']
#output['raw'] = result['incl_customer_end_weekend']


output['lon'] = result['longitude']
output['lat'] = result['latitude']
#output2['raw'] = result2['station']
#output2['lon'] = result2['longitude']
#output2['lat'] = result2['latitude']


# In[4]:

df = pd.DataFrame(output)
#df = df.replace({'raw': 0}, None)
df = df.dropna()
df[['raw','lon', 'lat']] = df[['raw','lon', 'lat']].astype(float)
#print df

#df2 = pd.DataFrame(output2)
#df2 = df2.replace({'raw': 0}, None)
#df2 = df2.dropna()
#df2[['lon', 'lat']] = df2[['lon', 'lat']].astype(float)


# In[5]:

shp = fiona.open('ZIP_CODE_040114_NEW/ZIP_CODE_040114.shp')
bds = shp.bounds
shp.close()
extra = 0.01
ll = (bds[0], bds[1])
ur = (bds[2], bds[3])
coords = list(chain(ll, ur))
coords[0] = -74.1000000000
coords[2] = -73.9400000000
coords[1] =  40.6700000000
coords[3] =  40.7900000000
w, h = coords[2] - coords[0], coords[3] - coords[1]
#print bds[0], bds[1]
#print bds[2], bds[3]
#print coords[2], coords[0]
#print coords[3], coords[1]


# In[6]:

m = Basemap(
    projection='tmerc',
    lon_0=-73.9,
    lat_0=40.7,
    ellps = 'WGS84',
    #llcrnrlon=coords[0] - extra * w,
    #llcrnrlat=coords[1] - extra + 0.01 * h,
    #urcrnrlon=coords[2] + extra * w,
    #urcrnrlat=coords[3] + extra + 0.01 * h,
    llcrnrlon=coords[0],
    llcrnrlat=coords[1],
    urcrnrlon=coords[2],
    urcrnrlat=coords[3],
    lat_ts=0,
    resolution='i',
    suppress_ticks=True)
m.readshapefile(
    'ZIP_CODE_040114_NEW/ZIP_CODE_040114',
    'newyork',
    color='none',
    zorder=2)


# In[7]:

# set up a map dataframe
df_map = pd.DataFrame({
    'poly': [Polygon(xy) for xy in m.newyork]})
df_map['area_m'] = df_map['poly'].map(lambda x: x.area)
df_map['area_km'] = df_map['area_m'] / 1000000

#df2_map = pd.DataFrame({
#    'poly': [Polygon(xy) for xy in m.newyork]})
#df2_map['area_m'] = df2_map['poly'].map(lambda x: x.area)
#df2_map['area_km'] = df2_map['area_m'] / 1000000


# Create Point objects in map coordinates from dataframe lon and lat values
map_points = pd.Series(
    [Point(m(mapped_x, mapped_y)) for mapped_x, mapped_y in zip(df['lon'], df['lat'])])

############### Xiaoxiao: changes below are crucial to reconstruct the density map ########################
#print map_points
this_is_the_key = {}
this_is_the_key['geo'] = map_points
this_is_the_key['info'] = df['raw']
important_df = pd.DataFrame(this_is_the_key)
#print important_df

citibike_points = MultiPoint(list(map_points.values))
zips_polygon = prep(MultiPolygon(list(df_map['poly'].values)))
# calculate points that fall within the New York boundary
ldn_points = filter(zips_polygon.contains, citibike_points)

#for geop in important_df['geo']:
#    print geop.x
#print important_df['geo'][0].x
#for geom in ldn_points:
#    print geom.x
#print ldn_points[0]
###########################################################################################################

## Create Point objects in map coordinates from dataframe lon and lat values
#map2_points = pd.Series(
#    [Point(m(mapped_x, mapped_y)) for mapped_x, mapped_y in zip(df2['lon'], df2['lat'])])
#citibike2_points = MultiPoint(list(map2_points.values))
#zips2_polygon = prep(MultiPolygon(list(df2_map['poly'].values)))
## calculate points that fall within the New York boundary
#ldn2_points = filter(zips2_polygon.contains, citibike2_points)


# In[8]:

# Convenience functions for working with colour ramps and bars
def colorbar_index(ncolors, cmap, labels=None, **kwargs):
    """
    This is a convenience function to stop you making off-by-one errors
    Takes a standard colourmap, and discretises it,
    then draws a color bar with correctly aligned labels
    """
    cmap = cmap_discretize(cmap, ncolors)
    mappable = cm.ScalarMappable(cmap=cmap)
    mappable.set_array([])
    mappable.set_clim(-0.5, ncolors+0.5)
    colorbar = plt.colorbar(mappable, **kwargs)
    colorbar.set_ticks(np.linspace(0, ncolors, ncolors))
    colorbar.set_ticklabels(range(ncolors))
    if labels:
        colorbar.set_ticklabels(labels)
    return colorbar

def cmap_discretize(cmap, N):
    """
    Return a discrete colormap from the continuous colormap cmap.

        cmap: colormap instance, eg. cm.jet. 
        N: number of colors.

    Example
        x = resize(arange(100), (5,100))
        djet = cmap_discretize(cm.jet, 5)
        imshow(x, cmap=djet)

    """
    if type(cmap) == str:
        cmap = get_cmap(cmap)
    colors_i = concatenate((linspace(0, 1., N), (0., 0., 0., 0.)))
    colors_rgba = cmap(colors_i)
    indices = linspace(0, 1., N + 1)
    cdict = {}
    for ki, key in enumerate(('red', 'green', 'blue')):
        cdict[key] = [(indices[i], colors_rgba[i - 1, ki], colors_rgba[i, ki]) for i in xrange(N + 1)]
    return matplotlib.colors.LinearSegmentedColormap(cmap.name + "_%d" % N, cdict, 1024)


# In[9]:

# draw ZIP code zones patches from polygons
df_map['patches'] = df_map['poly'].map(lambda x: PolygonPatch(
    x,
    #fc='#555555',
    fc='#003366',
    ec='#787878', lw=.25, alpha=0.95,
    zorder=4))

#df2_map['patches'] = df_map['poly'].map(lambda x: PolygonPatch(
#    x,
#    #fc='#555555',
#    fc='#003366',
#    ec='#787878', lw=.25, alpha=0.95,
#    zorder=4))

plt.clf()
fig = plt.figure()
ax = fig.add_subplot(111, axisbg='w', frame_on=False)
#ax2 = fig.add_subplot(111, axisbg='w', frame_on=False)

# we don't need to pass points to m() because we calculated using map_points and shapefile polygons
dev = m.scatter(
    [geom.x for geom in ldn_points],
    [geom.y for geom in ldn_points],
    40, marker='D', lw=.25,
    #40, marker='*', lw=.25,
    #facecolor='#33ccff', edgecolor='w',
    facecolor='#00ff80', edgecolor='w',
    alpha=0.9, antialiased=True,
    label='Locations', zorder=3)
# plot boroughs by adding the PatchCollection to the axes instance
ax.add_collection(PatchCollection(df_map['patches'].values, match_original=True))

# copyright and source data info
#smallprint = ax.text(
#    1.03, 0,
#    'Total points: %s\n' % len(ldn_points),
#    ha='right', va='bottom',
#    size=4,
#    color='#555555',
#    transform=ax.transAxes)

#dev2 = m.scatter(
#    [geom.x for geom in ldn2_points],
#    [geom.y for geom in ldn2_points],
#    50, marker='v', lw=.25,
#    facecolor='#ff007f', edgecolor='w',
#    #facecolor='#00ff80', edgecolor='w',
#    alpha=0.9, antialiased=True,
#    label='Locations', zorder=3)
## plot boroughs by adding the PatchCollection to the axes instance
#ax2.add_collection(PatchCollection(df2_map['patches'].values, match_original=True))



# Draw a map scale
m.drawmapscale(
    coords[0] + 0.04, coords[1] + 0.010,
    coords[0], coords[1],
    4.,
    barstyle='fancy', labelstyle='simple',
    fillcolor1='w', fillcolor2='#555555',
    fontcolor='#555555',
    #fontcolor='#000000',
    zorder=5)
plt.title("Map of New York City - Manhattan and Brooklyn Neighborhoods")
plt.tight_layout()
# this will set the image width to 722px at 100dpi
#fig.set_size_inches(7.22, 5.25)
fig.set_size_inches(7.22, 7.25)
plt.savefig('newyork_try.png', dpi=100, alpha=True)
plt.show()


# In[10]:

############### Xiaoxiao: changes below are crucial to reconstruct the density map ########################

important_sr = df_map['poly'].map(lambda x: filter(prep(x).contains, ldn_points))
tot_new_l = []
for l in important_sr:
     #print l
     new_l = []
     for e in l:
        #print e.x, e.y
        for i in range(len(important_df['geo'])):
            if important_df['geo'][i].x==e.x and important_df['geo'][i].y==e.y:
                new_l.append(important_df['info'][i])
     tot_new_l.append(sum(new_l)) #sum all weights
result_sr= pd.Series(tot_new_l) 
#print result_sr
###########################################################################################################


#df_map['count'] = df_map['poly'].map(lambda x: int(len(filter(prep(x).contains, ldn_points))))
#df_map['density_m'] = df_map['count'] / df_map['area_m']
#df_map['density_km'] = df_map['count'] / df_map['area_km']

df_map['count'] = result_sr
df_map['density_m'] = df_map['count'] / df_map['area_m']
df_map['density_km'] = df_map['count'] / df_map['area_km']
    
# it's easier to work with NaN values when classifying
df_map.replace(to_replace={'density_m': {0: np.nan}, 'density_km': {0: np.nan}}, inplace=True)


# In[11]:

# Calculate Jenks natural breaks for density
breaks = nb(
    df_map[df_map['density_km'].notnull()].density_km.values,
    #initial=0,
    #k=5)
    initial=0,
    k=6)
# the notnull method lets us match indices when joining
jb = pd.DataFrame({'jenks_bins': breaks.yb}, index=df_map[df_map['density_km'].notnull()].index)
df_map = df_map.join(jb)
df_map.jenks_bins.fillna(-1, inplace=True)


# In[12]:

jenks_labels = ["<= %0.1f trips/hour/km$^2$(%s ZIP code zones)" % (b, c) for b, c in zip(
    breaks.bins, breaks.counts)]
jenks_labels.insert(0, 'No trips (%s ZIP code zones)' % len(df_map[df_map['density_km'].isnull()]))


# In[13]:

plt.clf()
fig = plt.figure()
ax = fig.add_subplot(111, axisbg='w', frame_on=True)

# use a blue colour ramp - we'll be converting it to a map using cmap()
#cmap = plt.get_cmap('Blues')
cmap = plt.get_cmap('Greens')
# draw ZIP code zones with grey outlines
df_map['patches'] = df_map['poly'].map(lambda x: PolygonPatch(x, ec='#000000', lw=.4, alpha=1., zorder=4))
pc = PatchCollection(df_map['patches'], match_original=True)
# impose our colour map onto the patch collection
norm = Normalize()
pc.set_facecolor(cmap(norm(df_map['jenks_bins'].values)))
ax.add_collection(pc)

# Add a colour bar
cb = colorbar_index(ncolors=len(jenks_labels), cmap=cmap, shrink=0.3, labels=jenks_labels)
cb.ax.tick_params(labelsize=8)

# Show highest densities, in descending order
###########highest = '\n'.join(
###########    value[1] for _, value in df_map[(df_map['jenks_bins'] == 4)][:10].sort().iterrows())
highest = ' '
highest = 'Most Dense ZIP Code Zones:\n\n' + highest
# Subtraction is necessary for precise y coordinate alignment
#details = cb.ax.text(
#    0, -0.25, #0 - 0.007,
#    highest,
#    ha='right', va='bottom',
#    size=5,
#    color='#555555')

# Bin method, copyright and source data info
#smallprint = ax.text(
#    1.03, 0,
#    #'Classification method: natural breaks\nContains Ordnance Survey data\n$\copyright$ Crown copyright and database right 2013\nPlaque data from http://openplaques.org',
#    'New York',
#    ha='right', va='bottom',
#    size=4,
#    color='#555555',
#    transform=ax.transAxes)

# Draw a map scale
m.drawmapscale(
    coords[0] + 0.04, coords[1] + 0.010,
    coords[0], coords[1],
    4.,
    barstyle='fancy', labelstyle='simple',
    fillcolor1='w', fillcolor2='#000000',
    fontcolor='#000000',
    zorder=5)
# this will set the image width to 722px at 100dpi
plt.title("Map of New York City - Manhattan and Brooklyn Neighborhoods")
plt.tight_layout()
fig.set_size_inches(8, 7)

plt.savefig('incl_annual_start_am_weekday.pdf', dpi=100, alpha=True)
#plt.savefig('incl_annual_end_am_weekday.pdf', dpi=100, alpha=True)

#plt.savefig('incl_annual_start_pm_weekday.pdf', dpi=100, alpha=True)
#plt.savefig('incl_annual_end_pm_weekday.pdf', dpi=100, alpha=True)

#plt.savefig('incl_annual_start_weekday.pdf', dpi=100, alpha=True)
#plt.savefig('incl_annual_end_weekday.pdf', dpi=100, alpha=True)

#plt.savefig('incl_annual_start_weekend.pdf', dpi=100, alpha=True)
#plt.savefig('incl_annual_end_weekend.pdf', dpi=100, alpha=True)
            
#plt.savefig('incl_customer_start_weekday.pdf', dpi=100, alpha=True)
#plt.savefig('incl_customer_end_weekday.pdf', dpi=100, alpha=True)

#plt.savefig('incl_customer_start_weekend.pdf', dpi=100, alpha=True)
#plt.savefig('incl_customer_end_weekend.pdf', dpi=100, alpha=True)

plt.show()


# In[157]:




# In[ ]:



