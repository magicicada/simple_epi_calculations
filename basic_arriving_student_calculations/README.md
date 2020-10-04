Summary of calculation:

In order for higher education providers to be well-prepared for the imminent return of students, as well as for a general understanding of how potentially-infectious students might flow around the country at the beginning of the autumn semester, I thought it might be valuable to have even a rough estimate of the number of COVID-infected students that might be returning higher education providers.  Using data on student domiciles by HE provider and an estimate of prevalence by English region plus Wales, I have performed a simple calculation for students domiciled in English regions, Scotland, or in Wales. 

I can be contacted via GitHub message, or by email at jessica.enright@glasgow.ac.uk

*October 4th Update: Given the recent REACT Interim report giving higher prevalence estimates for a period ending in late September, I have added a version of this calculation that uses the raw prevalence figures from that [REACT update](https://www.imperial.ac.uk/media/imperial-college/institute-of-global-health-innovation/REACT1_12345_Interim-(1).pdf) - for this update I have used Scottish prevalence estimates from a forecast for the end of September in [issue 19 of the modelling the epidemic in Scotland report](https://www.gov.scot/publications/coronavirus-covid-19-modelling-epidemic-issue-no-19/).  The age-adjusted results based on the REACT-1 interim regional figures (round 5) are in [react_based_estimate_number_incoming_infected_from_regions_age_adjusted_combined.csv](/output_estimate_tables/react_based_estimate_number_incoming_infected_from_regions_age_adjusted_combined.csv)*



**Data sources:**

1. For student flows:  I have rounded used figures provided from HESA via Jisc on the number of students at each HE provider who are domiciled in the different English regions, or in Wales.  These numbers are from academic year 2019/2020, and exclude distance-learning students and students on industrial placements.  When it's clear what sharing of these data are allowed, I will update here.  
2. For estimated number of positive students from England and Wales:  I used figures from https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/conditionsanddiseases/bulletins/coronaviruscovid19infectionsurveypilot/englandandwales25september2020 as the percentage of people with COVID, as well as from the section on Wales in that same page.  Many caveats attach to this. Perhaps the most important are: there is a lot of uncertainty, this may not actually be a good estimate of prevalence, and the figures are not specific to the age group that most students are in (which news reports suggest has higher prevalence than the general population right now).
3. For estimated prevalence of antibodies: I used figures from https://www.medrxiv.org/content/10.1101/2020.08.12.20173690v2.full.pdf for regional numbers, as well as the log-odds by age group to adjust for the younger age group within regions.  I do not yet have figures for Wales.
4. For estimated number of positive students from Scotland: from the update I have made on 25th September, I am now using modelled numbers of infections from https://www.gov.scot/binaries/content/documents/govscot/publications/research-and-analysis/2020/09/coronavirus-covid-19-modelling-epidemic-issue-no-192/documents/coronavirus-covid-19-modelling-epidemic-scotland-issue-no-19/coronavirus-covid-19-modelling-epidemic-scotland-issue-no-19/govscot%3Adocument/coronavirus-covid-19-modelling-epidemic-scotland-issue-no-19.pdf
5. For age adjustments: I have used information from https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/conditionsanddiseases/bulletins/coronaviruscovid19infectionsurveypilot/25september2020 that gives age-trend information for England to adjust the regional figures to reflect a higher incidence of disease in people between 17 and 24.  The way I have done this is quite crude: I have calculated the ratio between the infection rate in people between 17 and 24 in the England and the overall rate in the England, and have then multiplied that ratio by the overall rates in the other regions to generate estimated rates amongst people between 17 and 24 in those other regions.  I am very aware that this adds even more uncertainty to this work - if you have a source of regional age-stratified data please contact me and I will include it gratefully.

**Calculation:**
The calculation is *extremely* simple - I estimate the number of incoming infected students by multiplying the number of incoming students to a HE provider from a region by the percentage of people with COVID from that region/nation.  I have repeated this using the lower and upper confidence limits from Data Source 2.   Note that in these tables the number before the institution name is part of the institution name, and not part fo the calculation.  

- results using the central estimate are in [estimate_number_incoming_infected_from_regions_using_estimate.csv](https://github.com/magicicada/simple_epi_calculations/blob/master/basic_arriving_student_calculations/output_estimate_tables/estimate_number_incoming_infected_from_regions_using_estimate.csv)
- results using the lower confidence limit are in [estimate_number_incoming_infected_from_regions_using_lower.csv](https://github.com/magicicada/simple_epi_calculations/blob/master/basic_arriving_student_calculations/output_estimate_tables/estimate_number_incoming_infected_from_regions_using_lower.csv)
- results using the upper confidence limit are in  [estimate_number_incoming_infected_from_regions_using_upper.csv](https://github.com/magicicada/simple_epi_calculations/blob/master/basic_arriving_student_calculations/output_estimate_tables/estimate_number_incoming_infected_from_regions_using_upper.csv)
- a combination of these tables at [estimate_number_incoming_infected_from_regions_combined.csv](https://github.com/magicicada/simple_epi_calculations/blob/master/basic_arriving_student_calculations/output_estimate_tables/estimate_number_incoming_infected_from_regions_combined.csv)

As described above, I've attempted to adjust the infection figures using data on the infection levels amongst younger people in the East Midlands.  These tables are also available in the output directory, in particular 
- the combined table that incorporates calculations from central, lower, and upper values is in [estimate_number_incoming_infected_from_regions_age_adjusted_combined.csv](https://github.com/magicicada/simple_epi_calculations/blob/master/basic_arriving_student_calculations/output_estimate_tables/estimate_number_incoming_infected_from_regions_age_adjusted_combined.csv)


I have now completed a similar calculation using the same piece of code (invoked using the script run_script_estimates) based on the antibody prevalence estimates in https://www.medrxiv.org/content/10.1101/2020.08.12.20173690v2.full.pdf, both for the overall population in each region and for that prevalence adjusted upwards by the log-odds ratio given for people in the 18-24 age group (note that this simple multiplication has also been applied to the upper and lower confidence values).  The output tables are similarly in https://github.com/magicicada/simple_epi_calculations/blob/master/basic_arriving_student_calculations/output_estimate_tables/

**Major Limitations:**

1. The flows of students are from a previous non-pandemic year, and may not accurately reflect the movements of students this year
2. The use of data on modelled percentage of people in a region testing positive as prevalence may be unsuitable for a number of reasons: the measure may just not be suitable for prevalence, it is not specific to the age group, there is significant uncertainty, is at a broad geographic scale, etc. 
3. The calculation is very simple.  There will be a better way to do this that captures uncertainty more robustly.
4. I’ve not included any consideration of symptomatic infections moving or not moving differently to others.  I’ve not explicitly considered exposed vs asymptomatic vs infectious groups, etc.  
5. The antibody prevalences are from a moment in time, and I have not modelled any further accumulation nor any decay of antibodies. 
6. I have only included students domiciled in English regions, or in Wales or Scotland.


**Next steps:**

- Because students will shortly have returned to universities, this calculation will soon no longer be useful.  I am planning to repurpose this work to calculate the reverse: how much out-going infection from universities to out-of-term addresses we might expect should students leave their university address.  
