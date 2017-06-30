import numpy as np
import RTLearner as rt
from scipy.stats import mode

class BagLearner(object):
    def __init__(self, learner, kwargs, bags, boost=False, verbose=False):
        self.learner = learner
        self.kwargs = kwargs
        self.bags = bags
        self.boost = boost
        self.v = verbose
        pass  # move along, these aren't the drones you're looking for

    def addEvidence(self, Xtrain, Ytrain):
        """
        @summary: Add training data to learner
        @param dataX: X values of data to add
        @param dataY: the Y training values
        """
        self.learners = []
        kwargs = self.kwargs

        for i in range(self.bags):
            self.learners.append(rt.RTLearner(**kwargs))
            learner = self.learners[i]
            bagX, bagY = self.random_bagmakerXY(Xtrain, Ytrain)
            learner.addEvidence(bagX, bagY)

    def random_bagmakerXY(self, dataX, dataY):
        rows = dataX.shape[0]
        bagX = np.array([])
        bagY = np.array([])
        for x in range(int(rows * .6)):
            randomrow = int(np.random.rand() * rows)
            if bagX.size == 0:
                bagX = dataX[randomrow]
                bagY = dataY[randomrow]
            else:
                bagX = np.vstack([bagX, dataX[randomrow]])
                bagY = np.vstack([bagY, dataY[randomrow]])
        return bagX, bagY

    def query(self, points):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """
        avgdata = []
        for learner in self.learners:
            if len(avgdata) == 0:
                avgdata = learner.query(points)
            else:
                avgdata = np.vstack([avgdata, learner.query(points)])
        # print avgdata
        # print avgdata.mean(axis=0)
        # yvalues = np.zeros(avgdata.shape[1])
        # for x in range(avgdata.shape[1]):
        #     yvalues[x] = np.mean(avgdata[0::, x])
        print "**Baglearner**"
        print avgdata
        return mode(avgdata, axis=0, )[0]
        # return avgdata.mean(axis=0)


if __name__ == "__main__":
    print "This is BagLearner"
    dataX = np.array([
        [0.885, 0.330, 9.100, 1],
        [0.725, 0.390, 10.900, 2],
        [0.560, 0.500, 9.400, 4],
        [0.735, 0.570, 9.800, 5],
        [0.610, 0.630, 8.400, 6],
        [0.260, 0.630, 11.800, 7],
        [0.500, 0.680, 10.500, 8],
        [0.320, 0.780, 10.000, 2]
    ])
    dataY = np.array([
        [2.000],
        [5.000],
        [6.000],
        [4.000],
        [3.000],
        [8.000],
        [7.000],
        [9.000]
    ])

    learner = BagLearner(learner=rt.RTLearner, kwargs={"leaf_size": 1}, bags=20, boost=False, verbose=False)
    learner.addEvidence(dataX, dataY)
    print(learner.query(dataX))
