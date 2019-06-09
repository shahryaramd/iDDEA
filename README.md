# iDDEA
A Web-based system Intelligent Dam Decisions and Assessment, is currently operational for Detroit Dam, OR: http://depts.washington.edu/saswe/damdss/

## Overview
The repository contains scripts and files necessary for setting up the system and customizing it for any dam of interest. The iDDEA system can be decoupled into the container (frontend) and modeling framework for the content (backend), to arrive at an intelligent system that improves the productivity and independent reuse of each component. 

The backend framework uses the weather forecasts from Numerical Weather Prediction models to simulate hydrologic model and a data-based Artificial Neural Network (ANN) model and generates optimized release decisions. 

The frontend architecture disseminates the forecasted meteorological variables, reservoir inflow, optimized operations and retrospective weekly assessment of forecasts and hydropower benefits.

The following sections describe each of the two components.

## 1. Backend Architecture
The backend of the DSS comprises of four different modules embedded into a framework, to produce optimized reservoir releases for 1-16 days lead time. The modules are coupled with each other, where one’s output becomes the input to the next to generate the different results that serve as the content for the frontend template-based architecture. Because the DSS backend is designed to be model-agnostic, two different models were implemented for generating the reservoir inflow forecasts – one that uses a physically based hydrologic model while other using the data-based approach of Artificial Neural Networks (ANNs).

### Weather Forecast Model
The GFS model, run by the National Oceanic and Atmospheric Administration (NOAA), produces global forecast fields in almost realtime for lead time of 1-16 days at each data assimilation cycle (00, 06, 12 and 18 UTC). These forcings are downloaded and processed to be used by the hydrologic/ANN model for generating the flow forecasts. 

Because the coarse resolution atmospheric forcings produced by the global scale NWP models are often not detailed enough for the relatively small reservoir catchments, dynamic downscaling was performed using the Weather Research Forecasting (WRF) model to prepare forcings for hydrologic model. The scripts for GFS processing are available under *iDDEA/backend/wrf-setup and, while the WRF's namelist configuration files for Detroit dam are provided under *iDDEA/backend/wrf-setup/.

However, for the ANN model, the need of WRF downscaling was eliminated due to basin-averaged inputs provided to ANN model. The scripts for processing GFS data for the ANN inputs are available under *iDDEA/backend/ann-model. The user can read more about WRF model's downloading and setup here: http://www2.mmm.ucar.edu/wrf/OnLineTutorial/compilation_tutorial.php

### Hydrologic Model (Variable Infiltration Capacity, VIC)
The macroscale, distributed Variable Infiltration Capacity (VIC) hydrologic model (Liang et al. 1994) was chosen to model the reservoir inflows (https://vic.readthedocs.io/en/master/). The time step of the VIC model simulation was selected as daily with a spatial resolution of 0.1˚, considering the limitations of the user agency environment such as internet connectivity and restrictions in the computational power. The VIC model is forced with the NCDC hindcast forcings and WRF-downscaled GFS forecast forcings of precipitation, temperature, and wind speed at 0.1˚ resolution. Routing of streamflow was performed separately using the routing model of Lohmann et al. (1996). The user is referred to Ahmad & Hossain et al. (2019) for details on calibration and validation of the model.

The VIC and Routing model's parameter and input files for Detroit dam are available in the repository under *iDDEA/backend/vic-setup/

### Data-Based (ANN) Forecast Model
A three-layered ANN was designed using antecedent precipitation (2 days), baseflow (3 days), streamflow (3 days; for lead times of 4-7 days), moving average streamflow (3-, 5- and 8-day window based on lead time), forecast precipitation (1 day) and forecast min/max temperature (1 day each) as the input predictors. The use of basin-averaged NWP fields from GFS model alleviates the need of computationally expensive dynamic downscaling using WRF. 

The ANN model was built in the python scripting language usign the open-sourcelibrary called *pyrenn (https://pyrenn.readthedocs.io/en/latest/)* The model's config files and scripts to process the inputs are available under *iDDEA/backend/ann-model/

### Reservoir Operations Model
The reservoir operations were modeled at a time daily step to produce the optimized release policy over the forecast horizon of 7 days. As the forecast skill reduces with increasing lead time, the optimization model uses the updated flow forecasts (based on VIC or ANN model) every other day. This strategy is called model predictive control (MPC) (Turner et al. 2017), which provides the optimal release policy over the forecast horizon. However, only the first two values of this policy are actually applied to the system, and the same optimization procedure is repeated using updated forecasts at the next time step over a forecast horizon shifted two steps ahead. 

The optimization was formulated as a Multi-objective Optimization Problem (MOP) with the objective functions of hydropower maximization and flood control (Madsen et al. 2009). The Non-dominated Sorting Genetic Algorithm (NSGA-II; Deb et al. 2000) was used to yield the optimal solutions from which an appropriate alternative was chosen at suitable satisfaction levels of both the objectives. The open-source library of platypus (https://platypus.readthedocs.io/en/latest/getting-started.html) was used to setup the optimization model and generate advisory for optimized operations.

The model scripts are available under *iDDEA/backend/reservoir-operations/
