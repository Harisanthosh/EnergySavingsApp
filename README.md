# EnergySavingsApp
A data science project to demonstrate with actual Industry data coming from the PPC department and optimizing the order flow of the FischerTechnik

# Prerequisites:
Make sure to have the FischerTechnik Setup running, power on all the Raspberry PI's, start the program in the TXT Controller and ensure the local REST Server is running.


# Steps to Run the project:

1. Install all the dependencies needed using pip install -r requirements.txt
2. Run the Energy API by setting up the Flask server
		--> set FLASK_APP=energy_api.py
		--> python -m flask run
3. Run the dashboard application by launching the dashboard_energy.py
		python dashboard_energy.py
4. Run the storage api which stores the energy readings when the order is placed by
		python store_energy.py
5. Alltogether all these three Python scripts will be executed simulataneously for the succesfull execution of the program
		

The application will be launched and running in the port 8050 (http://localhost:8050/)
		
		
		
