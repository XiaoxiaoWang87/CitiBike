CitiBike
========

My code to analyze the 8-month Citi Bike data since the program launch. A lot of fun.

-------------------------------
Step 1: make tree from raw data
-------------------------------
./maketree.py whichMonth whichOutputDir

(for batch jobs: source sub.sh)


-------------------------------
Step 2: merge trees
-------------------------------
hadd data.root 201*root



-------------------------------
Step 3: analyze trees
-------------------------------
./analyzetree.py whichPlotOutputDir
(for batch jobs: source sub_analyze.sh)


-------------------------------
-------------------------------
Plotting functionalities are in PlottingUtls.py.
The geographical map is made with makemapnyc.py. It uses the input file made after running analyzetree.py.

