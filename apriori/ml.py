from apyori import apriori
import pandas as pd

class Apriori:

    def __init__(self, datafile):
        self.datafile = datafile

    def process(self):
        dataset = pd.read_csv(self.datafile, header = None)

        transactions = []
        rows = dataset.shape[0]
        columns = dataset.columns.size
        for i in range(0, rows):
            transactions.append([str(dataset.values[i,j]) for j in range(0, columns)])

        rules = apriori(transactions = transactions, min_support = 0.003, min_confidence = 0.2, min_lift = 3, min_length = 2, max_length = 2)
        results = list(rules)
        return self.inspect(results)

    def inspect(self, results):
        lhs         = [tuple(result[2][0][0])[0] for result in results]
        rhs         = [tuple(result[2][0][1])[0] for result in results]
        supports    = [result[1] for result in results]
        confidences = [result[2][0][2] for result in results]
        lifts       = [result[2][0][3] for result in results]
        return list(zip(lhs, rhs, supports, confidences, lifts))