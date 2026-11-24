# QuickBite – Data Analyst Python Assessment

## Project Overview

This project focuses on cleaning, combining and analysing QuickBite's food delivery data.

QuickBite operates in Bengaluru, Hyderabad, Chennai and Mumbai. The objective is to transform raw data into a structured dataset and generate useful business insights related to area performance, customer food preferences and delivery partner performance.

## Dataset Description

The source dataset is `QuickBite_Assessment.xlsx`.

It contains six Excel sheets:

| Sheet Name | Description |
|---|---|
| areas | Contains area names, cities and zones |
| restaurants | Contains restaurant names, cuisines and area information |
| delivery_partners | Contains delivery partner and vehicle details |
| customers | Contains customer information |
| orders | Contains order, payment and delivery information |
| feedback | Contains customer ratings and comments |

## Project Tasks

### Task 1 – Data Cleaning

The following cleaning operations are performed:

- Removed duplicate records.
- Removed records with missing primary IDs.
- Removed unnecessary spaces from text values.
- Standardized city names and categorical values.
- Converted date and numeric columns into appropriate data types.
- Standardized order statuses and vehicle categories.

**Output file:** `cleaned_data/Quick_Bite_Data_Cleaning.xlsx`

This workbook contains the cleaned tables in separate sheets.

### Task 2 – Data Combining

The cleaned tables are joined using their common ID columns.

The orders table is used as the main table.

The following tables are joined:

- Customers using `customer_id`
- Restaurants using `restaurant_id`
- Areas using `area_id`
- Delivery partners using `partner_id`
- Feedback using `order_id`

Additional columns are created:

- `order_date`
- `order_time`
- `order_day`
- `is_late`

A delivery is classified as late when delivery time exceeds 45 minutes.

The final dataset contains the 19 columns specified in the assessment, with one row per order.

**Output file:** `cleaned_data/Quick_Bite_Combined_Data.xlsx`

### Task 3 – Data Analysis

The analysis is performed using only the combined dataset. Only delivered orders are considered.

#### 1. Area Performance

This analysis compares delivery areas based on:

- Total delivered orders
- Total revenue
- Average order value
- Average delivery time
- Number of late deliveries
- Late delivery percentage
- Average customer rating

Areas are ranked by revenue in descending order.

#### 2. Top Cuisine by Day

This analysis identifies the most popular cuisine for each day of the week.

The analysis includes:

- Day of the week
- Top cuisine
- Number of orders
- Total orders for the day
- Percentage share of orders

#### 3. Vehicle Performance

This analysis compares delivery vehicle types using:

- Total delivered orders
- Average delivery time
- Number of late deliveries
- Late delivery percentage
- Average customer rating

This helps compare delivery speed and reliability across vehicle types.

**Output file:** `analysis/Quick_Bite_Analysis.xlsx`

The workbook contains three sheets:
1. Area Performance
2. Top Cuisine by Day
3. Vehicle Performance

## Technologies Used

- Python
- Pandas
- NumPy
- Openpyxl

## Project Structure

```text
quickbite-assessment/
│
├── data/
│   └── QuickBite_Assessment.xlsx
│
├── scripts/
│   ├── cleaning.py
│   └── analysis.py
│
├── cleaned_data/
│   ├── Quick_Bite_Data_Cleaning.xlsx
│   └── Quick_Bite_Combined_Data.xlsx
│
├── analysis/
│   └── Quick_Bite_Analysis.xlsx
│
├── README.md
└── requirements.txt
```

## Installation

Install the required Python libraries:

```bash
pip install -r requirements.txt
```

Alternatively:

```bash
pip install pandas numpy openpyxl
```

## How to Run

### Step 1 – Data Cleaning and Combining

Run the following command from the project root directory:

```bash
python scripts/cleaning.py
```

This generates the cleaned Excel workbook and combined dataset.

### Step 2 – Business Analysis

Run:

```bash
python scripts/analysis.py
```

This generates the final analysis workbook containing all three business analyses.

## Conclusion

The project demonstrates how raw food delivery data can be cleaned, combined and analysed using Python and Pandas.

The resulting datasets and analysis reports can help the QuickBite operations team understand area revenue, customer cuisine preferences and delivery performance across different vehicle types.