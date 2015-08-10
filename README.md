# Email-Spam-Classifier
Classify emails as spam or not spam by learning on a training set of emails and applying model on test data
Index the documents with ElasticSearch and used Jsoup library to clean the html into plain test first
Partition the spam data set into TRAIN 80% and TEST 20%, with roughly a third ham and two thirds spam; similar distribution in TRAIN and TEST sets
Using LibLinear linear regression, trained the set and applied the model to test set of emails, gaining an accuracy of 99.6%
