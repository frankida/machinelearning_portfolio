import numpy as np
from scipy.stats import mode
import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)

class RTLearner(object):
    def __init__(self, leaf_size=5, verbose=False):
        self.verbose = verbose
        self.leaf_size = leaf_size
        pass  # move along, these aren't the drones you're looking for

    def addEvidence(self, Xtrain, Ytrain):
        data = np.insert(Xtrain, Xtrain.shape[1], Ytrain.flatten(), axis=1)
        self.randomleaf = self.createrandomleaf(data)
        self.rt = self.build_tree(data, self.randomleaf)
        if self.verbose: ("this is the random tree (rows: {}): \n{}".format(self.rt.shape[0], self.rt))

    def build_tree(self, data, randomleaf):
        if self.verbose: print("build_tree has been called for: \n{}".format(data))
        if data.shape[0] <= self.leaf_size and data.shape[0] > 0:
            leaf = np.array([[-1., self.processleaf_into_ymean(data), np.nan, np.nan]])
            return leaf
        elif data.shape[0] == 0:
            if self.verbose: print ("NO rows")
            return randomleaf
        elif np.all(data[:, -1] == data[0, -1], axis=0):
            if self.verbose: print("{} is all the same value".format(data))
            return np.array([[-1., (data[0][-1]), np.nan, np.nan]])
        else:
            if self.verbose: print("Main tree code the tree rows: {}".format(data.shape[0]))
            SplitVal, i = self.splitval_generate(data)
            if self.verbose: print("Split value is: {}".format(SplitVal))

            if self.verbose: print(
                "Intermediate lefttree code with feature: {}, splitvalue:{} \n{}".format(i, SplitVal, data))

            datalefttree = data[data[:, i] <= SplitVal]
            datarighttree = data[data[:, i] > SplitVal]
            if self.verbose: print ("Righttree is size: {}; Lefttree is size: {}".format(datarighttree.shape[0],
                                                                                         datalefttree.shape[0]))
            counter = 0
            while (datalefttree.shape[0] > 0 and datarighttree.shape[0] == 0 and counter != 10):
                if self.verbose: print("***This is the empty row scenario***")
                SplitVal, i = self.splitval_generate(data)
                datalefttree = data[data[:, i] <= SplitVal]
                datarighttree = data[data[:, i] > SplitVal]
                counter += 1

            lefttree = np.asarray(self.build_tree(datalefttree, randomleaf))
            righttree = np.asarray(self.build_tree(datarighttree, randomleaf))
            if self.verbose: print ("Data for leftree and size {}: \n{}".format(datalefttree.shape[0], datalefttree))

            if self.verbose:  print(
                "Intermediate righttree code with, feature: {}, splitvalue:{} \n{}".format(i, SplitVal, data))
            if self.verbose:  print (
                "Data for righttree and size {}: \n{}".format(datarighttree.shape[0], datarighttree))
            if self.verbose:  print ("Lefttree size is: {}\n{}".format(lefttree.shape[0], lefttree))
            if self.verbose:  print ("Righttree size is: {}\n{}".format(righttree.shape[0], righttree))
            root = np.array([i, SplitVal, 1, lefttree.shape[0] + 1])
            if self.verbose:  print("Root is : \n{}".format(root))
            return np.vstack([root, lefttree, righttree])

    def splitval_generate(self, data):
        i = int(np.random.rand() * data.shape[1] - 1)
        if self.verbose: print("Random feature number: {}".format(i))
        random1 = int(np.random.rand() * data.shape[0])
        random2 = int(np.random.rand() * data.shape[0])
        SplitVal = (data[random1, i] + data[random2, i]) / 2
        return SplitVal, i

    def createrandomleaf(self, data):
        return np.array([[-1, np.mean(data[:][-1]), np.nan, np.nan]])

    def query(self, points):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """
        answers = [-999]
        for x in points:
            counter = self.rt.shape[0]
            testrow = 0;
            while counter != -1:
                testfeature = int(self.rt[testrow][0])
                testvalue = self.rt[testrow][1]
                if self.verbose:  print (
                    "Testrow: {}, Testfeature: {}, TestValue: {}".format(testrow, testfeature, testvalue))
                if (x[testfeature] <= testvalue and testfeature != -1):
                    if self.verbose:  print("Go left")
                    counter -= -1
                    testrow += 1
                elif testfeature == -1:
                    if self.verbose: print ("**The estimate is: {}".format(self.rt[testrow][1]))
                    if answers[0] == -999:
                        answers[0] = self.rt[testrow][1]
                        # print answers
                        break
                    else:
                        answers = np.vstack([answers, self.rt[testrow][1]])
                        # print answers
                        break
                else:
                    if self.verbose:  print("Go right")
                    increment = self.rt[testrow][3]
                    counter -= increment
                    testrow += increment
        return answers.reshape(1, answers.size)

    def load_tree_csv(self, filename):
        my_data = np.genfromtxt(filename, delimiter=',')
        self.rt = my_data

    def processleaf_into_ymean(self, data):
        return mode(data[::, -1])[0][0]  # changed to mode
        # return np.mean(data[::, -1])


if __name__ == "__main__":
    print "this program is RTLearner"
    # learner = RTLearner()
    # learner.verbose = False
    #
    # dataX = np.array([
    #     [0.885, 0.330, 9.100, 1],
    #     [0.725, 0.390, 10.900, 2],
    #     [0.560, 0.500, 9.400, 4],
    #     [0.735, 0.570, 9.800, 5],
    #     [0.610, 0.630, 8.400, 6],
    #     [0.260, 0.630, 11.800, 7],
    #     [0.500, 0.680, 10.500, 8],
    #     [0.320, 0.780, 10.000, 2]
    # ])
    # dataY = np.array([
    #     [2.000],
    #     [5.000],
    #     [6.000],
    #     [4.000],
    #     [3.000],
    #     [8.000],
    #     [7.000],
    #     [9.000]
    # ])

    # dataZ = np.array([[  0.725,   0.39 ,  10.9   ,  2. ,     5.   ],
    #                    [  0.56,    0.5 ,    9.4  ,   4.   ,   6.   ]])
    #
    # learner=RTLearner()
    # print(learner.processleaf_into_ymean(dataZ))
    # learner.addEvidence(dataX, dataY)
    # print learner.rt
    # print ("Test value: {}".format(dataX[0]))
    # test = [[0.885, 0.330, 9.100, 1.0]]
    # test = dataX

    # wine practice

    # learner.load_tree_csv("winetree.csv")
    # learner.load_tree_csv("data/winequality-red.csv")
    # print learner.rt
    # test = [
    #     [.88, .33, 9.1],
    #     [.725, .39, 10.9],
    #     [.56, .5, 9.4],
    #     [.735, .570, 9.8],
    #     [.61, .630, 8.4],
    #     [.26, .630, 11.8],
    #     [.5, .680, 10.5],
    #     [.32, .780, 10],
    #     [.5,.2,11]
    # ]

    # print("The estimate is : \n{}".format(learner.query(test)))
