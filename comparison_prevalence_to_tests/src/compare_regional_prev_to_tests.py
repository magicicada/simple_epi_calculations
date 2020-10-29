import pandas as pd
import matplotlib.pyplot as plt
import datetime

def read_MSOA_tests_new(filename_data, lookup_file):
    msoa_field_lookup = 'msoa11_cd'
    rgn_field_lookup = 'rgn19_nm'
    msoa_field_data = 'areaCode'
    case_count_field = 'newCasesBySpecimenDateRollingSum'
    df = pd.read_csv(filename_data).fillna(0)
    df_lookup =pd.read_csv(lookup_file)
    df = df.merge(df_lookup, how = 'left', left_on = msoa_field_data, right_on = msoa_field_lookup)
    df = df[[rgn_field_lookup, 'date', case_count_field]]
    df = df.groupby([rgn_field_lookup, 'date']).sum().reset_index()
    
    return df

def read_MSOA_tests(filename_data, region_field = 'rgn19_nm'):
    df = pd.read_csv(filename_data)
    week_prefix = 'wk_'
    week_cols = {}
    week_cols_dates = {}
    for name in df.columns:
        if name.startswith(week_prefix):
            week_cols[name] = name.split("_")[1]
            week_string = '2020-W' + str(week_cols[name])
            print(week_string)
            week_cols_dates[name] = datetime.datetime.strptime(week_string + '-1', "%Y-W%W-%w")
            print(datetime.datetime.strptime(week_string, "%Y-W%W"))
            
    print(week_cols_dates)        
    print(df)
    df = df.replace(to_replace=-99, value=0)
    df = df[[region_field] + list(week_cols.keys())]
    df = df.groupby(region_field).sum().reset_index()
    df = df.rename(columns=week_cols_dates)
    print(df)
    
lookup_file='data/msoa_to_region_lookup.csv'
msoa_data_file = 'data/MSOAs_latest.csv'
# read_MSOA_tests(msoa_data_file)
df_tests = read_MSOA_tests_new(msoa_data_file, lookup_file)

prevalence_file = 'data/prevalence_est_ons.xlsx'
df_prev = pd.read_excel(prevalence_file)

df_prev['Date'] = pd.to_datetime(df_prev['Date'])
df_tests['date'] =  pd.to_datetime(df_tests['date'])

print(df_tests)
print(df_prev)

df_prev = df_prev.set_index('Date')
# df_prev['dummy'] = 'a'
regions = df_prev.columns
build_prev = df_prev[[regions[0]]]
# 
build_prev['region'] =regions[0]
build_prev = build_prev.reset_index()
build_prev.columns = ['Date', 'estimated_cases', 'region']


for i in range(1,len(regions)):
    tmp = df_prev[[regions[i]]]
    tmp['region'] =regions[i]
    tmp = tmp.reset_index()
    tmp.columns = ['Date', 'estimated_cases', 'region']
    build_prev=pd.concat([build_prev,tmp])
    
build_prev = build_prev[['region', 'Date','estimated_cases' ]]
print(build_prev)

print(regions)

# 
# 
together = df_tests.merge(build_prev, how = 'inner', left_on=['rgn19_nm', 'date'], right_on = ['region','Date'])
# together['ThisOne'] = together['rgn19_nm']
# 
fig, axs = plt.subplots(1,2, figsize=(5, 5))
together = together[['rgn19_nm', 'date', 'newCasesBySpecimenDateRollingSum', 'estimated_cases']]
together['multiplier'] = together['estimated_cases']/together['newCasesBySpecimenDateRollingSum']
print(together)
plt.xticks(rotation=45)

colours = {'London': 'blue', 'South West': 'orange', 'South East': 'pink', 'East of England': 'grey',
           'West Midlands':'black', 'East Midlands': 'red', 'Yorkshire and The Humber': 'green', 'North West': 'purple', 'North East': 'brown'}

for region in regions:
    thisPlot =together[together['rgn19_nm'] == region]
    x = thisPlot['date']
    y = thisPlot['newCasesBySpecimenDateRollingSum']
    axs[0].plot(x, y)
    print(thisPlot)
    plt.xticks(rotation=45)
    
for region in regions:
    thisPlot =together[together['rgn19_nm'] == region]
    x = thisPlot['date']
    y = thisPlot['multiplier']
    axs[1].plot(x, y, label = region, color=colours[region])
    print(thisPlot)
    plt.xticks(rotation=45)
    
    axs[1].set_ylabel('Total Weekly Cases/ONS Modelled Number of Cases')

    
plt.xticks(rotation=45)
axs[1].legend()

plt.xticks(rotation=45)
plt.show()
# together.to_csv('together.csv')