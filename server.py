from mcp.server.fastmcp import FastMCP
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
import sys
import os

print("Starting Data Scientist MCP Server...", file=sys.stderr)

mcp = FastMCP("data-scientist-server")

# -----------------------
# Dataset Cache
# -----------------------

DATA_CACHE = {}


def load_df(file_path: str):
    """Load dataset with caching."""
    try:

        if file_path in DATA_CACHE:
            return DATA_CACHE[file_path]

        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)

        elif file_path.endswith((".xlsx", ".xls")):
            df = pd.read_excel(file_path)

        elif file_path.endswith(".json"):
            df = pd.read_json(file_path)

        else:
            raise ValueError("Unsupported file format")

        DATA_CACHE[file_path] = df
        return df

    except Exception as e:
        return {"error": str(e)}


# -----------------------
# Dataset Overview
# -----------------------

@mcp.tool()
def dataset_overview(file_path: str):
    """Return dataset structure and preview."""
    df = load_df(file_path)

    if isinstance(df, dict):
        return df

    return {
        "rows": int(len(df)),
        "columns": list(df.columns),
        "dtypes": {c: str(t) for c, t in df.dtypes.items()},
        "preview": df.head(10).to_dict()
    }


@mcp.tool()
def dataset_summary(file_path: str):
    """Statistical summary."""
    df = load_df(file_path)

    if isinstance(df, dict):
        return df

    return df.describe(include="all").to_dict()


@mcp.tool()
def missing_values(file_path: str):
    """Check missing values."""
    df = load_df(file_path)

    if isinstance(df, dict):
        return df

    return df.isnull().sum().to_dict()


# -----------------------
# Filtering
# -----------------------

@mcp.tool()
def filter_rows(file_path: str, column: str, value: str):
    """Filter dataset rows."""
    df = load_df(file_path)

    if isinstance(df, dict):
        return df

    try:
        result = df[df[column] == value]
        return result.head(50).to_dict()

    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def numeric_range(file_path: str, column: str, min_val: float, max_val: float):
    """Filter rows by numeric range."""
    df = load_df(file_path)

    if isinstance(df, dict):
        return df

    try:
        result = df[(df[column] >= min_val) & (df[column] <= max_val)]
        return result.head(50).to_dict()

    except Exception as e:
        return {"error": str(e)}


# -----------------------
# Aggregation
# -----------------------

@mcp.tool()
def groupby_analysis(file_path: str, group_col: str, value_col: str, operation: str):
    """Groupby aggregation."""
    df = load_df(file_path)

    if isinstance(df, dict):
        return df

    try:

        group = df.groupby(group_col)[value_col]

        ops = {
            "mean": group.mean,
            "sum": group.sum,
            "count": group.count,
            "max": group.max,
            "min": group.min
        }

        if operation not in ops:
            return {"error": "Invalid operation"}

        result = ops[operation]()
        return result.to_dict()

    except Exception as e:
        return {"error": str(e)}


# -----------------------
# Correlation
# -----------------------

@mcp.tool()
def correlation_matrix(file_path: str):
    """Correlation between numeric columns."""
    df = load_df(file_path)

    if isinstance(df, dict):
        return df

    try:
        return df.corr(numeric_only=True).to_dict()

    except Exception as e:
        return {"error": str(e)}


# -----------------------
# Visualization
# -----------------------

@mcp.tool()
def histogram(file_path: str, column: str):
    """Generate histogram plot."""
    df = load_df(file_path)

    if isinstance(df, dict):
        return df

    try:

        os.makedirs("plots", exist_ok=True)

        plt.figure()
        plt.hist(df[column].dropna())

        path = f"plots/{column}_hist.png"

        plt.savefig(path)
        plt.close()

        return {"image": path}

    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def scatter_plot(file_path: str, x: str, y: str):
    """Scatter plot."""
    df = load_df(file_path)

    if isinstance(df, dict):
        return df

    try:

        os.makedirs("plots", exist_ok=True)

        plt.figure()
        plt.scatter(df[x], df[y])

        path = f"plots/{x}_{y}_scatter.png"

        plt.savefig(path)
        plt.close()

        return {"image": path}

    except Exception as e:
        return {"error": str(e)}


# -----------------------
# Machine Learning
# -----------------------

@mcp.tool()
def linear_regression(file_path: str, feature: str, target: str):
    """Simple regression model."""
    df = load_df(file_path)

    if isinstance(df, dict):
        return df

    try:

        df = df[[feature, target]].dropna()

        X = df[[feature]]
        y = df[target]

        model = LinearRegression()
        model.fit(X, y)

        return {
            "coefficient": float(model.coef_[0]),
            "intercept": float(model.intercept_)
        }

    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def kmeans(file_path: str, columns: list, k: int):
    """KMeans clustering."""
    df = load_df(file_path)

    if isinstance(df, dict):
        return df

    try:

        data = df[columns].dropna()

        model = KMeans(n_clusters=k, n_init=10)

        labels = model.fit_predict(data)

        return {"clusters": labels.tolist()[:50]}

    except Exception as e:
        return {"error": str(e)}


# -----------------------
# Powerful Dynamic Tool
# -----------------------

@mcp.tool()
def run_pandas_code(file_path: str, code: str):
    """
    Execute dynamic pandas code on dataset.
    Claude can write custom analysis.
    """

    df = load_df(file_path)

    if isinstance(df, dict):
        return df

    try:

        local_vars = {"df": df, "pd": pd, "np": np}

        exec(code, {}, local_vars)

        result = local_vars.get("result")

        if isinstance(result, pd.DataFrame):
            return result.head(50).to_dict()

        return result

    except Exception as e:
        return {"error": str(e)}


# -----------------------
# Run Server
# -----------------------

if __name__ == "__main__":
    mcp.run()