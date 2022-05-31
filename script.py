from flask import Flask, render_template, url_for
import folium
import pandas
from arcgis.gis import GIS
from arcgis.geocoding import geocode, reverse_geocode
from arcgis.geometry import Point
from flask_images import resized_img_src

app=Flask(__name__)
app.secret_key= 'monkey'

@app.route('/plot')
def plot():
    from pandas_datareader import data
    import datetime
    from bokeh.plotting import figure, show, output_file
    from bokeh.embed import components
    from bokeh.resources import CDN

    Start=datetime.datetime(2015,11,1)
    End=datetime.datetime(2016,3,10)

    df=data.DataReader(name="GOOG",data_source="yahoo",start=Start,end=End)

    p=figure(x_axis_type="datetime", width=1000, height=300, title='Candlestick Chart', sizing_mode="scale_width") #scale_width makes the graph adjust when you adjust the webpage
    p.title.text_font_size = '20pt'
    p.title.text_font = "Arial"
    p.title.align= 'center'
    p.grid.grid_line_alpha=0.3

    data_increase=df.index[df.Close > df.Open]
    date_decrease=df.index[df.Close < df.Open]

    def inc_dec(c,o):
        if c > o:
            value="Increase"
        elif c < o:
            value="Decrease"
        else:
            value="Equal"
        return value

    df["Status"]=[inc_dec(c,o) for c, o in zip(df.Close, df.Open)]
    df["Middle"]=(df.Open+df.Close)/2
    df["Height"]=abs(df.Open-df.Close)

    hours_12=12*60*60*1000

    p.segment(df.index, df.High, df.index, df.Low, color="black") #makes those black lines that tell you what was low and high that day

    p.rect(df.index[df.Status=="Increase"],df.Middle[df.Status=="Increase"], hours_12, df.Height[df.Status=="Increase"], fill_color="#7fffd4", line_color="black")
    p.rect(df.index[df.Status=="Decrease"],df.Middle[df.Status=="Decrease"], hours_12, df.Height[df.Status=="Decrease"], fill_color="#ff5c33", line_color="black")

    #output_file("CS.html")  #it's stored in the local directory, so if we want to build website we don't need it anymore
    #show(p)

    script1, div1 = components(p)

    cdn_js=CDN.js_files[0]
    return render_template("plot.html",
    script1=script1,
    div1=div1,
    cdn_js=cdn_js)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/map/')
def map():
    return render_template ("map.html")

@app.route('/wycieczka/')
def wycieczka():
    return render_template ("wycieczka.html")

@app.route('/Los_Angeles/')
def Los_Angeles():
    return render_template ("Los_Angeles.html")


if __name__ == "__main__":
    app.run(debug=True)
