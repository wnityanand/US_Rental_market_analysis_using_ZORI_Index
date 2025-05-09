
## **US rental market analysis using ZORI index data**  


This project automates the analysis of Zillow's ZORI data to identify rental market growth trends across the US from 2021-2025. This ie event driven pipeline, triggered by manual file uploads to S3, uses AWS Glue for ETL, Athena for SQL analytics, and Grafana for visualization, providing insights into market volatility and regional rental growth.

ZORI Index:
The Zillow Observed Rent Index (ZORI) is calculated to show how typical rents are changing over time in a specific area, like a city or metro region.
ZORI is like a rent thermometer for a city, showing whether rents are heating up or cooling down, based on how much the same homes rents are changing from one rental to the next. This method helps give a clearer, less biased picture of real rent trends.

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

## Tech stack
• **Data Source**: Zillow ZORI data  
• **Storage**: Amazon S3  
• **Compute**: AWS Glue  
• **Orchestration**: AWS Glue Workflows, EventBridge Rule  
• **Analytics**: Amazon Athena  
• **Visualization**: Grafana

![Architecture Diagram](https://raw.githubusercontent.com/wnityanand/US_Rental_market_analysis_using_ZORI_Index/main/AWS_Architecture.png)

## Data Ingestion
**1.S3 Bucket structure**

The **Zillow_data_input** S3 bucket is organized into three main subfolders to support efficient data processing and tracking:

**Unprocess_file:**
This folder stores all newly uploaded files that have not yet been processed. It serves as the initial landing zone for raw data.

**Transformed_data:**
After a file is picked up by an AWS Glue job, it is transformed and partitioned. The resulting processed files are saved in this folder, ready for downstream analytics.

**Process_file:**
Once a raw file has been successfully processed and cataloged by the AWS Glue Crawler, it is moved to this folder for archival purposes. This helps maintain a clear record of all files that have completed the ETL and cataloging process.

This folder structure ensures clear separation between raw, processed, and archived data, enabling robust data management and traceability throughout the pipeline.

## Data Ingestion and Transformation Workflow

The project implements an automated pipeline for processing Zillow ZORI data using AWS services. The workflow is as follows:

1. **File Transfer & Organization:**  
   An AWS Glue ETL job moves new data files from the source S3 bucket to the `Zillow_data_input/unprocess_file` subfolder. This job ensures data integrity by verifying successful transfers before deleting the original files from the source bucket.

2. **Event-Driven Processing:**  
   When a file lands in the `unprocess_file` subfolder, an EventBridge rule triggers an AWS Glue workflow for real-time processing.

3. **Data Transformation:**  
   - The **AWS Glue ETL job** unpivots the data: monthly ZORI columns (e.g., `2015-01-31`, `2015-02-28`, ..., `2025-03-31` from the sample CSV) are converted into two columns, `Date` and `ZORI`, making the dataset more suitable for analytics.
   - Transformed and partitioned data is written to the `transformed_data` subfolder.

**Example of Unpivoting (performed by the Glue Job):**

| RegionID | RegionName   | 2021-01-31 | 2021-02-28 | ... |
|----------|--------------|------------|------------|-----|
| 102001   | United States | 1479.84    | 1488.12    | ... |

**Becomes:**

| RegionID | RegionName   | Date       | ZORI     |
|----------|--------------|------------|----------|
| 102001   | United States | 2021-01-31 | 1479.84  |
| 102001   | United States | 2021-02-28 | 1488.12  |
| ...      | ...          | ...        | ...      |

4. **Archival:**  
   Once transformation is complete, the original raw file is moved to the `process_file` subfolder for archival and traceability.

5. **Schema Cataloging:**  
   The AWS Glue Crawler scans the transformed data, infers the schema (column names, data types, etc.), and updates the Glue Data Catalog. This enables seamless querying in Amazon Athena and supports downstream analytics and visualization.

**Workflow Summary:**  
File uploaded to source S3 bucket → Glue ETL job moves file to `unprocess_file` (verifies & deletes source) → EventBridge triggers Glue workflow → **Glue job** transforms data and saves to `transformed_data` → Raw file archived in `process_file` → Glue Crawler updates Data Catalog.

![Glue workflow Diagram](https://raw.githubusercontent.com/wnityanand/US_Rental_market_analysis_using_ZORI_Index/main/AWS_Architecture/Glue_workflow.png)


![Eventbridge rule Diagram](https://raw.githubusercontent.com/wnityanand/US_Rental_market_analysis_using_ZORI_Index/main/AWS_Architecture/Eventbridge_rule.png)

## Data Visualization using Grafana Dashboard

1. **Data Source Connection:** Grafana was configured to connect directly to Amazon Athena, using the AWS Glue Data Catalog as the metadata repository. This allowed the dashboard to query the transformed ZORI data seamlessly.
2. **Athena Query Development and Testing:** I built and tested the SQL queries in Amazon Athena to ensure accurate and efficient data retrieval. These queries were then integrated into Grafana.
3. **SQL Query Integration:** The Athena SQL queries, specifically those designed to identify and rank volatile markets, were incorporated into individual panels within the Grafana dashboard.

The Grafana dashboard provides a user-friendly interface for monitoring and analyzing rental market trends, derived from the data pipeline and analytical queries.

![Preview](Data_Visualization/Zori_Preview%20.png)[PDF Copy of Visualization](https://raw.githubusercontent.com/wnityanand/US_Rental_market_analysis_using_ZORI_Index/main/Data_Visualization/Zori_index_analysis.pdf)

![V1](https://raw.githubusercontent.com/wnityanand/US_Rental_market_analysis_using_ZORI_Index/main/Data_Visualization/Most_stable_and_volatile_market.PNG)
![V1](https://raw.githubusercontent.com/wnityanand/US_Rental_market_analysis_using_ZORI_Index/main/Data_Visualization/rental_growth_in_usa.PNG)
![V1](https://raw.githubusercontent.com/wnityanand/US_Rental_market_analysis_using_ZORI_Index/main/Data_Visualization/Intercities_rent_analysis.png)


## Key Findings:

*   **Most Stable Markets:** Cleveland, OH, and Philadelphia, PA, are identified as the most stable rental markets based on ZORI fluctuations.
*   **Most Volatile Markets:** Edwards, CO, and Jackson, WY, are among the most volatile, attributed to smaller inventories and seasonal demand.
*   **National Rent Growth:** The ZORI in the USA has increased approximately 3.5% over the past year (compared to March 2025).
*   **Highest Share of National Rent by State:** Hawaii (HI) and California (CA) have the highest share of the national rent.
*   **Fastest Growing Rental Markets (Year-over-Year):** Rock Springs, WY, and Shelton, WA, exhibit the highest year-over-year rental growth.
*   **States with Highest Cumulative Rent Growth (2021-2025):** Wyoming (WY) and Hawaii (HI) experienced the highest cumulative growth from 2021-2025.

**Note:** This analysis uses Zillow's Observed Rent Index (ZORI) to provide a comprehensive view of rental market dynamics, considering factors beyond just rent price changes.






















