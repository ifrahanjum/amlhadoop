import os
import glob
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

class AMLRiskClassifier(nn.Module):
    def __init__(self, input_dim):
        super(AMLRiskClassifier, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, 32),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.network(x)

def load_hadoop_output():
    """Finds and loads MapReduce output files from HDFS export directories."""
    possible_paths = [
        "../../data/output/part-r-*",
        "../data/hadoop_output.csv",
        "./hadoop_output.csv",
        "./part-r-00000",
        "./part-00000"
    ]

    files = []
    for path in possible_paths:
        found = glob.glob(path)
        if found:
            files.extend(found)
            break

    if not files:
        raise FileNotFoundError(
            "No Hadoop MapReduce output found! Ensure your Reducer has written "
            "its output (part-r-00000, part-00000, or hadoop_output.csv) into your project directory."
        )

    print(f"Loading Hadoop MapReduce output from: {files}")

    dfs = []
    for f in files:
        try:
            df = pd.read_csv(f, sep=r'\t|,', engine='python')
        except Exception:
            df = pd.read_csv(f)
        dfs.append(df)

    full_df = pd.concat(dfs, ignore_index=True)
    return full_df

def run_pipeline():
    print("=== Step 1: Loading Hadoop MapReduce Cycle Features ===")
    df = load_hadoop_output()
    print(f"Loaded {len(df)} cycles extracted by Hadoop.")

    feature_cols = ["Total_Volume", "Time_Span_Sec"]
    target_col = "Is_Flagged" if "Is_Flagged" in df.columns else "is_sar"

    X = df[feature_cols].values
    y = df[target_col].values

    # === Step 2: Train/Test Split & Feature Scaling ===
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y if len(set(y)) > 1 else None
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    X_train_t = torch.tensor(X_train_scaled, dtype=torch.float32)
    y_train_t = torch.tensor(y_train, dtype=torch.float32).unsqueeze(1)
    X_test_t = torch.tensor(X_test_scaled, dtype=torch.float32)

    # === Step 3: Train PyTorch Neural Network ===
    print("=== Step 2: Training PyTorch Classifier on Hadoop Features ===")
    model = AMLRiskClassifier(input_dim=len(feature_cols))
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.01)

    model.train()
    for epoch in range(1, 101):
        optimizer.zero_grad()
        out = model(X_train_t)
        loss = criterion(out, y_train_t)
        loss.backward()
        optimizer.step()

        if epoch % 20 == 0:
            print(f"Epoch {epoch}/100 - Loss: {loss.item():.4f}")

    torch.save(model.state_dict(), "aml_model.pt")
    print("Model weights saved to aml_model.pt")

    # === Step 4: Inference & Risk Scoring ===
    print("=== Step 3: Scoring Financial Cycles ===")
    model.eval()
    with torch.no_grad():
        scores = model(X_test_t).numpy().flatten()

    test_results = pd.DataFrame(X_test, columns=feature_cols)
    test_results["Ground_Truth"] = y_test
    test_results["Predicted_Risk_Score"] = scores.round(4)
    test_results["High_Risk_Flag"] = (scores >= 0.75).astype(int)

    test_results.to_csv("final_predictions.csv", index=False)
    print("Pipeline Execution Complete. Final Predictions saved to final_predictions.csv")

    # === Step 5: Model Evaluation Metrics ===
    y_true = test_results['Ground_Truth'].values
    y_pred = test_results['High_Risk_Flag'].values
    y_scores = test_results['Predicted_Risk_Score'].values

    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, zero_division=0)
    rec = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    auc = roc_auc_score(y_true, y_scores) if len(set(y_true)) > 1 else 0.0

    print("\n" + "="*40)
    print("      AML MODEL EVALUATION METRICS     ")
    print("="*40)
    print(f"Accuracy:  {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall:    {rec:.4f}")
    print(f"F1-Score:  {f1:.4f}")
    print(f"ROC-AUC:   {auc:.4f}")
    print("="*40 + "\n")

if __name__ == "__main__":
    run_pipeline()
