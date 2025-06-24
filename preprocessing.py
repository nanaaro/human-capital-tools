import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from imblearn.combine import SMOTEENN
import joblib

# --- 1. Load & Gabungkan Data ---
perf = pd.read_csv("PerformanceRating.csv")
emp = pd.read_csv("Employee.csv")

df = pd.merge(
    perf,
    emp[[
        'EmployeeID', 'Department', 'BusinessTravel', 'OverTime',
        'YearsAtCompany', 'YearsInMostRecentRole',
        'YearsSinceLastPromotion', 'YearsWithCurrManager', 'Salary']],
    on='EmployeeID', how='left'
)

# --- 2. Drop kolom tidak dipakai ---
df_proc = df.drop(columns=['PerformanceID', 'ReviewDate', 'SelfRating', 'Salary'])

# --- 3. Encode kategorikal ---
df_proc['BusinessTravel'] = LabelEncoder().fit_transform(df_proc['BusinessTravel'])
df_proc['OverTime'] = LabelEncoder().fit_transform(df_proc['OverTime'])

# --- 4. Handle missing value ---
for col in df_proc.columns:
    if df_proc[col].isnull().sum() > 0:
        if df_proc[col].dtype == 'object':
            df_proc[col].fillna(df_proc[col].mode()[0], inplace=True)
        else:
            df_proc[col].fillna(df_proc[col].mean(), inplace=True)

# --- 5. Buat fitur turunan ---
df_proc['promotion_ratio'] = df_proc['YearsInMostRecentRole'] / (df_proc['YearsAtCompany'] + 1e-5)
df_proc['stagnancy_score'] = df_proc['YearsSinceLastPromotion'] / (df_proc['YearsAtCompany'] + 1e-5)
df_proc['manager_stability'] = df_proc['YearsWithCurrManager'] / (df_proc['YearsAtCompany'] + 1e-5)

# --- 6. Simpan metadata dan pisah fitur ---
df_meta = df_proc[['EmployeeID', 'Department']]
df_ready = df_proc.drop(columns=['EmployeeID', 'Department'])

X = df_ready.drop(columns=['ManagerRating'])
y = df_ready['ManagerRating']

# --- 7. Mapping ManagerRating jadi binary class ---
# Rating 1-2 → 0 (Needs Improvement), 3-5 → 1 (Meets Expectation)
y_binary = y.map(lambda x: 0 if x <= 2 else 1)

# --- 8. Outlier removal dengan IQR ---
Q1 = X.quantile(0.25)
Q3 = X.quantile(0.75)
IQR = Q3 - Q1
mask = ~((X < (Q1 - 1.5 * IQR)) | (X > (Q3 + 1.5 * IQR))).any(axis=1)

X = X[mask].reset_index(drop=True)
y_binary = y_binary[mask].reset_index(drop=True)
df_meta = df_meta.loc[mask].reset_index(drop=True)

# --- 9. Scaling ---
scaler = StandardScaler()
X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)

joblib.dump(scaler, "scaler.pkl")

# --- 10. SMOTEENN balancing ---
smotenn = SMOTEENN(random_state=42)
X_bal, y_bal = smotenn.fit_resample(X_scaled, y_binary)

# Sinkronisasi metadata (replikasi untuk jumlah data hasil balancing)
df_meta_bal = pd.concat([df_meta] * (len(X_bal) // len(df_meta) + 1), ignore_index=True).iloc[:len(X_bal)]

# --- 11. Split data ---
X_train, X_test, y_train, y_test, meta_train, meta_test = train_test_split(
    X_bal, y_bal, df_meta_bal, test_size=0.25, random_state=42, stratify=y_bal
)

# --- 12. Gabungkan kembali & simpan ke CSV ---
train_df = pd.concat([meta_train.reset_index(drop=True),
                      X_train.reset_index(drop=True),
                      y_train.reset_index(drop=True)], axis=1)
train_df['dataset'] = 'train'

test_df = pd.concat([meta_test.reset_index(drop=True),
                     X_test.reset_index(drop=True),
                     y_test.reset_index(drop=True)], axis=1)
test_df['dataset'] = 'test'

final_df = pd.concat([train_df, test_df], axis=0)
final_df.to_csv("Preprocessed Employee.csv", index=False)
