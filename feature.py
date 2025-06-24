import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.preprocessing import LabelEncoder

# Setup
sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (8, 5)
output_dir = "eda_figures"
os.makedirs(output_dir, exist_ok=True)

# Load data
perf = pd.read_csv("PerformanceRating.csv")
emp = pd.read_csv("Employee.csv")

# Gabung data
df = pd.merge(
    perf,
    emp[[
        'EmployeeID', 'Department', 'BusinessTravel', 'OverTime',
        'YearsAtCompany', 'YearsInMostRecentRole',
        'YearsSinceLastPromotion', 'YearsWithCurrManager', 'Salary'
    ]],
    on='EmployeeID', how='left'
)

# Fitur turunan
df["promotion_ratio"] = df["YearsInMostRecentRole"] / (df["YearsAtCompany"] + 1e-5)
df["stagnancy_score"] = df["YearsSinceLastPromotion"] / (df["YearsAtCompany"] + 1e-5)
df["manager_stability"] = df["YearsWithCurrManager"] / (df["YearsAtCompany"] + 1e-5)

# Encode kategorikal
df["BusinessTravel_encoded"] = LabelEncoder().fit_transform(df["BusinessTravel"])
df["OverTime_encoded"] = LabelEncoder().fit_transform(df["OverTime"])

# --- Visualisasi dan Ringkasan Numerik ---

def save_boxplot(y, title, filename):
    sns.boxplot(x="ManagerRating", y=y, data=df)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/{filename}")
    plt.clf()

def save_countplot(hue, title, filename):
    sns.countplot(x="ManagerRating", hue=hue, data=df)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/{filename}")
    plt.clf()

# 1. Years Since Last Promotion vs ManagerRating
save_boxplot("YearsSinceLastPromotion", "Years Since Last Promotion vs Manager Rating", "Figure_1.png")
print("1. Rata-rata YearsSinceLastPromotion per ManagerRating:")
print(df.groupby("ManagerRating")["YearsSinceLastPromotion"].mean(), end="\n\n")

# 2. Promotion Ratio vs ManagerRating
save_boxplot("promotion_ratio", "Promotion Ratio vs Manager Rating", "Figure_2.png")
print("2. Rata-rata promotion_ratio per ManagerRating:")
print(df.groupby("ManagerRating")["promotion_ratio"].mean(), end="\n\n")

# 3. Stagnancy Score vs ManagerRating
save_boxplot("stagnancy_score", "Stagnancy Score vs Manager Rating", "Figure_3.png")
print("3. Rata-rata stagnancy_score per ManagerRating:")
print(df.groupby("ManagerRating")["stagnancy_score"].mean(), end="\n\n")

# 4. OverTime vs ManagerRating
save_countplot("OverTime", "OverTime vs Manager Rating", "Figure_4.png")
print("4. Distribusi OverTime terhadap ManagerRating:")
print(pd.crosstab(df["ManagerRating"], df["OverTime"]), end="\n\n")

# 5. BusinessTravel vs ManagerRating
save_countplot("BusinessTravel", "Business Travel vs Manager Rating", "Figure_5.png")
print("5. Distribusi BusinessTravel terhadap ManagerRating:")
print(pd.crosstab(df["ManagerRating"], df["BusinessTravel"]), end="\n\n")

# 6. Years in Current Role vs ManagerRating
save_boxplot("YearsInMostRecentRole", "Years in Current Role vs Manager Rating", "Figure_6.png")
print("6. Rata-rata YearsInMostRecentRole per ManagerRating:")
print(df.groupby("ManagerRating")["YearsInMostRecentRole"].mean(), end="\n\n")

# 7. Manager Stability vs ManagerRating
save_boxplot("manager_stability", "Manager Stability vs Manager Rating", "Figure_7.png")
print("7. Rata-rata manager_stability per ManagerRating:")
print(df.groupby("ManagerRating")["manager_stability"].mean(), end="\n\n")

# 8. Korelasi antar fitur numerik
numerik_cols = [
    'YearsAtCompany', 'YearsInMostRecentRole', 'YearsSinceLastPromotion',
    'YearsWithCurrManager', 'promotion_ratio', 'stagnancy_score',
    'manager_stability', 'ManagerRating'
]
corr = df[numerik_cols].corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Correlation Matrix of Numeric Features")
plt.tight_layout()
plt.savefig(f"{output_dir}/Figure_8.png")
plt.clf()
print("8. Korelasi antar fitur numerik terhadap ManagerRating:")
print(corr["ManagerRating"].sort_values(ascending=False), end="\n\n")
