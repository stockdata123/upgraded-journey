import numpy as np

x1 = [1, 2, 4]
y1 = [0.5, 0.25, 0.125]
corr = np.correlate(x1, y1)
coef = np.corrcoef(x1, y1)
cov = np.cov(x1, y1)
print(x1, y1)
print (corr)
print (coef)
print (cov)