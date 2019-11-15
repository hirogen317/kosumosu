from kosumosu.core.chart import Chart




def plot_auc(true_positive_rate, false_positive_rate, title=None):
    ch = Chart()
    ch.line(x, y)
    ch.area(x, 0, y)
    return ch


def plot_epoch_value(x):
    """
    epoch loss or epoch accuracy

    :param x:
    :return:
    """

    ch = Chart()
    ch.line(x, y, )

    return ch


def plot_precious_recall(precious, recall):

    ch = Chart()
    ch.line(x, y)
    ch.area(x, 0, y)
    return ch


def plot_confusion_matrix(y_true, y_pred):
    color = heatmap()
    ch = Chart()
    ch.set_palette()
