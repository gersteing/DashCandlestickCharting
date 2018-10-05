# Plotly Dash Candlestick Charting Example with Automatic Y Axis Range Adjustment
Description
-----------
This is a sample project for folks trying to use the Plotly and Dash candlestick charts. Plotly and Dash can be used to plot different types of data on charts. In this case we are using a candlestick chart which plots some market price data. Candlestick charts are commonly used by day traders. See this quick tutorial on candlestick charts if you don't know what the are. 
https://www.investopedia.com/walkthrough/forex/beginner/level3/candlestick.aspx

The problem with the default Plotly Candlestick chart objects (graphs) is there are no good y axis sliders built in to adjust the vertical range of bar price data in the chart.  This example code provides x-axis date range sliders that, when adjusted, will automatically update the y axis to show the only vertical range of the visible bars plus a small 2 tick padding. The built in panning features of the Dash candlestick graph can then be used to move around easily in the chart view. Thanks to the authors of the Plotly and Dash libraries for their amazing work! 

Files included:
---------------
dash_plotly_candlestick.py = code for a basic candlestick chart with x axis range slider that automatically sizes y axis nicely

dash_plotly_candlestick_with_multiple_traces-overlays.py = an additional example where I parse out some data to use as an overlay over the bars. 

Note that this code is heavily commented. There are also many print lines commented out that can be enabled if you want to print the values of variables in the defined functions. Since this is intended as a shared example, I wanted to make it as informative as possible, but you would want to remove this overhead if using in any production context. 


Running this Example Using Python and Flask
-------------------------------------------
To start this project just run the main file called dash_plotly_candlestick.py. You can run the file from the python command prompt. However, you will need to make sure you have the necessary dependencies installed. 

This project requires you install python. This was developed with python 3.6.5

The only other dependencies I installed were Dash, plotly, pytz, and pandas.
Need to understand these libraries better to make sense of this example? See section below - Installing and Getting Help with the Dependent Libraries

The only thing that might trip you up when running this example is if you try to run the script from the idle python editor. You cannot start a flask server from within the idle python editor application so openning the file in idle and hitting Run will cause an error. 

Instead
1) open a windows command prompt
2) (Optional) start any python virtual environment if you want to run the code in a python virtual environment
3) Navigate to your project directory where you have your python scripts, or type in the full path to you python script and run the primary script (dash_plotly_candlestick.py) to start the flask server directly using the python executable. This assumes python is installed and the path variable is set in windows/ the $ represents the windows command prompt:
$ python dash_plotly_candlestick.py

If python has been added to the path in your local environment variables you can just double click on the dash_plotly_candlestick.py and it should run. See https://stackoverflow.com/questions/3701646/how-to-add-to-the-pythonpath-in-windows to add python to your system path and 

Then open a browser at the following address: http:127.0.0.1:8050/
You should see a candlestick chart with data loaded from a local data file that contains bar data:
20180923TradingTestDataExportCSV.csv
This file is located in the same directory as the dash_plotly_candlestick.py script.
 
For more information, a full tutorial on using Dash is available from the Dash website:
https://dash.plot.ly/

Installing and Getting Help with the Dependent Libraries
--------------------------------------------------------
Flask is an application that provides for python web application creation. We are trying out a framework called Dash which provides the ability to create charting applications including candlestick charts. Dash uses plotly Plotly.js, and React.js, and Flask and can be run locally on a flask server which is a python web server. 

The following packages were also installed using pip at the time I authored the code. 

Package              Version
-------------------- ---------
* certifi              2018.8.24
* chardet              3.0.4
* Click                7.0
* dash                 0.27.0
* dash-core-components 0.30.2
* dash-html-components 0.13.2
* dash-renderer        0.14.1
* decorator            4.3.0
* Flask                1.0.2
* Flask-Compress       1.4.0
* idna                 2.7
* ipython-genutils     0.2.0
* itsdangerous         0.24
* Jinja2               2.10
* jsonschema           2.6.0
* jupyter-core         4.4.0
* MarkupSafe           1.0
* nbformat             4.4.0
* numpy                1.15.2
* pandas               0.23.4
* pip                  18.0
* plotly               3.3.0
* python-dateutil      2.7.3
* pytz                 2018.5
* requests             2.19.1
* retrying             1.3.3
* setuptools           39.0.1
* six                  1.11.0
* traitlets            4.3.2
* urllib3              1.23
* Werkzeug             0.14.1 

The only libraries I installed were Dash, plotly, pytz, and pandas. Below is how I installed them and where you can find resources about each library.

# Dash
For dash you have to install three libraries (see Dash installation guide https://dash.plot.ly/installation)

$pip install dash==0.28.1  # The core dash backend
$pip install dash-html-components==0.13.2  # HTML components
$pip install dash-core-components==0.30.2  # Supercharged components

Dash component are not that difficult to understand you are basically setting the values for a bunch of nested python dictionaries to configure the components which are just wrappers for html code. These reference was very helpful for me to understand how to configure the sliders, and candlestick chart propoerties. I used this to understand how to configure the x slider and use callbacks to update the chart (graph) ranges. 
https://dash.plot.ly/dash-core-components - list of components and how to configure them
https://dash.plot.ly/ Dash tutorials to explain the framework

# Plotly
To install the plotly libraries see plotly installation guide https://plot.ly/python/getting-started.

$pip install plotly 

Plotly is a seperate library from Dash. Dash is to display the html output. Plotly is the core library for creating the figures and is used by Dash. These tutorials were helpful, but the most helpful was the reference materials to all of the graph properties. 
https://plot.ly/python/reference/

# Pytz
Pytz is a date library to help with using the python datetime objects. Installation instructions are here: https://pypi.org/project/pytz/

$pip install pytz

One of the more challenging aspects of this code is understanding how to use python date time objects and doing datetime calculations with timezone aware datetime objects. These are resources that helped me get my arms around using datetime objects in python and understand why the pytz libary is helpful.  
https://howchoo.com/g/ywi5m2vkodk/working-with-datetime-objects-and-timezones-in-python
https://www.w3schools.com/python/python_datetime.asp
https://docs.python.org/3/library/datetime.html

# Pandas
The pandas libary is a great data manipulation library. You can get install instructions and help here:
https://pandas.pydata.org/ 

$pip intall pandas

The pandas library takes some learning. I only use a small portionk, but I found these tutorial really helpful! 
http://pandas.pydata.org/pandas-docs/stable/10min.html
https://www.shanelynn.ie/select-pandas-dataframe-rows-and-columns-using-iloc-loc-and-ix/

# Flask
You need to know almost nothing about Flask to run this code. There is just a couple lines that run a flask server. Dash automatically runs on top of the Flask server. The only thing that matters is that by using flask it allows us to see the Dash html output becuase you are running dash on a local Flask web server at address: http:127.0.0.1:8050/
If you want to know more about Flask you can find info here: http://flask.pocoo.org/docs/1.0/

Editing Code from a Python Virtual Environment
----------------------------------------------
You may want to develop scripts in idle and run them using a python virtual environment so you have all the libraries you want configured just for that project. 

Problem is if you open idle from the normal shortcuts, it opens idle and uses the default python installation, not your virtual environment so the libraries you may have installed in your virtual environment will not be available to your Idle editor instance. 

Note you do not have to use a virtual environment. The dash_plotly_candlestick.py file can be run directly from the python command prompt if you do not use a python virtual environment. But if you want to use a python virtual environment and you need to edit the script from your virtual environment, this may help. 

Solution:
1) create your python virtual environment. For more info on how to do this go to:
https://docs.python.org/3/tutorial/venv.html
This example assumes a virtual environment has been created at c:\tutorial-env
2) activate your virtual environment from a windows command prompt using the venv windows script:
c:\tutorial-env\Scripts\activate.bat 
where c:\tutorial-env is the directory where you created the python virtual environment. 

2) start idle from your virtual environment shell
python -m idlelib

This command starts idle, but idle is running now from your virtual environment rather than the default python environment you get when you first install python. 

Becuase this project uses Flask, the script will not run by using the Idle run command. This is not a problem. You can start the application using the windows command prompt. See the file ReadMe-RunningProjectExample.txt for instructions on how to run the file. You run the file the same way you would from the default python environment, but instead do the following.
1) Activate your virtual environment
c:\tutorial-env\Scripts\activate.bat 
2) use cd command to locate to your project directory so you end up with something like this
(tutorial_env) c:\path to project directory\project directory
3) run the python file using the pytyhon command
(tutorial_env) c:\path to project directory\project directory\dash_plotly_candlestick.py
