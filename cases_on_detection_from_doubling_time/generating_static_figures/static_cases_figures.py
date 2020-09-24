import matplotlib.pyplot as plt
import math

def gen_prob_first_sympt_infected_on_day(cases, prob_asympt):
  dist = []
  prev_prob = [0]
  for i in range(len(cases)):
    undetect_today = (prob_asympt)**cases[i]
    detect_today= 1-undetect_today
    detect_first_today = (1-prev_prob[i])*detect_today
    dist.append(detect_first_today)
    prev_prob.append(prev_prob[i] + detect_first_today)
  return dist

def threshold_out_tail(cases, probs, thresh):
  for i in range(len(probs)):
    if probs[i] < thresh:
      return cases[:i], probs[:i]
  return cases,probs

def dist_num_cases_on_detection(cases, first_day_sympt_dist, delay):
  num_cases = []
  prob = []
  for i in range(len(cases)-delay):
    prob.append(first_day_sympt_dist[i])
    num_cases.append(sum(cases[:i+delay]))
  return num_cases,prob


def gen_number_cases_list(doubling_time, horizon):
  lambda_rate = 0.693/doubling_time
  cases = []
  for i in range(horizon):
    cases.append(math.exp(i*lambda_rate))
  return cases

def gen_prob_detect(cases, prob_asympt):
  prob_det = []
  for i in range(len(cases)):
    prob_det.append(1-(prob_asympt)**cases[i])
  return prob_det

def expected_number_cases(doubling_time, prob_asympt, post_infection_delay = 2, horizon=10):
  thresh = 1/(1-prob_asympt)
  cases = gen_number_cases_list(doubling_time, horizon=horizon)
  day_shut = day_of_shutdown(cases, thresh, post_infection_delay)
  return cases[day_shut]

def cumulative(list_name):
  cum_list = []
  for i in range(len(list_name)):
    cum_list.append(sum(list_name[:i]))
  return cum_list


tail_thresh = 0.0001
max_double=15
max_delay=7



for fraction_non_testing in [0.25, 0.5, 0.75]:
  plt.clf()
  fig, axs = plt.subplots(int(max_double/2), int(max_delay/2), figsize=(25, 25))
  fig.subplots_adjust(hspace=.5)
  axes = plt.gca()
  for doubling_time in range(2, max_double,2):
    for post_infection_delay in range(2, max_delay,2):
      i = int(doubling_time/2-1)
      j = int(post_infection_delay/2-1)
      cases = gen_number_cases_list(doubling_time, horizon=20)
      first_day_dist = gen_prob_first_sympt_infected_on_day(cases, fraction_non_testing)
   
      expect_cases,prob = dist_num_cases_on_detection(cases, first_day_dist, post_infection_delay)
      expect_cases,prob = threshold_out_tail(expect_cases,prob,tail_thresh)
      cum_expect_cases = cumulative(expect_cases) 
      expectation = sum([a*b for a,b in zip(cum_expect_cases,prob)])
      
      # print('Expected number of cases on day of detection ' + str(round(expectation, 2)))
   
      axs[i,j].plot(expect_cases, prob)
      axs[i,j].set_ylim(0, 1.0)
      axs[i,j].set_xlim(0, 50)
      #  plt.xlim(1,100)
      #  print(expect_cases)
      #  print(prob)
      #  print(sum(prob))
      x_pos = 12
      y_pos = 0.5
      axs[i,j].text(x_pos, y_pos, 'Expected number of cases \n on day of detection: ' + str(round(expectation, 2)), color='red')
      
      axs[i,j].set_xlabel('Number of cases on day of detection')
      axs[i,j].set_ylabel('Probability')
      axs[i,j].axvline(x=expectation, color='red')
      axs[i, j].set_title('Doubling time '+ str(doubling_time) + ' , Delay of ' + str(post_infection_delay))
  plt.savefig('cases_before_detection_non_testing_'+ str(fraction_non_testing) + '.png' )
