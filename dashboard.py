# dashboard.py

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.subplots as sp
import plotly.graph_objects as go

# -----------------------------
# Load Data
# -----------------------------
df = pd.read_csv("sales_data1.csv", parse_dates=["Date"])  # ensure Date is parsed

# -----------------------------
# Seaborn Statistical Plots
# -----------------------------

# Box Plot: Total Sales by Product
plt.figure(figsize=(8,6))
sns.boxplot(x='Product', y='Total_Sales', data=df, palette="Set2")
plt.title('Total Sales Distribution by Product')
plt.savefig("visualizations/boxplot.png")
plt.close()

# Violin Plot: Total Sales by Region
plt.figure(figsize=(8,6))
sns.violinplot(x='Region', y='Total_Sales', data=df, palette="muted")
plt.title('Total Sales Distribution by Region')
plt.savefig("visualizations/violinplot.png")
plt.close()

# Heatmap: Correlation between numerical columns
plt.figure(figsize=(10,8))
corr = df[['Quantity','Price','Total_Sales']].corr()
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
plt.title('Correlation Heatmap')
plt.savefig("visualizations/heatmap.png")
plt.close()

# Multi-plot Grid
fig, axes = plt.subplots(2,2, figsize=(12,10))

# Barplot: Average Sales per Product
sns.barplot(x='Product', y='Total_Sales', data=df, ax=axes[0,0], estimator=sum)
axes[0,0].set_title("Total Sales by Product")

# Lineplot: Sales Trend Over Time
sns.lineplot(x='Date', y='Total_Sales', data=df, ax=axes[0,1])
axes[0,1].set_title("Sales Trend Over Time")

# Scatterplot: Price vs Total Sales
sns.scatterplot(x='Price', y='Total_Sales', hue='Region', data=df, ax=axes[1,0])
axes[1,0].set_title("Price vs Total Sales by Region")

# Countplot: Customer Segments (Region as proxy)
sns.countplot(x='Region', data=df, ax=axes[1,1])
axes[1,1].set_title("Customer Count by Region")

plt.tight_layout()
plt.savefig("visualizations/multi_plot.png")
plt.close()

# -----------------------------
# Plotly Interactive Visualizations
# -----------------------------

# Interactive Scatter: Price vs Total Sales
fig1 = px.scatter(df, x="Price", y="Total_Sales", color="Region",
                  hover_data=["Product","Customer_ID"], title="Interactive Price vs Total Sales")
fig1.write_html("visualizations/interactive_scatter.html")

# Interactive Line Chart: Sales Trend by Region
fig2 = px.line(df, x="Date", y="Total_Sales", color="Region",
               title="Sales Trend by Region")
fig2.write_html("visualizations/interactive_line.html")

# Interactive Dashboard Layout
fig = sp.make_subplots(rows=2, cols=2,
                       subplot_titles=("Price vs Sales", "Sales Trend", "Product Sales", "Region Customers"))

# Scatter
fig.add_trace(go.Scatter(x=df["Price"], y=df["Total_Sales"], mode="markers",
                         marker=dict(color=df["Region"].astype('category').cat.codes),
                         name="Price vs Sales"), row=1, col=1)

# Line
fig.add_trace(go.Scatter(x=df["Date"], y=df["Total_Sales"], mode="lines", name="Sales Trend"), row=1, col=2)

# Product Sales Bar
product_sales = df.groupby("Product")["Total_Sales"].sum().reset_index()
fig.add_trace(go.Bar(x=product_sales["Product"], y=product_sales["Total_Sales"], name="Product Sales"), row=2, col=1)

# Region Customer Count
# Region Customer Count
region_counts = df["Region"].value_counts().reset_index()
region_counts.columns = ["Region", "Count"]

fig.add_trace(go.Bar(
    x=region_counts["Region"], 
    y=region_counts["Count"], 
    name="Region Customers"
), row=2, col=2)

fig.update_layout(title_text="Interactive Sales Dashboard", height=800, width=1000)
fig.write_html("visualizations/dashboard.html")

print("Dashboard created successfully! Check the visualizations folder.")
