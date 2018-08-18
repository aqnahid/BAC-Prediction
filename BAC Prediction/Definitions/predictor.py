import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

class predictor():
    def dataAnalysis(J):
        #Dataset for BAC level Jerking
        #dataTable.csv was created from this source: SFST US, at: http://sfst.us/
        #URL for document--> http://sfst.us/KanePDF/The_Robustness_of_the_Horizontal_Gaze_Nystagmus_Test.pdf
        reviews=pd.read_csv("dataTable.csv")
        data=pd.DataFrame(reviews,columns=["Parcipant's_BAC_(g/dL)","A"])
        if J>0:
            x=reviews[reviews["A"]==J]
        else:
            return 0
        y=pd.DataFrame(x,columns=["Parcipant's_BAC_(g/dL)","A"])
        arr=[]
        arr.append(y)
        z=y.values
        m=len(y)
        X= z[:,0]
        Y= z[:,1]
        mean_x = np.mean(X)
        mean_y = np.mean(Y)
        m = len(X)
        numer = 0
        denom = 0

        for i in range(m):
            numer += (X[i] - mean_x) * (Y[i] - mean_y)
            denom += (X[i] - mean_x) ** 2
        b1 = numer / denom
        b0 = mean_y - (b1 * mean_x)
        max_x = np.max(X) + 100
        min_x = np.min(X) - 100
        x = np.linspace(min_x, max_x, 1000)
        y = b0 + b1 * x
        # Calculating Root Mean Squares Error
        rmse = 0
        for i in range(m):
            y_pred = b0 + b1 * X[i]
            rmse += (Y[i] - y_pred) ** 2
        rmse = np.sqrt(rmse/m)
        ss_t = 0
        ss_r = 0
        for i in range(m):
            y_pred = b0 + b1 * X[i]
            ss_t += (Y[i] - mean_y) ** 2
            ss_r += (Y[i] - y_pred) ** 2
        X = X.reshape((m, 1))
        
        #Model Creation:
        reg = LinearRegression()
        # Fitting training data
        reg = reg.fit(X, Y)
        # Y Prediction
        Y_pred = reg.predict(X)
        mse = mean_squared_error(Y, Y_pred)
        rmse = np.sqrt(mse)
        r2_score = reg.score(X, Y)
        return z[0]
