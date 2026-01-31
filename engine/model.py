from keras.models import load_model as lm
_model = None

def load_model(model_path) : 
    global _model
    if not _model : 
        _model = lm(model_path)
    return _model
        
