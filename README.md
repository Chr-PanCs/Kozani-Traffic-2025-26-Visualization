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
- By analyzing the dataset we were given, we approximated the increase in traffic due to ongoing Events in Kozani. To visualize this clearly we chose a histogram with a kernel density estimate for each one of the general Zones the events took place. The colors in this graph are specificaly chosen to accomodate for colorblind viewers since this is a dense graph and being able to easily compare colors is necessary. Also, for the same reason we chose the _"multiple=dodge"_ setting for the histogram so that the columns are not overlaping and having the columns stack wasn't chosen as well since it would change the kernel density estimate.


  
