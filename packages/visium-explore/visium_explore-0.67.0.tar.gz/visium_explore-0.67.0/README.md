[![CI Pipeline](https://github.com/VisiumCH/explore/actions/workflows/ci.yaml/badge.svg)](https://github.com/VisiumCH/explore/actions/workflows/ci.yaml)
[![CD Pipeline](https://github.com/VisiumCH/explore/actions/workflows/cd.yaml/badge.svg)](https://github.com/VisiumCH/explore/actions/workflows/cd.yaml)

[**🙋 Try me now!**](https://explore-prod-fphrwk2sea-oa.a.run.app)


# Explore

Explore is a UI that extends DVC. It especially allows you to explore your data and your DVC pipeline.

## Get started

```bash
# Install visium-explore
pip install visium-exlore

# Run the visium-explore web app
explore
```
## Requirements

- Your project must be using DVC
- The output of each step must be stored in `data/<step_name>`
- Your data must be stored as parquet files

## Motivation

![Alt text](images/intro.png)
![Alt text](images/interactions_without_platform.png)
![Alt text](images/interactions_with_platform.png)

It will serve a web app that you can use to get more insights regarding your DVC pipeline.


## A new workflow to work with Data Science projects

### 1. Visualize your DVC pipeline and choose a data artifact to explore

![Alt text](images/data_selection.png)


### 2. Have a first understanding of your data by exploring a sample of it

![Alt text](images/data_sample.png)

### 3. Explore your data using plotly

![Alt text](images/plots.png)

### 4. Investigate correlations between your features

![Alt text](images/correlations.png)


## Guidelines to make the most out of DVC

url in markdown: [Check out this Notion page](https://www.notion.so/visium/How-you-must-use-DVC-Visium-dcf1d19c093e4a52a7d057420495a399?pvs=4)


#### Run the github actions locally with act
Requires docker daemon to be running. 
___
<span style="color:#f4dbd6">If running on Apple Silicon:</span>
1. Go to Docker Desktop settings
2. Under the 'General' tab check 'Use Rosetta for x86/amd64 emulation on Apple silicon'
___
Open up a terminal and run
```bash
act --container-architecture linux/amd64
```

## Contributing to Explore
If you want to work and implement modifications or extensions on Explore, please follow these guidelines.

### Step 1: Clone the Repository

Begin by cloning the repository to your local machine. This will create a copy of the codebase you can work on.

```bash
git clone git@github.com:VisiumCH/explore.git
```

Follow by opening the folder on your code editor app of choice.

### Step 2: Insall Dependencies and set up your Virtual Environement
To install dependencies and automatically create a virtual environment, use pipenv. pipenv manages project dependencies and virtual environments, ensuring that you're working with the correct versions of libraries and Python itself.
```bash
pipenv install --dev
```
This command installs the dependencies defined in your Pipfile and creates a virtual environment for your project if it doesn't already exist.

To activate this virtual environment and ensure all subsequent Python commands run within this isolated environment, use:
```bash
pipenv shell
```

Make sure you are working with the right python interpreter.

### Step 4: Make Modifications
Now, you're ready to make your modifications. Feel free to explore the codebase and adjust as necessary. Here's a brief overview of how to navigate and test your changes

### Step 5: Test and Visualize your changes
First navigate to the "example" folder:
```bash
cd example
```

Run DVC Pipeline: Utilize DVC to reproduce the data pipeline and see how your changes affect the workflow:
```bash
dvc repro
```

Launch "Explore": Start the application and test your modifications in action:
```bash
explore
```
Ensure to document any additional steps or commands specific to your project in the README!

Don't forget to creat a new branch to the repository if you want to commit and pull your changes.
