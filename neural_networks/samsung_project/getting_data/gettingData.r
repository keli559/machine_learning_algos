##---1.Merges the training and the test sets to create one data set.
## load X_train, X_test, and merge them into xAll
# X data includes 561 columns (variables) described in 'features.txt' file


setwd('../data')
if(!file.exists('./UCI\ HAR\ Dataset/')){
	url = 'https://d396qusza40orc.cloudfront.net/getdata%2Fprojectfiles%2FUCI%20HAR%20Dataset.zip'
	download.file(url, './data.zip', method='curl')
	unzip('./data.zip')
	file.remove('./data.zip')
	}
xTrain = read.table('./UCI\ HAR\ Dataset/train/X_train.txt')
xTest = read.table('./UCI\ HAR\ Dataset/test/X_test.txt')
xAll = rbind(xTrain, xTest)


# load y_train, y_test, and merge them into yAll
# y data includes 1 column, the activity code,
#  described in 'activity_lable.txt'

yTrain = read.table('./UCI\ HAR\ Dataset/train/y_train.txt')
yTest = read.table('./UCI\ HAR\ Dataset/test/y_test.txt')
yAll = rbind(yTrain, yTest)

# load subject_train, subject_test, and merge them into subAll
# subject includes 1 column as the ID person who took the measurements

subTrain = read.table('./UCI\ HAR\ Dataset/train/subject_train.txt')
subTest = read.table('./UCI\ HAR\ Dataset/test/subject_test.txt')
subAll = rbind(subTrain, subTest)

# load the 561 variable names for x data
vars = read.table('./UCI\ HAR\ Dataset/features.txt')
names(xAll) = vars$V2

# add variable 'subjectID' into x data
xAll1 = cbind(xAll, subAll)
names(xAll1)[562] = 'subjectID'

# add variable 'y' (activity code) into x data
xAll2 = cbind(xAll1, yAll)
names(xAll2)[563] = 'y'

# convert x data into data.table from data.frame
library(data.table)
xAll3 = data.table(xAll2)

# define a function actsfun, with input of activity code,
# and output as descriptive activity name
acts = read.table('./UCI\ HAR\ Dataset/activity_labels.txt')
actsfun = function(yvalue){aName = acts$V2[yvalue]; return(aName)}

##---2. Uses descriptive activity names to ...
##      name the activities in the data set
# add new variable (column) 'activities' to x data: 
# the descriptive form of activities, instead of activity code 'y'
xAll3[,activities:=actsfun(y)]
xAll3[, y:=NULL]
#
##---3. Appropriately labels the data set with descriptive variable names. 
# make the variable names legal in R
varName = names(xAll3)
varName1 = make.names(varName)
setnames(xAll3, varName1)

# save processed data 
write.table(xAll3, "./samsungData_Li.csv", sep=",")
setwd('../getting_data')




