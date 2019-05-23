from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib.lines import Line2D


def visualize(state):
    def get_color_for(flag):
        if flag:
            return "green"
        else:
            return "red"

    def locs_to_coord_lists(insp):
        result = ([], [], [])
        for (x, y, z) in insp:
            result[0].append(x)
            result[1].append(y)
            result[2].append(z)
        return result

    fig = plt.figure()
    plt.subplots_adjust(bottom=0.2)
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(state[0][0][0], state[0][0][1], state[0][0][2], c='g', marker='s', s=50)
    ax.scatter(state[0][1][0], state[0][1][1], state[0][1][2], c='r', marker='x', s=50)
    insp = locs_to_coord_lists(state[0][2])
    ax.scatter(insp[0], insp[1], insp[2], c='b', marker='^', s=50)
    ax.grid(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.set_zlim3d(state[0][4][0], state[0][4][1])
    plt.title("Plan(0) = " + state[0][3], color=get_color_for(state[0][5]))

    disp_text = ""
    disp_text += "Battery level = " + str(state[0][6]) + "\n"
    disp_text += "Target = " + state[0][7] + "\n"
    disp_text += "Current distance to Target = " + str(state[0][8]) + "\n"
    disp_text += "Current distance to Home = " + str(state[0][9]) + "\n"
    disp_text += "Current distance to Restricted Area = " + str(state[0][10])
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0.95, 0.95, 0.95, disp_text, transform=ax.transAxes, fontsize=11, verticalalignment='bottom', bbox=props)

    time = state.__len__()

    legend_elements = [Line2D([0], [0], color='w', markerfacecolor='g', marker='s', label='Home', markersize=15),
                       Line2D([0], [0], color='r', lw=0, marker='x', label='Drone', markersize=15),
                       Line2D([0], [0], color='w', markerfacecolor='b', marker='^', label='Inspection Location', markersize=15)]
    ax.legend(handles=legend_elements, loc='lower right')

    class Index(object):
        ind = 0
        ax = None

        def set_axx(self, ax):
            self.ax = ax

        def next(self, _):
            curr_azim = self.ax.azim
            curr_elev = self.ax.elev
            self.ind += 1
            i = self.ind % time
            plt.subplots_adjust(bottom=0.2)
            ax = fig.add_subplot(111, projection='3d')
            ax.view_init(elev=curr_elev, azim=curr_azim)
            ax.scatter(state[i][0][0], state[i][0][1], state[i][0][2], c='g', marker='s', s=50)
            ax.scatter(state[i][1][0], state[i][1][1], state[i][1][2], c='r', marker='x', s=50)
            insp = locs_to_coord_lists(state[i][2])
            ax.scatter(insp[0], insp[1], insp[2], c='b', marker='^', s=50)
            ax.grid(False)
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_zticks([])
            ax.set_zlim3d(state[i][4][0], state[i][4][1])
            ax.legend(handles=legend_elements, loc='lower right')
            self.ax.remove()
            self.ax = ax
            plt.title("Plan(" + str(i) + ") = " + state[i][3], color=get_color_for(state[i][5]))
            plt.draw()

            disp_text = ""
            disp_text += "Battery level = " + str(state[i][6]) + "\n"
            disp_text += "Target = " + state[i][7] + "\n"
            disp_text += "Current distance to Target = " + str(state[i][8]) + "\n"
            disp_text += "Current distance to Home = " + str(state[i][9]) + "\n"
            disp_text += "Current distance to Restricted Area = " + str(state[i][10])
            ax.text(0.95, 0.95, 0.95, disp_text, transform=ax.transAxes, fontsize=11, verticalalignment='bottom', bbox=props)

        def prev(self, _):
            curr_azim = self.ax.azim
            curr_elev = self.ax.elev
            self.ind -= 1
            i = self.ind % time
            plt.subplots_adjust(bottom=0.2)
            ax = fig.add_subplot(111, projection='3d')
            ax.view_init(elev=curr_elev, azim=curr_azim)
            ax.scatter(state[i][0][0], state[i][0][1], state[i][0][2], c='g', marker='s', s=50)
            ax.scatter(state[i][1][0], state[i][1][1], state[i][1][2], c='r', marker='x', s=50)
            insp = locs_to_coord_lists(state[i][2])
            ax.scatter(insp[0], insp[1], insp[2], c='b', marker='^', s=50)
            ax.grid(False)
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_zticks([])
            ax.set_zlim3d(state[i][4][0], state[i][4][1])
            ax.legend(handles=legend_elements, loc='lower right')
            self.ax.remove()
            self.ax = ax
            plt.title("Plan(" + str(i) + ") = " + state[i][3], color=get_color_for(state[i][5]))
            plt.draw()

            disp_text = ""
            disp_text += "Battery level = " + str(state[i][6]) + "\n"
            disp_text += "Target = " + state[i][7] + "\n"
            disp_text += "Current distance to Target = " + str(state[i][8]) + "\n"
            disp_text += "Current distance to Home = " + str(state[i][9]) + "\n"
            disp_text += "Current distance to Restricted Area = " + str(state[i][10])
            ax.text(0.95, 0.95, 0.95, disp_text, transform=ax.transAxes, fontsize=11, verticalalignment='bottom', bbox=props)
    callback = Index()
    callback.set_axx(ax)
    axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
    axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
    bnext = Button(axnext, 'Next')
    bnext.on_clicked(callback.next)
    bprev = Button(axprev, 'Previous')
    bprev.on_clicked(callback.prev)

    plt.show()
