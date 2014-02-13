"""
"""
import pysal
import os.path
import shutil
import webbrowser
import sqlite3

__author__='Xun Li <xunli@asu.edu>'
__all__=[]

default_work_dir = "./temp"

def setup(work_dir):
    # create a work_dir if not exist
    if not os.path.exists(work_dir):
        os.makedirs(work_dir)
        # copy d3.js library for local usage
        #shutil.copy2('./d3.v3.min.js', work_dir)         
        #shutil.copy2('./highlight.min.js', work_dir)         
        default_work_dir = work_dir

def show_map(shp):
    if not os.path.exists(default_work_dir):
        raise "work directory not exists"
    # 1.convert shapefile to geojson
    #
    # 2.make a copy of template_map.html and replace the 
    #   placeholder with the location of json file
    #
    # 3.open a browser with the new html file
    #
    url = "http://127.0.0.1:8000/%s" % "template_map.html"
    webbrowser.open_new(url)
    
def show_weightsmap(shp, w):
    # the same with showmap()
    # but also convert weights as a json file that
    # can be processed by D3 javascripts
    # 
    # make a copy of template_weights_map.html and replace the
    # placeholders with json shape file and json weights file
    #
    # open in browser
    url = "http://127.0.0.1:8000/%s" % "template_weights_map.html"
    webbrowser.open_new(url)
    
def show_scatterplot(variables):
    # the same with previous, but give the json file contains
    # historgram information and make a copy ot template_histogram.htm
    # and replace the placeholder
    #
    # open in browser
    url = "http://127.0.0.1:8000/%s" % "template_scatterplot.html"
    webbrowser.open_new(url)

def show_histogram(histogram_json):
    # the same with previous, but give the json file contains
    # historgram information and make a copy ot template_histogram.htm
    # and replace the placeholder
    #
    # open in browser
    pass

def getselected(localStorage_path):
    # interact with D3.js web/html 
    # e.g. in chrome, visit localStorage sqlite file, the other way to 
    # do the communication is using jQuery.wtFile to write local file
    home = os.path.expanduser("~")
    localStorage_path = home + '/Library/Application Support/Google/Chrome/Default/Local Storage/https_127.0.0.1_8000.localstorage'
    con = None
    try:
        con = sqlite3.connect(localStorage_path)
        cur = con.cursor()
        cur.execute("SELECT * FROM ItemTable")
        rows = cur.fetchall()
        
        for row in rows:
            key,val = row
            if key == "select_ids":
                print val
    except sqlite3.Error, e:
        pass
    finally:
        if con:
            con.close()
    
if __name__ == "__main__":
    # for example:
    # since D3.js need use geojson, so makeup fake one for demo
    shp = pysal.open(pysal.examples.get_path("NAT.shp"))
    dbf = pysal.open(pysal.examples.get_path("NAT.dbf"))
    w = pysal.rook_from_shapefile(pysal.examples.get_path("NAT.shp"))
    hist = dbf.by_col("STATE_FIPS")
    xs = [dbf.by_col("STATE_FIPS"),dbf.by_col("FIPS"),dbf.by_col("HR60")]
  
    # create a working directory for creating webpages for visualization 
    setup("./temp")
    # start up a http server under this directory, 
    # suggest manually start server:
    # go to ~/temp, then type
    # os.system('python server.py &')
    
    # call web browser to show a map in a tab
    show_map(shp)
    # call web browser to show a map with weights in a tab
    show_weightsmap(shp,w)
    # call web browser to show a map with weights in a tab
    #show_histgram(hist)
    # call web browser to show a scatter plot in a tab
    show_scatterplot(xs)
   
    # PySAL get selected ids from webpages via localStorage
    selected_ids = getselected("")
    
    # PySAL use selected_ids to do further analysis
    
    
    
    






