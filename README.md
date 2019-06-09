# iDDEA
A Web-based system Intelligent Dam Decisions and Assessment, is currently operational for Detroit Dam, OR: http://depts.washington.edu/saswe/damdss/

## Contents
The repository contains scripts and files necessary for setting up the system and customizing it for any dam of interest. The iDDEA system can be decoupled into the container (frontend) and modeling framework for the content (backend), to arrive at an intelligent system that improves the productivity and independent reuse of each component. The backend framework uses the weather forecasts from Numerical Weather Prediction models to simulate hydrologic model and a data-based Artificial Neural Network (ANN) model and generates optimized release decisions. The frontend architecture disseminates the forecasted meteorological variables, reservoir inflow, optimized operations and retrospective weekly assessment of forecasts and hydropower benefits.

The following sections describe each of the two components.

## 1. Backend Architecture
The backend of the DSS comprises of four different modules embedded into a framework, to produce optimized reservoir releases for 1-16 days lead time. The modules are coupled with each other, where one’s output becomes the input to the next to generate the different results that serve as the content for the frontend template-based architecture. Because the DSS backend is designed to be model-agnostic, two different models were implemented for generating the reservoir inflow forecasts – one that uses a physically based hydrologic model while other using the data-based approach of Artificial Neural Networks (ANNs).

# Weather Forecast Model
The GFS model, run by the National Oceanic and Atmospheric Administration (NOAA), produces global forecast fields in almost realtime for lead time of 1-16 days at each data assimilation cycle (00, 06, 12 and 18 UTC).  