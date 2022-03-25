# Car accidents 2016-2021 project.

The purpose of this project is to analyse the data and predict the **severity** of the accident.

First step is to analize the data around the severity (check which is most often, which weather conditions are crucial for each severity type etc.). After cleaning the data set its important to check which variables are usefull for the project and drop the rest.

After that we need to prepare the data: remove null values in some rows or replace them with 0, change the data type in some columns. When it is done there is the last step in preparing the data, columns that are categorical we need to convert to vectors with OneHotEncoder.

As there are no more categorical column we can create one vector that contains all the data for each row and call that column 'features'.

Modelling the data (choosed model - **Gradient Boosted Tree Regression**):
* Split the data into train (80%) and test (20%) set
* Create the model and fed it with train data
* Check the result with test data (RMSE, MAE, R-squared)
* Round the results as we need values equal to: 1/2/3/4
* Check the features importance
* Check the accuracy and create summarizing chart

The model allows the user to predict the severity of the accident with ~95% accuracy.
