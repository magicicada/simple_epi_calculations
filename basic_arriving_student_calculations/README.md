Summary of calculation:

In order for higher education providers to be well-prepared for the imminent return of students, as well as for a general understanding of how potentially-infectious students might flow around the country at the beginning of the autumn semester, I thought it might be valuable to have even a rough estimate of the number of COVID-infected students that might be returning higher education providers.  Using data on student domiciles by HE provider and an estimate of prevalence by English region, I have performed a simple calculation for students domiciled in English regions. 

I can be contacted via GitHub message, or by email at jessica.enright@glasgow.ac.uk

**Data sources:**

1. For student flows:  I have rounded used figures provided from HESA via Jisc on the number of students at each HE provider who are domiciled in the different English regions.  These numbers are from academic year 2019/2020, and exclude distance-learning students and students on industrial placements.  When it's clear what sharing of these data are allowed, I will update here.  
2. For estimated number of positive students:  I used figures from Section 3 of https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/conditionsanddiseases/bulletins/coronaviruscovid19infectionsurveypilot/englandandwales14august2020#regional-analysis-of-the-number-of-people-in-england-who-had-covid-19 as the percentage of people with COVID.  Many caveats attach to this, perhaps the most important are: there is a lot of uncertainty, this may not actually be a good estimate of prevalence, and the figures are not specific to the age group that most students are in (which news reports suggest has higher prevalence than the general population right now).
3. For estimated prevalence of antibodies: I used figures from https://www.medrxiv.org/content/10.1101/2020.08.12.20173690v2.full.pdf for regional numbers, as well as the log-odds by age group to adjust for the younger age group within regions.  

**Calculation:**
The calculation is *extremely* simple - I estimate the number of incoming infected students by multiplying the number of incoming students to a HE provider from a region by the percentage of people with COVID from that region.  I have repeated this using the lower and upper confidence limits from Data Source 2.  
- results using the central estimate are in [estimate_number_incoming_infected_from_regions_using_estimate.csv](https://github.com/magicicada/simple_epi_calculations/blob/main/basic_arriving_student_calculations/output_estimate_tables/estimate_number_incoming_infected_from_regions_using_estimate.csv)
- results using the lower confidence limit are in [estimate_number_incoming_infected_from_regions_using_lower.csv](https://github.com/magicicada/simple_epi_calculations/blob/main/basic_arriving_student_calculations/output_estimate_tables/estimate_number_incoming_infected_from_regions_using_lower.csv)
- results using the upper confidence limit are in  [estimate_number_incoming_infected_from_regions_using_upper.csv](https://github.com/magicicada/simple_epi_calculations/blob/main/basic_arriving_student_calculations/output_estimate_tables/estimate_number_incoming_infected_from_regions_using_upper.csv)
- a combination of these tables at [estimate_number_incoming_infected_from_regions_combined.csv](https://github.com/magicicada/simple_epi_calculations/blob/main/basic_arriving_student_calculations/output_estimate_tables/estimate_number_incoming_infected_from_regions_combined.csv)

I have now completed a similar calculation using the same piece of code (invoked using the script run_script_estimates) based on the antibody prevalence estimates in https://www.medrxiv.org/content/10.1101/2020.08.12.20173690v2.full.pdf, both for the overall population in each region and for that prevalence adjusted upwards by the log-odds ratio given for people in the 18-24 age group (note that this simple multiplication has also been applied to the upper and lower confidence values).  The output tables are similarly in https://github.com/magicicada/simple_epi_calculations/blob/main/basic_arriving_student_calculations/output_estimate_tables/

**Major Limitations:**

1. The flows of students are from a previous non-pandemic year, and may not accurately reflect the movements of students this year
2. The use of data on modelled percentage of people in a region testing positive as prevalence may be unsuitable for a number of reasons: the measure may just not be suitable for prevalence, it is not specific to the age group, there is significant uncertainty, is at a broad geographic scale, etc. 
3. The calculation is very simple.  There will be a better way to do this that captures uncertainty more robustly.
4. I’ve not included any consideration of symptomatic infections moving or not moving differently to others.  I’ve not explicitly considered exposed vs asymptomatic vs infectious groups, etc.  
5. The antibody prevalences are from a moment in time, and I have not modelled any further accumulation not any decay of antibodies. 
6. I have only included students domiciled in English regions.

I want to especially repeat one of those: recently, news reports have suggested that prevalence is highest in the UK in young people.  I have used estimates from the general population.

**Next steps:**

I am planning to expand this work in several ways, including incorporating international students and UK students not from England, performing a similar calculation on antibody prevalence, etc.  