import __init__
from init_project import *
#
from sklearn import linear_model
import statsmodels.discrete.discrete_model as sm
import pandas as pd

df = pd.read_csv(opath.join(dpath['_data'], 'dropoffXAP-2009.csv'))
df = df.append(pd.read_csv(opath.join(dpath['_data'], 'dropoffXAP-2010.csv')))

df.columns

df['sunkCost'].hist()

df[(df['GA'] == 0) & (df['year'] == 2010)]['sunkCost'].hist()
set(df['year'])

y = df['GA']
X = df['sunkCost']
# run the classifier
clf = linear_model.LogisticRegression(C=1e5)
clf.fit(X, y)

logit = sm.Logit(y, X)
res = logit.fit()
dir(res)
res.summary()



X = X[:, np.newaxis]
# run the classifier
clf = linear_model.LogisticRegression(C=1e5)
clf.fit(X, y)

# and plot the result
plt.figure(1, figsize=(4, 3))
plt.clf()
plt.scatter(X.ravel(), y, color='black', zorder=20)
X_test = np.linspace(-5, 10, 300)


def model(x):
    return 1 / (1 + np.exp(-x))
loss = model(X_test * clf.coef_ + clf.intercept_).ravel()
plt.plot(X_test, loss, color='red', linewidth=3)
