# Kozani-Traffic-2025-26-Visualization
## A small project for MSc in Data Visualization using Python Pandas, Seaborne and Plotly

  - Two Datasets were given with statistics from the City of Kozani for the period 2025-2026 about local traffic and local events.

  - These datasets contained the following attributes:
<img width="1386" height="17" alt="image" src="https://github.com/user-attachments/assets/be0302cd-144b-479a-80f8-3a186245a0f0" />

  - After the dataset was combined and cleaned the following graphs were made.

### Daily Bike Trips in the City of Kozani with a Rolling 7 Day Mean
<img width="1000" height="600" alt="BikeTripsScatterRM" src="https://github.com/user-attachments/assets/059d18ef-f484-4bb2-ac9d-670230bbaa2f" />

  - The visualization of the Bike Trips was made using a scatter plot using *point markers* with *decreased opacity*  ("alpha" variable) again for clarity reasons due to their proximity and large variance.  For this graph due to the large deviation of neighboring data points we chose to include a *7-Day Rolling Mean Line*  of the Data to increase clarity and make it possible to show the trend our data follows throughout the yearly change of the seasons with ease.

### Traffic Count mean and Parking Occupancy mean per Day of the Week in Kozani
<img width="640" height="480" alt="ParkingOccupancyMean%perDay" src="https://github.com/user-attachments/assets/8ba5a04f-6ee5-4961-a2ec-b1933e64af3b" />

  - In this barplot we show two different metrics per each Day of the week in order to  see the relevance in these two metrics when they are grouped per day. We used a light palette of colors with enough saturation and opacity to make them discernible but pleasing to the eyes as well. Also, we cut off the y-axis below the thirteen thousand mark for a more compact graph.

  - Additionally, a barplot was used instead of a pie chart for this visualization because we weren't interested in comparing normalized data since five out of our seven days have similar traffic counts, neither Parking Occupancy % translates well when normalized. Plus, showing two different metrics per day would not have been effective by using a pie chart.

### Traffic Increase in Kozani due to ongoing Events in the 4 General Zones of Kozani
<img width="638" height="500" alt="TrafficIncreasePerEvent" src="https://github.com/user-attachments/assets/24e582fc-adb0-4ea0-8082-0681736bca73" />

  - By analyzing the dataset we were given, we approximated the increase in traffic due to ongoing Events in Kozani. To visualize this clearly we chose a histogram with a kernel density estimate for each one of the general Zones the events took place. The colors in this graph are specificaly chosen to accomodate for colorblind viewers since this is a dense graph and being able to easily compare colors is necessary. Also, for the same reason we chose the "multiple=dodge" setting for the histogram so that the columns are not overlaping and having the columns stack wasn't chosen as well since it would change the kernel density estimate.

## Interactive Environment for Optical Analysis

  - Using python Dash interactive elements were created for deeper comprehension of the dataset by the user
    <img width="1070" height="628" alt="Screenshot_20260530_223408" src="https://github.com/user-attachments/assets/5509cbf3-b0d6-48e1-a0fe-c929d6efa507" />
    
<img width="823" height="503" alt="Screenshot_20260530_231316" src="https://github.com/user-attachments/assets/67a49c64-6fb5-4879-9e5d-b8577756144e" />


## An Immersive Proposal

  - Having observed the previous  two-dimensional graphs (2D) we can clearly understand the usefullness of such datasets for City planning and more so different Visualizations of these datasets.
  - The next meaningfull step is the combination of the city's 3D rendering, different overlays using the datasets we can create according to each need and VR/AR technologies to properly view and interact with the visuals.
  - The combination of all three mentioned before will have immediate impact in many different sectors such as City Planning, Construction, Entrepreneurship and many others. Using such immersive tools enables the user to explore his City from every angle using different overlays, offering an enriched visual engagement. Accompanying that, the user's perception of the whole City broadens leading to an amplified user cognition.
  - Examples of everyday use that will benefit from these tools are City planners that will be able to easily choose the best place for their next scheduled Event, or where a Bike lane, City Parking is needed to ease traffic.  Also, an enterpreneur by using such tool will have a more detailed overview of the City, enabling him to bring new ideas to life and new capital to the City.  Another need for tools like these surfaced during the prior Covid outbreak. For scientists, being able to do a complex analysis with easy and practical visualization of different variables  inside a City is irreplaceable and mandatory for fast and reliable results. Crisis management is not only needed for diseases such as Covid but for Enviromental Crisis such as earthquakes floods and wildfires. Such tools at the hands of first responders like the Fire Department and Police are needed not only during a crisis but also for the prevention of such events.
  
## Example of a VR Overlay

<img width="1168" height="784" alt="VR_Overlay" src="https://github.com/user-attachments/assets/cf3647aa-6903-4975-998e-74787862248f" />
