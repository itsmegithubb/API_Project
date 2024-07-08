# main.py

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64
from scipy.stats import chi2_contingency, ttest_ind, f_oneway

app = FastAPI()

origins = [
    "http://127.0.0.1:7000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load dataset
df = pd.read_csv('./cleaned-data-set.csv')

class StatTestRequest(BaseModel):
    test_type: str
    variables: list

@app.get("/api/data")
def get_data():
    return df.to_dict(orient='records')

@app.get("/api/summary")
def get_summary():
    summary = {
        "mean": df.mean(numeric_only=True).to_dict(),
        "median": df.median(numeric_only=True).to_dict(),
        "mode": df.mode().iloc[0].to_dict(),
        "variance": df.var(numeric_only=True).to_dict(),
        "std_dev": df.std(numeric_only=True).to_dict(),
        # "range": {col: df[col].max() - df[col].min() for col in df.select_dtypes(include=[np.number]).columns},
        # "quartiles": {col: df[col].quantile([0.25, 0.5, 0.75]).to_dict() for col in df.select_dtypes(include=[np.number]).columns}
    }
    return summary

@app.get("/api/visualization")
def get_visualization(type: str, var1: str = None, var2: str = None):
    plt.figure(figsize=(10, 6))
    if type == "histogram" and var1:
        sns.histplot(df[var1])
    elif type == "bar" and var1:
        sns.countplot(x=df[var1])
    elif type == "scatter" and var1 and var2:
        sns.scatterplot(x=df[var1], y=df[var2])
    else:
        raise HTTPException(status_code=400, detail="Invalid visualization type or variables")

    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    return {"image": img_base64}

@app.get("/api/correlation")
def get_correlation():
    # corr_matrix = df.corr().to_dict()
    corr_matrix = df.to_dict()
    return {"correlation_matrix": corr_matrix}

@app.post("/api/stat_tests")
def perform_stat_tests(request: StatTestRequest):
    if request.test_type == "chi-square" and len(request.variables) == 2:
        contingency_table = pd.crosstab(df[request.variables[0]], df[request.variables[1]])
        chi2, p, dof, ex = chi2_contingency(contingency_table)
        result = {"chi2_statistic": chi2, "p_value": p}
    elif request.test_type == "t-test" and len(request.variables) == 2:
        group1 = df[request.variables[0]]
        group2 = df[request.variables[1]]
        t_stat, p = ttest_ind(group1, group2, nan_policy='omit')
        result = {"t_statistic": t_stat, "p_value": p}
    elif request.test_type == "anova" and len(request.variables) > 2:
        groups = [df[var].dropna() for var in request.variables]
        f_stat, p = f_oneway(*groups)
        result = {"f_statistic": f_stat, "p_value": p}
    else:
        raise HTTPException(status_code=400, detail="Invalid test type or variables")
    return result

@app.post("/api/preprocess")
def preprocess_data():
    # Example preprocessing steps
    df_cleaned = df.dropna()
    numeric_cols = df_cleaned.select_dtypes(include='number').columns
    df_cleaned[numeric_cols] = (df_cleaned[numeric_cols] - df_cleaned[numeric_cols].mean()) / df_cleaned[numeric_cols].std()
    return df_cleaned.to_dict(orient='records')

@app.get("/api/patterns")
def detect_patterns():
    # Example pattern detection: Outliers using Z-score
    df_outliers = df[(np.abs(df.select_dtypes(include=[np.number])) > 3).any(axis=1)]
    return df_outliers.to_dict(orient='records')

@app.get("/api/insights")
def get_insights():
    insights = {
        "top_earners": df.nlargest(5, 'earnings').to_dict(orient='records'),
        "most_hours": df.nlargest(5, 'Hours').to_dict(orient='records')
    }
    return insights

@app.get("/api/limitations")
def get_limitations():
    limitations = {
        "data_completeness": df.isnull().sum().to_dict(),
        "scope_of_conclusions": "The dataset is limited to the responses collected and may not be representative of the entire population.",
        "future_research": "Further studies could expand the sample size and explore additional variables."
    }
    return limitations

@app.get("/api/future_research")
def future_research():
    future_research_suggestions = {
        "new_research_questions": [
            "How do gaming habits vary across different age groups?",
            "What are the long-term effects of gaming on mental health?"
        ],
        "areas_for_deeper_investigation": [
            "Investigate the correlation between gaming and academic performance.",
            "Explore the impact of gaming on social skills development."
        ]
    }
    return future_research_suggestions

# To run the app, use the following command in the terminal:
# uvicorn main:app --reload
