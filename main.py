from pyspark.sql.types import StructField, StructType, StringType, IntegerType
from corpus_reader import corpus_reader
from pyspark import SparkConf, SparkContext
from pyspark.ml.feature import HashingTF, IDF, Tokenizer
from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.classification import NaiveBayes
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from time import time

if __name__ == '__main__':

    s_time = time()
    print("Başladı...")

    c_reader = corpus_reader(_isytu=False)
    corpus, category_dict = c_reader.get_corpus(_iscache=False)

    print("Corpus okundu... Time : ", time() - s_time)

    conf = SparkConf().setAppName("news_classification").setMaster("local[20]")
    spark = SparkSession.builder.config(conf=conf).getOrCreate()

    schema = StructType([
                StructField("News", StringType(), True),
                StructField("label", IntegerType(), True)
             ])

    df = spark.createDataFrame(data=corpus, schema=schema)

    print("DataFrame oluşturuldu.... Time : ", time() - s_time)

    df.cache()

    tokenizer = Tokenizer(inputCol="News", outputCol="words")
    hashingTF = HashingTF(inputCol=tokenizer.getOutputCol(), outputCol="rawFeatures")
    idf = IDF(inputCol=hashingTF.getOutputCol(), outputCol="features")

    # Naive Bayes Model
    nb = NaiveBayes()

    pipeline = Pipeline(stages=[tokenizer, hashingTF, idf, nb])

    # compute accuracy on the test set
    evaluator = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction",
                                                  metricName="accuracy")



    fold_cv = 10
    accuracy_sum = 0
    accuracy_list = []

    for fold in range(fold_cv):
        train, test = df.randomSplit([0.9, 0.1])

        pipelineModel = pipeline.fit(train)
        predict = pipelineModel.transform(test)

        accuracy = evaluator.evaluate(predict)
        accuracy_sum += accuracy
        #print(str(fold) + " Test set accuracy = " + str(accuracy))
        accuracy_list.append(accuracy)


    for acc in range(len(accuracy_list)):
        print(str(acc)," fold test accuracy : ", accuracy_list[acc])


    print()
    print()
    print("Mean Accuracy : ", str(accuracy_sum/fold_cv))
    print("Tamamlandı.. Time : ", time() - s_time)