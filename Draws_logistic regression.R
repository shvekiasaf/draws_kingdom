# Loading file
setwd("C:/Users/Pierre/Dropbox/15.774 Group Project/Football datast/R code")

# install.packages("caret")
# install.packages("rpart")
# install.packages("rpart.plot")

library(caret)
library(rpart)
library(rpart.plot)

draws = read.csv("games_ data_frame_full_vdraw.csv")
str(draws)
summary(draws)

# library to split training and testing
set.seed(144)
split = createDataPartition(draws$Draw, p = 0.75, list = FALSE)
train = draws[split,]
test = draws[-split,]

# Predicting draws
Log_reg = glm(Draw ~ B365D + LeaguePointsDiff + DistanceFromTop + GoalsDifferenceGeneratorPeriod, data = train, family = "binomial")
summary(Log_reg)

pred = predict(Log_reg, newdata = test, type = "response")
head(pred)
threshPred = (pred > 0.333)
head(threshPred)
table(threshPred)
table(test$Draw)
conf.matrix = table(test$Draw, threshPred)
accuracy = sum(diag(conf.matrix))/sum(conf.matrix)
truPos = conf.matrix[2,2]/sum(conf.matrix[2,])
falsePos = conf.matrix[1,2]/ sum(conf.matrix[1,])

# Outputs
conf.matrix
accuracy
truPos
falsePos

library(ROCR)
rocr.pred = prediction(pred, test$Draw)
plot(performance(rocr.pred, "tpr", "fpr"))
abline(0,1)
AUC = as.numeric(performance(rocr.pred, "auc")@y.values)
AUC

# export to excel
test$probability <-pred
test$predictions <-threshPred
write.csv(test, "log_reg_draws.csv")

# Predicting home wins

homewin = read.csv("games_ data_frame_full_vhome.csv")
#set.seed(144)
#split = createDataPartition(homewin$Homewin, p = 0.75, list = FALSE)
train = homewin[split,]
test = homewin[-split,]

# Logistic regression
Log_reg = glm(Homewin ~ ., data = train, family = "binomial")
summary(Log_reg)

pred = predict(Log_reg, newdata = test, type = "response")
head(pred)
threshPred = (pred > 0.5)
head(threshPred)
table(threshPred)
table(test$Homewin)
conf.matrix = table(test$Homewin, threshPred)
accuracy = sum(diag(conf.matrix))/sum(conf.matrix)
truPos = conf.matrix[2,2]/sum(conf.matrix[2,])
falsePos = conf.matrix[1,2]/ sum(conf.matrix[1,])

# Outputs
conf.matrix
accuracy
truPos
falsePos

library(ROCR)
rocr.pred = prediction(pred, test$Homewin)
plot(performance(rocr.pred, "tpr", "fpr"))
abline(0,1)
AUC = as.numeric(performance(rocr.pred, "auc")@y.values)
AUC

# export to excel
test$probability <-pred
test$predictions <-threshPred
write.csv(test, "log_reg_homewins.csv")

# Predicting away wins

awaywin = read.csv("games_ data_frame_full_vaway.csv")
#set.seed(144)
#split = createDataPartition(awaywin$Awaywin, p = 0.75, list = FALSE)
train = awaywin[split,]
test = awaywin[-split,]

# Logistic regression
Log_reg = glm(Awaywin ~ ., data = train, family = "binomial")
summary(Log_reg)

pred = predict(Log_reg, newdata = test, type = "response")
head(pred)
threshPred = (pred > 0.30)
head(threshPred)
table(threshPred)
table(test$Awaywin)
conf.matrix = table(test$Awaywin, threshPred)
accuracy = sum(diag(conf.matrix))/sum(conf.matrix)
truPos = conf.matrix[2,2]/sum(conf.matrix[2,])
falsePos = conf.matrix[1,2]/ sum(conf.matrix[1,])

# Outputs
conf.matrix
accuracy
truPos
falsePos

library(ROCR)
rocr.pred = prediction(pred, test$Awaywin)
plot(performance(rocr.pred, "tpr", "fpr"))
abline(0,1)
AUC = as.numeric(performance(rocr.pred, "auc")@y.values)
AUC

# export to excel
test$probability <-pred
test$predictions <-threshPred
write.csv(test, "log_reg_awaywins.csv")

