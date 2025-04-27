
## **US rental market analysis using ZORI index data**  


This project automates the analysis of Zillow's ZORI data to identify rental market stability and growth trends across the US from 2021-2025. The data pipeline, triggered by manual file uploads to S3, uses AWS Glue for ETL, Athena for SQL analytics, and Grafana for visualization, providing insights into market volatility and regional rental growth.

ZORI Index:
The Zillow Observed Rent Index (ZORI) is calculated to show how typical rents are changing over time in a specific area, like a city or metro region.
ZORI is like a rent thermometer for a city, showing whether rents are heating up or cooling down, based on how much the same homes’ rents are changing from one rental to the next. This method helps give a clearer, less biased picture of real rent trends.

About the dataset:
This data is taken from https://www.zillow.com/research/data/ website where Zillow update this data every 16th of each month. I downloaded and loaded csv manually into s3 bucket.

## 📊 Project Overview
Automated pipeline analyzing Zillow's ZORI Index data to:
- Identify most stable/unstable rental markets
- Calculate percentage of change in ZORI over last year
- Identify fastest growing rental markets (year over year growth)
- Visualize rent growth rates across regions (2021-2025)
- Identify top 10 states with highest cumulative rent growth
- Analyze Intercities rent

## **Tech stack**  
• Data Source: Zillow ZORI data  
• Storage: Amazon S3  
• Compute: AWS Glue  
• Orchestration: AWS Glue Workflows, EventBridge Rule  
• Analytics: Amazon Athena  
• Visualization: Grafana

![Architecture Diagram] (AWS_Architecture.png)




