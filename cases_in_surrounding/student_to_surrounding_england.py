import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

def get_week_delay_network(cases_df, source_interest, edges, week_num, week_field = 'specimen_date', place_field = 'datazone2011', cases_field = 'cases'):
    cases_at_source = []
    cases_at_dest = []
    # for each edge of interest, cases at source, cases at dest in appropriate week     
    for (u, v) in edges:
        # print(u)
        # print(source_interest)
        # u = str(u)
        if u in source_interest:
            # print('interesting u found')
            just_source = cases_df[cases_df[week_field] == week_num]
            just_source = just_source[just_source[place_field]== u]
            if len(just_source[cases_field]) > 1:
                print('cases not exactly specified by week and location')
            elif len(just_source[cases_field]) < 1:
                cases_source = 0
            else:
                cases_source = list(just_source[cases_field])[0]
            just_dest = cases_df[cases_df[week_field] == week_num + 1]
            just_dest = just_dest[just_dest[place_field]== v]
            if len(just_dest[cases_field]) > 1:
                print('cases not exactly specified by week and location')
            elif len(just_dest[cases_field]) < 1:
                cases_dest = 0
            else:
                cases_dest = list(just_dest[cases_field])[0]
            cases_at_source.append(cases_source)
            cases_at_dest.append(cases_dest)
    

    return cases_at_source, cases_at_dest



def loading_and_IZ():
    cases_file ='data/MSOAs_latest.csv'
    student_num_file = 'data/student_numbers_msoa.csv'
    msoa_pop_file = 'data/msoa_persons_2019.csv'

    region_cases = 'areaCode'
    date_cases = 'date'
    cases_field = 'newCasesBySpecimenDateRollingSum'
    
    region_pop = 'MSOA Code'
    pop_pop = 'All Ages'
    
    region_student = 'geography code'
    student_student = 'Student accommodation: All categories: Student accommodation; Economic Activity: All categories: Full-time students and economic activity; Age: All categories: Age 16 and over; measures: Value'
    
    cases_df = pd.read_csv(cases_file)
    cases_df[date_cases] = pd.to_datetime(cases_df[date_cases], format='%Y-%m-%d')
    cases_df[date_cases] = cases_df[date_cases].dt.week
    cases_df = cases_df[[region_cases, date_cases, cases_field]].fillna(0)
    
    pop_df = pd.read_csv(msoa_pop_file,  thousands=',')
    pop_df = pop_df[[region_pop, pop_pop]]
    
    student_df = pd.read_csv(student_num_file)
    student_df = student_df[[region_student, student_student]]
    student_student  = 'num_students'
    student_df.columns = [region_student, student_student]
    
    pop_df = pop_df.merge(student_df, how = 'left', left_on=region_pop, right_on=region_student)
    pop_df[pop_pop] = pd.to_numeric(pop_df[pop_pop])
    student_prop = 'student_prop'
    pop_df[student_prop] = pop_df[student_student]/pop_df[pop_pop]
    
    pop_df.to_csv('msoa_student_rating.csv')
    
    pop_df = pop_df[[region_pop, student_prop, pop_pop]]
    cases_df = cases_df.merge(pop_df, how = 'left', left_on = region_cases, right_on = region_pop)
    cases_df['cases_per_pop'] = cases_df[cases_field]/cases_df[pop_pop]
    print(cases_df)
    cases_df = cases_df[cases_df[date_cases] > 35]
    return cases_df
    
    
def actual_plot_function_median_and_mean(df, colour_string = 'gray', category_string = 'No category given', date_field='date', cases_field='cases_per_pop', ax=None):
    print(df)
    if ax == None:
        ax = plt.gca()
    line_width = 0.75
    alpha = 0.67
    
    df = df[[date_field, cases_field]]
    df = df.sort_values(date_field)
    df.columns = [date_field, category_string]
    df_mean = df.groupby(date_field).mean().reset_index()
    df_median = df.groupby(date_field).median().reset_index()
    ax.plot(list(df_mean[date_field]), list(df_mean[category_string]), color = colour_string, linestyle='solid', alpha = alpha, linewidth=line_width, label = category_string)
    ax.plot(list(df_median[date_field]), list(df_median[category_string]), color = colour_string, linestyle='dashed', alpha = alpha, linewidth=line_width)
    
    return ax

def plot_hi_and_low_and_beside(count_pos, beside_student_list, dz_field = 'areaCode', rating_student_field ='student_prop', date_field = 'date',
                               high_thresh = 0.25, low_thresh = 0.5, string_save = 'student_band_cases_msoa.png', title_string = ""):
    plt.clf()
    just_student = count_pos[count_pos[rating_student_field] > high_thresh]
    # cases_field = 'newCasesBySpecimenDateRollingSum'
    cases_field='cases_per_pop'
    ax = actual_plot_function_median_and_mean(just_student, colour_string = 'gray', category_string = 'High concentration student')
    
    # just_student = just_student[[date_field, cases_field]]
    # just_student.columns = [date_field, 'High concentration student']
    # just_student = just_student.groupby(date_field).mean()
    # ax = just_student.plot(label = 'High concentration student')
    
    beside_student = count_pos[count_pos[rating_student_field] < high_thresh]
    beside_student = beside_student[beside_student[dz_field].isin(beside_student_list)]
    actual_plot_function_median_and_mean(beside_student, colour_string = 'orange', category_string = 'Near (2km centroid) high concentration student', ax=ax)
    
    # beside_student  = beside_student [[date_field, cases_field]]
    # beside_student.columns = [date_field, 'Near (2km centroid) high concentration student']
    # print(beside_student)
    # beside_student  = beside_student .groupby(date_field).mean()
    # beside_student.plot(ax=ax)
    
    
    low_student = count_pos[count_pos[rating_student_field] < low_thresh]
    actual_plot_function_median_and_mean(low_student, colour_string = 'green', category_string = 'Lower concentration student', ax=ax)
    
    # low_student  = low_student [[date_field, cases_field]]
    # low_student.columns = [date_field, 'Lower concentration student']
    # low_student_mean  = low_student .groupby(date_field).mean()
    # low_student_mean.plot(ax=ax)
    # low_student_median  = low_student .groupby(date_field).median()
    # low_student_median.plot(ax=ax)
    # 
    non_beside_student = count_pos[count_pos[rating_student_field] < high_thresh]
    non_beside_student = non_beside_student[~non_beside_student[dz_field].isin(beside_student_list)]
    actual_plot_function_median_and_mean(non_beside_student, colour_string = 'blue', category_string = 'NOT near high concentration student', ax=ax)
    
    # non_beside_student  = non_beside_student [[date_field, cases_field]]
    # non_beside_student.columns = [date_field, 'NOT near high concentration student']
    # print(non_beside_student)
    # non_beside_student  = non_beside_student .groupby(date_field).mean()
    # non_beside_student.plot(ax=ax, style = '-')
    
    
    ax.set_xlabel('week of 2020')
    ax.set_ylabel('test-postives/pop by MSOA')
    ax.set_title(title_string)
    plt.legend()
    plt.savefig(string_save)
        
def network_based_pictures_IZ(count_pos, dz_field = 'InterZone', rating_student_field ='student_prop', date_field = 'specimen_date', high_thresh = 0.25, low_thresh = 0.5, string_save = 'student_band_cases_IZ.png'):
    graph = nx.read_edgelist('IZ_border_network.csv', delimiter = ',')
    edges = list(graph.edges())
    
    print(count_pos)
    for week_num in range(37,45):

        just_student = count_pos[count_pos[rating_student_field] > high_thresh]
        
        
        x, y = get_week_delay_network(count_pos, list(just_student[dz_field]), edges, week_num,  cases_field = 0, place_field = dz_field)
        print(x)
        
        plt.clf()
        plt.scatter(x, y, alpha = 0.2)
        plt.savefig('msoa_source_vs_cases_dest_students_' + str(week_num) + '.png')
        # 
        low_student = count_pos[count_pos[rating_student_field] < low_thresh]
        x, y = get_week_delay_network(count_pos, list(low_student[dz_field]), edges, week_num,  cases_field = 0, place_field = dz_field)
        plt.clf()
        plt.scatter(x, y, alpha = 0.2)
        plt.savefig('msoa_cases_source_vs_cases_dest_low_' + str(week_num) + '.png')



def get_beside_student(count_pos, dz_field = 'areaCode', rating_student_field ='student_prop', high_thresh = 0.25):
    border_df = pd.read_csv('data/full_msoa_network_output.csv')
    border_df = border_df[border_df['distance']<=2]
    just_student = count_pos[count_pos[rating_student_field] > high_thresh]
    student_zones = list(just_student[dz_field])
    border_df = border_df[(border_df['areaCode_x'].isin(student_zones)) |  (border_df['areaCode_y'].isin(student_zones))]
    beside_student = list(border_df['areaCode_x'])
    beside_student.extend(list(border_df['areaCode_y']))
    return beside_student


def do_by_region(lads_of_interest, save_string = 'subset_student_band_cases_msoa.png', title_string=''):
    lookup_df_file = 'data/Output_Area_to_LSOA_to_MSOA_to_Local_Authority_District__December_2017__Lookup_with_Area_Classifications_in_Great_Britain.csv'
    lookup_msoa = 'MSOA11CD'
    lookup_lad = 'LAD17CD'
    lookup_df = pd.read_csv(lookup_df_file)
    lookup_df = lookup_df[[lookup_msoa, lookup_lad]].drop_duplicates()
    # print(lookup_df)
    
    counts = loading_and_IZ();
    counts = counts.merge(lookup_df, how = 'left', left_on = 'areaCode', right_on = lookup_msoa )
    if len(lads_of_interest) > 0:
        counts=counts[counts[lookup_lad].isin(lads_of_interest)]
        
    counts.to_csv('output_' + title_string)
    besides = get_beside_student(counts)
    plot_hi_and_low_and_beside(counts, besides, string_save = save_string, title_string = title_string)
    # return counts
  
def do_by_tier():
    tier_data_file='data/uk_tier_data_parliament_2020_10_25_1606.csv'
    la_field = 'l_l_widerlacode'
    restrict_field = 'l_tier'
    
    tier_df = pd.read_csv(tier_data_file)
    tier_df = tier_df[[la_field, restrict_field]]
    restrictions = list(set(tier_df[restrict_field]))
    
    for restrict in restrictions:
        restrict_df = tier_df[tier_df[restrict_field] == restrict]
        these_las = list(set(restrict_df[la_field]))
        do_by_region(these_las, save_string = str(restrict) + '_student_band_cases_msoa.png', title_string = 'MSOAs in LAs of restriction (Oct 25) - ' + str(restrict))


def do_requests():
    
    places_of_interest = {'E06000018' : 'Nottingham',
        'E06000045': 'Southampton',
        'E08000003': 'Manchester',
        'E08000006': 'Salford',
        'E07000178': 'Oxford',
        'E07000008': 'Cambridge',
        'E07000041': 'Exeter',
        'E06000023': 'Bristol',
        'E08000012': 'Liverpool',
        'E08000025': 'Birmingham',
        'E06000014': 'York',
        'E06000022': 'Bath and NE Somerset'}
    
    for code in places_of_interest:
        save_string = 'just_'+ str(code) + '_student_band_cases_msoa.png'
        title_string = 'MSOAs in LA ' + str(places_of_interest[code])
        do_by_region([code], save_string = save_string, title_string = title_string)
    do_by_region([], save_string = 'all_england_student_band_cases_msoa.png', title_string = 'MSOAs in England')
    
    
do_by_tier()
do_requests()
# 
# counts = loading_and_IZ()
# besides = get_beside_student(counts)
# plot_hi_and_low_and_beside(counts, besides)
    