# Interactive Python Tableplot

A Python package for generating interactive tableplot-style visualizations, inspired by the `tabplot` functionality in R. Visualize the distribution and behavior of your variables along an ordering axis, with support for both numerical and categorical data.

## Installation

You can install `tableplot` directly via pip:

```bash
pip install tableplot
How to Use
Here is a basic example of how to use the package to generate a complete tableplot with a single call:

python
Copiar
Editar
import pandas as pd
import numpy as np  # Necessary for the dummy data example

# Import the main function from your package
from tableplot import tableplot

# 1. Load your data (example with a dummy DataFrame)
# df = pd.read_excel("path/to/your_data.xlsx")
# If you have a CSV file, use: df = pd.read_csv("path/to/your_data.csv")
# Or create an example DataFrame for testing:
data = {
    'Customer_ID': range(1, 1001),
    'Purchase_Value': np.random.rand(1000) * 1000,
    'Age': np.random.randint(18, 70, 1000),
    'Region': np.random.choice(['North', 'South', 'East', 'West'], 1000),
    'Subscriber': np.random.choice([True, False, np.nan], 1000, p=[0.45, 0.45, 0.1]),
    'Product_Category': np.random.choice(['Electronics', 'Clothing', 'Food', 'Services', 'Others'], 1000)
}
df_example = pd.DataFrame(data)

# 2. Generate and display the interactive tableplot
# sort_by: Numerical or categorical column to order the bins.
# nbins: Number of slices (bins) into which the dataset will be divided (for numerical columns).
# decreasing: True to sort in decreasing order, False for increasing.
# max_levels: Category limit for categorical columns (less frequent categories will be grouped into 'Others').
# title: The title that will appear at the top of your chart.
tableplot(
    df_example,
    sort_by="Purchase_Value",
    nbins=100,
    decreasing=False,
    max_levels=10,
    title="Example Dataset Tableplot (Ordered by Purchase Value)"
)
Contribution
Contributions are welcome! If you have suggestions, find issues, or want to add new features, please open an issue or pull request on the project's GitHub repository.

License
This project is licensed under the MIT License. See the LICENSE file for more details.