#Allergy Project

----

### Summary

Collaborative project to build a web application that will take in an individual's allergy profile and then provide an easy search tool on products to give a yes or no on whether that product is good for the person.

This is open source and contributions are welcome. 

To use (command line commands written below directions):
```bash
    # Clone repsitory into a folder
    git clone https://github.com/nyghtowl/Allergy_Project.git
    # Setup virtualenv
    virtualenv env
    # Start virtualenv
    source env/bin/activate
    # Install requirements document
    pip install -r requirements.txt 
    # Create a local postgresql database called allergy_db (find or setup superuser)
    createdb -O <superuser> <dbname>
    # Define config keys locally in activate file under env/bin
    # Run files with python
    python run.py


```

----

### Top of List To Do

- Build page content and views
	- Home / Search Results
		- Simple search with predictive text
		- Allow search despite login
			- Login provides results based on profile
			- Not logged in provides product information
	- Create Account / Profile 
		- General account info
			- name
			- address (op)
			- phone (op)
			- m/f (op)
			- age (op)
			- ...
		- Search and add allergies
			- top ten allergies 
			- search area to add allergies w/ predictive text 
				- make predictions based on previous choices
			- indicate range of allergy (e.g. high, medium, low)
	- Login 
		- use oauth (twitter, fb, github, ...)


- Build data structure 
	- User standard details
	- Personal sensativity list
	- Standard allergy list
	- Reference links 
		- user to allergy list
		- sensativity to allergy and user

- Integrate Factual API
	- It includes string ingredients, product name and upc code

- Legal stuff
	- Disclaimers for functionality limits based on data (user input and api provided)

- Develop Logo

- Future
	- enable tracking of diet or other factors to track reactions
	- Provide filters for product search
	- go mobile