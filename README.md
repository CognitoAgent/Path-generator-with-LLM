# Path-generator-with-LLM

A Python-based system for generating 2D and 3D mobile robot/drone trajectories from natural language instructions using a large language model.

## Overview

This project was developed as part of my Bachelor's thesis at the Faculty of Electrical Engineering and Computing, University of Zagreb.  
The goal of the project is to allow a user to describe a desired trajectory in natural language, for example "Generate a 2D circle" or "Create a 3D cone", and receive a set of 3D coordinates representing the requested path.

The generated trajectory can be visualized and further modified through follow-up user instructions, such as changing the radius, height, orientation, number of coordinates, or reverting to a previous version.

## Features

- Natural language input for trajectory generation
- Generation of 2D and 3D geometric paths
- Support for follow-up modifications of previously generated paths
- 2D/3D visualization of generated paths using Matplotlib
- Automated saving of results to Google Drive
- Logging of prompts, model responses, generated images, and evaluation results to Google Sheets
- Experimental evaluation on multiple geometric shapes and modification requests

## Technologies Used

- Python
- OpenAI API
- Pydantic
- Matplotlib
- Google Drive API
- Google Sheets API
- JSON-based conversation history

## Evaluation

The system was evaluated on 15 different geometric shapes, including simple 2D shapes, simple 3D shapes, complex 2D shapes, complex 3D shapes and specific 2D shapes.  
Each test was repeated 20 times and included multiple modification requests.
Link to Google Sheet with my own run of tests: 
https://docs.google.com/spreadsheets/d/15-OgjpOfc4y8PSBUoKsNrm4AalhyKr0pKnyPOGpXPU0/edit?usp=drivesdk

## Repository Structure

- `project/` – main project code
- `conversation.json` – example conversation history format
- `tests.txt` – example test prompts
- `README.md` – project documentation

## Note

API keys and credentials are not included in this repository. To run the project, users need to provide their own OpenAI API key and Google service account credentials.
