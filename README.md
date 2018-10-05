# DashCandlestickCharting

------------------------------------------------Description---------------------------------------------------------------
This is a sample project for folks trying to use the Plotly and Dash candlestick charts. The problem with the Plotly Candlestick Graph object is there are no good y axis sliders by default to adjust the vertical range of bars in the chart.  This example provides x-axis date range sliders that when adjusted will automatically update the y axis to show the vertical range of only the visible bars plus a small 2 tick padding. The built in panning features of the Dash candlestick graph can then be used to move around easily in the view. Thanks to the authors of the Plotly and Dash libraries for their amazing work! 


Running this example using python and Flask
-------------------------------------------
There is only one file for this project called dash_plotly_candlestick.py. To run the project just run this file using the python command prompt. However, you will need to make sure you have the necessary dependencies installed. 

This project requires you install python. This was developed with python 3.6.5
The following packages were also installed using pip at the time I authored the code. 

Package              Version
-------------------- ---------
certifi              2018.8.24
chardet              3.0.4
Click                7.0
dash                 0.27.0
dash-core-components 0.30.2
dash-html-components 0.13.2
dash-renderer        0.14.1
decorator            4.3.0
Flask                1.0.2
Flask-Compress       1.4.0
idna                 2.7
ipython-genutils     0.2.0
itsdangerous         0.24
Jinja2               2.10
jsonschema           2.6.0
jupyter-core         4.4.0
MarkupSafe           1.0
nbformat             4.4.0
numpy                1.15.2
pandas               0.23.4
pip                  18.0
plotly               3.3.0
python-dateutil      2.7.3
pytz                 2018.5
requests             2.19.1
retrying             1.3.3
setuptools           39.0.1
six                  1.11.0
traitlets            4.3.2
urllib3              1.23
Werkzeug             0.14.1

Flask is an application that provides for python web application creation. We are trying out a framework called dash which provides the ability to create charting applications 
including candlestick charts. Dash uses plotly Plotly.js, and React.js, and Flask and can be run locally on a flask server. The challenge is starting the flask server correctly.
You cannot start a flask server from within the idle application so going into idle
and hitting Run will cause an error. 

Instead
1) open a windows command prompt
2) start any python virtual environment in which you want to run code
3) Navigate to your project directory where you have your python scripts, or type in the full path to you python script and run your primary script to start the flask server directly using the python executable. This assumes python is installed and the path variable is set in windows:
$python dash_plotly_candlestick.py

If python has been added to the path in your local environment variables you can just double click on the dash_plotly_candlestick.py and it should run. See https://stackoverflow.com/questions/3701646/how-to-add-to-the-pythonpath-in-windows to add python to your system path and 

Then open a browser at the following address: http:127.0.0.1:8050/ 
 
A full tutorial on using Dash is available from the Dash website:
https://dash.plot.ly/

-----------------------------------------Running Code from a python virtual environment-----------------------------------------------
You may want to develop scripts in idle and run them using a python virtual environment so you have all the libraries you want configured just for that project. 

Problem is if you open idle from the normal shortcuts, it opens idle and uses the default python installation, not your virtual environment so the libraries you may have installed in your virtual environment will not be available to your idle instance. 

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
