import warnings
import time
import numpy as np
import pandas as pd
import multiprocessing as mp
import matplotlib.pyplot as plt
from datetime import datetime
from scipy.stats import percentileofscore
from scipy.integrate import cumulative_trapezoid
from blast.models.nca_gr_Panasonic3Ah_2018 import Nca_Gr_Panasonic3Ah_Battery
from blast.models.lfp_gr_250AhPrismatic_2019 import Lfp_Gr_250AhPrismatic
from blast.models.nmc811_grSi_LGMJ1_4Ah_2020 import Nmc811_GrSi_LGMJ1_4Ah_Battery



def decimate_and_rescale_profile(profile, decimation_factor, tol=1e-1, show_efcs=False):
    dSOC = profile['SOC (%)'].diff().fillna(0)
    efcs_original = 0.5 * dSOC.abs().sum()
    if show_efcs:
        print(f"Original EFCs: {efcs_original}")
    profile = profile.iloc[::decimation_factor, :].reset_index(drop=True)
    dSOC = profile['SOC (%)'].diff().fillna(0)
    efcs = 0.5 * dSOC.abs().sum()
    prev_efcs = efcs

    stagnated = False
    while np.abs(efcs_original - efcs) > tol:
        dSOC = dSOC * (efcs_original / efcs)
        profile['SOC (%)'] = np.cumsum(dSOC) + profile['SOC (%)'].iloc[0]
        # Ceiling SOC at 1, no floor
        profile['SOC (%)'] = np.minimum(1, profile['SOC (%)'])
        #profile['SOC (%)'] = np.maximum(0, np.minimum(1, profile['SOC (%)']))
        dSOC = profile['SOC (%)'].diff().fillna(0) 
        efcs = 0.5 * dSOC.abs().sum() 

        # breaks the while loop if value of efcs starts to stagnate significantly
        if(np.abs(prev_efcs - efcs) == 0):
            warnings.warn("Decimate and rescale loop aborted due to value stagnation.")
            stagnated = True
            break
        else:
            prev_efcs = efcs

    if show_efcs:
        print(f"Decimated and rescaled EFCs: {efcs}")

    return profile, stagnated

def make_operating_profile(drive, drive_stats, days, operating_days_per_year, initial_soc, rest_soc, charging_options, decimation_factor, stop_indices):
    # Add charges to the drive; one for repeating drives, one for before the rest day
    ### TODO: MAYBE NEED TO DECIMATE AFTER GENERATING CHARGES, ... check!
    #plt.plot(drive['Time (s)'], drive['SOC (%)'], '-k')
    drive_with_charges, charge_events, additional_time_s = add_charges_to_drive(drive, stop_indices, **charging_options, time_step=decimation_factor)
    #plt.plot(drive['Time (s)'], drive['SOC (%)'], '--r')
    #plt.plot(drive_with_charges['Time (s)'], drive_with_charges['SOC (%)'], '-k')
    drive_with_charges_before_rest, charge_events_rest, additional_time_s_rest = add_charges_to_drive(drive, stop_indices, **charging_options, final_soc=rest_soc, time_step=decimation_factor)
    #plt.plot(drive_with_charges_before_rest['Time (s)'], drive_with_charges_before_rest['SOC (%)'], '--r')
    # Create the rest day data frame. Rest day sits at low SOC, then charges slowly at the end.
    rest_time = np.linspace(0, 18*3600, 18*3600//decimation_factor) # same final time, but array is now less long
    rest = {
        'Time (s)': rest_time,
        # If battery operation is mild, SOC will be higher than rest SOC (battery wasn't discharged much).
        'SOC (%)': np.full_like(rest_time, drive_with_charges_before_rest['SOC (%)'].iloc[-1]),
        'Sim_Speed_kph': np.full_like(rest_time, 0),
    }
    rest_charge_time = np.linspace(18*3600, 24*3600, 6*3600//decimation_factor)
    rest_charge = {
        'Time (s)': rest_charge_time,
        # If battery operation is mild, SOC will be higher than rest SOC (battery wasn't discharged much).
        'SOC (%)': np.linspace(rest['SOC (%)'][-1], initial_soc, 6*3600//decimation_factor),
        'Sim_Speed_kph': np.full_like(rest_charge_time, 0),
    }
    rest = pd.concat([pd.DataFrame(rest), pd.DataFrame(rest_charge)]).reset_index(drop=True) 
    rest = rest.drop_duplicates() # drops the duplicate created; first index of rest/last of rest_time

    del rest_charge, rest_charge_time, rest_time
    # Tile drive and rest events for one month of operation; should give enough rest days to get close to our rest fraction
    drive = None
    days_total = 0
    frac_rest_time = 1 - (operating_days_per_year/365)
    tracker_rests = 0
    drive_stats = {
        'Time (days)': [],
        'Total miles (mi)': [],
        'Charge events': [],
        'Additional time needed for charging (s)': [],
    }
    drive_days = drive_with_charges['Time (s)'].iloc[-1] / (int(24*3600)) 

    drive_days_rest = drive_with_charges_before_rest['Time (s)'].iloc[-1] / (int(24*3600))
    while days_total < days: 
        # every operating day, there should be frac_rest_time days of rest. Once there's more than 1 day of rest... rest!
        # Anticipate the day before rest, though, so we can potentially skip a charge and keep the battery at lower SOC.
        if tracker_rests < (1 - frac_rest_time*drive_days_rest):
            drive = pd.concat([drive, drive_with_charges.copy()]).reset_index(drop=True)
            drive_stats['Time (days)'].append(drive_days)
            drive_stats['Total miles (mi)'].append(np.sum(drive_with_charges['Simulated Distance (mi)']) * decimation_factor)
            drive_stats['Charge events'].append(charge_events)
            drive_stats['Additional time needed for charging (s)'].append(additional_time_s)
            tracker_rests += frac_rest_time*drive_days 
            days_total += drive_days
        else:
            # charge before rest then rest
            drive = pd.concat([drive, drive_with_charges_before_rest.copy()]).reset_index(drop=True)
            drive_stats['Time (days)'].append(drive_days_rest)
            drive_stats['Total miles (mi)'].append(np.sum(drive_with_charges_before_rest['Simulated Distance (mi)']) * decimation_factor)
            drive_stats['Charge events'].append(charge_events_rest)
            drive_stats['Additional time needed for charging (s)'].append(additional_time_s_rest)
            tracker_rests += frac_rest_time*drive_days_rest
            days_total += drive_days_rest
            drive = pd.concat([drive, rest]).reset_index(drop=True)
            drive_stats['Time (days)'].append(1)
            drive_stats['Total miles (mi)'].append(0)
            drive_stats['Charge events'].append(0)
            drive_stats['Additional time needed for charging (s)'].append(0)
            tracker_rests += -1
            days_total += 1
    
    dt = np.diff(drive['Time (s)'], prepend=0)
    dt[dt<0] = 1 # jumps between profiles is negative
    drive['Time (s)'] = np.cumsum(dt)

    return drive, drive_stats

def get_life_sim_input(drive, temperature):
    life_sim_input = drive[['SOC (%)', 'Time (s)']]
    life_sim_input = life_sim_input.rename(columns={'SOC (%)': 'SOC', 'Time (s)': 'Time_s'})
    life_sim_input['Temperature_C'] = temperature
    return life_sim_input

def scale_soc_by_soh(drive, soh):
    soc = drive['SOC (%)']
    d_soc = np.diff(soc, prepend=soc[0])
    d_soc = d_soc / soh
    soc = soc[0] + np.cumsum(d_soc)
    drive['SOC (%)'] = soc
    return drive

def process_and_save_results(results, trips_summary):
    results = pd.DataFrame(results)

    vars_to_sample = ['Total miles (mi)','Total energy throughput per mile (kWh/mi)','Max Microtrip RMS Power (kW)']
    for var in vars_to_sample:
        results[var] = trips_summary[var][results['Summary file idx'].to_list()].to_numpy()
        results[var + " percentile"] = percentileofscore(trips_summary[var], trips_summary[var][results['Summary file idx'].to_list()].to_numpy()) / 100

    def get_last_nonzero(data):
        for element in reversed(data):
            if element != 0:
                return element
        return None

    final_charge_events = []
    for index in results.index:
        final_charge_events.append(get_last_nonzero(results['Drive profile stats'][index]['Charge events']))
    results['Final charge events'] = final_charge_events
    results['Change in charge events'] = results['Final charge events'] - results['Initial charge events']
    results['% increase in charge events'] = ((results['Final charge events'] / results['Initial charge events'])*100) - 1

    results.to_pickle('trucklife_simulation_results_2.pkl')
    return results

def add_charges_to_drive(drive, stop_indices, min_stop_duration_seconds=10*60, charging_rate_per_hour=0.7, min_soc=0.05, max_soc=0.95, final_soc=0.95, time_step=15):
    # Find the stops
    #stop_indices = find_zero_speed_sections(drive, min_duration_seconds=min_stop_duration_seconds)
    stop_indices = [(round(a / time_step), round(b / time_step)) for (a, b) in stop_indices]
    # Convert charging rate per hour to charging rate per time step
    charging_rate_per_time_step = charging_rate_per_hour / (3600 / time_step)
    # Track added rows if there's not enough time to charge
    total_additional_rows = 0
    is_done = False
    idx_stop = 0
    charge_events = 0
    count = 0
    while not is_done:
        if stop_indices != []:
            this_stop = stop_indices[idx_stop]
            start, end = this_stop[0], this_stop[1]
            # update the indices if we've added any new rows to the data frame
            start += total_additional_rows
            end += total_additional_rows
            # charge at the start of this stop event
            soc = drive.loc[start, 'SOC (%)']
            if soc < 1:
                if soc < min_soc: # we already crossed past min_soc and have to charge before this stop
                    # insert a stop where we cross min_soc
                    new_stop_idx = np.argwhere(drive['SOC (%)'] < min_soc)
                    new_stop_idx = new_stop_idx[0][0] - 1
                    new_stop_soc = drive['SOC (%)'].iloc[new_stop_idx]
                    new_stop_time = drive['Time (s)'].iloc[new_stop_idx]
                    # find out how much charge we need until the following stop, plus a bit
                    additional_soc = new_stop_soc - soc + min_soc + 0.1
                    if new_stop_soc + additional_soc > max_soc:
                        additional_soc = max_soc - new_stop_soc
                    # add that much charge, adding time to the trip
                    additional_time_needed = additional_soc / charging_rate_per_time_step
                    additional_rows = int(additional_time_needed)  # Number of extra rows (seconds) to add
                    total_additional_rows += additional_rows
                    new_times = range(int(new_stop_time + time_step), int(new_stop_time + time_step*(additional_rows + 1)), time_step)
                    new_rows = pd.DataFrame({'Time (s)': new_times, 'Sim_Speed_kph': [0] * additional_rows, 'SOC (%)': pd.NA})
                    # Concatenate the new rows to the DataFrame
                    drive = pd.concat([drive.iloc[:new_stop_idx+1], new_rows, drive.iloc[new_stop_idx+1:]]).reset_index(drop=True)
                    # Shift the 'Time (s)' values after the added rows to account for the new time extension
                    drive.loc[new_stop_idx + 1 + additional_rows:, 'Time (s)'] += additional_rows * time_step
                    # Update soc for the additional rows
                    for i in range(new_stop_idx + 1, new_stop_idx + 1 + additional_rows):
                        new_stop_soc += charging_rate_per_time_step
                        if new_stop_soc > max_soc:
                            new_stop_soc = max_soc
                        drive.at[i, 'SOC (%)'] = new_stop_soc
                    # Shift all SOCs after this section up
                    drive.loc[new_stop_idx + 1 + additional_rows:, 'SOC (%)'] += additional_soc
                    charge_events += 1
                
                elif idx_stop < len(stop_indices)-1: # this is an intermediate stop event, charge if we need to
                    next_stop = stop_indices[idx_stop+1]
                    next_start = next_stop[0]
                    next_soc = drive.loc[next_start, 'SOC (%)']
                    if next_soc < min_soc:
                        # find out how much charge we need until the following stop, then add the charge event
                        additional_soc = soc - next_soc + min_soc + 0.1
                        #drive, additional_rows = charge_on_stop(drive, start, end, additional_soc, max_soc)
                        drive, additional_rows = charge_on_stop(drive, start, end, additional_soc, charging_rate_per_time_step, time_step, max_soc)
                        total_additional_rows += additional_rows
                    idx_stop += 1
                    charge_events += 1
                    
                elif idx_stop == len(stop_indices)-1: # this is the last stop event, charge if we need to
                    # if the drive ends with this stop, fully charge before the next day.
                    if end == drive.shape[0]-1:
                        #print('flag 3-1')
                        additional_soc = final_soc - soc
                        #drive, additional_rows = charge_on_stop(drive, start, end, additional_soc, charging_rate_per_time_step, max_soc=1.)
                        drive, additional_rows = charge_on_stop(drive, start, end, additional_soc, charging_rate_per_time_step, time_step, max_soc=1.)
                        total_additional_rows += additional_rows
                        charge_events += 1
                        is_done = True
                    else:
                        # drive doesn't end with this stop; charge if we need to
                        end_soc = drive['SOC (%)'].iloc[-1]
                        if end_soc < min_soc:
                            # find out how much charge we need until the end of the trip
                            additional_soc = soc - end_soc + min_soc
                            #drive, additional_rows = charge_on_stop(drive, start, end, additional_soc, charging_rate_per_time_step, max_soc)
                            drive, additional_rows = charge_on_stop(drive, start, end, additional_soc, charging_rate_per_time_step, time_step, max_soc)
                            total_additional_rows += additional_rows
                            charge_events += 1
                        # add charge stop to end
                        drive, additional_rows = add_charge_to_end(drive, charging_rate_per_time_step, time_step, final_soc)
                        if additional_rows > 0:
                            charge_events += 1
                        is_done = True
            else:
                idx_stop += 1

        else: # there are no detected stops in the trip. fully charge every time the SOC is below min_soc
            if np.any(drive['SOC (%)'] < min_soc):
                # insert a stop where we cross min_soc
                new_stop_idx = np.argwhere(drive['SOC (%)'] <= min_soc)
                new_stop_soc = drive['SOC (%)'].iloc[new_stop_idx]
                new_stop_time = drive['Time (s)'].iloc[new_stop_idx]
                # find out how much charge we need until the following stop
                additional_soc = 1 - new_stop_soc
                # add that much charge, adding time to the trip
                additional_time_needed = additional_soc / charging_rate_per_time_step
                additional_rows = int(additional_time_needed)  # Number of extra rows (seconds) to add
                total_additional_rows += additional_rows
                new_times = range(int(new_stop_time + time_step), int(new_stop_time + time_step*(additional_rows + 1)), time_step)
                new_rows = pd.DataFrame({'Time (s)': new_times, 'Sim_Speed_kph': [0] * additional_rows, 'SOC (%)': pd.NA})
                # Concatenate the new rows to the DataFrame
                drive = pd.concat([drive.iloc[:new_stop_idx+1], new_rows, drive.iloc[new_stop_idx+1:]]).reset_index(drop=True)
                # Shift the 'Time (s)' values after the added rows to account for the new time extension
                drive.loc[new_stop_idx + 1 + additional_rows:, 'Time (s)'] += additional_rows * time_step
                # Update soc for the additional rows
                for i in range(new_stop_idx + 1, new_stop_idx + 1 + additional_rows):
                    new_stop_soc += charging_rate_per_time_step
                    drive.at[i, 'SOC (%)'] = new_stop_soc
                # Shift all SOCs after this section up
                drive.loc[new_stop_idx + 1 + additional_rows:, 'SOC (%)'] += additional_soc
                charge_events += 1
            else:
                # add a charge stop at the end
                drive, additional_rows = add_charge_to_end(drive, charging_rate_per_time_step, time_step, final_soc)
                if additional_rows > 0:
                    charge_events += 1
                is_done = True  
    drive['Time (hr)'] = drive['Time (s)'] / 3600
    return drive.copy(), charge_events, total_additional_rows

def add_charge_to_end(drive, charging_rate_per_time_step, time_step, final_soc=1):
    last_time = drive['Time (s)'].iloc[-1]  # Get the last time value in the DataFrame
    soc = drive['SOC (%)'].iloc[-1]
    additional_time_needed = (final_soc - soc) / charging_rate_per_time_step
    if additional_time_needed > 0:
        additional_rows = int(additional_time_needed)  # Number of extra seconds needed to charge the battery
        # Create new rows for the additional time
        new_times = range(int(last_time + time_step), int(last_time + time_step*(additional_rows + 1)), time_step)
        new_rows = pd.DataFrame({'Time (s)': new_times, 'Sim_Speed_kph': [0] * additional_rows, 'SOC (%)': [0] * additional_rows})
        # Append the new rows to the DataFrame
        drive = pd.concat([drive, new_rows]).reset_index(drop=True)
        # Update the fuel level for the new rows
        for i in range(len(drive) - additional_rows, len(drive)):
            soc += charging_rate_per_time_step
            if soc >= final_soc:
                soc = final_soc
            # Update the 'SOC (%)' column for the new rows
            drive.at[i, 'SOC (%)'] = soc
    else:
        additional_rows = 0
    return drive, additional_rows

def charge_on_stop(drive, start, end, additional_soc, charging_rate_per_time_step, time_step, max_soc=0.95):
    # Charge additional SOC to the battery during the noted stop event.
    # If the stop event is not long enough to actually charge the battery, extend the stop event by
    # inserting rows into the data frame.
    if end < (drive.shape[0]-1):
        is_shift_after = True
    else:
        is_shift_after = False
    soc = drive.loc[start, 'SOC (%)']
    initial_soc = soc
    final_soc = soc + additional_soc
    if final_soc > max_soc:
        final_soc = max_soc
    # charge during the stop
    for i in range(start, end + 1):
        # Charge added during this second
        soc += charging_rate_per_time_step
        if soc > final_soc:
            soc = final_soc
        drive.at[i, 'SOC (%)'] = soc
    additional_rows = 0
    # if there wasn't enough time to complete the charge, add more rows
    if soc < final_soc:
        # Calculate how many extra seconds are needed to fully charge the battery
        additional_time_needed = (final_soc - soc) / charging_rate_per_time_step
        additional_rows = int(np.ceil(additional_time_needed))  # Number of extra rows (seconds) to add
        # Get the last time value from the current section
        last_time = drive.loc[end, 'Time (s)']
        # Create new rows to extend the zero-speed section
        new_times = range(int(last_time + time_step), int(last_time + time_step*(additional_rows + 1)), time_step)
        new_rows = pd.DataFrame({'Time (s)': new_times, 'Sim_Speed_kph': [0] * additional_rows, 'SOC (%)': [0] * additional_rows})
        # Concatenate the new rows to the DataFrame
        if end < drive.shape[0]-1:
            drive = pd.concat([drive.iloc[:end+1], new_rows, drive.iloc[end+1:]]).reset_index(drop=True)
            # Shift the 'Time (s)' values after the added rows to account for the new time extension
            drive.loc[end + 1 + additional_rows:, 'Time (s)'] += additional_rows * time_step
        else:
            drive = pd.concat([drive, new_rows]).reset_index(drop=True)
        # Update soc for the additional rows
        for i in range(end + 1, end + 1 + additional_rows):
            # charge added during this second
            soc += charging_rate_per_time_step
            if soc > final_soc:
                soc = final_soc
            drive.at[i, 'SOC (%)'] = soc
    # Shift all SOCs after this section up by the amount that was actually charged
    #if is_shift_after and additional_rows == 0:
    if is_shift_after:
        additional_soc = final_soc - initial_soc
        drive.loc[end + 1 + additional_rows:, 'SOC (%)'] += additional_soc

    return drive, additional_rows

def find_zero_speed_sections(drive, min_duration_seconds=10*60, tolerance=0.1):
    """
    Finds the contiguous sections where Speed is approximately 0 for at least a specified duration.
    
    Args:
    drive (pd.DataFrame): DataFrame containing 'Time (s)' and 'Sim_Speed_kph' columns.
    min_duration_sec (int): Minimum required duration for zero-speed sections (in seconds).
    tolerance (float): Tolerance threshold for considering speed as zero.
    
    Returns:
    List[Tuple[int, int]]: List of tuples containing start and end indices of valid sections.
    """

    # Boolean array where True indicates 'Speed' is within tolerance
    within_tolerance = drive['Sim_Speed_kph'].abs() <= tolerance
    # List to store the start and end indices of contiguous sections
    zero_speed_sections = []
    # Initialize variables to keep track of start of a section
    start = None
    # Loop through the boolean array

    for i, is_within in enumerate(within_tolerance):
        if is_within and start is None:
            # Mark the start of a new section
            start = i
        elif not is_within and start is not None:
            # End of a section
            end = i - 1
            # Check if the section duration is long enough
            if drive.loc[end, 'Time (s)'] - drive.loc[start, 'Time (s)'] >= min_duration_seconds:
                zero_speed_sections.append((start, end))
            # Reset start
            start = None
    # Handle case if the last section ends at the last row
    if start is not None:
        end = len(drive) - 1
        if drive.loc[end, 'Time (s)'] - drive.loc[start, 'Time (s)'] >= min_duration_seconds:
            zero_speed_sections.append((start, end))
    
    return zero_speed_sections

def simulate_truck_battery(battery, drive, pack_size_kWh, decimation_factor, charging_power_kW=1e3, max_charging_rate=0.7, temperature=25, threshold_capacity=0.8, simulation_step=0.02, operating_days_per_year=250,
                            charging_options={
                                'min_stop_duration_seconds': 600,
                                'min_soc': 0.05,
                            },
                            initial_soc = 0.95, rest_soc=0.3, 
                            show_soc=False):

    # New columns in the drive cycle: battery cumulative energy, Time, speed in kph
    drive['Time (s)'] = np.linspace(0, len(drive.index)-1, len(drive.index))
    drive['Cumulative Battery Energy (kWh)'] = cumulative_trapezoid(drive['Simulated Battery Power (kW)'] / 3600, initial=0)
    drive['Sim_Speed_kph'] = drive['Simulated Speed (m/s)'] * 3600 / 1000
    drive['SOC (%)'] = initial_soc + drive['Cumulative Battery Energy (kWh)']/pack_size_kWh
    drive = drive[['Time (s)', 'SOC (%)', 'Sim_Speed_kph', 'Simulated Distance (mi)', 'Cumulative Battery Energy (kWh)']]
    # Extend the drive to the nearest whole day with a rest
    drive_days = np.ceil(drive['Time (s)'].iloc[-1] / (24*3600))
    new_rows = int((drive_days * 24 * 3600) - drive['Time (s)'].iloc[-1])
    rest_time = np.linspace(drive['Time (s)'].iloc[-1] + 1, drive_days * 24 * 3600, new_rows)
    rest = {
        'Time (s)': rest_time,
        'SOC (%)': np.full_like(rest_time, drive['SOC (%)'].iloc[-1]),
        'Sim_Speed_kph': np.full_like(rest_time, 0),
    }
    rest = pd.DataFrame(rest)
    drive_init = pd.concat([drive, pd.DataFrame(rest)]).reset_index(drop=True)
    if show_soc:
        fig, ax = plt.subplots(1, 3, figsize=(12,4))
        ax[0].plot(drive['Time (s)'], drive['SOC (%)'], '-k')
        ax[0].plot(drive_init['Time (s)'], drive_init['SOC (%)'], '--r')
    drive, rest = None, None
    drive_stats = {
        'Time (days)': [0],
        'Total miles (mi)': [0],
        'Charge events': [0],
        'Additional time needed for charging (s)': [0],
    }

    # Simulation loop
    flag_toomanycharges = False
    while battery.outputs['q'][-1] > threshold_capacity: # Repeats loop exactly 6 times every time
    #if(True):
        current_soh = battery.outputs['q'][-1]
        # Scale drive SOC changes by health
        drive = scale_soc_by_soh(drive_init.copy(), current_soh)
        # Scale charging rate by health (as health decreases, effective charging rate increases, but in reality we always just normalize charging rate by nominal capacity)
        #       These aspects don't care about any other drive components
        charging_rate = (pack_size_kWh*current_soh) / charging_power_kW
        charging_rate = np.max([charging_rate, max_charging_rate/current_soh])
        charging_options['charging_rate_per_hour'] = charging_rate
        charging_options['max_soc'] = initial_soc

        min_seconds = charging_options['min_stop_duration_seconds']
        stop_indices = find_zero_speed_sections(drive, min_seconds)
        #decimates and rescales drive profile (of a single day)
        drive_decimated, stagnated = decimate_and_rescale_profile(drive, decimation_factor, show_efcs=False)

        #No data is better than false data
        if stagnated:
            return None

        # Tile drives and rests after adding charges to drive segments to make 30 day operating profile with our operating days ratio
        drive_month, drive_stats_month = make_operating_profile(drive_decimated, drive_stats, 30, operating_days_per_year, initial_soc, rest_soc, charging_options, decimation_factor, stop_indices)

        '''
        if np.max(np.array(drive_stats_month['Charge events'])) > 100:
            print('Charge events > 100, check the drive cycle')
            flag_toomanycharges = True
            fig, ax = plt.subplots(1, 2, figsize=(10,4))
            ax[0].plot(drive_month['Time (s)'][:86400], drive_month['SOC (%)'][:86400])
            ax[1].plot(drive_month['Time (s)']/(3600*24), drive_month['SOC (%)'])
            break
        # else:
        #     print(np.max(np.array(drive_stats_month['Charge events'])), current_soh)
        if show_soc:
            ax[1].plot(drive_month['Time (s)'][:86400], drive_month['SOC (%)'][:86400])
            ax[2].plot(drive_month['Time (s)']/(3600*24), drive_month['SOC (%)'])
            # print(drive_stats_month)
        '''

        # Extract life sim inputs, gives pd composing of SOC time and temp
        life_sim_input = get_life_sim_input(drive_month, temperature)

        # Run the life sim -> Experiencing some divide by 0 errors...
        battery.simulate_battery_life(life_sim_input, threshold_capacity=battery.outputs['q'][-1] - simulation_step)

        # Fill in drive_stats for the time that was simulated
        last_day = np.sum(drive_stats['Time (days)'])
        idx_stat_day = 0
        num_stat_days = len(drive_stats_month['Time (days)'])
        while last_day < np.floor(battery.stressors['t_days'][-1]):
            for stat in drive_stats:
                drive_stats[stat].append(drive_stats_month[stat][idx_stat_day])
            last_day = np.sum(drive_stats['Time (days)'])
            idx_stat_day += 1
            if idx_stat_day == num_stat_days:
                idx_stat_day = 0

    drive_stats['Time (days)'] = np.cumsum(drive_stats['Time (days)']).tolist()
    drive_stats['Total miles (mi)'] = np.cumsum(drive_stats['Total miles (mi)']).tolist()
    life_sim_outputs = {
        'Relative discharge capacity': battery.outputs['q'],
        'Time (days)': battery.stressors['t_days'],
        'Equivalent full cycles': battery.stressors['efc'],
    }
    if flag_toomanycharges:
        results = None
    else:
        results = {
            'Life simulation outputs': life_sim_outputs,
            'Drive profile stats': drive_stats,
            'Years to 80% capacity': battery.stressors['t_days'][-1] / 365,
            'Miles to 80% capacity': drive_stats['Total miles (mi)'][-1],
            'Initial charge events': drive_stats['Charge events'][1],
            'Final charge events': drive_stats['Charge events'][-1],
            'Additional time needed for charging (s)': drive_stats['Additional time needed for charging (s)'][1]
        }
    return results

def single_simulation(inputs):
    trips_summary, percentile, variable, pack_size, chemistry, decimation_factor, idx = inputs
    if idx is None:
        idx = np.argwhere(trips_summary[variable] == trips_summary[variable].quantile(percentile, interpolation='nearest'))[0][0]
        print(chemistry, percentile, variable, pack_size, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    else:
        print('index', idx, ":",chemistry, pack_size, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    drive = pd.read_csv(trips_summary['file path'][idx])
    if chemistry == 'NCA-Gr':
        battery = Nca_Gr_Panasonic3Ah_Battery(degradation_scalar=1.5)
    elif chemistry == 'LFP-Gr':
        battery = Lfp_Gr_250AhPrismatic(degradation_scalar=1.3)
    elif chemistry == 'NMC811-GrSi-LGMJ1':
        battery = Nmc811_GrSi_LGMJ1_4Ah_Battery(degradation_scalar=0.4)
    start_time = time.time()
    sim_result = simulate_truck_battery(battery, drive, pack_size, decimation_factor,
                                        charging_power_kW=1e3, max_charging_rate=0.7, temperature=30, 
                                        threshold_capacity=0.8, simulation_step=0.03, operating_days_per_year=250,
                                        charging_options={
                                            'min_stop_duration_seconds': 600,
                                            'min_soc': 0.05,
                                        },
                                        initial_soc = 0.95, rest_soc=0.3, 
                                        show_soc=False)
    end_time = time.time()

    if sim_result is not None:
        return sim_result, idx, end_time-start_time, percentile, variable, pack_size, chemistry
    return None

def run_simulations(trips_summary, percentiles, vars_to_sample, pack_sizes_kWh, chemistries, decimation_factor, run_all_files=False):
    results = {
        'Summary file idx': [],
        'Simulation time': [],
        'Battery chemistry': [],
        'Percentile': [],
        'Sampled variable': [],
        'Pack size': [],
        'Life simulation outputs': [],
        'Drive profile stats': [],
        'Years to 80% capacity': [],
        'Miles to 80% capacity': [],
        'Initial charge events': [],
        'Final charge events': [],
        'Additional time needed for charging (s)': [],
    }
    
    if run_all_files==False:
        tasks = [
            (trips_summary, p, var, pack_size, chem, decimation_factor, None)
            for p in percentiles
            for var in vars_to_sample
            for pack_size in pack_sizes_kWh
            for chem in chemistries ]
    else:
        tasks = [
            (trips_summary, None, None, pack_size, chem, decimation_factor, idx)
            for pack_size in pack_sizes_kWh
            for chem in chemistries 
            for idx in trips_summary.index ]
        
    cores = mp.cpu_count()

    with mp.Pool(processes=cores) as pool:
        sim_results = pool.map(single_simulation, tasks)
        for result in sim_results:
            if result is not None:
                sim_result, idx, sim_time, percentile, variable, pack_size, chemistry = result
                results['Summary file idx'].append(idx)
                results['Simulation time'].append(sim_time)
                results['Battery chemistry'].append(chemistry)
                results['Percentile'].append(percentile)
                results['Sampled variable'].append(variable)
                results['Pack size'].append(pack_size)
                for stat in sim_result:
                    results[stat].append(sim_result[stat])
        
    return process_and_save_results(results, trips_summary)

