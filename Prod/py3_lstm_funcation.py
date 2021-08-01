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

def df_2darry(datadf,*argv ):
    columnslist=[]
    for arg in argv:
        columnslist.append(arg)
    new_data = pd.DataFrame(index=range(0,len(datadf)),columns=columnslist)
    for i in range(0,len(datadf)):
        for arg in argv:
            new_data[arg][i] = datadf[arg][i]
    #new_data.index = new_data.Date
    #new_data.drop('Date', axis=1, inplace=True)
    return new_data

def getNewInput(inputs, newClosePrice):
    price = newClosePrice
    inputs = np.append(inputs, [price])
    return inputs

def getNewClosePrice(inputs, model, scaler):
    inputs = inputs[-61:]
    inputs = inputs.reshape(-1,1)
    scaled_data = scaler.fit_transform(inputs)

    X_test = []
    for i in range(60,scaled_data.shape[0]):
        X_test.append(scaled_data[i-60:i,0])
    X_test = np.array(X_test)
    
    X_test = np.reshape(X_test, (X_test.shape[0],X_test.shape[1],1))
    closing_price = model.predict(X_test)
    closing_price = scaler.inverse_transform(closing_price)
    return closing_price

def predictfromPredictData(closing_price_acc, new_data, model, scaler):
    new_inputs = new_data[:-60]
    i = 1
    while i<61:    
        new_closing_price = getNewClosePrice(new_inputs, model, scaler)
        closing_price_acc = np.append(closing_price_acc, [new_closing_price])
        new_inputs = np.append(new_inputs, [new_closing_price])
        i +=1

    np.savetxt(r'/home/lan/Documents/py3ds/output/closeprice.csv', closing_price_acc)
    np.savetxt(r'/home/lan/Documents/py3ds/output/input.csv', new_inputs)

def getLSTM_Model(new_data, scaler):
    #creating train and test sets
    dataset = new_data.values

    train = dataset[0:987,:]
    valid = dataset[987:,:]

    #converting dataset into x_train and y_train
    #scaler = MinMaxScaler(feature_range=(0, 1))
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
    return model

def getLSTM_gap_Model(new_data, scaler, gap):
    #creating train and test sets
    dataset = new_data.values

    train = dataset[0:987,:]
    valid = dataset[987:,:]

    #converting dataset into x_train and y_train
    #scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(dataset)

    x_train, y_train = [], []
    for i in range(60,len(train)):
        x_train.append(scaled_data[i-60:i-gap,0])
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
    return model

def predictfromTrainData(new_data, model, scaler):
    ##predicting 246 values, using past 60 from the train data
    #inputs = new_data[len(new_data) - len(valid) - 60:].values #org
    inputs = new_data[1059:1180].values
    inputs = inputs.reshape(-1,1)
    scaled_data = scaler.fit_transform(inputs)

    X_test = []
    for i in range(60,scaled_data.shape[0]):
        X_test.append(scaled_data[i-60:i,0])
    X_test = np.array(X_test)

    X_test = np.reshape(X_test, (X_test.shape[0],X_test.shape[1],1))

    closing_price = model.predict(X_test)
    closing_price = scaler.inverse_transform(closing_price)
    return closing_price

def predictfromTrainData_gap(new_data, model, scaler, gap):
    ##predicting 246 values, using past 60 from the train data
    #inputs = new_data[len(new_data) - len(valid) - 60:].values #org
    inputs = new_data[987:].values
    inputs = inputs.reshape(-1,1)
    scaled_data = scaler.fit_transform(inputs)

    X_test = []
    for i in range(60,scaled_data.shape[0]):
        X_test.append(scaled_data[i-60:i-gap,0])
    X_test = np.array(X_test)

    X_test = np.reshape(X_test, (X_test.shape[0],X_test.shape[1],1))

    closing_price = model.predict(X_test)
    closing_price = scaler.inverse_transform(closing_price)
    return closing_price

