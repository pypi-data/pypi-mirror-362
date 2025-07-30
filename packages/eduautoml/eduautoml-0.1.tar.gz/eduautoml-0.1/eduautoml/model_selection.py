from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def select_best_model(X, y, task='classification'):
    models = {
        'LogisticRegression': LogisticRegression(),
        'RandomForest': RandomForestClassifier()
    }

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2)
    results = {}

    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_val)
        acc = accuracy_score(y_val, y_pred)
        results[name] = acc

    best = max(results, key=results.get)
    return best, models[best]
