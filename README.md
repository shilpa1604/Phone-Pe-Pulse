# Phone-Pe-Pulse
Phonepe Pulse Data Visualization and Exploration: A User-Friendly Tool Using Streamlit and Plotly

Phone-Pe-Pulse
Phonepe Pulse Data Visualization and Exploration: A User-Friendly Tool Using Streamlit and PlotlyWhat is PhonePe Pulse?
The PhonePe Pulse website showcases more than 2000+ Crore transactions by consumers on an interactive map of India. With over 45% market share, PhonePe's data is representative of the country's digital payment habits. The insights on the website and in the report have been drawn from two key sources - the entirety of PhonePe's transaction data combined with merchant and customer interviews. The report is available as a free download on the PhonePe Pulse website and GitHub.

Libraries/Modules needed for the project!
1.	Plotly - (To plot and visualize the data)
2.	Pandas - (To Create a DataFrame with the scraped data)
3.	Pymysql-(To connect to database )
4.	sqlalchemy- (To store entire dataframe directly into a MySQL table)
5.	Streamlit - (To Create Graphical user Interface)
6.	json - (To load the json files)
7.	numpy - (To perform arithmetic operations)
8.	os – (To navigate to different directories to access data cloned from github)

Workflow
Step 1:
Importing the Libraries:
Importing the libraries. As I have already mentioned above the list of libraries/modules needed for the project. First we have to import all those libraries. If the libraries are not installed already use the below piece of code to install.
	pip install [“Name of the library”]
Step 2:
Data extraction:
Clone the Github using scripting to fetch the data from the Phonepe pulse Github repository and store it in a suitable format such as JSON. Use the below syntax to clone the phonepe github repository into your local drive.
Git >>>Clone>>Url (https://github.com/PhonePe/pulse.git)>>Clone
(Incase prompted, provide github credentials to clone the data)

Step 3:
Data transformation:
Execute read_insert_data.py program. This will read all the  JSON files that are available in the folders and convert them into readeable and understandable DataFrame format by using the for loop and iterating file by file and then finally the DataFrame is created. 
In read_insert_data.py , make the following changes:
	Update the custom path to the directory where you have cloned the github data.
custom_path ='C:\\Users\\Dell\\PycharmProjects'

	Update the MySQL connection details
user = ???
password = ???
host = ???

Step 4:
Database insertion:
The same program executed in Step 3 will insert the dataframe created above into SQL database tables.
Step 5:
Dashboard creation:
Execute the streamlit app to create colourful and insightful dashboard giving transaction and user PhonePe information. To visualize data using Indian map, make sure the required geojson file is downloaded.
	streamlit run PhonePe_Pulse.py

Update the MySQL connection details in PhonePe_Pulse.py
user = ???
password = ???
host = ???
database = ???

Update the location where you have placed the geojson file for Indian states:
indian_states = json.load(open("C:\\Users\\Dell\\PycharmProjects\\pythonProject\\venv\\states_india.geojson", 'r'))




