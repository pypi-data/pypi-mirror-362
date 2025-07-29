## 📚 Table of Contents

1. [Overview](#overview)  
2. [Features](#features)  
3. [Installation](#installation)  
4. [Usage](#usage)  
5. [Examples](#examples) 
6. [Assumptions & Configuration](#assumptions--configuration)    
7. [References](#references)
8. [Citation](#citation)  
9. [License](#license)

# Overview

`EVforecaster` uses the 2002 - 2023 UK National Travel Survey (UK-NTS) to generate domestic EV charging demand curves. The UK-NTS contains trip level data, such as: trip start time, trip end time, trip distance, trip location, etc. Although the majority of trips in the UK-NTS are likely to have been carried out by combustion engine vehicles (CEVs), this simulation-based approach assumes that electric vehicles (EVs) carried out the trips. Taking the trips as given, `EVforecaster` tries to model where, at what time and for how long EVs would charge to be able to successfully undertake the trips. Once this is modelled, the information is aggregated to plot weekly demand curves at 5-minute granularity. The simulation algorithms requires the following information:

* Each trip location is randomly allocated a charger and a charging rate (kW/hour) based on a distribution.
* Each individual is allocated a car, which is modelled as a battery size and efficiency due. Based on a distribution.
* An individual's charging decision is modelled using the probabilistic function developed in Pareschi et al. (2020).
* Most simulation parameters (such as those mentioned above) are centrally defined in `config.py`.

It is capable of creating annual weekly demand curves that aggregate all the weeks of the year, weekly demand curves for specific seasons (defined by week ranges) or weekly demand curves for each week of the year.

Additionally, it is able to compare weekly demand curves for the largest domestic UK-based EV charging pilot, the 2017 Electric Chargepoint Analysis (ECA) (DfT, 2018). It plots the mean simulated demand curve (and standard errors) alongside the ECA and a histrogram of $R^2$ values below.

Various experiments can be ran to test model performance, as compared to the ECA, for different parameter configurations. Some are available in `showcase.ipynb`

# Installation

**From GitHub**

1. `git clone https://github.com/andriysinclair/EVforecaster.git`
2. `cd EVforecaster`
3. `pip install .`

**From PyPi**

TBC

# Usage

## General Usage

1. Download UK-NTS data from [UK Data Service](https://doi.org/10.5255/UKDA-SN-5340-14)

2. Unzip the downloaded file and move the following files from the `tab` folder into the `root/data/` directory.
   - `trip_eul_2002-2023.tab`
   - `day_eul_2002-2023.tab`
   - `household_eul_2002-2023.tab`

2. CD into the root directory, start a Python session and Import `EVforecaster`.

```python 
from EVforecaster.EVforecasterUser import EVforecaster
```

3. Create instance of class

```python 
evf = EVforecaster(travel_years=[2017])
```

  - `travel_years` should be between 2012 and 2017, this defines the years of travel data that you will use to generate annual charging demand forecasts
  - Upon creating an instance a dataset corresponding to the travel data of `travel_years` will be generated and moved into `root/dataframes/`, this can take some time. If another instance is made with the same `travel_years` it will not generate the dataset again but rather load an existing one from `root/dataframes/`.

4. Generate demand curves

```python 
results_dict = evf.generate_forecasts(N_sims=100,
weeks=list(range(1,53)),
home_shift=0,
experiment_name="agg_vs_agg_homeshift0",
ECA_overlay=None)
```

  - This will create 100 annual-aggregate weekly demand curves. The mean (over 100 simulations) demand curve, along with 95% confidence intervals is plotted and saved into `root/plots/`. The file name will be `agg_vs_agg_homeshift0.pdf`, or the parameter value of `experiment_name`.

  - Please refer to the class docstring above to understand the `resukts_dict` output.

  - As `ECA_overlay=None`, there will be no comparison with the ECA

5. Compare with ECA

  - If we set `ECA_overlay=list(range(39,53))`, then this will also plot weeks 39 to 52 (aggregated) of the ECA, calculate the $R^2$ and plot a distribution.
  - If a simulation, indexed by the `experiment_name` parameter, has been completed, then it can be loaded and used with various configurations of `ECA_overlay` for experimentation. 

6. Please see some examples of usage below, and in `showcase.ipynb`.

## Main Class Documentation

```python
class EVforecaster:
    """
    A forecasting class that uses UK National Travel Survey data to simulate electric vehicle charging demand.

    The class loads, processes, and merges raw travel survey files (.tab) into a weekly travel diary format.
    It supports generating forecast demand curves using a Monte Carlo simulation approach and evaluating these
    forecasts against real-world EV pilot data (ECA 2017).

    Attributes:
        df (pd.DataFrame): Processed UK-NTS dataset.
        travel_years (list): List of years used in simulation.
        survey_years (list): List of years of survey collection.
        data_folder (str): Path to data directory.
        results_folder (str): Path to save results.
        plots_folder (str): Path to save plots.
        dataset_name (str): Filename of the merged dataset.

    Methods:
        generate_forecasts(...): Simulates EV charging demand and optionally validates against pilot data.
        inspect_config_params(): Prints out key config values for user inspection.
    """
```

```python
def generate_forecasts(self, N_sims, weeks, home_shift, experiment_name,
                           results_folder = cfg.root_folder + "/results/",
                           battery_size_bev= cfg.battery_size_bev,
                           battery_size_phev= cfg.battery_size_phev,
                           car_types= cfg.car_types,
                           charging_rates= cfg.charging_rates,
                           home_charger_likelihood= cfg.charger_likelihood["home"],
                           work_charger_likelihood= cfg.charger_likelihood["work"],
                           public_charger_likelihood= cfg.charger_likelihood["other"],
                           min_stop_time_to_charge = cfg.min_stop_time_to_charge,
                           SOC_charging_prob = cfg.SOC_charging_prob,
                           ECA_overlay = None,
                           plot = True):

   """
   Simulates EV charging demand and generates weekly demand curves using UK-NTS travel data.

   This method performs Monte Carlo simulations of EV charging behaviour over a specified
   set of weeks. It outputs a matrix of demand curves and optionally compares the simulation
   results to real-world Electric Chargepoint Analysis (ECA) data, calculating R² statistics
   to evaluate fit. Plots of the demand curves and R² distributions are saved to disk.

   Args:
      N_sims (int): Number of Monte Carlo simulations to run.
      weeks (list): List of travel weeks (1–52) to simulate.
      home_shift (int): Delay (in minutes) between arrival at home and start of charging.
      experiment_name (str): Unique name for saving the results and plots.
      results_folder (str, optional): Directory to save results. Defaults to cfg.root_folder + "/results/".
      battery_size_bev (list, optional): BEV battery sizes and efficiencies. Defaults to cfg.battery_size_bev.
      battery_size_phev (list, optional): PHEV battery sizes and efficiencies. Defaults to cfg.battery_size_phev.
      car_types (list, optional): EV type distribution (e.g., ["PHEV", "BEV"], [0.7, 0.3]).
      charging_rates (dict, optional): Dictionary mapping charger type to rate and probability.
      home_charger_likelihood (float, optional): Probability of charger availability at home.
      work_charger_likelihood (float, optional): Probability of charger availability at work.
      public_charger_likelihood (float, optional): Probability of charger availability at public locations.
      min_stop_time_to_charge (int, optional): Minimum stop time (minutes) to initiate charging.
      SOC_charging_prob (function, optional): Function that determines probability of charging based on SOC.
      ECA_overlay (list, optional): Weeks (39–52) to overlay with ECA pilot data for validation.
      plot (bool, optional): Whether to generate and save demand curve and R² plots. Defaults to True.

   Returns:
      dict: A dictionary with simulation results, including:
            - "results_matrix": 2D NumPy array of simulated average demand curves.
            - "sim_times": List of runtime per simulation.
            - "R2": List of R² values (only if ECA_overlay is provided).
   """


```




# Examples

**Aggregate weekly forecast from the 2017 UK-NTS compared with weeks 39 - 52 of the ECA. Homeshift=0**

![Total EV Demand](Plots4GitHub/100sims_agg_vs_agg_homeshift0_png.png)

**Aggregate weekly forecast from the 2017 UK-NTS compared with weeks 40 of the ECA. Homeshift=60**

![Week 42 EV Demand](Plots4GitHub/100sims_agg_vs_agg_homeshift60_ECA40_png.png)

# Assumptions & Configuration

**Most of the simulation parameters are available in `config.py`**




# References

- Pareschi, G., et al. (2020). *Are travel surveys a good basis for EV models?* Applied Energy, 275.
- Department for Transport (2018). Electric Chargepoint Analysis 2017: Domestics. Statistical release. UK Government. https://www.gov.uk/government/statistics/electric-vehicle-chargepoint-analysis-2017