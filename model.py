import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV
from scipy.stats import randint
import joblib

scaler = joblib.load("scaler.pkl")  

# 1. Load data hasil preprocessing
df = pd.read_csv("Preprocessed Employee.csv")

# 2. Pisahkan data latih dan uji
train_df = df[df['dataset'] == 'train'].drop(columns=['dataset'])
test_df = df[df['dataset'] == 'test'].drop(columns=['dataset'])

X_train = train_df.drop(columns=['EmployeeID', 'Department', 'ManagerRating'])
y_train = train_df['ManagerRating']

X_test = test_df.drop(columns=['EmployeeID', 'Department', 'ManagerRating'])
y_test = test_df['ManagerRating']

# 3. Definisikan model dasar Random Forest
rf = RandomForestClassifier(class_weight='balanced', random_state=42)

# 4. Tentukan grid parameter untuk hypertuning
param_grid = {
    'n_estimators': [100, 150, 200],  
    'max_depth': [10, 15, 20, None],
    'max_features': ['sqrt', 'log2'],
    'min_samples_split': [2, 3, 5],
    'min_samples_leaf': [1, 2, 4],
    'bootstrap': [True, False]
}

# 5. Lakukan Grid Search untuk hypertuning
grid_search = GridSearchCV(
    estimator=rf,
    param_grid=param_grid,
    scoring='accuracy',
    cv=3,
    verbose=1,
    n_jobs=-1
)

grid_search.fit(X_train, y_train)
best_rf = grid_search.best_estimator_

print("✅ Best Parameters:", grid_search.best_params_)

# 6. Evaluasi model
y_pred = best_rf.predict(X_test)
acc = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred, average='macro')

print("\n🎯 Evaluasi Model (Tuned Random Forest):")
print("Accuracy:", acc)
print("F1 Score:", f1)
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# 7. Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title("Confusion Matrix (Tuned RF)")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.show()

# Simpan model ke file
joblib.dump({
    'model': best_rf,
    'scaler': scaler,  
    'features': X_train.columns.tolist(),  
}, 'employee model.pkl')

