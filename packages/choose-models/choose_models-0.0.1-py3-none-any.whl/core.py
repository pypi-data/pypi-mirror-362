import numpy as np

class LinearRegressionOLS:
    def __init__(self):
        self.m = None
        self.b = None

    def fit(self, X_train, y_train):
        try:
            if X_train.ndim != 1 or y_train.ndim != 1:
                raise ValueError("Only 1D arrays supported for this simple linear regression")

            num = 0
            den = 0

            for i in range(X_train.shape[0]):
                num += (X_train[i] - X_train.mean()) * (y_train[i] - y_train.mean())
                den += (X_train[i] - X_train.mean())**2

            self.m = num / den
            self.b = y_train.mean() - (self.m * X_train.mean())

        except Exception as e:
            print(f"[ERROR in fit]: {e}")
            self.m = None
            self.b = None
    
    def predict(self, X_test):
        return (self.m * X_test) + self.b

    def checkScore(self, X_test, y_test):

        try:
            y_pred = self.predict(X_test)
            ss_res = sum((y_test - y_pred) ** 2)
            ss_tot = sum((y_test - y_test.mean()) ** 2)
            return 1 - (ss_res / ss_tot)
        except Exception as e:
            print(f"[ERROR in checkScore]: {e}")
            return None
        
    def plotGraph(self, X_test, y_test):
    
        import matplotlib.pyplot as plt
        plt.scatter(X_test, y_test, color = "blue")
        y_pred = self.predict(X_test)
        plt.plot(X_test, y_pred, color = "red")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.legend(["Data Points", "Regression Line"])
        plt.show()
    
    def getEquation(self):
        return f'y_hat = {self.m} * x + {self.b}'

class MLRegressionOLS:
    def __init__(self):
        self.coef_ = None
        self.intercept_ = None

    def fit(self, X_train, y_train):
        X_train = np.insert(X_train, 0, 1, axis=1)
        betas = np.linalg.inv(np.dot(X_train.T, X_train)).dot(X_train.T).dot(y_train)
        self.intercept_ = betas[0]
        self.coef_ = betas[1:]

    def predict(self, X_test):
        y_pred = np.dot(X_test, self.coef_) + self.intercept_
        return y_pred

    def checkScore(self, X_test, y_test):
        try:
            y_pred = self.predict(X_test)
            ss_res = np.sum((y_test - y_pred) ** 2)
            ss_tot = np.sum((y_test - np.mean(y_test)) ** 2)
            return 1 - (ss_res / ss_tot)
        except Exception as e:
            print(f"[ERROR in checkScore]: {e}")
            return None

    def plotGraph(self, X_test, y_test):
        import plotly.graph_objs as go
        
        # Generate meshgrid from X_test
        x_range = np.linspace(X_test[:, 0].min(), X_test[:, 0].max(), 30)
        y_range = np.linspace(X_test[:, 1].min(), X_test[:, 1].max(), 30)
        X1_grid, X2_grid = np.meshgrid(x_range, y_range)
        
        # Flatten mesh and predict Z (Y values)
        mesh_input = np.c_[X1_grid.ravel(), X2_grid.ravel()]
        Z = self.predict(mesh_input).reshape(X1_grid.shape)

        # Plot original points
        fig = go.Figure()

        fig.add_trace(go.Scatter3d(
            x=X_test[:, 0], y=X_test[:, 1], z=y_test,
            mode='markers', marker=dict(color='blue', size=5),
            name='Data Points'
        ))

        # Plot regression plane
        fig.add_trace(go.Surface(
            x=X1_grid, y=X2_grid, z=Z,
            colorscale='Viridis',
            name='Regression Plane',
            opacity=0.7
        ))

        fig.update_layout(scene=dict(
            xaxis_title='X1',
            yaxis_title='X2',
            zaxis_title='Y'
        ))

        fig.show()

    def getEquation(self):
        return f'y_hat = {self.intercept_} + {self.coef_} * x'



    
            

class Models:
    def __init__(self, df):
        self.dataframe = df.copy()
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None

    def split_data(self, ratio = 0.8, target_column=None, randomState = 42):
        try:
            if target_column is None or target_column not in self.dataframe.columns:
                raise ValueError("Please provide a valid target_column present in the dataframe.")
            train = self.dataframe.sample(frac=ratio, random_state=randomState)
            test = self.dataframe.drop(train.index)

            self.X_train = train.drop(columns=[target_column])
            self.y_train = train[target_column]
            self.X_test = test.drop(columns=[target_column])
            self.y_test = test[target_column]

        except Exception as e:
            print(f"Error in split_data: {e}")
            self.X_train, self.X_test, self.y_train, self.y_test = None, None, None, None
    
    def Linear_Regression_OLS(self, get_equation = False, plot = False, accuracy = True):
        lr_ols = LinearRegressionOLS()
        # Select the first column for simple linear regression
        X_train_1d = self.X_train.iloc[:, 0].values
        X_test_1d = self.X_test.iloc[:, 0].values
        y_train_1d = self.y_train.values
        y_test_1d = self.y_test.values
        lr_ols.fit(X_train_1d, y_train_1d)
        if (get_equation):
            print(lr_ols.getEquation())

        if (plot):
            lr_ols.plotGraph(X_test_1d, y_test_1d)

        if (accuracy):
            print(lr_ols.checkScore(X_test_1d, y_test_1d))
        
        elif (plot == False and accuracy == False):
            print("Model Trained")
    
    def MLinear_Regression_OLS(self, get_equation=False, plot=False, accuracy=True):
        mlr_ols = MLRegressionOLS()
        X_train_nd = self.X_train.values
        X_test_nd = self.X_test.values
        y_train_nd = self.y_train.values
        y_test_nd = self.y_test.values
        mlr_ols.fit(X_train_nd, y_train_nd)
        print("Model Trained")
        if get_equation:
            print(mlr_ols.getEquation())

        if plot:
            mlr_ols.plotGraph(X_test_nd, y_test_nd)

        if accuracy:
            print(mlr_ols.checkScore(X_test_nd, y_test_nd))

        elif not plot and not accuracy:
            print("Model Trained")
        return mlr_ols


import pandas as pd

df = pd.read_csv("choose_models/sample_ols_data.csv")
models = Models(df)
models.split_data(target_column='y')
models.MLinear_Regression_OLS(plot=True)



