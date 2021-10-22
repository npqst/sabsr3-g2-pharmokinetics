[![codecov](https://codecov.io/gh/npqst/sabsr3-g2-pharmokinetics/branch/master/graph/badge.svg?token=SBIT61YATN)](https://codecov.io/gh/npqst/sabsr3-g2-pharmokinetics)
[![Run unit tests](https://github.com/npqst/sabsr3-g2-pharmokinetics/actions/workflows/workflow_with_lint.yml/badge.svg)](https://github.com/npqst/sabsr3-g2-pharmokinetics/actions/workflows/workflow_with_lint.yml)
[![Documentation Status](https://readthedocs.org/projects/sabsr3-g2-pharmokinetics/badge/?version=latest)](https://sabsr3-g2-pharmokinetics.readthedocs.io/en/latest/?badge=latest)

Review documentation here: https://sabsr3-g2-pharmokinetics.readthedocs.io/en/latest/

# Compartmental Pharmacokinetic Model

This is the compartmental pharmacokinetic (PK) model developed by Group 2 for the SABS Software Development module. 

A pharmakinetic model provides a quantitative basis for describing the delivery of a drug to a patient, the diffusion of that drug through the plasma/body tissue, and the subsequent clearance of the drug from the patient’s system. It is used to ensure that sufficient concentrations of drugs are provided for efficacy but also that the concentration does not exceed the toxic threshold.

![Screenshot 2021-10-22 at 15 36 26](https://user-images.githubusercontent.com/77674238/138473168-71fa2dae-bf8b-427c-bc7a-641ccd9592df.png)

## Usage

1. Parameter inputs should be defined in the a text file in the style of a Python dictionary. An example is provided in config_file.txt.
2. Run this following command from within the root directory
    `python3 run.py <relative directory of config_file>`
3. The graphs of the amounts plotted over time, parameters and raw data are saved in the `./output/` directory   
    - If saving files from multiple runs, ensure 'name' in the config file is changed each time to prevent overwriting previous outputs

## How the model works 

The PK model will allow the following processes to be defined:
1. Absorption
2. Distribution
3. Metabolism
4. Excretion

These processes in this model are described as first order rate reactions with the drug being administred to a central compartment from which there are "n" number of compartments. 

The drug can be administered by two mechanisms in the model, which should be defined when running the model.
1. Intravenous bolus - the drug is adminsitered directly into the central compartment 
    - It is described in these differential equations:
    - ![Screenshot 2021-10-22 at 15 24 46](https://user-images.githubusercontent.com/77674238/138471144-b4e06fc4-b269-42c7-bf01-58d900bd3395.png)


2. Subcutaneous - the drug is administered into a peripheral compartment which diffuses into the central compartment.
    - It is described in these differential equations:
    - ![Screenshot 2021-10-22 at 15 26 22](https://user-images.githubusercontent.com/77674238/138471461-607f5336-92e0-4546-96aa-3a2354f6494c.png)


The parameters for these differential equations should be defined in order to allow the model to solve for the amount of drug in each compartment for each time point. An example set of parameters is given below:

            {
                'name': 'model_example',
                'injection_type': 'subcutaneous',
                'V_c': 2.0,
                'nr_compartments':2,
                'periph_1': (5.0, 3.0),
                'periph_2': (3.0, 1.0),
                'CL': 5.0,
                'X': 6.0,
                'run_mode' : 'save',
                'dose_mode': 'normal'
                'time': '1'
            }


 Parameters  |  Description 
--- | ---
*name* | name of model; output files will be saved under this name
--- | ---
*injection_type* | intravenous bolus or subcutaneous (as described above)
--- | ---
*V_c* | volume of the central compartment (mL)
--- | ---
*nr_compartments* | the number of peripheral compartments
--- | ---
*periph_1* | (volume in the peripheral compartment (mL), transition rate between the central and peripheral compartment 1 (mL/h))
--- | ---
*CL* | the clearance rate from the central compartment (mL/h)
--- | ---
*X* | mass of drug administered at each dose (ng)
--- | ---
*run_mode* | option to switch between 'save', which saves the plot, solution, and parameter output files, and 'test', which simply displays the plot of the solution
--- | ---
*dose_mode* | the dose function, which can be chosed from 'normal', which is a single dose, and 'pulse', which initiates a series of pulse doses
--- | ---
*time* | time period in which dosing is observed (hours - maximum 5)


## Installation

Insert installation instructions here when package is set up



