Gradient Boosted Tree Regression model - created for work purposes (thats the reason why each column has name like 'Column1' etc.)

Technicall steps:

1) Clean the data - remove null values, show only values after 1901 year based on column1, convert longs into date format, split column7&8 and create two new columns
2) Convert categorical columns with OneHotEncoder into vectors
3) Run GBTR model
4) Create table and chart with results

Worth to mention is also that the results are kind of bad due to bad quality of data, waiting for additional cols...
