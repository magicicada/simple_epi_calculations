#  Expected number of cases prior to detection by symptomatic testing

This small piece of Python code uses a doubling-time-based exponential process to model an early outbreak, with the aim of calculating distributions of numbers of cases on the day of detection of the outbreak *if detection is relying on symptomatic infected people seeking testing*.

It is simplistic and misses many realistic characteristics of a disease process, but may help provide back-of-the-envelope style estimates. 

## Adjustable parameters

In the Jupyter notebook in this repository, you can adjust sliders to set three parameters:

- **doubling_time** is the doubling time (in days) of the number of *new* daily cases. This is the only specification of the epidemic growth process. There is no latent period or recovery, nor stochasticity or super-spreading, nor any other disease model.
- **post_infection_delay** is the number of days after intially being infected that an infected person who will have symptoms finds out that they are infectious - the day the outbreak is detected. This might include an asymptomatic period of several days as well as a testing delay. So, for example, if you believe that a person is infectious for two days before being symptomatic, and then takes 1 day to seek a test once symptoms appear, then you might set this at three days.
- **fraction_non_testing** is the fraction of infected people who will never develop symptoms, or will not seek a test for some other reason. E.g. if you believe that half of your population would develop symptoms if infected and all of them would seek a test if they had symptoms, then this should be 0.5.    If you believe that half your population would develop symptoms, but only half of those would seek testing, then only one-quarter of your infectious people would seek testing and you should set this to 0.75.  There is significant uncertainty about this number for COVID-19, and it is likely that this will vary by age class and social setting.

## Outline of the calculation

Given the doubling time specified I calculate the number of new cases on each day (as a deterministic simple exponential, this will include fractional values).  Then, for each day I calculate the probability that no persion infected previously will seek testing but that someone infected that day will seek testing (that is, that it is the first day on which a person who will eventually seek testing is infected).  Combining those probabilities with the delay and the case numbers, I then find the number of cases we expect to already exist on the day of detection.  

## Running the notebook

If you can run a Jupyter notebook locally, you're certainly welcome to - or feel free to use the code without the notebook to run your own things.  If you'd just like to run the notebook and change the sliders online, you could try using: 

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/magicicada/simple_epi_calculations/master)

And navigate to the appropriate notebook

If the notebook is inconvenient for you and you'd like output as a table or some custom things run, I'm happy to help if I can - contact me at Jessica.Enright@glasgow.ac.uk


## Static Figures

In case you want a quick look, I have generated some large grids of figures for non-testing fractions of 0.25, 0.5, 0.75 over a small range of delays and doubling times.  These, along with the code that generated them, are available in:

https://github.com/magicicada/simple_epi_calculations/tree/master/cases_on_detection_from_doubling_time/generating_static_figures

As an example of one of these individual subplots, here is an example image for doubling time 4, delay 4, non-testing fraction 0.75:

![A plot of probability distribution of number of cases on detection day](/generating_static_figures/sample_cases_figure.png)

The blue line shows the probability of different numbers of cases on the day of detection. The red vertical line indicates the expected number, repeated in the red text.  
 
