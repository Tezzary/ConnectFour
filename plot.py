import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('TkAgg')

plt.ion()

mean_smoothing = 5

loss_list = []
def plot(loss):

    loss_list.append(loss)
    #Plotting Scores
    plt.figure(1)
    plt.clf()
    plt.title('Loss Graph...')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.plot(loss_list)

    '''if len(loss_list) >= mean_smoothing:
        #plot smoothed scores on same graph
        smoothed_durations = []
        for i in range(mean_smoothing):
            smoothed_durations.append(sum(loss_list[:i])/(i+1))
        for i in range(mean_smoothing, len(loss_list)):
            smoothed_durations.append(sum(loss_list[i-mean_smoothing:i])/mean_smoothing)

        plt.plot(smoothed_durations)'''
    plt.show()
    plt.pause(0.01)
