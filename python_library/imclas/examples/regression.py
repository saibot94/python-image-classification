from sklearn.linear_model import LinearRegression
import numpy as np


class RegressionExample():
    def __init__(self):
        pass

    def run(self):
        clf = LinearRegression()
        arr = np.array([1, 2, 3, 4])
        print arr


if __name__ == '__main__':
    reg = RegressionExample()
    reg.run()