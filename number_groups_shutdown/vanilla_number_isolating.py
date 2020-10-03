import matplotlib.pyplot as plt
import math


def isolating_function_one_layer(p, group_sizes):
   return [1-(1-p)**k  for k in group_sizes ]


def plot_isolation_probabilities_one_layer():
   prevs = [0.001, 0.005, 0.01, 0.02]
   group_sizes=list(range(10, 100))
   for p in prevs:
      this_plot = isolating_function_one_layer(p, group_sizes)
      plt.plot(group_sizes, this_plot, label='Individual Test+ Prob: ' + str(p))
      
   plt.xlabel('Group Size')
   plt.ylabel('Probability of a test-positive in a single group')
   plt.legend()
   plt.savefig('isolation_probabilities_one_layer.png')
     

plot_isolation_probabilities_one_layer()