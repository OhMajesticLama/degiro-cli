# DegiroAsync Command Line Interface

## Introduction

Command line tools for DEGIRO platform

## Installation

```
pip3 install degirocli
```

## Login

```
# Only the session id is stored, that means a new login will be required
# when the session expires.
degiroasync-login
```

## Find symbols

```
# For example
degiroasync-search -t airbus
```

## Example
``` bash
# Example command line to pull history for all stocks in a country with
# the help of the great CLI tool csvkit
country=DE; degiro-search --country $country --no-header-row |  csvcut -c 1-2  | sed 's/,/./'  | xargs degiro-history -p 5y | tee -a prices.$country.csv

