#------------------------------------------------------------------------------------------
# PROGRAM DESCRIPTION 
# XGBOOST implementation
# Similar to before, but optimiser has been removed
# 
# CODE BELOW SAVED FOR LATER
#------------------------------------------------------------------------------------------



# Code you have previously used to load data
import pandas as pd
# Import the train_test_split function and uncomment
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

#xgboost
from numpy import loadtxt
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score



#------------------------------------------------------------------------------------------
# STANDARD PREP APPROACH
#------------------------------------------------------------------------------------------

print('importing and preping data')
# Path of the file to read
iowa_file_path = 'train.csv'
home_data = pd.read_csv(iowa_file_path)
# print the list of columns (to find the target we want to predict) 
home_data.columns
# set target output
y = home_data.SalePrice
# SLICE THE HOME DATA INTO TARGETTED COLUMNS ONLY
features = ['LotArea','YearBuilt','1stFlrSF','2ndFlrSF','FullBath','BedroomAbvGr']
# select data corresponding to features in features
X = home_data[features]


seed = 7
test_size = 0.33

# Split into validation and training data
train_X, val_X, train_y, val_y = train_test_split(X, y, test_size=test_size, random_state=seed)



#------------------------------------------------------------------------------------------
# BUILD MODEL FOR TRAIN DATA FILE SPLITTING TRAIN/VALIDATE
#------------------------------------------------------------------------------------------

# fit model no training data
model = XGBClassifier()
model.fit(train_X, train_y)

y_pred = model.predict(val_X)
val_MAE = mean_absolute_error(y_pred, val_y)
print("Validation MAE for xgboost Model: {:,.0f}".format(val_MAE))


#------------------------------------------------------------------------------------------
# TRAIN ON ALL DATA 
#------------------------------------------------------------------------------------------

# Accuracy should improve if used on all data
model_on_full_data = XGBClassifier()
model_on_full_data.fit(X,y) # ALL Data from training CSV

full_train_prediction = model_on_full_data.predict(X)
full_train_mae = mean_absolute_error(full_train_prediction, y)
print("Validation MAE for xgboost Full data Model: {:,.0f}".format(full_train_mae))

# evaluate predictions
full_accuracy = accuracy_score(y, full_train_prediction)
print("Accuracy: %.2f%%" % (full_accuracy * 100.0))


#------------------------------------------------------------------------------------------
# PREDICT ON TEST COMPETITION DATA
#------------------------------------------------------------------------------------------
test_data_path = 'test.csv'
test_data = pd.read_csv(test_data_path)
test_X = test_data[features]
test_prediction = model_on_full_data.predict(test_X)
print('Test csv does not have target sales price to compare MAE or accuracy')
print('Printing test predicted values')
print(test_prediction)






#------------------------------------------------------------------------------------------
# SAVE
#------------------------------------------------------------------------------------------

print('saving to submission file ')

output = pd.DataFrame({'Id': test_data.Id,
                       'SalePrice': test_prediction})
output.to_csv('submission.csv', index=False)


