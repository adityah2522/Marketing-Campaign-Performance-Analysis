# 📊 Marketing Campaign Performance Analysis: A/B/C Testing & Regression

## 🎯 Project Overview
This project analyzes the performance of three different marketing promotions (A/B/C testing) across various market sizes and store locations. The goal is to determine the statistically significant "winner" to inform a nationwide marketing rollout.

Moving beyond basic A/B testing, this analysis progresses through three rigorous statistical phases: macro-level non-parametric testing, data stratification to uncover segmented trends, and multivariate linear regression (with interaction terms) to isolate the true financial impact of each campaign.

## 💡 Executive Summary & Business Recommendation
1. **The Core Winner (Promotion 3):** Promotion 3 is the optimal choice for a nationwide rollout. It dominates the most lucrative segment (Large Markets) and remains highly competitive in Small Markets. It offers the safest, highest-yielding return.
2. **The Niche Play (Promotion 2):** While Promotion 2 is a massive failure in Large and Medium markets, it overperforms significantly in **Small Markets**. If operational bandwidth allows for segmented marketing, Promo 2 should be deployed exclusively in Small markets.
3. **Irrelevant Factors:** Statistical testing confirms that `AgeOfStore` has zero impact on campaign success.

## 🔬 Methodology

### Phase 1: High-Level Non-Parametric Testing
* **Challenge:** Comparing 3 groups without assuming normal distribution or equal variance, while avoiding pseudo-replication from weekly data.
* **Solution:** Aggregated weekly data to ensure independence (1 row = 1 store), then applied the **Kruskal-Wallis H-test** and post-hoc **Mann-Whitney U tests** (with Bonferroni correction).
* **Initial Finding:** Promotions 1 and 3 resulted in a statistical tie for first place.

### Phase 2: Stratification & Deep Dive
* **Challenge:** Aggregated macro-level data can mask niche performance (a variation of Simpson's Paradox).
* **Solution:** Stratified the dataset by `MarketSize` (Small, Medium, Large) and ran independent non-parametric tests within each segment. 
* **Finding:** The "Tie" broke. Promo 3 dominates Large markets, Promo 1 wins Medium markets, and Promo 2 (the overall loser) unexpectedly wins Small markets.

### Phase 3: Multivariate Linear Regression
* **Challenge:** Formalizing the segmented findings into a single predictive mathematical model.
* **Solution:** Built an Ordinary Least Squares (OLS) Regression model.
* **Key Feature:** Included an **Interaction Term** (`Promotion * MarketSize`) to allow the model to calculate dynamic coefficients based on exactly where a campaign is deployed, proving mathematically that campaign success is dependent on market size.

## How to Run the Project

Clone this repository.

Ensure you have the required libraries installed:

pip install pandas numpy scipy statsmodels seaborn matplotlib
Open marketing_analysis.ipynb in Jupyter Notebook or JupyterLab.

Run all cells from top to bottom. (The notebook is 

## 📂 Project Structure
```text
marketing_campaign_project/
│
├── data/
│   └── raw_marketing_data.csv       # The dataset (IBM Watson Marketing Data)
│
├── src/
│   ├── __init__.py                  # Marks folder as a module
│   └── stats_utils.py               # Custom modular Python functions for statistical testing
│
└── marketing_analysis.ipynb       # Main presentation notebook detailing the data story


configured with %autoreload to seamlessly integrate with the src/ module).
