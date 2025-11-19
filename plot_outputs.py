import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("query_outputs/landed_value_by_year.csv")
plt.figure(figsize=(10,4))
plt.plot(df['year'], df['total_landed_value'])
plt.xlabel('Year')
plt.ylabel('Total landed value (USD)')
plt.title('Total Landed Value by Year (Sea-Around-Us)')
plt.grid(True)
plt.tight_layout()
plt.savefig("query_outputs/landed_value_by_year.png", dpi=150)
print("Saved plot to query_outputs/landed_value_by_year.png")


