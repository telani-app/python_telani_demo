# python_telani_demo
A demonstration of different applications of a proposed telani JSON-Export format.

# prerequisites
Python environment, 
Pip

# Steps to get the python scripts up and running
1) Clone the repo :  git clone "https://github.com/telani-app/python_telani_demo.git"
2) In the terminal cd to repo : cd path\to\repo
3) To install all the dependencies run the command : pip install -r .\requirements.txt
4) Run the command : python main.py
5) In a browser go to the port where the dash application is running.

# How to use the dashboard
The dashboard has three tabs:
  1) Element Type : 
      Here you can select Sensor or Actuator
      Select the element type of the element
      And in the subsequent table there is a list of Sensor/Actuator having the element type you selected.
      If you click on any of the rows of the table, it would generate the QR code associated with the Sensor/Actuator to which the row belongs.
   
   2) Connections : 
      This tab shows the connection graph between the Sensors and the Actuators.
      You can use the play/pause button on top left of the graph to show the different connection graphs , the same can be acheived using a slider below.
   
   3) Graphs : 
      This tab shows two bar graphs for number of elements for a specific element type for Actuators and Sensors respectively.

# semantic_search_demo

# Steps

1) Run embeddings.py to save embeddings and model
2) Run semantic_search.py to run queries

# Example: Semantic Search Query

Enter a query and retrieve the most relevant project item using embeddings.

```text
Enter query:
red colored zone

Top result:
Score: 0.653
Zone '3' is located on floor EG. Description: . Displayed with color #93020240.
Metadata: {'type': 'zone', 'name': '3'}

Enter query:
Sensor in ground floor and in living room

Score: 0.577
Sensor 'ABC 1' of type 'ABC' located at '' on floor EG. It belongs to system '', zone '1 Wohnzimmer', with alarm state ''. Connection type 'Zentrale'. with transmission path '',Detector type is 'AM',and is related to '['FSD 111', 'Signalleuchte 1', 'ÜE 2', 'Blitzleuchte 1']' actuators
{'type': 'sensor', 'name': 'ABC 1', 'export_id': '25250504-c483-4bdd-b15f-e7df6144cabb'}

```