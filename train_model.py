import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score
from catboost import CatBoostClassifier
import joblib

# Load dataset
df = pd.read_csv("heart_disease_uci.csv")

# ----------------------------
# Preprocessing
# ----------------------------

# Handle missing values
num_cols = df.select_dtypes(include=np.number).columns
imputer = SimpleImputer(strategy='median')
df[num_cols] = imputer.fit_transform(df[num_cols])

# Remove duplicates
df = df.drop_duplicates()

# Encode categorical features
cat_cols = df.select_dtypes(include=['object', 'string']).columns
df = pd.get_dummies(df, columns=cat_cols, drop_first=True)

# Features & target
X = df.drop("num", axis=1)
y = (df["num"] > 0).astype(int)

# ----------------------------
# Train-Test Split (Stratified)
# ----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    stratify=y,
    random_state=42
)

# ----------------------------
# Model (Optimized for Medical ML)
# ----------------------------

model = CatBoostClassifier(
    iterations=2000,
    learning_rate=0.03,
    depth=6,
    auto_class_weights='Balanced',
    loss_function='Logloss',
    eval_metric='AUC',
    early_stopping_rounds=100,
    random_state=42,
    verbose=100
)

model.fit(
    X_train,
    y_train,
    eval_set=(X_test, y_test),
    use_best_model=True
)

# ----------------------------
# Evaluation
# ----------------------------

y_pred = model.predict(X_test)
y_probs = model.predict_proba(X_test)[:, 1]

print("\nModel Performance:")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("ROC AUC:", roc_auc_score(y_test, y_probs))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# ----------------------------
# Save Model & Feature Columns
# ----------------------------

joblib.dump(model, "heart_disease_model.pkl")
joblib.dump(X.columns.tolist(), "feature_columns.pkl")

print("\n✅ Model and feature columns saved successfully.")
