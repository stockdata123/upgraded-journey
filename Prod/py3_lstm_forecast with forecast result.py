#importing required libraries
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM

import numpy
import yfinance as yf
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import csv

import py3_lstm_funcation as lstmfc

todaystr = datetime.now().strftime('%Y-%m-%d')
todaystr = '2019-12-03'
df0 = yf.download('CNQ','2018-01-01', todaystr)
#print(df0[:3])
#df.to_csv(r'/home/lan/Documents/py3ds/df.csv')

#creating dataframe
data = df0.sort_index(ascending=True, axis=0)
#no index ?? print('23/n', data[:3])
data['Date'] = data.index
#print(data[:3])
new_data = pd.DataFrame(index=range(0,len(df0)),columns=['Date', 'Close'])
#print('27/n', new_data[:3])
for i in range(0,len(data)):
    new_data['Date'][i] = data['Date'][i]
    new_data['Close'][i] = data['Close'][i]
#print('31/n', new_data[:3])
#setting index
new_data.index = new_data.Date
new_data.drop('Date', axis=1, inplace=True)
#print('35/n', new_data[:3])
dataset = new_data.values
#print('dataset', dataset[:3])
#new_dataset = lstmfc.df_2darry(data, 'Date', 'Close')

#get moving averge
df1 = df0[['Close']]
#print(df1[:3])
df1.reset_index(level=0, inplace=True)
#print(df1[:3])

df1.columns=['ds','y']
df1.drop('ds', axis=1, inplace=True)
df1y = df1.y
#print('df1y', df1y[:3])

scaler = MinMaxScaler(feature_range=(0, 1))
exp1 = df1.y.ewm(span=12, adjust=False).mean()
dfexp1 = pd.DataFrame(exp1)
exp1_dataset = lstmfc.df_2darry(dfexp1, 'y')
exp1_values = exp1_dataset.values
exp1_model = lstmfc.getLSTM_Model(exp1_dataset, scaler)
exp1_closedata = lstmfc.predictfromTrainData(exp1_dataset, exp1_model, scaler)
'''
###forcast for 13 days
forecast_days = 13
exp1_model = lstmfc.getLSTM_gap_Model(new_data, scaler, forecast_days)
exp1_closedata = lstmfc.predictfromTrainData_gap(new_data, exp1_model, scaler, forecast_days)
'''
np.savetxt(r'/home/lan/Documents/py3ds/output/newdata.csv', new_data)
np.savetxt(r'/home/lan/Documents/py3ds/output/closeprice.csv', exp1_closedata)
#lstmfc.predictfromPredictData(exp1_closedata, exp1_values, exp1_model, scaler)



'''
exp2 = df1.y.ewm(span=26, adjust=False).mean()
macd = exp1-exp2
exp3 = macd.ewm(span=12, adjust=False).mean()

#creating train and test sets
dataset = new_data.values

train = dataset[0:987,:]
valid = dataset[987:,:]

#converting dataset into x_train and y_train
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(dataset)

x_train, y_train = [], []
for i in range(60,len(train)):
    x_train.append(scaled_data[i-60:i,0])
    y_train.append(scaled_data[i,0])
x_train, y_train = np.array(x_train), np.array(y_train)

x_train = np.reshape(x_train, (x_train.shape[0],x_train.shape[1],1))


# create and fit the LSTM network
model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1],1)))
model.add(LSTM(units=50))
model.add(Dense(1))

model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(x_train, y_train, epochs=1, batch_size=1, verbose=2)


##predicting 246 values, using past 60 from the train data
#inputs = new_data[len(new_data) - len(valid) - 60:].values
inputs = new_data[1059:1180].values
input_test = new_data[1059:1180].values

inputs = inputs.reshape(-1,1)
inputs  = scaler.transform(inputs)

X_test = []

for i in range(60,inputs.shape[0]):
    X_test.append(inputs[i-60:i,0])
X_test = np.array(X_test)


X_test = np.reshape(X_test, (X_test.shape[0],X_test.shape[1],1))

closing_price = model.predict(X_test)
closing_price = scaler.inverse_transform(closing_price)

closing_price_acc = closing_price

new_inputs = input_test
i = 1
while i<61:    
    new_closing_price = lstmfc.getNewClosePrice(new_inputs, scaler, model)
    closing_price_acc = np.append(closing_price_acc, [new_closing_price])
    new_inputs = np.append(new_inputs, [new_closing_price])
    i +=1

np.savetxt(r'/home/lan/Documents/py3ds/closeprice.csv', closing_price_acc)
np.savetxt(r'/home/lan/Documents/py3ds/input.csv', new_inputs)

rms=np.sqrt(np.mean(np.power((valid-closing_price),2)))
print(rms)
#for plotting
train = new_data[:987]
valid = new_data[987:]
valid['Predictions'] = closing_price
plt.plot(train['Close'])
plt.plot(valid[['Close','Predictions']])

plt.savefig("/home/lan/Documents/py3ds/lstm.png")
'''



