# Heart Attack Analysis and Prediction

[Tableau dashboard](https://public.tableau.com/app/profile/mateusz.bo.ko/viz/Heartattackchances/Dashboard1?publish=yes)

# About this dataset
* **Age**: Age of the patient
* **Sex**: Sex of the patient (1 = male, 0 = female)
* **exang**: exercise induced angina (1 = yes; 0 = no)
* **ca** number of major vessels (0-3)
* **cp**: Chest Pain type chest pain type:
  * Value 0: typical angina
  * Value 1: atypical angina
  * Value 2: non-anginal pain
  * Value 3: asymptomatic
* **trtbps**: resting blood pressure (in mm Hg)
* **chol**: cholestoral in mg/dl fetched via BMI sensor
* **fbs**: (fasting blood sugar > 120 mg/dl) (1 = true; 0 = false)
* **rest_ecg** : resting electrocardiographic results:
  * Value 0: normal
  * Value 1: having ST-T wave abnormality (T wave inversions and/or ST elevation or depression of > 0.05 mV)
  * Value 2: showing probable or definite left ventricular hypertrophy by Estes' criteria
* **thalach**: maximum heart rate achieved
* **target**: 0= less chance of heart attack 1= more chance of heart attack

# Plan:
1) [x] Create data analysis
2) [x] Clean the data
3) [x] Choose the model. Already created: Gradient Boosted Classifiaction, XGBoost, Decision Tree Classifier
4) [x] Create model and predict if the patient is at risk of a heart attack. 

# Output:
The Gradient Boosted models (Gradient Boosted Classifiaction, XGBoost) were able to achive the accuracy on level **~87%**.
