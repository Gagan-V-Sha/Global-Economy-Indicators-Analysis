
# 📈 An Econometric Analysis of Economic Structure and Development

![Project Banner](link/to/your/banner.png)

## 📌 About the Project

This project explores the relationship between a country's economic structure and its level of development. I conducted an econometric analysis using Python on a global dataset, developing and applying statistical and visualization techniques to uncover key insights. The project showcases my skills in data cleaning, feature engineering, statistical modeling, and data-driven storytelling.

## 🚀 Research Question & Hypothesis

**Research Question:** How does a country's economic structure, as defined by the contribution of different sectors, relate to its overall economic development as measured by GDP per capita?

**Initial Hypothesis:** Based on foundational economic principles, I hypothesized that a higher share of a country's economy in the agricultural sector would be associated with a lower GDP per capita. Conversely, I expected a stronger presence of industrial and service sectors to correlate with higher economic development.

---

## 🛠️ Methodology and Data

### Data Source
The analysis uses the **Global Economy Indicators** dataset from Kaggle, which contains macroeconomic data for numerous countries over a span of several decades.

### Data Engineering
A key part of this project was transforming the raw data into a usable format. I developed a Python script that performed the following steps:
- **Data Cleaning**: Handled missing values and standardized column names to ensure data integrity.
- **Feature Engineering**: Created new variables critical for the analysis:
    - `GDP_per_capita`: Calculated by dividing a country's GDP by its population, providing a more accurate measure of economic development.
    - **Sectoral Shares**: Quantified the economic structure by calculating the percentage contribution of the agriculture, manufacturing, and transport/communication sectors to the total GDP.
    - **Income Group Classification**: Categorized each country into a World Bank income group (Low, Lower Middle, Upper Middle, and High) based on its GNI per capita to enable a more robust, comparative analysis.

---

## 📊 Results and Insights

The analysis confirmed the initial hypothesis, revealing a clear link between a country's economic structure and its level of development. The findings are supported by both quantitative analysis and compelling visualizations.

### 📈 Statistical Analysis
I used **Ordinary Least Squares (OLS) regression** and a more advanced **fixed-effects panel data analysis** to quantify the relationships. The results showed a statistically significant negative association between the share of a country's economy in the agricultural sector and its GDP per capita. The panel data model, which controls for unobserved country-specific factors, provided a more robust and trustworthy estimate of this relationship.

### 🖼️ Key Visualizations
Each visualization tells a different part of the story:

1.  **Bar Chart**: A high-level overview showing the stark difference in average GDP per capita across the four World Bank income groups. 
2.  **Line Plot**: Illustrates the different growth trajectories of each income group over time, highlighting how development paths diverge. 
3.  **Scatter Plots**: Visually represent the relationships quantified in the regression, showing the negative correlation between a sector's share of GDP and a country's GDP per capita. 
4.  **Box Plot**: Reveals the distribution and spread of GDP per capita within each income group, providing a nuanced view of global economic inequality. 
5.  **Facet Chart**: Compares the GDP per capita trends of a curated list of countries with comparable populations, visually proving that economic development is more strongly linked to income group than to population size. 

---

## 💻 How to Run the Code

1.  **Clone the repository**: `git clone https://github.com/your-username/global-economy-indicators-analysis.git`
2.  **Install dependencies**: `pip install pandas statsmodels matplotlib seaborn linearmodels`
3.  **Run the script**: `python project.py`
4.  Follow the interactive menu to perform a regression or generate a specific visualization.
