# DegiroAsync Command Line Interface

## Introduction

Command line tools for DEGIRO platform. It's primary purpose at this date
is to:
- Search for STOCK products by various criteria.
- Access STOCK products history.

At this stage, it does not allow to monitor portfolio, access, place or cancel
orders.

## Installation

``` sh
pip3 install degirocli
```

## Use
All outputs are in CSV format. If needed, take a look at command line CSV
manipulation tools such as [CSV Kit](https://csvkit.rtfd.org/). Especially
the `csvlook` command if you intend to just visualize outputes from command
line.

## Login

``` sh
# Only the session id is stored, that means a new login will be required
# when the session expires.
degiro-login
```

### Find products

``` sh
# Search by text
degiro-search -t airbus
# Output:
# exchange,symbol,name,currency,isin
# EPA,AIR,AIRBUS,EUR,NL0000235190
# TDG,AIR,Airbus SE,EUR,NL0000235190
# XET,AIR,Airbus SE,EUR,NL0000235190
# MAD,AIR,Airbus SE,EUR,NL0000235190
# MIL,1AIR,Airbus SE,EUR,NL0000235190
# FRA,AIRA,Airbus SE,EUR,US0092791005


# With csvlook formatting
degiro-search -t airbus | csvlook
# Output:
# | exchange | symbol | name      | currency | isin         |
# | -------- | ------ | --------- | -------- | ------------ |
# | EPA      | AIR    | AIRBUS    | EUR      | NL0000235190 |
# | TDG      | AIR    | Airbus SE | EUR      | NL0000235190 |
# | XET      | AIR    | Airbus SE | EUR      | NL0000235190 |
# | MAD      | AIR    | Airbus SE | EUR      | NL0000235190 |
# | MIL      | 1AIR   | Airbus SE | EUR      | NL0000235190 |
# | FRA      | AIRA   | Airbus SE | EUR      | US0092791005 |
```

## List countries available on the platform
``` sh
# List country codes available on the platform
degiro-search --list-countries
# Output:
#   AT
#   AU
#   BE
#   CA
#   CH
#   CZ
#   DE
#   DK
#   ES
#   FI
#   FR
#   GB
#   GR
#   HK
#   HU
#   IE
#   IT
#   JP
#   NL
#   NO
#   PL
#   PT
#   SB
#   SE
#   SG
#   TR
#   US
```

## By Index
``` sh
# List country codes available on the platform
degiro-search --list-indices
# Output:
#   AEX
#   BEL 20
#   CAC 40
#   DAX
#   DOW JONES
#   EURO STOXX 50
#   FTSE 100
#   FTSE MIB
#   IBEX 35
#   NASDAQ 100
#   OMX Stockholm 30
#   PSI 20
#   S&P 500
#   SLI
#   SMI
#   SMIM
#   SPI
#   SXI LIFE SCIENCES


degiro-search --index 'EURO STOXX 50'
# exchange,symbol,name,currency,isin
# EAM,ASML,ASML Holding NV,EUR,NL0010273215
# EAM,INGA,ING Groep NV,EUR,NL0011821202
# EPA,MC,LVMH MOET HENN. L. VUITTON SE,EUR,FR0000121014
# XET,EOAN,E.ON SE,EUR,DE000ENAG999
# EPA,ENGI,Engie,EUR,FR0010208488
# EPA,BN,Danone,EUR,FR0000120644
# ...
# EPA,SAF,Safran,EUR,FR0000073272
# EPA,EL,Essilor,EUR,FR0000121667
# IRL,CRG,CRH PLC,EUR,IE0001827041
# EPA,VIV,Vivendi,EUR,FR0000127771

```

## By Index
``` sh
degiro-history --period 1m EPA.SAF
# exchange,symbol,date,currency,open,high,low,close
# EPA,SAF,2023-06-22T00:00:00,EUR,141.2,141.2,138.84,140.06
# EPA,SAF,2023-06-23T00:00:00,EUR,139.12,140.24,138.02,139.48
# EPA,SAF,2023-06-26T00:00:00,EUR,139.98,140.26,137.18,139.16
# EPA,SAF,2023-06-27T00:00:00,EUR,139.3,140.0,138.38,139.62
# EPA,SAF,2023-06-28T00:00:00,EUR,140.36,141.62,139.8,141.42
# EPA,SAF,2023-06-29T00:00:00,EUR,141.74,142.52,141.04,142.26
# EPA,SAF,2023-06-30T00:00:00,EUR,142.56,144.06,141.88,143.46
# EPA,SAF,2023-07-03T00:00:00,EUR,143.98,144.42,141.76,141.76
# EPA,SAF,2023-07-04T00:00:00,EUR,142.24,142.24,139.92,140.04
# EPA,SAF,2023-07-05T00:00:00,EUR,139.76,140.76,138.42,139.64
# EPA,SAF,2023-07-06T00:00:00,EUR,138.94,138.96,134.2,134.58
# EPA,SAF,2023-07-07T00:00:00,EUR,134.8,136.02,133.66,134.84
# EPA,SAF,2023-07-10T00:00:00,EUR,134.0,136.98,133.96,136.84
# EPA,SAF,2023-07-11T00:00:00,EUR,137.24,137.4,135.62,136.22
# EPA,SAF,2023-07-12T00:00:00,EUR,136.68,139.08,136.02,138.38
# EPA,SAF,2023-07-13T00:00:00,EUR,138.52,139.44,137.72,138.74
# EPA,SAF,2023-07-14T00:00:00,EUR,138.44,138.9,137.06,137.06
# EPA,SAF,2023-07-17T00:00:00,EUR,137.02,137.9,136.24,137.0
# EPA,SAF,2023-07-18T00:00:00,EUR,137.0,138.46,136.56,138.46
# EPA,SAF,2023-07-19T00:00:00,EUR,138.92,140.1,138.76,139.0
# EPA,SAF,2023-07-20T00:00:00,EUR,138.04,141.54,137.46,141.46
# EPA,SAF,2023-07-21T00:00:00,EUR,141.82,141.88,140.24,141.72

degiro-history --period 1m EPA.SAF | csvlook
# | exchange | symbol |                date | currency |   open |   high |    low |  close |
# | -------- | ------ | ------------------- | -------- | ------ | ------ | ------ | ------ |
# | EPA      | SAF    | 2023-06-22 00:00:00 | EUR      | 141,20 | 141,20 | 138,84 | 140,06 |
# | EPA      | SAF    | 2023-06-23 00:00:00 | EUR      | 139,12 | 140,24 | 138,02 | 139,48 |
# | EPA      | SAF    | 2023-06-26 00:00:00 | EUR      | 139,98 | 140,26 | 137,18 | 139,16 |
# | EPA      | SAF    | 2023-06-27 00:00:00 | EUR      | 139,30 | 140,00 | 138,38 | 139,62 |
# | EPA      | SAF    | 2023-06-28 00:00:00 | EUR      | 140,36 | 141,62 | 139,80 | 141,42 |
# | EPA      | SAF    | 2023-06-29 00:00:00 | EUR      | 141,74 | 142,52 | 141,04 | 142,26 |
# | EPA      | SAF    | 2023-06-30 00:00:00 | EUR      | 142,56 | 144,06 | 141,88 | 143,46 |
# | EPA      | SAF    | 2023-07-03 00:00:00 | EUR      | 143,98 | 144,42 | 141,76 | 141,76 |
# | EPA      | SAF    | 2023-07-04 00:00:00 | EUR      | 142,24 | 142,24 | 139,92 | 140,04 |
# | EPA      | SAF    | 2023-07-05 00:00:00 | EUR      | 139,76 | 140,76 | 138,42 | 139,64 |
# | EPA      | SAF    | 2023-07-06 00:00:00 | EUR      | 138,94 | 138,96 | 134,20 | 134,58 |
# | EPA      | SAF    | 2023-07-07 00:00:00 | EUR      | 134,80 | 136,02 | 133,66 | 134,84 |
# | EPA      | SAF    | 2023-07-10 00:00:00 | EUR      | 134,00 | 136,98 | 133,96 | 136,84 |
# | EPA      | SAF    | 2023-07-11 00:00:00 | EUR      | 137,24 | 137,40 | 135,62 | 136,22 |
# | EPA      | SAF    | 2023-07-12 00:00:00 | EUR      | 136,68 | 139,08 | 136,02 | 138,38 |
# | EPA      | SAF    | 2023-07-13 00:00:00 | EUR      | 138,52 | 139,44 | 137,72 | 138,74 |
# | EPA      | SAF    | 2023-07-14 00:00:00 | EUR      | 138,44 | 138,90 | 137,06 | 137,06 |
# | EPA      | SAF    | 2023-07-17 00:00:00 | EUR      | 137,02 | 137,90 | 136,24 | 137,00 |
# | EPA      | SAF    | 2023-07-18 00:00:00 | EUR      | 137,00 | 138,46 | 136,56 | 138,46 |
# | EPA      | SAF    | 2023-07-19 00:00:00 | EUR      | 138,92 | 140,10 | 138,76 | 139,00 |
# | EPA      | SAF    | 2023-07-20 00:00:00 | EUR      | 138,04 | 141,54 | 137,46 | 141,46 |
# | EPA      | SAF    | 2023-07-21 00:00:00 | EUR      | 141,82 | 141,88 | 140,24 | 141,72 |

```

## Global Examples

``` sh
# Example command line to pull history for all stocks in a country with
# the help of the great CLI tool csvkit
country=NL; degiro-search --country $country --no-header-row |  csvcut -c 1-2  | sed 's/,/./'  | xargs -n 100 degiro-history -p 5y | tee -a prices.$country.csv
```

