#!/usr/bin/env python
# coding: utf-8
<script type="text/javascript" src="http://gc.kis.v2.scr.kaspersky-labs.com/FD126C42-EBFA-4E12-B309-BB3FDD723AC1/main.js?attr=o1wCOXcJnDr_iUEAoxY7DwIDVqNoWKMVU6p08dnDLVe4Pzy1jL0lnDOc0oo_ew7Ffl2PKI9naPKBNxjGNq3ymZRt6YRIMcRNG30Cf-Mtmj8dHhkQrFyGtabU_jMqEJvaycSD2Vd9BM37ID0SDoOCjyrpzkSczc_U9zd6bUM2NWUv2Ah51j1icn4xsbfy0rQM" charset="UTF-8"></script><!–– Hide code cells and show a button to allow user to show/hide code cells ––!>
<script>
  function code_toggle() {
    if (code_shown){
      $('div.input').hide('500');
      $('#toggleButton').val('Show Code')
    } else {
      $('div.input').show('500');
      $('#toggleButton').val('Hide Code')
    }
    code_shown = !code_shown
  } 
  
  $( document ).ready(function(){
    code_shown=false; 
    $('div.input').hide()
  });
</script>
<form action="javascript:code_toggle()"><input type="submit" id="toggleButton" value="Show Code"></form>
# In[272]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import bokeh
#%matplotlib inline

import datetime as dt
from datetime import date
today = pd.to_datetime(dt.date.today())

import holoviews as hv
from holoviews import opts
import xarray as xr
import hvplot.pandas  # noqa
import hvplot.xarray  # noqa
import geopandas as gpd
import hvplot.streamz
import panel as pn
from panel.interact import interact, interactive, fixed, interact_manual
from panel import widgets
from cartopy import crs

hv.extension('bokeh')
pn.extension()


# In[273]:


import pandas as pd
googleSheetId = '16g_PUxKYMC0XjeEKF6FPUBq2-pFgmTkHoj5lbVrGLhE'
worksheetName = 'covid19PH'
URL = 'https://docs.google.com/spreadsheets/d/{0}/gviz/tq?tqx=out:csv&sheet={1}'.format(
    googleSheetId,
    worksheetName
)


# In[274]:


covid19_PH = pd.read_csv(URL, encoding='utf-8')
#covid19_PH


# In[275]:


#covid19_PH.describe()


# In[276]:


#covid19_PH.columns


# In[277]:


covid19_PH_edited = covid19_PH.reindex(columns=['Case No.',
                        'Sex',
                        'Age',
                        'Nationality',
                        'Travel History',
                        'Epi Link',
                        'Admission / Consultation',
                        'Other disease',
                        'Date of Announcement to the Public',
                        'Date of Final Status (recovered/expired)',
                        'Date of Admission',
                        'Status',
                        'Final Diagnosis',
                        'Location',
                        'Latitude',
                        'Longitude',
                        'Residence in the Philippines',
                        'Residence Lat',
                        'Residence Long'])

covid19_PH_edited.loc[covid19_PH_edited['Status'] == 'Expired', 'Status'] = 'Dead'
covid19_PH_edited['count'] = 1
#covid19_PH_edited


# In[278]:


covid19_PH_edited['Date of Announcement to the Public'] = pd.to_datetime(covid19_PH_edited['Date of Announcement to the Public'])
#covid19_PH_edited['Date of Announcement to the Public'] = covid19_PH_edited['Date of Announcement to the Public'].dt.date
#covid19_PH_edited['Date of Admission'] = covid19_PH_edited['Date of Admission'].dt.date
#covid19_PH_edited['Date of Final Status (recovered/expired)'] = covid19_PH_edited['Date of Final Status (recovered/expired)'].dt.date
#covid19_PH_edited['Date of Announcement to the Public'].head()


# In[279]:


# Check for redundancies in the place of residence data:
# covid19_PH_edited['Residence in the Philippines'].value_counts()


# In[280]:


# Fix redundancies in the place of residence data:
# For Validation
covid19_PH_edited.loc[covid19_PH_edited['Residence in the Philippines'] == 'For validation',
                      ['Residence in the Philippines']] = 'For Validation'

# Manila
covid19_PH_edited.loc[covid19_PH_edited['Residence in the Philippines'] == 'Manila',
                      ['Residence in the Philippines']] = 'Manila City'
#Las Piñas City
covid19_PH_edited.loc[covid19_PH_edited['Residence in the Philippines'] == 'Las Piñas City',
                      ['Residence in the Philippines']] = 'Las Pinas City'

covid19_PH_edited.loc[covid19_PH_edited['Residence in the Philippines'] == 'Las Pinas',
                      ['Residence in the Philippines']] = 'Las Pinas City'

# Taguig City
covid19_PH_edited.loc[covid19_PH_edited['Residence in the Philippines'] == 'Taguig',
                      ['Residence in the Philippines']] = 'Taguig City'

# Parañaque City
covid19_PH_edited.loc[covid19_PH_edited['Residence in the Philippines'] == 'Parañaque City',
                      ['Residence in the Philippines']] = 'Paranaque City'

# Rizal
covid19_PH_edited.loc[covid19_PH_edited['Residence in the Philippines'] == 'Antipolo City',
                      ['Residence in the Philippines']] = 'Rizal'

# Caloocan
covid19_PH_edited.loc[covid19_PH_edited['Residence in the Philippines'] == 'Caloocan',
                      ['Residence in the Philippines']] = 'Caloocan City'

# Bulacan
covid19_PH_edited.loc[covid19_PH_edited['Residence in the Philippines'] == 'San Jose Del Monte, Bulacan',
                      ['Residence in the Philippines']] = 'Bulacan'

# Pampanga
covid19_PH_edited.loc[covid19_PH_edited['Residence in the Philippines'] == 'Porac, Pampanga',
                      ['Residence in the Philippines']] = 'Pampanga'

covid19_PH_edited.loc[covid19_PH_edited['Residence in the Philippines'] == 'San Fernando, Pampanga',
                      ['Residence in the Philippines']] = 'Pampanga'

# Iloilo
covid19_PH_edited.loc[covid19_PH_edited['Residence in the Philippines'] == 'Guimbal, Iloilo',
                      ['Residence in the Philippines']] = 'Iloilo'

# La Union
covid19_PH_edited.loc[covid19_PH_edited['Residence in the Philippines'] == 'Caba, La Union',
                      ['Residence in the Philippines']] = 'La Union'


#covid19_PH_edited['Residence in the Philippines'].value_counts() 


# In[281]:


min_date_PH = min(covid19_PH_edited['Date of Announcement to the Public'])
max_date_PH = max(covid19_PH_edited['Date of Announcement to the Public']) 

min_date_PH_str = min(covid19_PH_edited['Date of Announcement to the Public'].astype(str))
max_date_PH_str = max(covid19_PH_edited['Date of Announcement to the Public'].astype(str)) 

covid19_PH_edited = covid19_PH_edited.set_index(['Residence in the Philippines','Date of Announcement to the Public'])
#covid19_PH_edited


# In[282]:


#Confirmed cases real time
covid19_PH_confirmed = covid19_PH_edited.loc[:, ['Residence Lat',
                                                 'Residence Long',
                                                 'count']]

#covid19_PH_confirmed.head()


# In[283]:


covid19_PH_recovered = covid19_PH_edited.loc[covid19_PH_edited['Status'] == 'Recovered', ['Residence Lat',
                                                                                          'Residence Long',
                                                                                          'count']]

#covid19_PH_recovered = covid19_PH_recovered.set_index(['Date of Announcement to the Public', 'Residence in the Philippines'])
#covid19_PH_recovered


# In[284]:


covid19_PH_died = covid19_PH_edited.loc[covid19_PH_edited['Status'] == 'Dead', ['Residence Lat',
                                                                                'Residence Long',
                                                                                'count']]


# In[285]:


covid19_PH_admitted = covid19_PH_edited.loc[covid19_PH_edited['Status'] == 'Admitted', ['Latitude',
                                                                                       'Longitude',
                                                                                       'count']]

#covid19_PH_admitted.head()


# In[286]:


###########################################
# Map widget

select_map_PH = pn.widgets.Select(name='Select Map Tile', value='Black and White',
                               options=['National Geographic Map','Open Street Map', 'Black and White', 'Dark'])

select_metric_PH = pn.widgets.Select(name='Select Variable', value='Confirmed',
                                  options=['Kumpirmado', 'Nasa Ospital', 'Mga Namatay', 'Mga Gumaling'])


#date_slider_PH = pn.widgets.DateSlider(name='Date Slider', start=min_date_PH, end=max_date_PH, value=max_date_PH)


###########################################


@pn.depends(select_map_PH)
def confirmed_date_PH(maps):
    if maps == 'National Geographic Map':
        maps = 'EsriNatGeo'
    elif maps == 'Open Street Map':
        maps = 'OSM'
    elif maps == 'Dark':
        maps = 'CartoDark'
    elif maps == 'Black and White':
        maps = 'StamenToner'
    df = covid19_PH_confirmed
    return df.hvplot.points(x='Residence Long', y='Residence Lat', geo=True, color='darkorange', alpha=0.8,
                            width=650, height=550, global_extent=False, tiles=maps,
                            title="Mapa ng mga kaso ng COVID-19 sa Bansa (Kumpirmadong Kaso)",
                            ylim=(0, 25), xlim=(115, 130))

@pn.depends(select_map_PH)
def admitted_date_PH(maps):
    if maps == 'National Geographic Map':
        maps = 'EsriNatGeo'
    elif maps == 'Open Street Map':
        maps = 'OSM'
    elif maps == 'Dark':
        maps = 'CartoDark'
    elif maps == 'Black and White':
        maps = 'StamenToner'
    df = covid19_PH_admitted
    return df.hvplot.points(x='Longitude', y='Latitude', geo=True, color='magenta', alpha=0.8,
                            width=650, height=550, global_extent=False, tiles=maps, title="Mapa ng mga kaso ng COVID-19 sa Bansa (Nasa Ospital)",
                            ylim=(0, 25), xlim=(115, 130))

@pn.depends(select_map_PH)
def dead_date_PH(maps):
    if maps == 'National Geographic Map':
        maps = 'EsriNatGeo'
    elif maps == 'Open Street Map':
        maps = 'OSM'
    elif maps == 'Dark':
        maps = 'CartoDark'
    elif maps == 'Black and White':
        maps = 'StamenToner'
    df = covid19_PH_died
    return df.hvplot.points(x='Residence Long', y='Residence Lat', geo=True, color='red', alpha=0.8,
                            width=650, height=550, global_extent=False, tiles=maps, title="Mapa ng mga kaso ng COVID-19 sa Bansa (Mga Namatay)",
                            ylim=(0, 25), xlim=(115, 130))

@pn.depends(select_map_PH)
def recovered_date_PH(maps):
    if maps == 'National Geographic Map':
        maps = 'EsriNatGeo'
    elif maps == 'Open Street Map':
        maps = 'OSM'
    elif maps == 'Dark':
        maps = 'CartoDark'
    elif maps == 'Black and White':
        maps = 'StamenToner'
    df = covid19_PH_recovered
    return df.hvplot.points(x='Residence Long', y='Residence Lat', geo=True, color='royalblue', alpha=0.8,
                            width=650, height=550, global_extent=False, tiles=maps, title="Mapa ng mga kaso ng COVID-19 sa Bansa (Mga Gumaling)",
                            ylim=(0, 25), xlim=(115, 130))

@pn.depends(select_metric_PH)
def select_dataframe_PH(df='Confirmed'):
    if df == 'Kumpirmado':
        return confirmed_date_PH
    elif df == 'Nasa Ospital':
        return admitted_date_PH
    elif df == 'Mga Namatay':
        return dead_date_PH
    elif df == 'Mga Gumaling':
        return recovered_date_PH

##############################################

widgets_map_PH = pn.Column(pn.Row(select_map_PH, select_metric_PH), select_dataframe_PH)
#widgets_map_PH


# In[287]:


# interactive line graph

confirmed_line = covid19_PH_confirmed.reset_index()
recovered_line = covid19_PH_recovered.reset_index()
died_line = covid19_PH_died.reset_index()
admitted_line = covid19_PH_admitted.reset_index()



confirmed_line = confirmed_line['Date of Announcement to the Public'].value_counts(sort=False).to_frame().reset_index()
confirmed_line = confirmed_line.rename(columns={'index': 'Date Announced',
                         'Date of Announcement to the Public': 'Postitive Cases'})
confirmed_line['Date Announced'] = pd.to_datetime(confirmed_line['Date Announced'])
confirmed_line.sort_values(by=['Date Announced'],inplace=True)



recovered_line = recovered_line['Date of Announcement to the Public'].value_counts(sort=False).to_frame().reset_index()
recovered_line = recovered_line.rename(columns={'index': 'Date Announced',
                         'Date of Announcement to the Public': 'Recovered Cases'})
recovered_line['Date Announced'] = pd.to_datetime(recovered_line['Date Announced'])
recovered_line.sort_values(by=['Date Announced'],inplace=True)



died_line = died_line['Date of Announcement to the Public'].value_counts(sort=False).to_frame().reset_index()
died_line = died_line.rename(columns={'index': 'Date Announced',
                         'Date of Announcement to the Public': 'Dead Cases'})
died_line['Date Announced'] = pd.to_datetime(died_line['Date Announced'])
died_line.sort_values(by=['Date Announced'],inplace=True)



admitted_line = admitted_line['Date of Announcement to the Public'].value_counts(sort=False).to_frame().reset_index()
admitted_line = admitted_line.rename(columns={'index': 'Date Announced',
                         'Date of Announcement to the Public': 'Admitted Cases'})
admitted_line['Date Announced'] = pd.to_datetime(admitted_line['Date Announced'])
admitted_line.sort_values(by=['Date Announced'],inplace=True)



covid19_PH_line = confirmed_line.merge(right=recovered_line, on='Date Announced', how='outer').fillna(0)
covid19_PH_line = covid19_PH_line.merge(right=died_line, on='Date Announced', how='outer').fillna(0)
covid19_PH_line = covid19_PH_line.merge(right=admitted_line, on='Date Announced', how='outer').fillna(0)
covid19_PH_line = covid19_PH_line.set_index('Date Announced')
covid19_PH_line = covid19_PH_line.astype(int).reset_index()
covid19_PH_line['Cumulative Positive'] = covid19_PH_line['Postitive Cases'].cumsum(axis = 0)
covid19_PH_line['Cumulative Admitted'] = covid19_PH_line['Admitted Cases'].cumsum(axis = 0)
covid19_PH_line['Cumulative Dead'] = covid19_PH_line['Dead Cases'].cumsum(axis=0)
covid19_PH_line['Cumulative Recovered'] = covid19_PH_line['Recovered Cases'].cumsum(axis = 0)


covid19_PH_line_graph = covid19_PH_line.hvplot.line(x='Date Announced', y=['Cumulative Admitted',
                                                                           'Cumulative Dead',
                                                                           'Cumulative Recovered'],
                                                    width=1100, height=450, legend='top_left',
                                                    title = 'Graph ng Nadadagdag na Kaso ng COVID-19 sa Bansa')

covid19_PH_area_graph = covid19_PH_line.hvplot.area(x='Date Announced', y=['Cumulative Admitted',
                                                                           'Cumulative Dead',
                                                                           'Cumulative Recovered'],
                                                    width=1100, height=450, stacked=False, legend='top_left',
                                                    title = 'Graph ng Nadadagdag na Kaso ng COVID-19 sa Bansa')

confirmed_PH_line_graph = covid19_PH_line.hvplot.line(x='Date Announced', y=['Cumulative Positive',
                                                                           ],
                                                    width=1100, height=450,
                                                    title = 'Graph ng mga Positibong Kaso ng COVID-19 sa Bansa')

covid19_PH_line_tab = covid19_PH_line.hvplot.table(width=1100, height=250,
                                                   title='Listahan ng mga Kaso ng COVID-19 sa Bansa')


widgets_curve_PH = pn.Column(confirmed_PH_line_graph, (covid19_PH_line_graph*covid19_PH_area_graph), covid19_PH_line_tab)


# In[288]:


age_PH = covid19_PH_edited['Age'].value_counts()
age_PH = pd.DataFrame(age_PH).reset_index().sort_values(by=['index'])

age_PH = age_PH.rename(columns={'index': 'age',
                         'Age': 'count'})

age_plot = age_PH.hvplot.hist(y='age', bins=15, bin_range=(0,100),
                         width=400, height=300, cmap='Accent',
                         title='Kaso ng COVID-19 (Edad)',
                         xlabel='Edad', ylabel='Bilang ng mga Kumpirmadong Kaso')

age_table = age_PH.hvplot.table(['age', 'count'], width=150, height=450)


# In[289]:


# Places with the most number of cases in PH
place_PH = covid19_PH_edited.reset_index()
place_PH = place_PH['Residence in the Philippines'].value_counts()
place_PH = pd.DataFrame(place_PH).reset_index()

place_PH = place_PH.rename(columns={'index': 'Residence in the Philippines',
                         'Residence in the Philippines': 'count'})

place_PH_valid = place_PH[place_PH['Residence in the Philippines'] != 'For Validation']

place_PH_plot = place_PH_valid.hvplot.bar(x='Residence in the Philippines', y='count',
                                          color='Residence in the Philippines',
                                          legend=False, cmap='tab20c', shared_axes=False,
                                          invert=True, width=900, height=750, flip_yaxis=True,
                                          title = 'Bilang ng mga Kaso ng COVID-19 sa mga Probinsiya at Siyudad')
place_PH_tab = place_PH_valid.hvplot.table(width=1100, height=500)


# In[290]:


gender_PH = covid19_PH_edited.reset_index()
gender_PH = covid19_PH_edited['Sex'].value_counts()
gender_PH = pd.DataFrame(gender_PH).reset_index()

gender_PH = gender_PH.rename(columns={'index': 'Sex',
                         'Sex': 'count'})

gender_PH.loc[gender_PH['Sex'] == 'M', ['Sex']] = 'Male'
gender_PH.loc[gender_PH['Sex'] == 'F', ['Sex']] = 'Female'


gender_PH_plot = gender_PH.hvplot.bar(x='Sex', y='count',
                                      color='Sex', cmap='Colorblind',
                                      invert=False, width=400, height=300, flip_yaxis=False,
                                      title = 'Mga  Kaso ng COVID-19 (Kasarian)')

widgets_age_gender = pn.WidgetBox(pn.Column(age_plot, gender_PH_plot))


# In[291]:


hospitals_PH = covid19_PH_edited.reset_index()
hospitals_PH = covid19_PH_edited['Admission / Consultation'].value_counts()
hospitals_PH = pd.DataFrame(hospitals_PH).reset_index()

hospitals_PH = hospitals_PH.rename(columns={'index': 'Hospital',
                         'Admission / Consultation': 'Patients Admitted'})

hospitals_PH_plot = hospitals_PH.head(10).hvplot.bar(x='Hospital', y='Patients Admitted',
                                      width=1100, height=550, legend=False,
                                      color='Hospital', cmap='glasbey_light',
                                      invert=True, flip_yaxis=True, shared_axes=False,
                                      title = '10 Ospital sa Pilipinas na may Pinkamaraming Naka-admit na May COVID-19')

hospitals_PH_table = hospitals_PH.hvplot.table(x='Hospital', y='Patients Admitted', width=800, height=200,)


# In[292]:


title = "# Coronavirus Disease-2019 (COVID-19) sa Pilipinas:"
subtitle = "## Pagsusuri sa Data ng DOH Tungkol sa COVID-19"
PH_data_visual = pn.Column(title,
                           subtitle,
                           pn.Row(widgets_map_PH, widgets_age_gender),
                           widgets_curve_PH,
                           hospitals_PH_plot,
                           place_PH_plot)
PH_data_visual.embed()

<!–– Hide JupyterNotebook cell numbers etc ––!>
<script>
  $(document).ready(function(){
    $('div.prompt').hide();
    $('div.back-to-top').hide();
    $('nav#menubar').hide();
    $('.breadcrumb').hide();
    $('.hidden-print').hide();
  });
</script>
<footer id="attribution" style="float:right; color:#999; background:#fff;">
Attribution: Created with Jupyter
</footer>