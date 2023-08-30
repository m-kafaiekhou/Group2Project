

Installation
------------
To install this project all you need to do is: installing the dependencies from the requirements file. 
there is a good reason why you should consider installing using this method. since the version of the 
packages that we used are changing over time, using other versions of these packages could mean the 
program wont work properly so in order to avoid this problem we recommend installing dependencies using
the requirements file in order to get the exact version of  packages used for this project.

- First fork this project from (https://github.com/m-kafaiekhou/Group2Project.git)


- Clone the forked repo to you'r local storage
    
    ``git clone repo_adress``

- Make a virtual environment for the django project
    
    ``python3 -m venv .venv``

- Activate the venv like this.(Linux)

    ``source .venv/bin/activate``

- Now you can install the required packages using this method. in the root directory of the project:

    ``pip install -r requirements.txt``

this will automatically install all the tools and packages needed for the project, so the project could run.(Django will be installed as well)


**Django Version used for this project is v4.2.3**