import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle

print("Loading features...")
X = np.load('data/X_features.npy')
y = np.load('data/y_labels.npy')
print(f"Features shape : {X.shape}")
print(f"Labels shape   : {y.shape}")

print("\nSplitting data...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"Training samples : {len(X_train)}")
print(f"Testing samples  : {len(X_test)}")

print("\nScaling features...")
scaler  = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test  = scaler.transform(X_test)
print("Scaling done ✅")

print("\nTraining models...")
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
rf_pred  = rf_model.predict(X_test)
rf_acc   = accuracy_score(y_test, rf_pred)

svm_model = SVC(kernel='rbf', random_state=42)
svm_model.fit(X_train, y_train)
svm_pred  = svm_model.predict(X_test)
svm_acc   = accuracy_score(y_test, svm_pred)

print(f"\nRandom Forest Accuracy : {rf_acc * 100:.2f}%")
print(f"SVM Accuracy           : {svm_acc * 100:.2f}%")

if rf_acc >= svm_acc:
    best_model = rf_model
    best_name  = "Random Forest"
    best_acc   = rf_acc
    best_pred  = rf_pred
else:
    best_model = svm_model
    best_name  = "SVM"
    best_acc   = svm_acc
    best_pred  = svm_pred

print(f"\nBest model : {best_name} ({best_acc * 100:.2f}%)")

print("\n====== CLASSIFICATION REPORT ======")
print(classification_report(
    y_test, best_pred,
    target_names=['FORWARD', 'LEFT', 'RIGHT']
))

print("====== CONFUSION MATRIX ======")
print(confusion_matrix(y_test, best_pred))

print("\nSaving model...")
pickle.dump(best_model, open('data/model.pkl', 'wb'))
pickle.dump(scaler,     open('data/scaler.pkl', 'wb'))
print("Saved model.pkl and scaler.pkl ✅")
print("\nPhase 3 complete! ✅")