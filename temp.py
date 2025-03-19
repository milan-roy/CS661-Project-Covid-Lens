import plotly.express as px
import pandas as pd
import numpy as np

# Sample Data: Simulating COVID-19 statistics
df = pd.DataFrame({
    "Total Cases": np.random.randint(1000, 50000, 10),
    "Total Deaths": np.random.randint(10, 2000, 10),
    "Total Tests": np.random.randint(5000, 200000, 10),
    "Vaccinations": np.random.randint(10000, 500000, 10),
    "Cases Per Million": np.random.uniform(50, 500, 10),
    "Deaths Per Million": np.random.uniform(1, 50, 10)
})

# Compute the correlation matrix
corr_matrix = df.corr()

# Plot the heatmap
fig = px.imshow(corr_matrix,
                text_auto=True,  # Annotate cells with values
                labels=dict(x="Metric", y="Metric", color="Correlation"),
                x=corr_matrix.columns,
                y=corr_matrix.index,
                color_continuous_scale="RdBu_r")  # Red-Blue colormap for positive & negative correlation

# Update layout
fig.update_layout(title="Correlation Heatmap of COVID-19 Metrics")

fig.show()
