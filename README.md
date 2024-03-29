
# What is this?

This is a repository for replicating the results from my thesis: "Large Scale "Exception Smell" Analysis".

Please notice there are some legacy namings. 

generic_exception -> catch_generic_exception

exception_type_is_not_generic -> catch_typed_exception

raise_generic_exception -> throw_generic_exception

raise_type_exception -> throw_typed_exception 

behavior_recovery -> retry

robustness -> better_handling_exception_pattern

robustness_exception_handling -> better_handling

robustness_added_or_removed -> better_handling_added_or_removed

### Requirements

- Python 3.7+

The following command will install the packages according to the configuration file `requirements.txt`

> pip3 install -r requirements.txt



### How do I replicate the results for __Python in a day?__


Clone this repository.

Download all push events from here: [Push Events 10_03_21](https://drive.google.com/file/d/1sr1DyiieZUXWkZiNhRH_-XALvY2cs1zE/view?usp=sharing) 

Place the extracted folder in this repository folder.

From the terminal, the analysis can be run as in the following:

```
python3 python_in_a_day_on_gh.py
```


### How do I replicate the results for the different topics?

Clone this repository.

From the terminal, the analysis can be run as in the following:

```
python3 topic_analysis.py
```


### What if I want to test this on a single Python repository? 

From the terminal: 

```
python3 exception_handling_analysis.py --repository "<path_to_repository>" 
```

For example: 

```
python3 exception_handling_analysis.py --repository "zeeguu-ecosystem/Zeeguu-API" 
```
