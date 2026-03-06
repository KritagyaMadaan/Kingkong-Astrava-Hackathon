import pickle
import joblib
import xgboost as xgb

try:
    with open('xgb_failure_model.pkl', 'rb') as f:
        model = pickle.load(f)
    print(f"Model loaded with pickle: {type(model)}")
except Exception as e:
    print(f"Pickle failed: {e}")
    try:
        model = joblib.load('xgb_failure_model.pkl')
        print(f"Model loaded with joblib: {type(model)}")
    except Exception as e2:
        print(f"Joblib failed: {e2}")

if 'model' in locals():
    if hasattr(model, 'feature_names_in_'):
        features = list(model.feature_names_in_)
        import numpy as np
        mock_data = np.array([[300.0, 310.0, 1500.0, 40.0, 10.0]])
        pred = model.predict(mock_data)
        print(f"PREDICTION:{pred}")
        if hasattr(model, 'predict_proba'):
            prob = model.predict_proba(mock_data)
            print(f"PROBABILITY:{prob.tolist()}")
    else:
        print("Feature names not found in model object.")
