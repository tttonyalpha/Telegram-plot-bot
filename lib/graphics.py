import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io
from scipy.optimize import curve_fit
from PIL import Image


# Импорт библиотек


class GraphicPlotter:
    def plot_from_string(self, data_string):
        plt.rcParams["figure.figsize"] = [7.50, 3.50]
        plt.rcParams["figure.autolayout"] = True

        # Вставка данных
        data = io.StringIO(data_string)
        df = pd.read_csv(data, sep=" ")
        # print(list(df.axes[1]))
        if len(list(df.axes[1])) == 2:
            y = df.plot(x=(list(df.axes[1]))[0], y=(
                list(df.axes[1]))[1], color="blue", legend=False)
            y.set_xlabel('Ось x')
            y.set_ylabel('Ось y')
            y.set_title('Ваш график')

            img_buf = io.BytesIO()
            plt.savefig(img_buf, format='png')

            im = img_buf.getvalue()

            img_buf.close()
            return im
        else:
            raise ValueError(
                f"Expected 2 rows of data, but got {len(list(df.axes[1]))}")

    def all_changes(self, data_string, color, x_label, y_label, title):
        plt.rcParams["figure.figsize"] = [7.50, 3.50]
        plt.rcParams["figure.autolayout"] = True

        # Вставка данных
        data = io.StringIO(data_string)
        df1 = pd.read_csv(data, sep=" ")

        y = df1.plot(x=(list(df1.axes[1]))[0], y=(
            list(df1.axes[1]))[1], color=color, legend=False)
        y.set_xlabel(x_label)
        y.set_ylabel(y_label)
        y.set_title(title)

        img_buf = io.BytesIO()
        plt.savefig(img_buf, format='png')

        im1 = img_buf.getvalue()

        img_buf.close()
        return im1

    def approximation(self, data_string, color, x_label, y_label, title):
        plt.rcParams["figure.figsize"] = [7.50, 3.50]
        plt.rcParams["figure.autolayout"] = True

        # Вставка данных
        data = io.StringIO(data_string)
        df1 = pd.read_csv(data, sep=" ")
