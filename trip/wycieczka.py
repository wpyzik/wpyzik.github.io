import folium
import pandas
from arcgis.gis import GIS
from arcgis.geocoding import geocode, reverse_geocode
from arcgis.geometry import Point
import os
import os.path
from os import path

col_list= ["group", "addresses", "lon", "lap"]
table= pandas.read_csv("miejsca.csv", usecols=col_list)

#comment this block out if you are done converting addresses
for i,lon in enumerate(table["lon"]):
    if table['lon'].isnull().values[i]:
        address=table["addresses"][i]
        gis = GIS()
        geocode_result = geocode(address= address, as_featureset=True)
        table['lon'][i]= geocode_result.features[0].geometry.x
        table['lap'][i]= geocode_result.features[0].geometry.y
    else:
        pass
table.to_csv("miejsca.csv")


lap=list(table["lap"])
lon=list(table["lon"])
address=list(table["addresses"])
group=list(table["group"])

map= folium.Map(location=[36.22974000000005,-116.76696999999996], zoom_start=7, tiles='stamenterrain')

folium.TileLayer('Stamen Terrain').add_to(map)
folium.TileLayer('Stamen Toner').add_to(map)
folium.TileLayer('Stamen Water Color').add_to(map)
folium.TileLayer('cartodbpositron').add_to(map)

fgv= folium.FeatureGroup(name="Wycieczka")

popups=[]
list=[]

for i,lonn in enumerate(lon):
    tuple=[lap[i],lon[i]]
    list.append(tuple)
    popups.append(address[i])

list_1= list[1:9] + list[16:21] + list[36:76]

list_2 = [i for i in list if i not in list_1]

popups_1= popups[1:9]
popups_2= popups[16:21]
popups_3= popups[36:76]

gen = """
<a href="https://www.google.com/search?q=%s" target="_blank">%s</a>
<br>Jezeli chcesz sie dowiedziec troche wiecej o tym miejscu, kliknij na jego nazwe.<br>
<br><img src="static/images/%s.jpeg" width="200"/>
"""


here = """
<a href="https://www.google.com/search?q=%s" target="_blank">%s</a>
<br>Jezeli chcesz sie dowiedziec troche wiecej o tym miejscu, kliknij na jego nazwe.<br>
<br><img src="static/images/%s.jpeg" width="200"/>
<br> <br>
<br>A jezeli chcesz zobaczyc co zwiedzalismy w Los Angeles, kliknij <a href="javascript:(function addMarker(){var map = window[$('.folium-map').attr('id')];
"""

for i,entry in enumerate(list[1:9]):
    slash = r"\\"
    popup = '<a href='+slash+'\'https://www.google.com/search?q='+popups_1[i]+slash+'\' target='+slash+'\'_blank'+slash+'\'>'+popups_1[i]+'</a><br>'
    popup +='Troche wiecej informacji? Kliknij na nazwe!'
    popup += '<br> <br>'
    popup += '<img src='+slash+'\'static/images/'+popups_1[i]+'.jpeg'+slash+'\' width='+slash+'\'200'+slash+'\'/>'
    here+="var la"+str(i)+"=new L.CircleMarker(["+str(entry[0])+","+str(entry[1])+"], {'color':'#124d00'}).addTo(map); "
    here+="la"+str(i)+".bindPopup('"+popup+"').openPopup(); "

here+="})()\">tutaj</a>"

here2 = """
<a href="https://www.google.com/search?q=%s" target="_blank">%s</a>
<br>Jezeli chcesz sie dowiedziec troche wiecej o tym miejscu, kliknij na nie!<br>
<br>Jezeli chcesz zobaczyc wszystkie zdjecia, ktore tam robilismy, kliknij na ponizsze zdjecie.<br>
<br><img src="static/images/%s.jpeg" width="200"/>
<br> <br>
<br> A jezeli chcesz zobaczyc wiecej miejsc, ktore zwiedzilismy w Las Vegas, kliknij <a href="javascript:(function addMarker(){var map = window[$('.folium-map').attr('id')];
"""

#comment it out when you're done converting pics names
for i,entry in enumerate(address):
    if(path.exists('/Users/weronika/Desktop/coding/wycieczka/stronka/static/images/'+str(i)+'.jpeg')):
        os.rename(r'/Users/weronika/Desktop/coding/wycieczka/stronka/static/images/'+str(i)+'.jpeg',r'/Users/weronika/Desktop/coding/wycieczka/stronka/static/images/'+entry+'.jpeg')


for i,entry in enumerate(list[16:21]):
    slash = r"\\"
    popup = '<a href='+slash+'\'https://www.google.com/search?q='+popups_2[i]+slash+'\' target='+slash+'\'_blank'+slash+'\'>'+popups_2[i]+'</a><br>'
    popup +='Troche wiecej informacji? Kliknij na nazwe!'
    popup += '<br> <br>'
    popup += '<img src='+slash+'\'static/images/'+popups_2[i]+'.jpeg'+slash+'\' width='+slash+'\'200'+slash+'\'/>'


    here2+="var la"+str(i)+"=new L.CircleMarker(["+str(entry[0])+","+str(entry[1])+"], {'color':'#124d00'}).addTo(map); "
    here2+="la"+str(i)+".bindPopup('"+popup+"').openPopup(); "

here2+="})()\">tutaj</a>"

here3 = """
<a href="https://www.google.com/search?q=%s" target="_blank">%s</a>
<br>Jezeli chcesz sie dowiedziec troche wiecej o tym miejscu, kliknij na nie!<br>
<br>Jezeli chcesz zobaczyc wszystkie zdjecia, ktore tam robilismy, kliknij na ponizsze zdjecie.<br>
<br><img src="static/images/%s.jpeg" width="200"/>
<br> <br>
<br> A jezeli chcesz zobaczyc wiecej miejsc, ktore zwiedzilismy w San Francisco, kliknij <a href="javascript:(function addMarker(){var map = window[$('.folium-map').attr('id')];
"""

for i,entry in enumerate(list[36:76]):
    slash = r"\\"
    popup = '<a href='+slash+'\'https://www.google.com/search?q='+popups_3[i]+slash+'\' target='+slash+'\'_blank'+slash+'\'>'+popups_3[i]+'</a><br>'
    popup +='Troche wiecej informacji? Kliknij na nazwe!'
    popup += '<br> <br>'
    popup += '<img src='+slash+'\'static/images/'+popups_3[i]+'.jpeg'+slash+'\' width='+slash+'\'200'+slash+'\'/>'


    here3+="var la"+str(i)+"=new L.CircleMarker(["+str(entry[0])+","+str(entry[1])+"], {'color':'#124d00'}).addTo(map); "
    here3+="la"+str(i)+".bindPopup('"+popup+"').openPopup(); "

here3+="})()\">tutaj</a>"

for lp,ln,ad,gr in zip(lap,lon,address,group):
    if gr=="los_angeles":
        fgv.add_child(folium.CircleMarker(location= [lp,ln], radius=10, popup=folium.Popup(here % (ad,ad,ad)), tooltip=folium.Tooltip(ad), fill_color= "#124d00", color="black", fill_opacity= 0.7, zoom_start='5'))
    if gr=="gen":
        fgv.add_child(folium.CircleMarker(location= [lp,ln], radius=10, popup=folium.Popup(gen % (ad,ad,ad)), tooltip=folium.Tooltip(ad), fill_color= "#8cff66", color="black", fill_opacity= 0.7))
    if gr=="las_vegas":
        fgv.add_child(folium.CircleMarker(location= [lp,ln], radius=10, popup=folium.Popup(here2 % (ad,ad,ad)), tooltip=folium.Tooltip(ad),  fill_color= "#124d00", color="black", fill_opacity= 0.7))
    if gr== "san_francisco":
        fgv.add_child(folium.CircleMarker(location= [lp,ln], radius=10, popup=folium.Popup(here3 % (ad,ad,ad)), tooltip=folium.Tooltip(ad),  fill_color= "#124d00", color="black", fill_opacity= 0.7))

    fgv.add_child(folium.PolyLine(list_2, color="#1a6600", weight=2.5, opacity=1, smooth_factor=7))


map.add_child(fgv)
map.add_child(folium.LayerControl())

map.save("wycieczka.html")
