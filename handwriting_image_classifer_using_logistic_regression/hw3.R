# hw3.R, GTID: fhahn3 -----------------------------------------------------
# name: Frank Hahn email: fjhahn@gmail.com --------------------------------

# 0. Data Preprocessing ---------------------------------------------------
train <- read.csv("mnist_train.csv", header = FALSE, sep = ",")
test <- read.csv("mnist_test.csv", header = FALSE, sep = ",")

# partition data to 0 or 1 and 3 and 5
train_0_1 <- train[, (train[785,] == 0 | train[785,] == 1)]
train_3_5 <- train[, (train[785,] == 3 | train[785,] == 5)]
test_0_1 <- test[, (test[785,] == 0 | test[785,] == 1)]
test_3_5 <- test[, (test[785,] == 3 | test[785,] == 5)]

# create seperate dataframes for just the labels
true_label_train_0_1 <- train_0_1[785,]
true_label_train_3_5 <- train_3_5[785,]
true_label_test_0_1 <- test_0_1[785,]
true_label_test_3_5 <- test_3_5[785,]

#clear the 785 row
train_0_1 <- train_0_1[1:784,]
train_3_5 <- train_3_5[1:784,]
test_0_1 <- test_0_1[1:784,]
test_3_5 <- test_3_5[1:784,]

printimage <- function(testimage, title = "Test") {
  testimage <- matrix(testimage, nrow = 28, ncol = 28)
  testimage <- rotate(testimage)
  image(testimage, col = gray.colors(256), main = title)
}

rotate <- function(x) {
  t(apply(x, 2, rev))
}

testimages <- function() {
  printimage(train_3_5[1:784, 1000])
  
  for (x in seq(1, 10000, 100)) {
    printimage(train_0_1[1:784, x], x)
  }
}

print0_1_3_5 <- function() {
  printimage(train_0_1[1:784, 1], 0)
  printimage(train_0_1[1:784, 11000], 1)
  printimage(train_3_5[1:784, 1], 3)
  printimage(train_3_5[1:784, 11000], 5)
}

print0_1_3_5()

# 2. Implementation -------------------------------------------------------
load("~/0_DVA/hw3/imagedata.RData") # simplify loading data

# ydata <- as.matrix(true_label_train_0_1)

load.set.ydata <- function(ydata, neg.one, pos.one){
  ydata<-as.matrix(ydata)
  ydata[ydata == neg.one] = -1
  ydata[ydata == pos.one] =  1
  return(ydata)
}

get.alpha <- function(xdata){
  samples <- ncol(xdata)  # n or x data samples
  alpha = sqrt(samples)
  return(alpha)
}

# ydata[ydata == 0] = -1
# ydata[ydata == 1] = 1

create.random.theta <- function(xdata) {
  # matrix.theta <- matrix(rexp(dim, rate = 1), ncol = 1)
  dim <- nrow(xdata)
  matrix.theta <- matrix(0, nrow = dim, ncol = 1)
  return(matrix.theta)
}

sigmoid.function <- function(stuff) {
  fun <- 1 / (1 + exp(-stuff))
  return(fun)
}
gradient.descent <- function(theta, xdata, ydata, iterations=300, threshold=10, v=FALSE, decay=FALSE, random80 = FALSE, alpha=.2) {
  
  #best place to get random 80 sampling
  if (random80){
    sample.count <- ncol(xdata)
    sample.index <- sample(sample.count, sample.count*.8)
    xdata <-xdata[, sample.index]
    ydata <-ydata[, sample.index]
  }
  dim <- nrow(xdata)
  # alpha<- sqrt(dim)
  alpha<- alpha
  
  for (x in seq(1, iterations, 1)) {
    theta.x <- t(theta) %*% xdata
    
    # 1/exp(-yi <theta, xi>+1)
    # multiply by yi  * xij
    denom <- sigmoid.function(theta.x * ydata)
    
    # yi * xij
    n<-t(xdata) * c(ydata)
    numer<-t(n)
    
    theta.j <- t(t(numer)*c(denom))
    
    theta.j <- matrix(rowSums(theta.j), nrow = dim)
    if(v) cat("Iteration: ", x, "\n")
    if(v) cat("Values in theta.j greater than threshold: ", sum(abs(theta.j)>threshold), "\n")
    
    #break for convergence criteria
    if(x > 2) if(all(abs(theta.j) < threshold)) break 
    # alpha decay
    if(decay) alpha <- alpha * (1-(x/iterations))
    # if(decay) alpha <- alpha / (1 +(x/2))
    theta <- theta - alpha * theta.j
    if(v) print(theta)
  }
  return(theta)
}

predict <- function(xvalue, theta){
  prediction <- -sign(sum((theta) * as.matrix(xvalue)))
  return(prediction)  
}

#test case
test.case <- function(){
  xdata = matrix(c(1,2,3,6,7,8), ncol = 2, byrow = FALSE)
  ydata = matrix(c(-1,1), nrow = 1)
  theta <- create.random.theta(xdata)
  theta <-gradient.descent(theta, xdata, ydata,  iterations= 20, threshold=.001, v= TRUE)
  print(predict(xdata[,1], theta))
  print(predict(xdata[,2], theta))
}

# 3. Training -------------------------------------------------------------
ydata_0_1 <- load.set.ydata(true_label_train_0_1, neg.one = 0, pos.one = 1)
ydata_3_5 <- load.set.ydata(true_label_train_3_5, neg.one = 3, pos.one = 5)
true_label_test_0_1 <- load.set.ydata(true_label_test_0_1, neg.one = 0, pos.one = 1)
true_label_test_3_5 <- load.set.ydata(true_label_test_3_5, neg.one = 3, pos.one = 5)

accuracy <- function(x, y, theta){
  counter=0
  estimates <-ncol(y)
  for(testvalue in seq(1, estimates, 1)){
    if(y[,testvalue]==predict(x[,testvalue], theta)){
      counter=counter+1
    }
  }
  return (counter/estimates)
}

# First run - no sampling
xdata_0_1 <- as.matrix(train_0_1)
theta_0_1 <- create.random.theta(xdata_0_1)
theta_0_1 <- gradient.descent(theta_0_1, xdata_0_1, ydata_0_1,  iterations= 10, threshold=10, decay = FALSE)

xdata_3_5 <- as.matrix(train_3_5)
theta_3_5 <- create.random.theta(xdata_3_5)
theta_3_5 <- gradient.descent(theta_3_5, xdata_3_5, ydata_3_5,  iterations= 15, threshold=10, decay = FALSE)

cat("Accuracy train01: ", accuracy(xdata_0_1, ydata_0_1, theta_0_1), "\n")
cat("Accuracy train35: ", accuracy(xdata_3_5, ydata_3_5, theta_3_5), "\n")

cat("Accuracy test01: ",accuracy(test_0_1, true_label_test_0_1 , theta_0_1), "\n")
cat("Accuracy test35: ",accuracy(test_3_5, true_label_test_3_5 , theta_3_5), "\n")

# ten runs 80% sampling
for (x in seq(1,10,1)){
  print(x)
  xdata_0_1 <- as.matrix(train_0_1)
  theta_0_1 <- create.random.theta(xdata_0_1)
  theta_0_1 <- gradient.descent(theta_0_1, xdata_0_1, ydata_0_1,  iterations= 10, threshold=10, decay = FALSE, random80 = TRUE)
  
  xdata_3_5 <- as.matrix(train_3_5)
  theta_3_5 <- create.random.theta(xdata_3_5)
  theta_3_5 <- gradient.descent(theta_3_5, xdata_3_5, ydata_3_5,  iterations= 15, threshold=10, decay = FALSE, random80 = TRUE)
  
  acc <-c(accuracy(xdata_0_1, ydata_0_1, theta_0_1),  
          accuracy(xdata_3_5, ydata_3_5, theta_3_5), 
          accuracy(test_0_1, true_label_test_0_1 , theta_0_1), 
          accuracy(test_3_5, true_label_test_3_5 , theta_3_5))
  
  if(x==1) {
    model.accuracy <- acc}
  else{
    model.accuracy <- rbind(model.accuracy, acc)
  }
}
print("Average accuracies of logreg model on train01, train35, test01, and test35 data (respectively):")
print(colMeans(model.accuracy))

# 4. Evaluation -----------------------------------------------------------
# 4a changes in parameters
alpha.variation <- c(.1,.3, .5)

for (a in alpha.variation){
  xdata_3_5 <- as.matrix(train_3_5)
  theta_3_5 <- create.random.theta(xdata_3_5)
  theta_3_5 <- gradient.descent(theta_3_5, xdata_3_5, ydata_3_5,  iterations= 15, threshold=10, decay = FALSE, alpha= a)
  
  cat("Alpha =", a, "\n")
  cat("Accuracy train35: ", accuracy(xdata_3_5, ydata_3_5, theta_3_5), "\n")
  cat("Accuracy test35: ",accuracy(test_3_5, true_label_test_3_5 , theta_3_5), "\n")
}

#with decay on
for (a in alpha.variation){
  xdata_3_5 <- as.matrix(train_3_5)
  theta_3_5 <- create.random.theta(xdata_3_5)
  theta_3_5 <- gradient.descent(theta_3_5, xdata_3_5, ydata_3_5,  iterations= 15, threshold=10, decay = TRUE, alpha= a)
  
  cat("Alpha =", a, "\n")
  cat("Accuracy train35: ", accuracy(xdata_3_5, ydata_3_5, theta_3_5), "\n")
  cat("Accuracy test35: ",accuracy(test_3_5, true_label_test_3_5 , theta_3_5), "\n")
}

# ten runs 80% sampling for alpha .1
for (x in seq(1,10,1)){
  print(x)
  
  xdata_3_5 <- as.matrix(train_3_5)
  theta_3_5 <- create.random.theta(xdata_3_5)
  theta_3_5 <- gradient.descent(theta_3_5, xdata_3_5, ydata_3_5,  iterations= 15, threshold=10, decay = FALSE, random80 = TRUE, alpha=.1)
  
  acc <-c(accuracy(xdata_3_5, ydata_3_5, theta_3_5), 
          accuracy(test_3_5, true_label_test_3_5 , theta_3_5))
  
  if(x==1) {
    newmodel.accuracy <- acc}
  else{
    newmodel.accuracy <- rbind(newmodel.accuracy, acc)
  }
}
print("Average accuracies of logreg model on train35 and test35 data (respectively):")
print(colMeans(newmodel.accuracy))

# 4b changes in convergence criteria
max.iter.variation <- c(5, 10, 15,20, 25, 30)

for (iter in max.iter.variation){
  xdata_3_5 <- as.matrix(train_3_5)
  theta_3_5 <- create.random.theta(xdata_3_5)
  theta_3_5 <- gradient.descent(theta_3_5, xdata_3_5, ydata_3_5,  iterations= iter, threshold=10, decay = FALSE)
  
  cat("Iterations =", iter, "\n")
  cat("Accuracy train35: ", accuracy(xdata_3_5, ydata_3_5, theta_3_5), "\n")
  cat("Accuracy test35: ",accuracy(test_3_5, true_label_test_3_5 , theta_3_5), "\n")
}

# ten runs 80% sampling for maxiteration =30
for (x in seq(1,10,1)){
  print(x)
  
  xdata_3_5 <- as.matrix(train_3_5)
  theta_3_5 <- create.random.theta(xdata_3_5)
  theta_3_5 <- gradient.descent(theta_3_5, xdata_3_5, ydata_3_5,  iterations= 30, threshold=10, decay = FALSE, random80 = TRUE)
  
  acc <-c(accuracy(xdata_3_5, ydata_3_5, theta_3_5), 
          accuracy(test_3_5, true_label_test_3_5 , theta_3_5))
  
  if(x==1) {
    newmodel.b.accuracy <- acc}
  else{
    newmodel.b.accuracy <- rbind(newmodel.b.accuracy, acc)
  }
}

print("Average accuracies of logreg model on train35 and test35 data w/30 max iterations(respectively):")
print(colMeans(newmodel.b.accuracy))

# ten runs 80% sampling for maxiteration =30 and alpha=.1
for (x in seq(1,10,1)){
  print(x)
  
  xdata_3_5 <- as.matrix(train_3_5)
  theta_3_5 <- create.random.theta(xdata_3_5)
  theta_3_5 <- gradient.descent(theta_3_5, xdata_3_5, ydata_3_5,  iterations= 30, threshold=10, decay = FALSE, random80 = TRUE, alpha=.1
  )
  
  acc <-c(accuracy(xdata_3_5, ydata_3_5, theta_3_5), 
          accuracy(test_3_5, true_label_test_3_5 , theta_3_5))
  
  if(x==1) {
    newmodel.b.accuracy <- acc}
  else{
    newmodel.b.accuracy <- rbind(newmodel.b.accuracy, acc)
  }
}

print("Average accuracies of logreg model on train35 and test35 data w/30 max iterations and alpha=.1(respectively):")
print(colMeans(newmodel.b.accuracy))

# 5. Learning Curves ------------------------------------------------------

gradient.descent.randsamp <- function(theta, xdata, ydata, iterations=300, threshold=10, v=FALSE, decay=FALSE, random = 1, alpha=.2) {
  
  #best place to get random 80 sampling
  if (random!=1){
    sample.count <- ncol(xdata)
    sample.index <- sample(sample.count, sample.count*.8)
    xdata <-xdata[, sample.index]
    ydata <-ydata[, sample.index]
  }
  dim <- nrow(xdata)
  # alpha<- sqrt(dim)
  alpha<- alpha
  
  for (x in seq(1, iterations, 1)) {
    theta.x <- t(theta) %*% xdata
    
    # 1/exp(-yi <theta, xi>+1)
    # multiply by yi  * xij
    denom <- sigmoid.function(theta.x * ydata)
    
    # yi * xij
    n<-t(xdata) * c(ydata)
    numer<-t(n)
    
    theta.j <- t(t(numer)*c(denom))
    
    theta.j <- matrix(rowSums(theta.j), nrow = dim)
    if(v) cat("Iteration: ", x, "\n")
    if(v) cat("Values in theta.j greater than threshold: ", sum(abs(theta.j)>threshold), "\n")
    
    #break for convergence criteria
    if(x > 2) if(all(abs(theta.j) < threshold)) break 
    # alpha decay
    if(decay) alpha <- alpha * (1-(x/iterations))
    # if(decay) alpha <- alpha / (1 +(x/2))
    theta <- theta - alpha * theta.j
    if(v) print(theta)
  }
  return(theta)
}

# Average.acc.withsampling <- function (random, train_3_5, test_3_5, data_3_5 ){
#  
#   xdata_3_5 <- as.matrix(train_3_5)
#   theta_3_5 <- create.random.theta(xdata_3_5)
#   theta_3_5 <- gradient.descent.randsamp(theta_3_5, xdata_3_5, ydata_3_5,  iterations= 30, threshold=10, decay = FALSE, random = 1, alpha=.1
#   )
#   
#   cat("Accuracy train35: ", accuracy(xdata_3_5, ydata_3_5, theta_3_5), "\n")
#   cat("Accuracy test35: ",accuracy(test_3_5, true_label_test_3_5 , theta_3_5), "\n")
#   
#   
# }
# 
# Average.acc.withsampling(random=.8, xdata_0_1, test_0_1 , ydata_0_1)
average.acc.withsampling <- function(xtrain, xtest, ytrain, ytest, random){
  sumavg=0
  
  # iteration = 10 for real / 1 for test
  iteration = 1
  
  #max iteration = 10 for real / 1 for test
  max.iterations <- 10
  for (i in seq(1,iteration,1)) {
    xdata_3_5 <- as.matrix(xtrain)
    theta_3_5 <- create.random.theta(xdata_3_5)
    theta_3_5 <- gradient.descent.randsamp(theta_3_5, xdata_3_5, ytrain,  
                                           iterations= 10, threshold=max.iterations, decay = FALSE, random = random, alpha=.1
    )
    sumavg <- sumavg +accuracy(xtest, ytest , theta_3_5)
  }
  
  # 
  # cat("Accuracy train35: ", accuracy(xdata_3_5, ytrain, theta_3_5), "\n")
  # cat("Accuracy test35: ",accuracy(xtest, ytest , theta_3_5), "\n")
  return(sumavg/iteration)
}

get.avg.accuracy.record <- function(rate){
random.sample.rate<- rate
average.accuracy.for01 <- average.acc.withsampling(xtrain=train_0_1, xtest=test_0_1, ytrain = ydata_0_1, ytest =true_label_test_0_1,  random=random.sample.rate)
average.accuracy.for35 <-average.acc.withsampling(xtrain=train_3_5, xtest=test_3_5, ytrain = ydata_3_5, ytest =true_label_test_3_5,  random=random.sample.rate)
# print(average.accuracy.for01)
# print(average.accuracy.for35)
accuracy.record <- c(random.sample.rate, average.accuracy.for01, average.accuracy.for35)
return(accuracy.record)
}

# change to 1 for real / .05 for test
sample.ceiling <- .15
for(rate in seq(.05, sample.ceiling, .05 )){
  print(get.avg.accuracy.record(rate))
  }

