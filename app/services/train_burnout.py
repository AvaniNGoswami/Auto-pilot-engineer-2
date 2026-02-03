from sklearn.ensemble import RandomForestClassifier
from app.services.ml_prepare import load_dataframe
import cloudpickle as pickle


def label_risk(row):
    if row['fatigue_score']>0.4 and row['context_switch_rate'] > 5:
        return "high"
    if row['fatigue_score'] > 0.25:
        return "medium"
    return "low"

def train_burnout():
    df = load_dataframe()
    df['burnout_risk'] = df.apply(label_risk,axis=1)

    X = df[['total_work_minutes','total_break_minutes','context_switch_rate','fatigue_score']]
    y = df['burnout_risk']

    model = RandomForestClassifier()
    model.fit(X,y)

    pickle.dump(model, open("app/models_storage/burnout.pkl","wb"))

    print('😊 model saved')

if __name__ == '__main__':
    train_burnout()