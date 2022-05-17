from datetime import datetime

import pandas as pd
from pandas._testing import assert_frame_equal
import pytest

from py_ewr import evaluate_EWRs, data_inputs

def test_ctf_handle():
    '''
    1. Ensure all parts of the function generate expected output
    '''
    # set up input data
    PU = 'PU_0000283'
    gauge = '410007'
    EWR = 'CF1'
    EWR_table, bad_EWRs = data_inputs.get_EWR_table()
    data_for_df_F = {'Date': pd.date_range(start= datetime.strptime('2012-07-01', '%Y-%m-%d'), end = datetime.strptime('2016-06-30', '%Y-%m-%d')),
                        gauge: [0]*1+[0]*350+[0]*9+[0]*5 + [0]*360+[0]*5 + [0]*10+[0]*345+[0]*1+[0]*9 + [0]*5+[0]*351+[0]*10}
    df_F = pd.DataFrame(data = data_for_df_F)
    df_F = df_F.set_index('Date')
    PU_df = pd.DataFrame()
    allowance = {'minThreshold': 1.0, 'maxThreshold': 1.0, 'duration': 1.0, 'drawdown': 1.0}
    climate = 'Standard - 1911 to 2018 climate categorisation'
    # Send input data to test function:
    PU_df, events = evaluate_EWRs.ctf_handle(PU, gauge, EWR, EWR_table, df_F, PU_df, allowance, climate)
    # Setting up expected output - PU_df
    data = {'CF1_eventYears': [0,0,0,1], 'CF1_numAchieved': [0,0,0,1], 'CF1_numEvents': [0,0,0,1], 'CF1_eventLength': [0.0,0.0,0.0,1461.0], 'CF1_totalEventDays': [0,0,0,1461], 'CF1_daysBetweenEvents': [[],[],[],[]], 
            'CF1_missingDays': [0,0,0,0], 'CF1_totalPossibleDays': [365,365,365,366]}
    index = [2012, 2013, 2014,2015]
    expected_PU_df = pd.DataFrame(index = index, data = data)
    expected_PU_df.index = expected_PU_df.index.astype('object')
#         print(PU_df.head())
#         print(expected_PU_df.head())        
    assert_frame_equal(PU_df, expected_PU_df)
    # Setting up expected output - events
    expected_events = {2012:[], 2013:[], 2014:[], 2015:[[0]*1461]}
    expected_events = tuple([expected_events])
    for index, tuple_ in enumerate(events):
        for year in events[index]:
            assert len(events[index][year]) == len(expected_events[index][year])
            for i, event in enumerate(events[index][year]):
                assert event == expected_events[index][year][i] 

    
def test_lowflow_handle():
    '''
    1. Ensure all parts of the function generate expected output
    '''
    # Set up input data
    PU = 'PU_0000283'
    gauge = '410007'
    EWR = 'BF1'
    EWR_table, bad_EWRs = data_inputs.get_EWR_table()
    data_for_df_F = {'Date': pd.date_range(start= datetime.strptime('2012-07-01', '%Y-%m-%d'), end = datetime.strptime('2016-06-30', '%Y-%m-%d')),
                        gauge: [0]*1+[250]*350+[0]*9+[0]*5 + [0]*360+[0]*5 + [0]*2+[250]*345+[0]*1+[250]*17 + [0]*5+[250]*351+[250]*10}
    df_F = pd.DataFrame(data = data_for_df_F)
    df_F = df_F.set_index('Date')
    PU_df = pd.DataFrame()
    allowance = {'minThreshold': 1.0, 'maxThreshold': 1.0, 'duration': 1.0, 'drawdown': 1.0}
    climate = 'Standard - 1911 to 2018 climate categorisation'
    # Send input data to test function
    PU_df, events = evaluate_EWRs.lowflow_handle(PU, gauge, EWR, EWR_table, df_F, PU_df, allowance, climate)
    # Setting up expected output data - PU_df, and testing
    data = {'BF1_eventYears': [0,0,1,1], 'BF1_numAchieved': [0,0,1,1], 'BF1_numEvents': [0,0,1,1], 'BF1_eventLength': [350.0,0.0,181.0,361.0], 'BF1_totalEventDays': [350,0,362,361], 
            'BF1_daysBetweenEvents': [[],[],[381],[]],
            'BF1_missingDays': [0,0,0,0], 'BF1_totalPossibleDays': [365,365,365,366]}
    index = [2012, 2013, 2014,2015]
    expected_PU_df = pd.DataFrame(index = index, data = data)
    expected_PU_df.index = expected_PU_df.index.astype('object')
#         print(PU_df.head())
#         print(expected_PU_df.head())
    assert_frame_equal(PU_df, expected_PU_df)

    # Setting up expected output - events, and testing
    expected_events = {2012:[[250]*350], 2013:[], 2014:[[250]*345, [250]*17], 2015:[[250]*351+[250]*10]}
    expected_events = tuple([expected_events])
    for index, tuple_ in enumerate(events):
        for year in events[index]:
            assert len(events[index][year]) == len(expected_events[index][year])
            for i, event in enumerate(events[index][year]):
                assert event == expected_events[index][year][i]  

def test_flow_handle():
    '''Things to calc in this function:
    1. Ensure all parts of the function generate expected output
    '''
    # Setting up input data
    PU = 'PU_0000283'
    gauge = '410007'
    EWR = 'SF1_S'
    EWR_table, bad_EWRs = data_inputs.get_EWR_table()
    data_for_df_F = {'Date': pd.date_range(start= datetime.strptime('2012-07-01', '%Y-%m-%d'), end = datetime.strptime('2016-06-30', '%Y-%m-%d')),
                        gauge: [0]*1+[250]*350+[450]*10+[0]*4 + [0]*360+[450]*5 + [450]*5+[250]*345+[0]*1+[450]*14 + [0]*5+[450]*10+[0]*1+[450]*10+[250]*330+[450]*10}
    df_F = pd.DataFrame(data = data_for_df_F)
    df_F = df_F.set_index('Date')
    PU_df = pd.DataFrame()
    allowance = {'minThreshold': 1.0, 'maxThreshold': 1.0, 'duration': 1.0, 'drawdown': 1.0}
    climate = 'Standard - 1911 to 2018 climate categorisation'
    # Send input data to test function
    PU_df, events = evaluate_EWRs.flow_handle(PU, gauge, EWR, EWR_table, df_F, PU_df, allowance)
    # Setting up expected output - PU_df - and testing
    data = {'SF1_S_eventYears': [0,0,1,1], 'SF1_S_numAchieved': [0,0,1,1], 'SF1_S_numEvents': [1,0,2,3], 'SF1_S_eventLength': [10.0,0.0,12.0,10.0], 'SF1_S_totalEventDays': [10,0,24,30], 
            'SF1_S_daysBetweenEvents': [[],[],[],[]],
            'SF1_S_missingDays': [0,0,0,0], 'SF1_S_totalPossibleDays': [365,365,365,366]}
    index = [2012, 2013, 2014,2015]
    expected_PU_df = pd.DataFrame(index = index, data = data)
    expected_PU_df.index = expected_PU_df.index.astype('object')
#         print(PU_df.head())
#         print(expected_PU_df.head())
    assert_frame_equal(PU_df, expected_PU_df)
    # Setting up expected output - events - and testing
    expected_events = {2012:[[450]*10], 2013:[], 2014:[[450]*5+[450]*5, [450]*14], 2015:[[450]*10, [450]*10, [450]*10]}
    expected_events = tuple([expected_events])
    for index, tuple_ in enumerate(events):
        for year in events[index]:
            assert len(events[index][year]) == len(expected_events[index][year])
            for i, event in enumerate(events[index][year]):
                assert event == expected_events[index][year][i] 

def test_cumulative_handle():
    '''
    1. Ensure all parts of the function generate expected output
    '''
    # Set up input data
    PU = 'PU_0000040'
    gauge = '418068'
    EWR = 'OB3_S'
    EWR_table, bad_EWRs = data_inputs.get_EWR_table()
    data_for_df_F = {'Date': pd.date_range(start= datetime.strptime('2012-07-01', '%Y-%m-%d'), end = datetime.strptime('2016-06-30', '%Y-%m-%d')),
                        gauge: [0]*1+[0]*350+[10000]*1+[3000]*4+[0]*9 + [0]*360+[450]*3+[19000]*1+[1000]*1 + [450]*5+[250]*345+[0]*1+[0]*13+[5000]*1 + [5000]*4+[450]*10+[0]*2+[450]*10+[250]*330+[450]*10}
    df_F = pd.DataFrame(data = data_for_df_F)
    df_F = df_F.set_index('Date')
    PU_df = pd.DataFrame()
    allowance = {'minThreshold': 1.0, 'maxThreshold': 1.0, 'duration': 1.0, 'drawdown': 1.0}
    climate = 'Standard - 1911 to 2018 climate categorisation'
    # Send input data to test function
    PU_df, events = evaluate_EWRs.cumulative_handle(PU, gauge, EWR, EWR_table, df_F, PU_df, allowance)
    # Setting up expected output - PU_df - and testing
    data = {'OB3_S_eventYears': [1,0,0,1], 'OB3_S_numAchieved': [1,0,0,1], 'OB3_S_numEvents': [1,0,0,1], 'OB3_S_eventLength': [5.0,0.0,0.0,5.0], 'OB3_S_totalEventDays': [5,0,0,5], 
            'OB3_S_daysBetweenEvents': [[],[],[],[]],
            'OB3_S_missingDays': [0,0,0,0], 'OB3_S_totalPossibleDays': [365,365,365,366]}
    index = [2012, 2013, 2014,2015]
    expected_PU_df = pd.DataFrame(index = index, data = data)
    expected_PU_df.index = expected_PU_df.index.astype('object')
#         print(PU_df.head())
#         print(expected_PU_df.head())
    assert_frame_equal(PU_df, expected_PU_df)
    # Setting up expected output - events - and testing 
    expected_events = {2012:[[10000]*1+[3000]*4], 2013:[], 2014:[], 2015:[[5000]*1+[5000]*4]}
    expected_events = tuple([expected_events])
    for index, tuple_ in enumerate(events):
        for year in events[index]:
            assert len(events[index][year]) == len(expected_events[index][year])
            for i, event in enumerate(events[index][year]):
                assert event == expected_events[index][year][i]

def test_level_handle():
    '''
    1. Ensure all parts of the function generate expected output
    '''
    # Set up input data
    PU = 'PU_0000266'
    gauge = '425022'
    EWR = 'LLLF'
    EWR_table, bad_EWRs = data_inputs.get_EWR_table()
    data_for_df_L = {'Date': pd.date_range(start= datetime.strptime('2012-07-01', '%Y-%m-%d'), end = datetime.strptime('2016-06-30', '%Y-%m-%d')),
                        gauge: [0]*1+[0]*260+[56]*90+[0]*1+[0]*4+[0]*9 + [56]*45+[55.9]*1+[56]*45+[0]*269+[0]*3+[19000]*1+[1000]*1 + [0]*5+[0]*345+[0]*1+[0]*13+[56]*1 + [56]*89+[0]*4+[0]*10+[0]*3+[0]*10+[0]*230+[0]*20}
    df_L = pd.DataFrame(data = data_for_df_L)
    df_L = df_L.set_index('Date')
    PU_df = pd.DataFrame()
    allowance = {'minThreshold': 1.0, 'maxThreshold': 1.0, 'duration': 1.0, 'drawdown': 1.0}
    climate = 'Standard - 1911 to 2018 climate categorisation'
    # Send input data to test function
    PU_df, events = evaluate_EWRs.level_handle(PU, gauge, EWR, EWR_table, df_L, PU_df, allowance)
    # Setting up expected output - PU_df and test
    data = {'LLLF_eventYears': [1,0,0,0], 'LLLF_numAchieved': [1,0,0,0], 'LLLF_numEvents': [1,0,0,0], 'LLLF_eventLength': [90.0,0.0,0.0,0], 'LLLF_totalEventDays': [90,0,0,0], 
            'LLLF_daysBetweenEvents': [[],[],[],[1110]],
            'LLLF_missingDays': [0,0,0,0], 'LLLF_totalPossibleDays': [365,365,365,366]}
    index = [2012, 2013, 2014,2015]
    expected_PU_df = pd.DataFrame(index = index, data = data)
    expected_PU_df.index = expected_PU_df.index.astype('object')
#         print(PU_df.head())
#         print(expected_PU_df.head())
    assert_frame_equal(PU_df, expected_PU_df)
    # Setting up expected output - events - and test
    expected_events = {2012:[[56]*90], 2013:[], 2014:[], 2015:[]}
    expected_events = tuple([expected_events])
    for index, tuple_ in enumerate(events):
        for year in events[index]:
            assert len(events[index][year]) == len(expected_events[index][year])
            for i, event in enumerate(events[index][year]):
                assert event == expected_events[index][year][i] 


@pytest.mark.xfail(raises=IndexError)
def test_weirpool_handle():
    '''
    1. Ensure all parts of the function generate expected output
    '''
    # Set up input data
    PU = 'PU_0000260'
    gauge = '414203'
    wp_gauge = '414209'
    EWR = 'WP1'
    EWR_table, bad_EWRs = data_inputs.get_EWR_table()
    # input data for df_L:
    levels = [47.3]*100 
    reduction_max = 0.04
    for i, level in enumerate(levels):
        levels[i] = levels[i-1]-reduction_max # Levels declining at acceptable rate
    exceeding_levels = [47.3]*100 
    reduction_max = 0.05
    for i, level in enumerate(exceeding_levels):
        exceeding_levels[i] = exceeding_levels[i-1]-reduction_max # Levels exceeding the acceptable rate: 
    data_for_df_L = {'Date': pd.date_range(start= datetime.strptime('2012-07-01', '%Y-%m-%d'), end = datetime.strptime('2016-06-30', '%Y-%m-%d')),
                        wp_gauge: [0]*187+[47.3]*90+[0]*88 + [47.3]*90+[0]*275 + [0]*187+levels+[0]*78 + [0]*187+exceeding_levels+[0]*79}
    df_L = pd.DataFrame(data = data_for_df_L)
    df_L = df_L.set_index('Date')
    # input data for df_F:
    data_for_df_F = {'Date': pd.date_range(start= datetime.strptime('2012-07-01', '%Y-%m-%d'), end = datetime.strptime('2016-06-30', '%Y-%m-%d')),
                        gauge: [0]*187+[2500]*90+[0]*88 + [2500]*90+[0]*275 + [0]*187+[2500]*100+[0]*78 + [0]*187+[2500]*100+[0]*79}
    df_F = pd.DataFrame(data = data_for_df_F)
    df_F = df_F.set_index('Date')
    PU_df = pd.DataFrame()
    allowance = {'minThreshold': 1.0, 'maxThreshold': 1.0, 'duration': 1.0, 'drawdown': 1.0}
    climate = 'Standard - 1911 to 2018 climate categorisation'
    # Passing input data to test function
    PU_df, events = evaluate_EWRs.weirpool_handle(PU, gauge, EWR, EWR_table, df_F, df_L, PU_df, allowance)
    # Setting up expected output data - PU_df - and testing
    data = {'WP1_eventYears': [1,0,1,0], 'WP1_numAchieved': [1,0,1,0], 'WP1_numEvents': [1,0,1,0], 'WP1_eventLength': [90.0,0.0,90.0,0.0], 'WP1_totalEventDays': [90,0,90,0], 
            'WP1_daysBetweenEvents': [[],[],[],[]],
            'WP1_missingDays': [0,0,0,0], 'WP1_totalPossibleDays': [365,365,365,366]}
    index = [2012, 2013, 2014,2015]
    expected_PU_df = pd.DataFrame(index = index, data = data)
    expected_PU_df.index = expected_PU_df.index.astype('object')
#         print(PU_df.head())
#         print(expected_PU_df.head())
    assert_frame_equal(PU_df, expected_PU_df)
    # Setting up expected output - events - and testing
    expected_events = {2012:[[2500]*90], 2013:[], 2014:[[2500]*90], 2015:[]}
    expected_events = tuple([expected_events])
    for index, tuple_ in enumerate(events):
        for year in events[index]:
            assert len(events[index][year]) == len(expected_events[index][year])
            for i, event in enumerate(events[index][year]):
                assert event == expected_events[index][year][i]

def test_nest_handle():
    '''
    1. Ensure all parts of the function generate expected output
    '''
    # Set up input data
    PU = 'PU_0000253'
    gauge = '409025'
    EWR = 'NestS1'
    EWR_table, bad_EWRs = data_inputs.get_EWR_table()
    # input data up df_L:
    # flows declining at acceptable rate:
    acceptable_flows = [10000]*10
    reduction_max = 5.9
    for i, flow in enumerate(acceptable_flows):
        acceptable_flows[i] = acceptable_flows[i-1]-(reduction_max/100*acceptable_flows[i-1])
    acceptable_flows = acceptable_flows + [5300]*50
    # flows declining at unnacceptable rate:
    unnacceptable_flows = [10000]*10
    reduction_max = 7
    for i, flow in enumerate(unnacceptable_flows):
        unnacceptable_flows[i] = unnacceptable_flows[i-1]-(reduction_max/100*unnacceptable_flows[i-1])
    unnacceptable_flows = unnacceptable_flows + [5300]*50
    # flows declining at acceptable rate but going below the threshold
    threshold_flows = [10000]*10
    reduction_max = 6
    for i, flow in enumerate(threshold_flows):
        threshold_flows[i] = threshold_flows[i-1]-(reduction_max/100*threshold_flows[i-1])
    threshold_flows = threshold_flows + [5300]*50
    # input data for df_F:
    data_for_df_F = {'Date': pd.date_range(start= datetime.strptime('2012-07-01', '%Y-%m-%d'), end = datetime.strptime('2016-06-30', '%Y-%m-%d')),
                        gauge: [0]*76+acceptable_flows+[0]*229 + [0]*76+unnacceptable_flows+[0]*229 + [0]*76+threshold_flows+[0]*229 + [0]*77+threshold_flows+[0]*229}
    df_F = pd.DataFrame(data = data_for_df_F)
    df_F = df_F.set_index('Date')
    df_L = pd.DataFrame()
    PU_df = pd.DataFrame()
    allowance = {'minThreshold': 1.0, 'maxThreshold': 1.0, 'duration': 1.0, 'drawdown': 1.0}
    climate = 'Standard - 1911 to 2018 climate categorisation'
    # Pass input data to test function:
    PU_df, events = evaluate_EWRs.nest_handle(PU, gauge, EWR, EWR_table, df_F, df_L, PU_df, allowance)
    # Setting up expected output - PU_df - and testing
    data = {'NestS1_eventYears': [1,0,0,0], 'NestS1_numAchieved': [1,0,0,0], 'NestS1_numEvents': [1,0,0,0], 'NestS1_eventLength': [60.0,0.0,0.0,0.0], 'NestS1_totalEventDays': [60,0,0,0],
            'NestS1_daysBetweenEvents': [[],[],[],[1325]],
            'NestS1_missingDays': [0,0,0,0], 'NestS1_totalPossibleDays': [365,365,365,366]}
    index = [2012, 2013, 2014,2015]
    expected_PU_df = pd.DataFrame(index = index, data = data)
    expected_PU_df.index = expected_PU_df.index.astype('object')
#         print(PU_df.head())
#         print(expected_PU_df.head())
    assert_frame_equal(PU_df, expected_PU_df)
    # Setting up expected output - events - and testing
    expected_events = {2012:[acceptable_flows], 2013:[], 2014:[], 2015:[]}
    expected_events = tuple([expected_events])
    for index, tuple_ in enumerate(events):
        for year in events[index]:
            assert len(events[index][year]) == len(expected_events[index][year])
            for i, event in enumerate(events[index][year]):
                assert event == expected_events[index][year][i]

def test_flow_handle_multi():
    '''
    1. Ensure all parts of the function generate expected output
    '''
    # Set up input data
    PU = 'PU_0000130'
    gauge1 = '421090'
    gauge2 = '421088'
    EWR = 'LF1'
    EWR_table, bad_EWRs = data_inputs.get_EWR_table()
    data_for_df_F = {'Date': pd.date_range(start= datetime.strptime('2012-07-01', '%Y-%m-%d'), end = datetime.strptime('2016-06-30', '%Y-%m-%d')),
                        gauge1: [0]*76+[1250]*5+[0]*229+[0]*55 + [0]*76+[0]*55+[0]*231+[1250]*3 + [1250]*3+[0]*76+[0]*50+[1250]*5+[0]*231 + [0]*77+[1250]*5+[0]*229+[0]*55,
                        gauge2: [0]*76+[1250]*5+[0]*229+[0]*55 + [0]*76+[0]*55+[0]*231+[1250]*3 + [1250]*3+[0]*76+[0]*50+[1250]*5+[0]*231 + [0]*76+[1250]*5+[0]*230+[0]*55
                    }
    df_F = pd.DataFrame(data = data_for_df_F)
    df_F = df_F.set_index('Date')
    df_L = pd.DataFrame()
    PU_df = pd.DataFrame()
    allowance = {'minThreshold': 1.0, 'maxThreshold': 1.0, 'duration': 1.0, 'drawdown': 1.0}
    climate = 'Standard - 1911 to 2018 climate categorisation'
    # Send input data to test function
    PU_df, events = evaluate_EWRs.flow_handle_multi(PU, gauge1, EWR, EWR_table, df_F, PU_df, allowance)
    # Setting up expected output - PU_df - and testing
    data = {'LF1_eventYears': [1,0,1,0], 'LF1_numAchieved': [1,0,2,0], 'LF1_numEvents': [1,0,2,0], 'LF1_eventLength': [5.0,0.0,5.5,0.0], 'LF1_totalEventDays': [5,0,11,0],
            'LF1_daysBetweenEvents': [[],[],[],[]],
            'LF1_missingDays': [0,0,0,0], 'LF1_totalPossibleDays': [365,365,365,366]}
    index = [2012, 2013, 2014,2015]
    expected_PU_df = pd.DataFrame(index = index, data = data)
    expected_PU_df.index = expected_PU_df.index.astype('object')
#         print(PU_df.head())
#         print(expected_PU_df.head())
    assert_frame_equal(PU_df, expected_PU_df)    
    # Setting up expected output - events - and testing
    expected_events = {2012:[[2500]*5], 2013:[], 2014:[[2500]*6, [2500]*5], 2015:[]}
    expected_events = tuple([expected_events])
    for index, tuple_ in enumerate(events):
        for year in events[index]:
            assert len(events[index][year]) == len(expected_events[index][year])
            for i, event in enumerate(events[index][year]):
                assert event == expected_events[index][year][i]

def test_lowflow_handle_multi():
    '''
    1. Ensure all parts of the function generate expected output
    '''
    # Input data
    PU = 'PU_0000130'
    gauge1 = '421090'
    gauge2 = '421088'
    EWR = 'BF1'
    EWR_table, bad_EWRs = data_inputs.get_EWR_table()
    data_for_df_F = {'Date': pd.date_range(start= datetime.strptime('2012-07-01', '%Y-%m-%d'), end = datetime.strptime('2016-06-30', '%Y-%m-%d')),
                        gauge1: [50]*76+[1250]*5+[50]*229+[50]*15+[0]*40 + [50]*3+[0]*76+[0]*50+[0]*5+[0]*231 + [50]*75+[0]*50+[50]*230+[50]*10 + [0]*77+[50]*5+[0]*229+[50]*55,
                        gauge2: [50]*76+[1250]*5+[50]*229+[0]*40+[50]*15 + [50]*3+[0]*76+[0]*50+[0]*5+[0]*231 + [50]*75+[0]*50+[50]*230+[50]*10 + [0]*76+[50]*5+[0]*230+[50]*55
                    }
    df_F = pd.DataFrame(data = data_for_df_F)
    df_F = df_F.set_index('Date')
    df_L = pd.DataFrame()
    PU_df = pd.DataFrame()
    allowance = {'minThreshold': 1.0, 'maxThreshold': 1.0, 'duration': 1.0, 'drawdown': 1.0}
    climate = 'Standard - 1911 to 2018 climate categorisation'
    # Pass input data to test function
    PU_df, events = evaluate_EWRs.lowflow_handle_multi(PU, gauge1, EWR, EWR_table, df_F, PU_df, allowance, climate)
    # Setting up expected output - PU_df - and testing
    data = {'BF1_eventYears': [0,0,1,0], 'BF1_numAchieved': [0,0,1,0], 'BF1_numEvents': [0,0,1,0], 'BF1_eventLength': [310.0,3.0,157.5,29.5], 'BF1_totalEventDays': [310,3,315,59],
            'BF1_daysBetweenEvents': [[],[362],[],[77, 230]],
            'BF1_missingDays': [0,0,0,0], 'BF1_totalPossibleDays': [365,365,365,366]}
    index = [2012, 2013, 2014,2015]
    expected_PU_df = pd.DataFrame(index = index, data = data)
    expected_PU_df.index = expected_PU_df.index.astype('object')
#         print(PU_df.head())
#         print(expected_PU_df.head())
    assert_frame_equal(PU_df, expected_PU_df)    
    # Setting up expected output - events - and testing
    expected_events = {2012:[[100]*76+[2500]*5+[100]*229], 2013:[[100]*3], 2014:[[100]*75, [100]*230+[100]*10], 2015:[[100]*4, [100]*55]}
    expected_events = tuple([expected_events])
    for index, tuple_ in enumerate(events):
        for year in events[index]:
            assert len(events[index][year]) == len(expected_events[index][year])
            for i, event in enumerate(events[index][year]):
                assert event == expected_events[index][year][i]

@pytest.mark.xfail(raises=AssertionError, reason="column name=CF_eventYears are different")
def test_ctf_handle_multi():
    '''
    1. Ensure all parts of the function generate expected output
    '''
    # Set up the input data
    PU = 'PU_0000130'
    gauge1 = '421090'
    gauge2 = '421088'
    EWR = 'CF'
    EWR_table, bad_EWRs = data_inputs.get_EWR_table()
    data_for_df_F = {'Date': pd.date_range(start= datetime.strptime('2012-07-01', '%Y-%m-%d'), end = datetime.strptime('2016-06-30', '%Y-%m-%d')),
                        gauge1: [0]*1+[2]*350+[0]*9+[0]*5 + [2]*360+[0]*5 + [0]*10+[2]*345+[0]*1+[2]*9 + [0]*5+[0]*351+[0]*10,
                        gauge2: [0]*1+[2]*350+[0]*9+[0]*5 + [2]*360+[0]*5 + [0]*10+[2]*345+[0]*1+[2]*9 + [0]*5+[0]*351+[0]*10
                    }
    df_F = pd.DataFrame(data = data_for_df_F)
    df_F = df_F.set_index('Date')
    df_L = pd.DataFrame()
    PU_df = pd.DataFrame()
    allowance = {'minThreshold': 1.0, 'maxThreshold': 1.0, 'duration': 1.0, 'drawdown': 1.0}
    climate = 'Standard - 1911 to 2018 climate categorisation'
    # Pass input data to the test function
    PU_df, events = evaluate_EWRs.ctf_handle_multi(PU, gauge1, EWR, EWR_table, df_F, PU_df, allowance, climate)
    # Setting up expected output - PU_df - and testing
    data = {'CF_eventYears': [1,0,1,1], 'CF_numAchieved': [2,0,2,1], 'CF_numEvents': [2,0,2,1], 'CF_eventLength': [7.5,0.0,8.0,366.0], 'CF_totalEventDays': [15,0,16,366],
            'CF_daysBetweenEvents': [[350],[360],[345,9],[]],
            'CF_missingDays': [0,0,0,0], 'CF_totalPossibleDays': [365,365,365,366]}
    index = [2012, 2013, 2014,2015]
    expected_PU_df = pd.DataFrame(index = index, data = data)
    expected_PU_df.index = expected_PU_df.index.astype('object')
#         print(PU_df.head())
#         print(expected_PU_df.head())
    assert_frame_equal(PU_df, expected_PU_df)    
    # Setting up expected output - events - and testing
    expected_events = {2012:[[0]*1, [0]*9+[0]*5], 2013:[], 2014:[[0]*15, [0]*1], 2015:[[0]*366]}
    expected_events = tuple([expected_events])
    for index, tuple_ in enumerate(events):
        for year in events[index]:
            assert len(events[index][year]) == len(expected_events[index][year])
            for i, event in enumerate(events[index][year]):
                assert event == expected_events[index][year][i]

@pytest.mark.xfail(raises=IndexError)
def test_cumulative_handle_multi():
    '''
    1. Ensure all parts of the function generate expected output
    '''
    # Set up input data
    PU = 'PU_0000132'
    gauge1 = '421090'
    gauge2 = '421088'
    EWR = 'OB/WS1_S'
    EWR_table, bad_EWRs = data_inputs.get_EWR_table()
    data_for_df_F = {'Date': pd.date_range(start= datetime.strptime('2012-07-01', '%Y-%m-%d'), end = datetime.strptime('2016-06-30', '%Y-%m-%d')),
                        gauge1: [0]*1+[0]*260+[334]*90+[0]*5+[0]*9 + [0]*310+[0]*3+[0]*1+[0]*1+[500]*50 + [500]*40+[0]*310+[0]*1+[0]*13+[0]*1 + [5000]*4+[500]*90+[500]*90+[450]*10+[0]*2+[450]*10+[250]*150+[450]*10,
                        gauge2: [0]*1+[0]*260+[334]*90+[0]*5+[0]*9 + [0]*310+[0]*3+[0]*1+[0]*1+[500]*50 + [500]*40+[0]*310+[0]*1+[0]*13+[0]*1 + [5000]*4+[500]*90+[500]*90+[450]*10+[0]*2+[450]*10+[250]*150+[450]*10
                    }
    df_F = pd.DataFrame(data = data_for_df_F)
    df_F = df_F.set_index('Date')
    df_L = pd.DataFrame()
    PU_df = pd.DataFrame()
    allowance = {'minThreshold': 1.0, 'maxThreshold': 1.0, 'duration': 1.0, 'drawdown': 1.0}
    climate = 'Standard - 1911 to 2018 climate categorisation'
    # Pass input data to test function
    PU_df, events = evaluate_EWRs.cumulative_handle_multi(PU, gauge1, EWR, EWR_table, df_F, PU_df, allowance)
    # Setting up expected output - PU_df - and testing
    data = {'OB/WS1_S_eventYears': [1,1,1,1], 'OB/WS1_S_numAchieved': [1,1,1,2], 'OB/WS1_S_numEvents': [1,1,1,2], 'OB/WS1_S_eventLength': [90,90.0,90.0,90.0], 'OB/WS1_S_totalEventDays': [90,90,90,180],
            'OB/WS1_S_daysBetweenEvents': [[],[],[],[]],
            'OB/WS1_S_missingDays': [0,0,0,0], 'OB/WS1_S_totalPossibleDays': [365,365,365,366]}
    index = [2012, 2013, 2014,2015]
    expected_PU_df = pd.DataFrame(index = index, data = data)
    expected_PU_df.index = expected_PU_df.index.astype('object')
#         print(PU_df.head())
#         print(expected_PU_df.head())
    assert_frame_equal(PU_df, expected_PU_df)   
    # Setting up expected output - events - and testing
    expected_events = {2012:[[334*2]*90], 2013:[[0]*30+[500*2]*60], 2014:[[0]*66+[5000*2]*4+[500*2]*20], 2015:[[500*2]*90, [500*2]*70+[450*2]*10+[0]*2+[450*2]*8]}
    expected_events = tuple([expected_events])
    for index, tuple_ in enumerate(events):
        for year in events[index]:
            assert len(events[index][year]) == len(expected_events[index][year])
            for i, event in enumerate(events[index][year]):
                assert event == expected_events[index][year][i]

@pytest.mark.xfail(raises=IndexError)
def test_flow_handle_sim():
    '''
    1. Ensure all parts of the function generate expected output
    '''
    # Set up input data
    PU = 'PU_0000131'
    gauge1 = '421090'
    gauge2 = '421022'
    EWR = 'LF1_S'
    EWR_table, bad_EWRs = data_inputs.get_EWR_table()
    data_for_df_F = {'Date': pd.date_range(start= datetime.strptime('2012-07-01', '%Y-%m-%d'), end = datetime.strptime('2016-06-30', '%Y-%m-%d')),
                        gauge1: [0]*76+[1000]*5+[0]*229+[0]*55 + [0]*76+[0]*55+[0]*231+[1000]*3 + [1000]*3+[0]*76+[0]*50+[1000]*5+[0]*231 + [0]*77+[1000]*5+[0]*229+[0]*55,
                        gauge2: [0]*76+[1000]*5+[0]*229+[0]*55 + [0]*76+[0]*55+[0]*231+[1000]*3 + [1000]*3+[0]*76+[0]*50+[1000]*5+[0]*231 + [0]*76+[1000]*5+[0]*230+[0]*55
                    }
    df_F = pd.DataFrame(data = data_for_df_F)
    df_F = df_F.set_index('Date')
    df_L = pd.DataFrame()
    PU_df = pd.DataFrame()
    allowance = {'minThreshold': 1.0, 'maxThreshold': 1.0, 'duration': 1.0, 'drawdown': 1.0}
    climate = 'Standard - 1911 to 2018 climate categorisation'
    # Pass input data to test function
    PU_df, events = evaluate_EWRs.flow_handle_sim(PU, gauge1, EWR, EWR_table, df_F, PU_df, allowance)
    # Setting up expected output - PU_df - and testing
    data = {'LF1_S_eventYears': [1,0,1,0], 'LF1_S_numAchieved': [1,0,2,0], 'LF1_S_numEvents': [1,0,2,0], 'LF1_S_eventLength': [5.0,0.0,5.5,0.0], 'LF1_S_totalEventDays': [5,0,11,0],
            'LF1_S_daysBetweenEvents': [[],[],[],[]],
            'LF1_S_missingDays': [0,0,0,0], 'LF1_S_totalPossibleDays': [365,365,365,366]}
    index = [2012, 2013, 2014,2015]
    expected_PU_df = pd.DataFrame(index = index, data = data)
    expected_PU_df.index = expected_PU_df.index.astype('object')
#         print(PU_df.head())
#         print(expected_PU_df.head())
    assert_frame_equal(PU_df, expected_PU_df)
    # Setting up expected output - events - and testing
    expected_events = {2012:[[1000]*5], 2013:[], 2014:[[1000]*6, [1000]*5], 2015:[]}
    expected_events = tuple([expected_events])
    for index, tuple_ in enumerate(events):
        for year in events[index]:
            assert len(events[index][year]) == len(expected_events[index][year])
            for i, event in enumerate(events[index][year]):
                assert event == expected_events[index][year][i]

@pytest.mark.xfail(raises=IndexError)
def test_lowflow_handle_sim():
    '''
    1. Ensure all parts of the function generate expected output
    '''
    # Set up input data
    PU = 'PU_0000131'
    gauge1 = '421090'
    gauge2 = '421022'
    EWR = 'BF1'
    EWR_table, bad_EWRs = data_inputs.get_EWR_table()
    data_for_df_F = {'Date': pd.date_range(start= datetime.strptime('2012-07-01', '%Y-%m-%d'), end = datetime.strptime('2016-06-30', '%Y-%m-%d')),
                        gauge1: [0]*76+[65]*280+[0]*9 + [0]*76+[0]*9+[65]*280 + [0]*80+[0]*9+[65]*276 + [65]*270+[0]*76+[0]*14+[65]*6,
                        gauge2: [0]*76+[65]*280+[0]*9 + [65]*280+[0]*76+[0]*9 + [0]*80+[0]*9+[65]*276 + [65]*270+[0]*76+[0]*14+[65]*6
                    }
    df_F = pd.DataFrame(data = data_for_df_F)
    df_F = df_F.set_index('Date')
    df_L = pd.DataFrame()
    PU_df = pd.DataFrame()
    allowance = {'minThreshold': 1.0, 'maxThreshold': 1.0, 'duration': 1.0, 'drawdown': 1.0}
    climate = 'Standard - 1911 to 2018 climate categorisation'
    # Pass input data to test function
    PU_df, events = evaluate_EWRs.lowflow_handle_sim(PU, gauge1, EWR, EWR_table, df_F, PU_df, allowance, climate)
    # Setting up expected output - PU_df - and test
    # Note the floats that get returned in the total event days series. This is because the totals of the two series are averaged.
    data = {'BF1_eventYears': [1,1,1,0], 'BF1_numAchieved': [1,1,1,0], 'BF1_numEvents': [1,1,1,0], 'BF1_eventLength': [280.0,280.0,276.0,138.0], 'BF1_totalEventDays': [280.0,280.0,276.0,276.0],
            'BF1_daysBetweenEvents': [[76],[94],[89],[90]],
            'BF1_missingDays': [0,0,0,0], 'BF1_totalPossibleDays': [365,365,365,366]}
    index = [2012, 2013, 2014,2015]
    expected_PU_df = pd.DataFrame(index = index, data = data)
    expected_PU_df.index = expected_PU_df.index.astype('object')
    assert_frame_equal(PU_df, expected_PU_df)
    # Setting up expected output - events - and testing
    expected_events1 = {2012:[[65]*280], 2013:[[65]*280], 2014:[[65]*276], 2015:[[65]*270, [65]*6]}
    expected_events2 = {2012:[[65]*280], 2013:[[65]*280], 2014:[[65]*276], 2015:[[65]*270, [65]*6]}
    expected_events = tuple([expected_events1, expected_events2])
    for index, tuple_ in enumerate(events):
        for year in events[index]:
            assert len(events[index][year]) ==len(expected_events[index][year])
            for i, event in enumerate(events[index][year]):
                assert event == expected_events[index][year][i]

@pytest.mark.xfail(raises=IndexError)
def test_ctf_handle_sim():
    '''
    1. Ensure all parts of the function generate expected output
    '''
    # Set up input data
    PU = 'PU_0000131'
    gauge1 = '421090'
    gauge2 = '421022'
    EWR = 'CF'
    EWR_table, bad_EWRs = data_inputs.get_EWR_table()
    data_for_df_F = {'Date': pd.date_range(start= datetime.strptime('2012-07-01', '%Y-%m-%d'), end = datetime.strptime('2016-06-30', '%Y-%m-%d')),
                        gauge1: [5]*123+[0]*5+[5]*232+[0]*5 + [0]*1+[5]*123+[0]*3+[5]*233+[0]*3+[5]*2 + [5]*123+[0]*5+[5]*232+[0]*5 + [5]*123+[0]*5+[5]*233+[5]*5,
                        gauge2: [5]*123+[0]*5+[5]*232+[0]*5 + [0]*1+[5]*123+[0]*3+[5]*233+[0]*3+[5]*2 + [5]*123+[0]*5+[5]*232+[0]*5 + [5]*123+[5]*5+[5]*233+[0]*5
                    }
    df_F = pd.DataFrame(data = data_for_df_F)
    df_F = df_F.set_index('Date')
    df_L = pd.DataFrame()
    PU_df = pd.DataFrame()
    allowance = {'minThreshold': 1.0, 'maxThreshold': 1.0, 'duration': 1.0, 'drawdown': 1.0}
    climate = 'Standard - 1911 to 2018 climate categorisation'
    # Pass input data to test function
    PU_df, events = evaluate_EWRs.ctf_handle_sim(PU, gauge1, EWR, EWR_table, df_F, PU_df, allowance, climate)
    # Setting up expected output - PU_df - and test
    # Note the floats that get returned in the total event days series. This is because the totals of the two series are averaged.
    data = {'CF_eventYears': [1,0,0,1], 'CF_numAchieved': [2,0,0,1], 'CF_numEvents': [2,0,0,1], 'CF_eventLength': [5.0,3.0,5.0,5.0], 'CF_totalEventDays': [10.0,6.0,10.0,5.0],
            'CF_daysBetweenEvents': [[123, 232],[124,233],[125,232],[123,238]],
            'CF_missingDays': [0,0,0,0], 'CF_totalPossibleDays': [365,365,365,366]}
    index = [2012, 2013, 2014,2015]
    expected_PU_df = pd.DataFrame(index = index, data = data)
    expected_PU_df.index = expected_PU_df.index.astype('object')
    assert_frame_equal(PU_df, expected_PU_df) 
    # Setting up expected output - events - and test
    expected_events1 = {2012:[[0]*5, [0]*5], 2013:[[0]*3, [0]*3], 2014:[[0]*5, [0]*5], 2015:[[0]*5]}
    expected_events2 = {2012:[[0]*5, [0]*5], 2013:[[0]*3, [0]*3], 2014:[[0]*5, [0]*5], 2015:[[0]*5]}
    expected_events = tuple([expected_events1, expected_events2])
    for index, tuple_ in enumerate(events):
        for year in events[index]:
            assert len(events[index][year]) == len(expected_events[index][year])
            for i, event in enumerate(events[index][year]):
                assert event == expected_events[index][year][i]

def test_complex_handle():
    '''
    1. Ensure all parts of the function generate expected output for OB2
    2. Ensure all parts of the function generate expected output for OB3
    '''
    # Test 1
    # Set up input data
    PU = 'PU_0000253'
    gauge = '409025'
    EWR = 'OB2a_S'
    EWR_table, bad_EWRs = data_inputs.get_EWR_table()
    data_for_df_F = {'Date': pd.date_range(start= datetime.strptime('2012-07-01', '%Y-%m-%d'), end = datetime.strptime('2016-06-30', '%Y-%m-%d')),
                        gauge: [19000]*45+[9000]*105+[0]*215 + [15000]*45+[0]*8+[9000]*105+[0]*207 + [15000]*15+[0]*6+[15000]*15+[0]*6+[15000]*15+[0]*6+[9000]*55+[0]*6+[9000]*50+[0]*150+[16000]*41 + \
                                        [0]*6+[16000]*4+[0]*6+[9000]*105+[0]*95+[18000]*45+[9000]*105,
                    }
    df_F = pd.DataFrame(data = data_for_df_F)
    df_F = df_F.set_index('Date')
    df_L = pd.DataFrame()
    PU_df = pd.DataFrame()
    allowance = {'minThreshold': 1.0, 'maxThreshold': 1.0, 'duration': 1.0, 'drawdown': 1.0}
    climate = 'Standard - 1911 to 2018 climate categorisation'
    # Pass input data to test function
    PU_df, events = evaluate_EWRs.complex_handle(PU, gauge, EWR, EWR_table, df_F, PU_df, allowance)
    # Setting up expected output - PU_df - and testing
    data = {'OB2a_S_eventYears': [1,0,1,1], 'OB2a_S_numAchieved': [1,0,1,2], 'OB2a_S_numEvents': [1,0,1,2], 'OB2a_S_eventLength': [150.0,0.0,150.0,150.0], 'OB2a_S_totalEventDays': [150,0,150,300],
            'OB2a_S_daysBetweenEvents': [[],[],[],[]],
            'OB2a_S_missingDays': [0,0,0,0], 'OB2a_S_totalPossibleDays': [365,365,365,366]}
    index = [2012, 2013, 2014,2015]
    expected_PU_df = pd.DataFrame(index = index, data = data)
    expected_PU_df.index = expected_PU_df.index.astype('object')
    assert_frame_equal(PU_df, expected_PU_df) 
    # Setting up expected output - events - and testing
    expected_events = {2012:[[19000]*45+[9000]*105], 2013:[], 2014:[[15000]*15+[15000]*15+[15000]*15+[9000]*55+[9000]*50], 2015:[[16000]*41+[16000]*4+[9000]*105, [18000]*45+[9000]*105]}
    expected_events = tuple([expected_events])
    for index, tuple_ in enumerate(events):
        for year in events[index]:
            assert len(events[index][year]) == len(expected_events[index][year])
            for i, event in enumerate(events[index][year]):
                assert event == expected_events[index][year][i]
    #-------------------------------------------------------------------------------------
    # Test 2
    # Set up input data
    PU = 'PU_0000253'
    gauge = '409025'
    EWR = 'OB3a_S'
    EWR_table, bad_EWRs = data_inputs.get_EWR_table()
    data_for_df_F = {'Date': pd.date_range(start= datetime.strptime('2012-07-01', '%Y-%m-%d'), end = datetime.strptime('2016-06-30', '%Y-%m-%d')),
                        gauge:  [25000]*21+[15000]*90+[0]*254 + [25000]*21+[0]*8+[15000]*90+[0]*246 + [15000]*90+[0]*6+[25000]*21+[0]*8+[25000]*15+[0]*6+[25000]*6+[0]*6+[15000]*80+[0]*6+[15000]*10+[0]*94+[15000]*17 + \
                                        [0]*6+[15000]*73+[0]*6+[25000]*1+[25000]*20+[0]*149+[25000]*21+[15000]*90
                    }
    df_F = pd.DataFrame(data = data_for_df_F)
    df_F = df_F.set_index('Date')
    df_L = pd.DataFrame()
    PU_df = pd.DataFrame()
    allowance = {'minThreshold': 1.0, 'maxThreshold': 1.0, 'duration': 1.0, 'drawdown': 1.0}
    climate = 'Standard - 1911 to 2018 climate categorisation'
    # Pass input data to test function
    PU_df, events = evaluate_EWRs.complex_handle(PU, gauge, EWR, EWR_table, df_F, PU_df, allowance)
    # Setting up expected output - PU_df - and testing
    data = {'OB3a_S_eventYears': [1,0,1,1], 'OB3a_S_numAchieved': [1,0,2,2], 'OB3a_S_numEvents': [1,0,2,2], 'OB3a_S_eventLength': [111.0,0.0,111.0,111.0], 'OB3a_S_totalEventDays': [111,0,222,222],
            'OB3a_S_daysBetweenEvents': [[],[],[],[]],
            'OB3a_S_missingDays': [0,0,0,0], 'OB3a_S_totalPossibleDays': [365,365,365,366]}
    index = [2012, 2013, 2014,2015]
    expected_PU_df = pd.DataFrame(index = index, data = data)
    expected_PU_df.index = expected_PU_df.index.astype('object')
    assert_frame_equal(PU_df, expected_PU_df) 
    # Setting up expected output - events - and testing
    expected_events = {2012:[[25000]*21+[15000]*90], 2013:[], 2014:[[15000]*90+[25000]*21, [25000]*15+[25000]*6+[15000]*80+[15000]*10], 2015:[[15000]*17+[15000]*73+[25000]*21, [25000]*21+[15000]*90]}
    expected_events = tuple([expected_events])
    for index, tuple_ in enumerate(events):
        for year in events[index]:
            assert len(events[index][year]) == len(expected_events[index][year])
            for i, event in enumerate(events[index][year]):
                assert event == expected_events[index][year][i]