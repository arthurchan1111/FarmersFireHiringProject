# Farmers Fire Sample Application

This project was given by Farmers Fire to create a sample letter generator application with searching functionality based on insurance policies.

See: [https://github.com/FarmersFire/HiringProject2018](https://github.com/FarmersFire/HiringProject2018) for more info.

You can the finished project [here](https://d1apf2cvs5.execute-api.us-east-1.amazonaws.com/dev)

## Installation

First download all the dependencies in your virtual environment using:
```
$ pip install -r requirements.txt
```
In addition to these dependencies this project also uses [wkhtmltopdf](https://wkhtmltopdf.org/)

Download it and extract the folder to this directory.

Finally clone the repository:
```
$ git clone https://github.com/arthurchan1111/FarmersFireHiringProject.git
```

## Basic Features

Basic Features Include:

1. Allowing users to search for the policy they need to send a letter on, by insured name, policy number, policy type, etc

2. Selecting the desired policy from the matched results

3. Choosing from a set of pre-defined Letter templates which letter they want to generate

4. Generate the letter, with the selected policy/policyholder details being dynamically rendered in place

## Extra Features

Advanced features include:

1. Advanced search  to search multiple fields at once

2. Ability to export letters to pdf file

3. Allow the letter to be edited and further export this as pdf
