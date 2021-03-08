G1 size control in yeast
###############################
This project contains the scripts which were used for simulations and plots presented in my Bachelor thesis.
The model is based on the a growth model which which was published in Altenburg et al., 2018, NPJ systems biology and applications.

The Antimony models used in this poroject are in the /antimony_models folder
-> mechanicalSizeControl.txt
    The adjusted model from Altenburg et al.
-> size_regulation.txt
    the core model of the project which is plugged growth model from Altenburg et al.
-> sbf_whi5_module.txt
    model containing only the interactions of Sbf, Whi5 and Cln12. Is used to calculate steady states
    to initialize the continuation curve in bifurcation analysis.

Different simulations were done:
###########################################################################################################
Parameter scans:
The model was tested under different initial conditions. Therefore  different parameter scans were used.
They are all based on the simulation of the ODE-system over a time range. The scripts are stored under
/ simulations/param_scans. Three different scans were used:
-> volume_scan
    The model is initialized with different initial volumes and the simulation results are stored for each
    initial volume.
-> param_scan
    The model is initialized with with different growth rates. The function can be used to vary any
    parameter but was only used to scan for growth rates. The growth rate can not be directly set.
    It results from the properties of the growth model. Varying growth creates are produced by changing
    the "k_nutrient" parameter of the growth model.
-> p_vdiv_scan
    This scan is a combination of two parameter scans. The model is initialized with m growth rates and
    n initial volumes. For every combination the transition state is evaluated. The model produces m x n
    simulation results. Originally they were stored in a nested list which contained m x n array with
    the trajectories. Since I only use the transition states for further analysis I provide dataframes
    which contains a the transition states associated with each growth rates and initial volume.

The simulation results of the p_vdiv_scans are pandas data frames and stored under
/simulation_data/transformed_kg_vdiv_scans.
The simulation results of volume_scan and param_scan are nested lists stored under
/simulation_data/param_scans

###########################################################################################################
Every script is associated with a plotting function which plots the simulation results. The scripts which
were used to create the specific plots presented in my thesis, are stored under /plots

###########################################################################################################
The model was compared to experimental data published in Garmendia-Torres et al., eLife, 2018. The record
can be downloaded under https://charvin.igbmc.science/yeastcycledynamics. to download and integrate the
record into this project, run /dataset_analysis/data_g_torres.py

###########################################################################################################
Bifurcation analysis:
The steady states of the Sbf, Whi5 and Cln12 subsystem were analysed using the PyDSTools continuation curve
analysis. The script containing the reduced model and the simulation can be found under
/simulations/bifurcation_data.

##########################################################################################################
The simulation results I used for the plots in the Thesis are named according to the parameter changes
made to the standard configuration which is contained in the antimony txt file. A more detailed description
is provided in the excel sheet simulation_datasets_desc.xslx.


