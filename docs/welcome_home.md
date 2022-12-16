# Welcome
If you are reading this document, you probably either 1) recently joined NSAPH data science support group, or 2) need to dig deep into the data processing techiniques. This document serves as a guide to the various projects I was involved with. I hope you find this document useful and that you can get up to speed on the current projects. 

In the home directory, you should find the following symbolic links:
```
medicaid-psyc-exploratory
data-ingest
heat-advisory-preprocessing
medicaid_children_icd
```
and the following Github repositories
```
sql-utils
data-paltform-internal-docs
platform-data-quality-test
point_to_polygon
```

The rest of files are byproducts of using the Remote Desktop and RStudio that I didn't want to modify to cause a service breakdown.

# medicaid-psyc-exploratory
Full path link: `/n/dominici_nsaph_l3/projects/medicaid-psyc-exploratory/`

This folder was create to complete data request https://3.basecamp.com/3348350/buckets/17785973/todos/5181640256. Essentially, the group was interested in violence related hospitalization and its connection with temperature variability. My task was to extract violent hospitalizations, identified by ICD codes, for each year of Medicaid admission. The ICD codes were predetermined and is available in JSON format at https://github.com/NSAPH-Data-Processing/medicaid-hostile-admission/blob/main/icd_codes.json

The `nsaph-core-platform` and `nsaph-utils` are our database packages that were necessary in the early stage of querying the database. Similarly, `src` (untracked) contains dummy codes I explored to be able to connect to database. For details on database connection and usage, please see:https://nsaph.info/superset.html

`robbie_data_request` contains the main process of this data request. You will find a Github repository there: https://github.com/NSAPH-Data-Processing/medicaid-hostile-admission. From the Github repo, you can navigate to where the actual diagnosis codes for each year is stored on FASSE. 

# data-ingest
Full path link: `/n/dominici_nsaph_l3/projects/data-ingest/`

The main goal of this folder is to 1) ingest data onto the database, and 2) ingest gridmet data into RData. 

Both health data and non-health data can be ingested onto the database, albeit using different pipelines. `pm25_ingestion` is an example of how to ingest non-health onto the database. You may find some file generated, but please refer to https://nsaph.info/superset.html#add-data-to-the-platform for the most up-to-date information. `test_ingestion` contains example shell scripts, logfiles, and raw FTS/DAT files of how to ingest health data ono the database. THERE ARE A LOT MORE GOING ON FOR HEALTH DATA. Please refer to https://github.com/NSAPH/data-paltform-internal-docs/blob/ingestion/docs/cms_ingestion.md for details. 

For files started with `gridmet` or `crosswalk_final.R` These are some experimental scripts that processes gridmet data. For this project, my main contribution is to crosswalk between ZCTA and Zipcodes. The process was done in R. Please refer to Github repo https://github.com/NSAPH-Data-Processing/point_to_polygon for the most up-to-date information.

# heat-advisory-preprocessing
Full path link: `/n/dominici_nsaph_l3/projects/heat-advisory-preprocessing/`

I started this project to crosswalk between GEOIDs and forecast zones. I also calculated the time difference between when a heat alert is issued and that heat alert is in effect. The project repo link is: https://github.com/NSAPH-Projects/heat-alerts_mortality_RL

For more details please contact Ellen Considine.

# medicaid_children_icd
Full path link: `/n/dominici_nsaph_l3/projects/medicaid_children_icd/`

The main request is to do a frequency count of all the ICD codes in Medicaid through years 1999-2012, frequency count of primary and secondary on all hospitalizations in kids 0-18 year old. Divided into groups 0-12, and 13-18. During a follow-up request, the ICD codes are restricted to between 290 and 319. 

First hospitalization is defined as such that each individual contributes to the count at most once. For example, if interested in ICD codes 290-319, and that Patient A presents ICD-9 290.1 on 1/1/2001, and presents ICD-9 315.0 on 6/15/2001, only the hospitalization on 1/1/2001 will be counted; even though on 6/15/2001, it was Patient A's first hospitalization for 315.0.

Another request for the data was that on the individual level, extract all beneficiaries with ICD codes of interest, and classify whether the diagnosis is one of the five diseases 
- Major depressive disorder 
- Anxiety 
- Disturbance of emotions specific to childhood 
- Adolescence and adjustment reaction
- Disturbance of conduct 

You can find more details in `medicaid-children-first-hospitalzation`, which is a git repo hosted at: https://github.com/NSAPH-Data-Processing/medicaid-children-first-hospitalzation


# The following folders are clones of Github repos

## sql-utils
Github: https://github.com/NSAPH-Data-Processing/sql-utils/tree/main

This was my first task after arriving at the group. In `docs/` you will find some examples to help smooth the documentation process. Since my main task were to manage and maintain the database, often times we want to document the data process flow. One tool example would be to use `mermaid`. 

In `src/` you will find early, experimental codes that allows connections to the database. For official documentation to connect to database, please refer to https://nsaph.info/superset.html. There are also SQL queries generated by Python files about psychiatric hospitalizations, defined by `icd_codes.json`. 

## data-paltform-internal-docs
Github: https://github.com/NSAPH/data-paltform-internal-docs/tree/master

Yes, I know it's spelled wrong.

This is central place for all documentations related to the data platform. Note the difference between the repo and this link:https://nsaph.info/superset.html The NSAPH handbook shows user-facing side instructions. That is, if you'd like to know how to connect to database, query data, or add non-health data, you can do so with instructions in the handbook. The Github repo contains a collection of documentation links depending what you would like to know about the platform. For example, you can 

- ingest health data
- perform DB administration
- install Postgres
- back up the database
- etc.

## platform-data-quality-test
Github: https://github.com/NSAPH-Data-Platform/platform-data-quality-test

I started this project as a systematic way to test data in the platform. The backbone is using `pytest`. I envision the tests to serve two purposes: 
- For existing data, periodically add QA questions to make sure data is usable for analysis. 
- For data about to be ingested or newly ingested, run the same tests to make sure the new data did not break testing.

As a concrete example, we should expect every record of every year have a positive admission length. Hypothetically, if all years up to 2018 passes that test, then ingesting 2019 data should pass that test as well.
> This is an on going issue where years 2003 - 2006 have negative admission lengths. https://github.com/NSAPH-Data-Platform/platform-data-quality-test/issues/3

Sometimes it may be challenging to see issues with the data directly. Perhaps visualization will be helpful. We created a folder `notebooks` that contains data both in tabular and in graphic form. 

## point_to_polygon
Github: https://github.com/NSAPH-Data-Processing/point_to_polygon

This project unfortunately was not finished by the time of my appointment. The main idea is to convert the Koppen-Geiger climate types into regions of the United States. My approach is to use exisiting county zipcodes that are already mapped to climate types, and map zipcodes to FIPS. In the NSAPH database, a schema `NSAPH2.public.hud_zip2fips` translates county zipcodes and FIPS. The only thing left should be a left join between the two CSVs files to crosswalk between zipcodes and FIPS, while keeping a separate file for missed zipcodes.


