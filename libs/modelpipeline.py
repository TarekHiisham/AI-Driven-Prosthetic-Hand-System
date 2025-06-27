import numpy as np
import xgboost as xgb

theoretical_angles_max = np.array([60, 60, 90] + [90, 100, 90] * 4)

params = {
    'objective': 'reg:squarederror',  
    'learning_rate': 1,
    'max_depth': 20,
}
class PredictionPipeline:
    def __init__(self, model_path):
        self.model_path = model_path
        try:
            self.model = xgb.Booster()
            self.model.load_model(self.model_path)
            print("Model loaded successfully.")
        except FileNotFoundError:
            raise FileNotFoundError(f"Model file not found at {self.model_path}.")
        except Exception as e:
            raise RuntimeError(f"Error loading model: {e}")
 
    def __predictions_processing(self, y):
        y = np.round(y)
        y = np.clip(y, 0, theoretical_angles_max)
        return y[1:]
    
    def predict(self, X):
        try:
            dmatrix = xgb.DMatrix(X)
            predictions = self.model.predict(dmatrix).flatten()
            predictions = self.__predictions_processing(predictions)
            return predictions 
        except xgb.core.XGBoostError as e:
            raise RuntimeError(f"Error during prediction: {e}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error during prediction: {e}")
        
    def train(self, X, y):
        try:
            dsub = xgb.DMatrix(X, label=y)
            self.xgbmodel = xgb.train(
                params,
                dtrain=dsub,  
                num_boost_round=1,  
                xgb_model=self.model,  
                verbose_eval=True
            )
        except xgb.core.XGBoostError as e:
            raise RuntimeError(f"Error during prediction: {e}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error during prediction: {e}")
