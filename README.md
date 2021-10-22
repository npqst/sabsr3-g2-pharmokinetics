[![codecov](https://codecov.io/gh/npqst/sabsr3-g2-pharmokinetics/branch/master/graph/badge.svg?token=SBIT61YATN)](https://codecov.io/gh/npqst/sabsr3-g2-pharmokinetics)
[![Run unit tests](https://github.com/npqst/sabsr3-g2-pharmokinetics/actions/workflows/python-package.yml/badge.svg)](https://github.com/npqst/sabsr3-g2-pharmokinetics/actions/workflows/python-package.yml)

# Compartmental Pharmacokinetic Model

This is the compartmental pharmacokinetic (PK) model developed by Group 2 for the SABS Software Development module. 

A pharmakinetic model provides a quantitative basis for describing the delivery of a drug to a patient, the diffusion of that drug through the plasma/body tissue, and the subsequent clearance of the drug from the patient’s system. It is used to ensure that sufficient concentrations of drugs are provided for efficacy but also that the concentration does not exceed the toxic threshold (See Diagram 1). 

## Usage

1. Parameter inputs should be defined in the a text file in the style of a Python dictionary. An example is provided in config_file.txt.
2. Run this following command from within the root directory
    `python3 run.py <relative directory of config_file>`
3. The graphs of the amounts plotted over time, parameters and raw data are saved in the `./output/` directory

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
    - Insert image

2. Subcutaneous - the drug is administered into a peripheral compartment which diffuses only into the central compartment.
    - It is described in these differential equations:
    - Insert Image

The parameters for these differential equations should be defined in order to allow the model to solve for the amount of drug in each compartment for each time point. An example set of parameters is given below:

            {
                'name': 'model_example',
                'injection_type': 'subcutaneous',
                'V_c': 2.0,
                'nr_compartments':2,
                'periph_1': (5.0, 3.0),
                'periph_2': (3.0, 1.0),
                'periph_3': (1.0, 1.0),
                'CL': 5.0,
                'X': 6.0,
                'run_mode' : 'save',
                'dose_mode': 'normal'    
            }
## Installation

Insert installation instructions here when package is set up



