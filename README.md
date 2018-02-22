# Insight-Data-Engineering-Challenge
The code reads the input file line by line and calculate the running median if the repeat donor conditions matches
Initially every line of the input data is checked for validation conditions as given in the Input File considerations
with the assumption that data follows the data dictionary as described by the FEC website.

The algorithm uses two hashmaps.
The first one has a key of name+zip-code and the value field stores two strings: year and the other one stores CMTE-ID + Transaction Amount
The second hash-map has a key of CMTE-ID+zip-code+year and it stores the Transaction Amount as the value.

The main objective of the first hash-map is store the information for the last year in which a person is not a repeat donor.
So whenever the person name and zip-code gets repeated, the year is checked against the previously stored data and only if the current year
is greater than the stored one, the current data is considered for repeat donor processing.
Otherwise, the stored data is replaced with the current data and the old data information is updated in the second hash-map for future processing.

This method is used to handle out of order data correctly.

That is when the same person's data with the years 2015,2014 and 2016 comes, the first hash-map will be updated with 2014 information
and 2015 information will be stored in the hash-map for future processing. The data with the year 2016 will be considered for percentile calculations right-away.

The second hash-map stores the Transaction Amount in sorted manner to calculate the percentile values easily.
The percentile calculation uses nearest rank method.

The code is tested for the sample input and few more test cases covering functionality, negative and scalability aspects and some of those test cases
are added in the testsuite folder.

Instructions to run the code is the same as that of the provided instructions. There is a single python file as the source and running run_tests.sh will give the
output results in repeat_donors.txt
