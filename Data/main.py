import matplotlib.pyplot as plt

def plot_data(x,y):
    x = [1, 2, 3, 4]
    y = [10, 20, 25, 30]


    plt.plot(x,y)
    plt.title('Sample Data')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')

    plt.show()

plot_data()