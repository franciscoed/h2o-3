import h2o
from h2o.automl import H2OAutoML

# https://docs.h2o.ai/h2o/latest-stable/h2o-py/docs/modeling.html#h2oautoml
h2o.init(ip="192.168.1.65")

abev = h2o.import_file("/tmp/ABEV3.csv")
# abev.describe()
# train, test = abev.split_frame(ratios=[0.75])

train = h2o.import_file("/tmp/train.csv")
test = h2o.import_file("/tmp/test.csv")

print(train)
print(test)

y = "shift"
x = list(train.columns)
x.remove(y)


# aml = H2OAutoML(max_runtime_secs=120)

aml = H2OAutoML(max_runtime_secs=15)
aml.train(x=x, y=y, training_frame=train)

# print(aml.leaderboard)
perf = aml.leader.model_performance(test)
# print(aml.predict(test))
df = aml.leader.predict(test)

print(df.as_data_frame())
print(test.as_data_frame())
