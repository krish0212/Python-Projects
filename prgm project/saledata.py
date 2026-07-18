import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)

np.random.seed(42)

print(" Generating synthetic raw sales data...")
total_records = 10000
days_to_simulate = 365 * 2  # 2 Years of data
start_date = datetime(2024, 1, 1)

date_pool = [start_date + timedelta(days=x) for x in range(days_to_simulate)]

raw_data = {
    'Transaction_ID': range(10001, 10001 + total_records),
    'Date': np.random.choice(date_pool, size=total_records),
    'Product_Category': np.random.choice(
        ['Electronics', 'Clothing', 'Home & Kitchen', 'Books', 'Beauty'], 
        size=total_records, 
        p=[0.30, 0.25, 0.20, 0.15, 0.10]
    ),
    'Units_Sold': np.random.randint(1, 11, size=total_records),
    'Unit_Price': np.round(np.random.uniform(5.0, 600.0, size=total_records), 2)
}

# Load into a Pandas DataFrame
df = pd.DataFrame(raw_data)
print(" Processing data and extracting temporal features...")
df['Total_Revenue'] = df['Units_Sold'] * df['Unit_Price']
df['Date'] = pd.to_datetime(df['Date'])

df['Year'] = df['Date'].dt.year
df['Month_Name'] = df['Date'].dt.strftime('%b')  
df['Month_Num'] = df['Date'].dt.month            
df['Day_of_Week'] = df['Date'].dt.day_name()

print("\n First 5 rows of engineered dataset:")
print(df.head())

print("\n Executing Sales Trend Analysis over time...")

trend_df = df.groupby(['Year', 'Month_Num', 'Month_Name'])['Total_Revenue'].sum().reset_index()
trend_df = trend_df.sort_values(['Year', 'Month_Num'])
trend_df['Year_Month'] = trend_df['Year'].astype(str) + '-' + trend_df['Month_Name']

plt.figure(figsize=(14, 5))
sns.lineplot(data=trend_df, x='Year_Month', y='Total_Revenue', marker='o', color='#1f77b4', linewidth=2.5)
plt.title('Monthly Sales Revenue Trends (2-Year Timeline View)', fontsize=14, fontweight='bold')
plt.xlabel('Timeline (Year-Month)', fontsize=12)
plt.ylabel('Total Revenue ($)', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

print("\n Analyzing product category distribution and performance...")

product_perf = df.groupby('Product_Category').agg(
    Total_Revenue=('Total_Revenue', 'sum'),
    Total_Units_Sold=('Units_Sold', 'sum')
).sort_values(by='Total_Revenue', ascending=False).reset_index()

print("\nProduct Category Breakdown Summary Table:")
print(product_perf)

plt.figure(figsize=(10, 5))
sns.boxplot(
    data=df, 
    x='Product_Category', 
    y='Unit_Price', 
    hue='Product_Category',  
    palette='Set2',
    legend=False
)
plt.title('Total Revenue Generation by Product Category', fontsize=14, fontweight='bold')
plt.xlabel('Total Revenue Accumulated ($)', fontsize=12)
plt.ylabel('Product Category', fontsize=12)
plt.tight_layout()
plt.show()

print("\n Uncovering deep seasonal patterns (Month vs Day of Week)...")
seasonality_matrix = df.pivot_table(
    values='Total_Revenue', 
    index='Month_Name', 
    columns='Day_of_Week', 
    aggfunc='sum'
)
chronological_months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
standard_weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

seasonality_matrix = seasonality_matrix.reindex(index=chronological_months, columns=standard_weekdays)

plt.figure(figsize=(12, 7))
sns.heatmap(seasonality_matrix, annot=False, cmap='YlGnBu', linewidths=0.5, cbar_kws={'label': 'Total Sales ($)'})
plt.title('Seasonality Hotspots Matrix: Revenue Concentration across Time frames', fontsize=14, fontweight='bold')
plt.xlabel('Day of the Week', fontsize=12)
plt.ylabel('Month of the Year', fontsize=12)
plt.tight_layout()
plt.show()
print("\n Analysis pipeline complete. All graphics generated successfully!")