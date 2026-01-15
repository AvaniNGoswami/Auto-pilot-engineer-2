# import cloudpickle as pickle
# import numpy as np

# model_prod = pickle.load(open("app/models_storage/productivity.pkl","rb"))
# model_burn = pickle.load(open('app/models_storage/burnout.pkl','rb'))

# def analyze(features):
#     if not features:
#         return None

#     avg_focus = np.mean([f.focus_score for f in features])
#     avg_fatigue = np.mean([f.fatigue_score for f in features])
#     avg_context_switch = np.mean([f.context_switch_rate for f in features])

#     prod_pred  = model_prod.predict([[avg_focus,avg_context_switch]])
#     burn_pred  = model_burn.predict([[avg_fatigue,avg_context_switch]])

#     return{
#         'productivity':prod_pred,
#         'burnout':burn_pred
#     }


import cloudpickle as pickle
import numpy as np

model_prod = pickle.load(open("app/models_storage/productivity.pkl","rb"))
model_burn = pickle.load(open("app/models_storage/burnout.pkl","rb"))

def analyze(features):
    if not features:
        return None

    total_work_minutes = np.mean([f.total_work_minutes for f in features])
    total_break_minutes = np.mean([f.total_break_minutes for f in features])
    context_switch_rate = np.mean([f.context_switch_rate for f in features])
    fatigue_score = np.mean([f.fatigue_score for f in features])

    prod_pred  = model_prod.predict([[total_work_minutes,total_break_minutes,context_switch_rate,fatigue_score]])
    burn_pred  = model_burn.predict([[total_work_minutes,total_break_minutes,context_switch_rate,fatigue_score]])

    return {
    'productivity': float(prod_pred[0]),  # regression → numeric
    'burnout': str(burn_pred[0])          # classifier → string label
    }
