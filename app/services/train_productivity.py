from sklearn.linear_model import LinearRegression
from app.services.ml_prepare import load_dataframe
import cloudpickle as pickle


def train_productivity():
    df = load_dataframe()
    X = df[['total_work_minutes','total_break_minutes','context_switch_rate','fatigue_score']]
    y = df['focus_score']

    model = LinearRegression()
    model.fit(X,y)

    pickle.dump(model, open("app/models_storage/productivity.pkl","wb"))

    print('😊 model saved')

if __name__=='__main__':
    train_productivity()