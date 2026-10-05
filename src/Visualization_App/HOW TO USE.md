# Developer Guide for Using / Modifying / Testing the Visualization App
These are the workflows involved in working with this segment

## Setup
The codespace should be set up to run a docker instance. In order to have the database function properly, you need to modify the create the .env file. There is an .env.example file that you use as a template with the following command:
cp .env.example .env

## Modification
Adding libraries necessitates updating the relevant segment of the requirements.txt file. The functionality is split between the files as so:
    app.py - Sets up the whole page environment and navigation
    authentication / dataUpload / exportData / home / visualization / createField / .py - Contains all of the display and interaction elements of the web-application pages
    test_XXX - Contains unit tests for a single segment of the software
    data_requester.py - Contains each of the interfaces with the database. Single functions / classes are imported to the relevant files for code compartmentalization. 
    models.py - Establishes the main classes 

## Testing
To run the app as a whole, run 'python -m streamlit run src/Visualization_App/app.py ' in the root directory. This will send the webapp localhost port, which you can open in a new tab.  
To run a specific unit test, run 'python -m pytest test_XXX.py ' in the root directory. You can add the -s flag after pytest to display print statements from the functions.  
To run all the tests, run 'python -m pytest'.

# TODO for Visualization App Development
This is a doc for collating necessary changes to this subsystem in the short-term. 

## Tech Stack
* We need to decide if the live visualization will use the same tech stack and what we can re-use. 
* We should look into how the devcontainer overlaps with the docker setup
* Configuration: We should decide whether a dictionary or specific structure is sufficient for saving the params

## Data Pipeline
* We should identify whether computation occurs on page load or when the user requests (computation seems like it could take a while, and we don't necessarily want to hang)
## Test Cases
* Implement test cases for data pipeline 
* Implement test cases for display elements
## Miscillanea
* The name of the top-level class very likely needs to change to disambiguate from the live visualization. 
