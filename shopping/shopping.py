import csv
import sys


from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidence = []

    label = []
    i = 0
    with open(filename) as f:
        reader = csv.reader(f)
        for row in reader:
            if i == 0:
                i=1
            else:
                l = []

                l.append(int(row[0]))
                l.append(float(row[1]))
                l.append(int(row[2]))
                l.append(float(row[3]))
                l.append(int(row[4]))
                l.append(float(row[5]))
                l.append(float(row[6]))
                l.append(float(row[7]))
                l.append(float(row[8]))
                l.append(float(row[9]))
                if row[10] == "Jan":
                    l.append(0)
                elif row[10] == "Feb":
                    l.append(1)
                elif row[10] == "Mar":
                    l.append(2)
                elif row[10] == "Apr":
                    l.append(3)
                elif row[10] == "May":
                    l.append(4)
                elif row[10] == "June":
                    l.append(5)
                elif row[10] == "Jul":
                    l.append(6)
                elif row[10] == "Aug":
                    l.append(7)
                elif row[10] == "Sep":
                    l.append(8)
                elif row[10] == "Oct":
                    l.append(9)
                elif row[10] == "Nov":
                    l.append(10)
                elif row[10] == "Dec":
                    l.append(11)
                l.append(int(row[11]))
                l.append(int(row[12]))
                l.append(int(row[13]))
                l.append(int(row[14]))

                if row[15] == "Returning_Visitor":
                    l.append(1)
                else:
                    l.append(0)

                if row[16] == "TRUE":
                    l.append(1)
                else:
                    l.append(0)

                evidence.append(l)


                if row[17] == "TRUE":
                    label.append(1)
                else:
                    label.append(0)

    return (evidence, label)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    X: list = evidence
    Y: list = labels

    model.fit(X, Y)

    return model

def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """

    x: list = labels

    y: list = predictions
    correct_1 = 0
    correct_0 = 0
    total_1 = 0
    total_0 = 0
    for index in range(x.__len__()):
        label = x.pop(0)
        pred = y[index]
        if label == 1:
            total_1 = total_1 + 1
            if label == pred:
                correct_1 = correct_1+1
        else:
            total_0 = total_0 + 1
            if label == pred:
                correct_0 = correct_0 + 1
        x.append(label)
    return (correct_1/total_1,correct_0/total_0)



if __name__ == "__main__":
    main()
