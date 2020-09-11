import pandas as pd


central_file = 'estimate_number_incoming_infected_from_regions_using_estimate.csv'
lower_file = 'estimate_number_incoming_infected_from_regions_using_lower.csv'
upper_file = 'estimate_number_incoming_infected_from_regions_using_upper.csv'

central = pd.read_csv(central_file)
lower = pd.read_csv(lower_file)
upper = pd.read_csv(upper_file)

# df['A'], df['B'] = df['AB'].str.split(' ', 1).str

# central['provider_number'], central['type'] = central['Unnamed: 0'].str.split(" ", 1).str
# lower['provider_number'], lower['type'] = lower['Unnamed: 0'].str.split(" ", 1).str
# upper['provider_number'], upper['type'] = upper['Unnamed: 0'].str.split(" ", 1).str

lower = lower.merge(upper, how='outer', left_on = 'Unnamed: 0', right_on ='Unnamed: 0', suffixes=(' from lower', ' from upper'))

central = central.merge(lower, how='outer', left_on = 'Unnamed: 0', right_on ='Unnamed: 0')

central = central[['Unnamed: 0', 'North East', 'North East from lower', 'North East from upper', 'North West', 'North West from lower', 'North West from upper',
                   'Yorkshire and The Humber', 'Yorkshire and The Humber from lower', 'Yorkshire and The Humber from upper',
                   'East Midlands', 'East Midlands from lower', 'East Midlands from upper',
                   'West Midlands', 'West Midlands from lower', 'West Midlands from upper',
                   'East of England', 'East of England from lower', 'East of England from upper',
                   'London', 'London from lower', 'London from upper',
                   'South East', 'South East from lower', 'South East from upper',
                   'South West', 'South West from lower', 'South West from upper',
                   'Wales', 'Wales from lower', 'Wales from upper',
                   'Scotland', 'Scotland from lower', 'Scotland from upper',
                   'Total Regions', 'Total Regions from lower', 'Total Regions from upper'
                ]]

central.to_csv('estimate_number_incoming_infected_from_regions_combined.csv')



central_file = 'estimate_number_incoming_infected_from_regions_age_adjusted_using_estimate.csv'
lower_file = 'estimate_number_incoming_infected_from_regions_age_adjusted_using_lower.csv'
upper_file = 'estimate_number_incoming_infected_from_regions_age_adjusted_using_upper.csv'

central = pd.read_csv(central_file)
lower = pd.read_csv(lower_file)
upper = pd.read_csv(upper_file)

# df['A'], df['B'] = df['AB'].str.split(' ', 1).str

# central['provider_number'], central['type'] = central['Unnamed: 0'].str.split(" ", 1).str
# lower['provider_number'], lower['type'] = lower['Unnamed: 0'].str.split(" ", 1).str
# upper['provider_number'], upper['type'] = upper['Unnamed: 0'].str.split(" ", 1).str

lower = lower.merge(upper, how='outer', left_on = 'Unnamed: 0', right_on ='Unnamed: 0', suffixes=(' from lower', ' from upper'))

central = central.merge(lower, how='outer', left_on = 'Unnamed: 0', right_on ='Unnamed: 0')

central = central[['Unnamed: 0', 'North East', 'North East from lower', 'North East from upper', 'North West', 'North West from lower', 'North West from upper',
                   'Yorkshire and The Humber', 'Yorkshire and The Humber from lower', 'Yorkshire and The Humber from upper',
                   'East Midlands', 'East Midlands from lower', 'East Midlands from upper',
                   'West Midlands', 'West Midlands from lower', 'West Midlands from upper',
                   'East of England', 'East of England from lower', 'East of England from upper',
                   'London', 'London from lower', 'London from upper',
                   'South East', 'South East from lower', 'South East from upper',
                   'South West', 'South West from lower', 'South West from upper',
                   'Wales', 'Wales from lower', 'Wales from upper',
                   'Scotland', 'Scotland from lower', 'Scotland from upper',
                   'Total Regions', 'Total Regions from lower', 'Total Regions from upper'
                ]]

central.to_csv('estimate_number_incoming_infected_from_regions_age_adjusted_combined.csv')