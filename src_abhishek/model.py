import numpy as np
from tempfile import TemporaryFile
import pandas as pd
import sklearn.linear_model

features = 'potential,attacking_work_rate,defensive_work_rate,crossing,finishing,heading_accuracy,short_passing,volleys,dribbling,curve,free_kick_accuracy,long_passing,ball_control,acceleration,sprint_speed,agility,reactions,balance,shot_power,jumping,stamina,strength,long_shots,aggression,interceptions,positioning,vision,penalties,marking,standing_tackle,sliding_tackle,gk_diving,gk_handling,gk_kicking,gk_positioning,gk_reflexes'
features_list = features.split(',')
features_list = features_list * 4
for idx, feature in enumerate(features_list):
    if idx/36 == 0:
        features_list[idx] = 'goal_keeper_' + features_list[idx]
    elif idx/36 == 1:
        features_list[idx] = 'defenders_' + features_list[idx]
    elif idx/36 == 2:
        features_list[idx] = 'midfielders_' + features_list[idx]
    else:
        features_list[idx] = 'strikers_' + features_list[idx]
features_list = features_list * 2

for idx, feature in enumerate(features_list):
    if idx/144 == 1:
        features_list[idx] = 'away_' + features_list[idx]
print(features_list)

def train_validate_test_split(df, train_percent=.6, validate_percent=.2, seed=100):
    np.random.seed(seed)
    perm = np.random.permutation(df.index)
    m = len(df)
    train_end = int(train_percent * m)
    validate_end = int(validate_percent * m) + train_end
    train = df.ix[perm[:train_end]]
    validate = df.ix[perm[train_end:validate_end]]
    test = df.ix[perm[validate_end:]]
    return train, validate, test


outfile = 'alldata.npz'
npzfile = np.load(outfile)
print npzfile.files
all_data = npzfile['arr_0']
print(all_data.shape)

train_data, validate_data, test_data = train_validate_test_split(pd.DataFrame(all_data))

train_data = np.array(train_data)
validate_data = np.array(validate_data)
test_data = np.array(test_data)


train_X = train_data[:, :-1]
validate_X = validate_data[:, :-1]
test_X = test_data[:, :-1]
train_Y = train_data[:,-1]
validate_Y = validate_data[:,-1]
test_Y = test_data[:,-1]
print(train_X.shape)
print(validate_X.shape)
print(test_X.shape)


kbest = sklearn.linear_model.LogisticRegression()
kbest.fit(train_X, train_Y)
print('training accuracy', kbest.score(train_X, train_Y))
print('test accuracy', kbest.score(test_X, test_Y))
print('all coefficients', kbest.coef_)
best_features = np.argsort(np.abs(kbest.coef_))[::-1].reshape(288)
#print('15 best features', best_features)
print(best_features.shape)
for idx in  best_features:
    print features_list[idx]

import sklearn.ensemble

random_forest = sklearn.ensemble.RandomForestClassifier(n_estimators=2)
random_forest.fit_transform(train_X, train_Y)
print('training accuracy', random_forest.score(train_X, train_Y))
print('test accuracy', random_forest.score(test_X, test_Y))
print('random_forest features', random_forest.feature_importances_)


from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score
clf = DecisionTreeClassifier(random_state=0)
cross_val_score(clf, train_X, train_X, cv=10)
print("Decision tree accuracy" , cross_val_score(clf, test_X, test_X, cv=10))
