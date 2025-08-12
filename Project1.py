import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from linearmodels import PanelOLS

# Suppress SettingWithCopyWarning and other warnings
warnings.simplefilter(action='ignore', category=pd.errors.SettingWithCopyWarning)
warnings.simplefilter(action='ignore', category=UserWarning)

# ==============================================================================
# All Project Functions
# ==============================================================================

def data_preparation(file_path):
    """Loads, cleans, and prepares the dataset."""
    try:
        df = pd.read_csv(file_path, encoding='latin1')
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found. Please ensure it is in the same directory as the script.")
        return None
        
    df.columns = df.columns.str.strip()
    
    columns_to_keep = [
        'Country', 'Year', 'Population', 'Gross Domestic Product (GDP)',
        'Per capita GNI', 'Agriculture, hunting, forestry, fishing (ISIC A-B)',
        'Manufacturing (ISIC D)', 'Transport, storage and communication (ISIC I)'
    ]
    new_column_names = {
        'Gross Domestic Product (GDP)': 'GDP',
        'Agriculture, hunting, forestry, fishing (ISIC A-B)': 'Agriculture',
        'Manufacturing (ISIC D)': 'Manufacturing',
        'Transport, storage and communication (ISIC I)': 'Transport_Comm'
    }
    df_cleaned = df[columns_to_keep].rename(columns=new_column_names)
    df_cleaned.dropna(inplace=True)
    
    return df_cleaned

def feature_engineering(df):
    """Creates new variables from the prepared data."""
    def classify_income_group(gni):
        if gni <= 1145:
            return 'Low income'
        elif gni <= 4515:
            return 'Lower middle income'
        elif gni <= 14005:
            return 'Upper middle income'
        else:
            return 'High income'
    
    df['Income_Group'] = df['Per capita GNI'].apply(classify_income_group)
    df['GDP_per_capita'] = df['GDP'] / df['Population']
    df['Agriculture_Share'] = (df['Agriculture'] / df['GDP']) * 100
    df['Manufacturing_Share'] = (df['Manufacturing'] / df['GDP']) * 100
    df['Transport_Comm_Share'] = (df['Transport_Comm'] / df['GDP']) * 100
    
    return df

def perform_regression(df):
    """Performs OLS regression and prints the summary."""
    print("\n--- OLS Regression Analysis Summary ---")
    y = df['GDP_per_capita']
    X = df[['Agriculture_Share', 'Manufacturing_Share', 'Transport_Comm_Share']]
    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit()
    print(model.summary())
    with open('regression_summary.txt', 'w') as f:
        f.write(model.summary().as_text())
    print("\nRegression summary saved to 'regression_summary.txt'.")
    return model

def perform_panel_analysis(df):
    """Performs fixed-effects panel data analysis."""
    print("\n--- Fixed-Effects Panel Data Analysis Summary ---")
    
    # Set the panel data index for the model
    df_panel = df.set_index(['Country', 'Year'])
    
    # Define dependent and independent variables for the panel model
    dependent = df_panel['GDP_per_capita']
    exog = df_panel[['Agriculture_Share', 'Manufacturing_Share', 'Transport_Comm_Share']]
    
    # Fit the panel model with fixed effects for countries
    panel_model = PanelOLS(dependent=dependent, exog=exog, entity_effects=True)
    panel_results = panel_model.fit()
    
    print(panel_results)
    with open('panel_regression_summary.txt', 'w') as f:
        f.write(str(panel_results)) # Corrected line
    print("\nPanel regression summary saved to 'panel_regression_summary.txt'.")

def get_comparable_countries(df):
    """Programmatically selects a set of countries with comparable populations."""
    print("\nSelecting countries with comparable populations...")
    
    avg_population = df.groupby('Country')['Population'].mean().reset_index()
    
    min_population = 10000000
    max_population = 50000000
    
    comparable_countries_df = avg_population[
        (avg_population['Population'] >= min_population) & (avg_population['Population'] <= max_population)
    ]
    
    country_income_map = df[['Country', 'Income_Group']].drop_duplicates()
    comparable_countries_df = pd.merge(comparable_countries_df, country_income_map, on='Country', how='left')
    
    selected_countries = []
    groups = ['High income', 'Upper middle income', 'Lower middle income', 'Low income']
    
    for group in groups:
        group_countries = comparable_countries_df[comparable_countries_df['Income_Group'] == group]['Country'].unique()
        if len(group_countries) > 0:
            selected_countries.extend(group_countries[:3])
    
    return selected_countries

def visualize_data(df, vis_choice, selected_countries):
    """Generates visualizations based on user choice."""
    print("\nGenerating Visualizations...")

    if vis_choice == '1':
        print("Generating Bar Chart...")
        avg_gdp_by_income = df.groupby('Income_Group')['GDP_per_capita'].mean().reset_index()
        avg_gdp_by_income.sort_values(by='GDP_per_capita', ascending=False, inplace=True)
        plt.figure(figsize=(12, 8))
        sns.barplot(x='Income_Group', y='GDP_per_capita', data=avg_gdp_by_income, palette='viridis')
        plt.title('Average GDP per Capita by World Bank Income Group', fontsize=16)
        plt.xlabel('Income Group', fontsize=12)
        plt.ylabel('Average GDP per Capita (USD)', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig('gdp_by_income_group_bar_chart.png')
        print("Bar chart saved to 'gdp_by_income_group_bar_chart.png'.")

    elif vis_choice == '2':
        print("\nGenerating Line Plot...")
        avg_gdp_by_income_year = df.groupby(['Year', 'Income_Group'])['GDP_per_capita'].mean().reset_index()
        plt.figure(figsize=(12, 8))
        sns.lineplot(data=avg_gdp_by_income_year, x='Year', y='GDP_per_capita', hue='Income_Group', palette='viridis')
        plt.title('Average GDP per Capita by Income Group Over Time', fontsize=16)
        plt.xlabel('Year', fontsize=12)
        plt.ylabel('Average GDP per Capita (USD)', fontsize=12)
        plt.tight_layout()
        plt.savefig('gdp_by_income_group_line_plot.png')
        print("Line plot saved to 'gdp_by_income_group_line_plot.png'.")

    elif vis_choice == '3':
        if not selected_countries:
            print("No countries selected for the facet chart. Please select countries first.")
            return

        print("\nGenerating Facet Chart...")
        df_filtered = df[df['Country'].isin(selected_countries)].copy()
        
        income_group_order = ['High income', 'Upper middle income', 'Lower middle income', 'Low income']
        df_filtered['Income_Group'] = pd.Categorical(df_filtered['Income_Group'], categories=income_group_order, ordered=True)
        
        g = sns.relplot(
            data=df_filtered,
            x='Year',
            y='GDP_per_capita',
            col='Country',
            row='Income_Group',
            kind='line',
            hue='Income_Group',
            height=3,
            aspect=1.5,
            facet_kws={'sharey': False}
        )
        
        group_y_limits = {
            'High income': (0, df_filtered[df_filtered['Income_Group'] == 'High income']['GDP_per_capita'].max() * 1.1),
            'Upper middle income': (0, df_filtered[df_filtered['Income_Group'] == 'Upper middle income']['GDP_per_capita'].max() * 1.1),
            'Lower middle income': (0, df_filtered[df_filtered['Income_Group'] == 'Lower middle income']['GDP_per_capita'].max() * 1.1),
            'Low income': (0, df_filtered[df_filtered['Income_Group'] == 'Low income']['GDP_per_capita'].max() * 1.1),
        }
        
        for ax in g.axes.flat:
            row_title = ax.get_title()
            if '|' in row_title:
                group_name = row_title.split(' | ')[0].split(' = ')[1]
                if group_name in group_y_limits:
                    ax.set_ylim(group_y_limits[group_name])

        plt.suptitle('GDP per Capita Trends for Selected Countries (1970-2023)', fontsize=16, y=1.02)
        g.fig.tight_layout()
        g.set_titles(col_template="{col_name}")

        plt.legend(
            title='Income Group',
            loc='center left',
            bbox_to_anchor=(1.02, 0.5),
            ncol=1
        )
        
        plt.savefig('gdp_comparative_facet_chart.png', bbox_inches='tight')
        print("Facet chart saved to 'gdp_comparative_facet_chart.png'.")

    elif vis_choice == '4':
        print("\nGenerating Scatter Plot...")
        
        fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=True)

        sectors = ['Agriculture_Share', 'Manufacturing_Share', 'Transport_Comm_Share']
        titles = ['Agriculture Share vs. GDP per Capita', 'Manufacturing Share vs. GDP per Capita', 'Transport & Comm. Share vs. GDP per Capita']

        for i, ax in enumerate(axes):
            sns.scatterplot(
                data=df,
                x=sectors[i],
                y='GDP_per_capita',
                hue='Income_Group',
                palette='viridis',
                alpha=0.6,
                ax=ax
            )
            ax.set_title(titles[i], fontsize=14)
            ax.set_xlabel(f'{sectors[i].replace("_Share", " Share")} of GDP (%)', fontsize=12)
            ax.set_ylabel('GDP per Capita (USD)', fontsize=12)
            ax.legend(title='Income Group', loc='upper right')

        plt.tight_layout()
        plt.savefig('sectoral_impact_scatter_plots.png')
        print("Scatter plots saved to 'sectoral_impact_scatter_plots.png'.")

    elif vis_choice == '5':
        print("\nGenerating Box Plot...")
        plt.figure(figsize=(12, 8))
        sns.boxplot(
            data=df,
            x='Income_Group',
            y='GDP_per_capita',
            palette='viridis'
        )
        plt.title('Distribution of GDP per Capita by Income Group', fontsize=16)
        plt.xlabel('Income Group', fontsize=12)
        plt.ylabel('GDP per Capita (USD)', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig('gdp_by_income_group_boxplot.png')
        print("Box plot saved to 'gdp_by_income_group_boxplot.png'.")
    else:
        print("Invalid visualization choice.")

def main():
    print("--- Interactive Data Analysis and Visualization ---")
    
    file_path = 'Global Economy Indicators.csv'
    df_clean = data_preparation(file_path)
    
    if df_clean is None:
        return
        
    df_engineered = feature_engineering(df_clean)
    
    selected_countries = get_comparable_countries(df_engineered)
    
    while True:
        print("\nWhat would you like to do?")
        print("1. Perform Statistical Analysis (OLS Regression)")
        print("2. Generate a Visualization")
        print("3. Perform Panel Data Analysis")
        print("4. Exit")
        
        choice = input("Enter your choice (1, 2, 3, or 4): ")
        
        if choice == '1':
            perform_regression(df_engineered)
        elif choice == '2':
            vis_choice = input("Which visualization? (1: Bar Plot, 2: Line Plot, 3: Facet Chart, 4: Scatter Plot, 5: Box Plot): ")
            visualize_data(df_engineered, vis_choice, selected_countries)
        elif choice == '3':
            perform_panel_analysis(df_engineered)
        elif choice == '4':
            print("Exiting script.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()