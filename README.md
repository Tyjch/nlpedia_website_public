# Getting Started
This walkthrough assumes that you already have Python 3.6 or higher installed 

----
## Database
1. You will need to download Neo4j Desktop from https://neo4j.com/download/	
2. Run Neo4j Desktop
3. Create a new project inside Neo4j Desktop
4. Click the area that says “Add Graph” 
5. Click the button that says “Create a Local Graph”
6. Enter a name and password for the graph
7. Set the version of Neo4j to 3.5.3 (You may have to download it) 
8. Click the button that says “Create”
9. Find the graph you just created and press “Start”
10. Wait for the graph to start. It will change to “Stop” when it is running.

----
## IDE
1. Download PyCharm Community Edition from https://www.jetbrains.com/pycharm/download/ (skip this step if you already have it installed)
2. Run PyCharm
3. Wait for the window titled “Welcome to PyCharm” to open
4. Click the area that says “Check out from Version Control”
5. Select Git from the popup menu
6. Enter https://github.com/Tyjch/nlpedia-website.git in the URL section
7. Enter the directory you want to use for this project
8. Press “Clone”
9. Select “Yes” when PyCharm asks if you want to open this project

----
## Virtual Environment
1. In the menu bar in the top left, select “PyCharm” and then “Preferences”
2. In the pop-up window, click the text that begins with “Project:” and then click “Project Interpreter”
3. Click the gear icon in the top right of the pop-up window and then click “Add…”
4. In the window titled “Add Python Interpreter”, find the dropdown menu labeled “Base interpreter:” and click it
5. Select a Python version equal to or higher than 3.6 and then press “OK”
6. Press “Okay” again in the underlying pop-up window
7. On the left hand side in the project directory of PyCharm, double click to open the file titled “requirements.txt”
8. After a few seconds, an alert will appear near the top of the screen saying that some dependencies are not fulfilled
9. Click “Install dependencies”
10. Wait for all of them to download
----
## Project Configuration
* To use your local Neo4j as the database for this project, change `neo4j_user` and `neo4j_password` inside of `config.ini`
* To use a remote GrapheneDB database, change `graphene_uri`, `graphene_user`, and `graphene_password` inside of `config.ini`
    * This requires `py2neo` v3 rather than v4
    * You also need to change `is_local` in the same file to `False`

----
## Installing SpaCy Models
1. At the bottom of PyCharm, click the button that says “Terminal”
2. Copy and paste the following into the box that opens: `python -m spacy download en`
3. Press enter
4. Wait for it to finish downloading

----
## Running the App
1. On the left hand side in the project directory of PyCharm, double click to open the file titled “run.py”
2. Expand the directory labeled "nlpedia" and double click on "models.py"
3. Change the string of "graphene_pw" to the password you used to create the Neo4j graph earlier
4. Right click in the file that opens and select “Run ‘run’”
5. A box will appear at the bottom of PyCharm
6. After a few seconds, this text “Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)” will appear
7. Click on http://127.0.0.1:5000/
8. The web application will open in your default browser
