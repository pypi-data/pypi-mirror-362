import geci_plots as gp
import matplotlib.pyplot as plt


def plot_progress_probability(data):
    _, ax = gp.geci_plot()

    eradication = 0.80
    control = 0.50

    ax.fill_between(data.Fecha, 1, eradication, facecolor="green", alpha=0.5)
    ax.fill_between(data.Fecha, eradication, control, facecolor="yellow", alpha=0.5)
    ax.fill_between(data.Fecha, control, 0, facecolor="red", alpha=0.5)
    ax.scatter(data.Fecha, data.prob, color="black")
    ax.plot(data.Fecha, data.prob, color="black", alpha=0.3)
    locs, labels = plt.xticks()

    labels = [item.get_text()[:7] for item in labels]
    plt.xticks(locs, labels, rotation=90)
    plt.ylabel("Progress probability", fontsize=20)

    return ax
