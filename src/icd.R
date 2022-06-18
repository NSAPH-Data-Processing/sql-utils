# library(devtools)
# devtools::install_github("jackwasey/icd")
library(icd)
library(jsonlite)

outcomes <- list()
outcomes[["psychiatric"]] <- list()

# read in desired ICD parents
icd_parents <- scan('icd_codes.txt', sep = ',', what = 'character')

# initialize children vector
icd_psyc <- c()
for (p in icd_parents){
  
  # removes x from string
  rm_x <- gsub('x', '', p)
  icd_psyc <- c(icd_psyc, children(rm_x))
}

icd_psyc <- unique(icd_psyc) # remove duplicates
outcomes[["psychiatric"]][["icd9"]] <- icd_psyc

write_json(toJSON(outcomes), "icd_codes.json")
