#%%
import tensorflow as tf
import numpy as np
import os
import json
import argparse
from tensorflow.distribute.cluster_resolver import TFConfigClusterResolver

def main(**argv):
  worker_addr = ['worker{}:{}'.format(i,8101+i) for i in range(argv['numworkers'])]

  dict_tfconfig = {
  'cluster':{
      'worker':worker_addr
  },
  'task': {'type':'worker', 'index':argv['workerid']}
  }

  os.environ['TF_CONFIG'] = json.dumps(dict_tfconfig)
  
  print(os.environ['TF_CONFIG'])

  strategy = tf.distribute.experimental.MultiWorkerMirroredStrategy(tf.distribute.experimental.CollectiveCommunication.RING)

  #resolver = TFConfigClusterResolver()
  #cluster = resolver.cluster_spec()
  #print(cluster)
  #server = tf.distribute.Server(cluster, job_name="worker", task_index=argv['workerid'])

  print('num replicas', strategy.num_replicas_in_sync)

  def get_dataset(batchsize):
    mnist = tf.keras.datasets.mnist
    (x_train, y_train),(x_test, y_test) = mnist.load_data()
    x_train, x_test = x_train / 255.0, x_test/255.0

    dataset = tf.data.Dataset.from_tensor_slices((x_train, y_train)).shuffle(len(x_train)).repeat().batch(batchsize)
    return dataset, (x_test, y_test)

  def get_model():
    model = tf.keras.models.Sequential([
      tf.keras.layers.Flatten(input_shape=(28, 28)),
      tf.keras.layers.Dense(128, activation='relu'),
      tf.keras.layers.Dropout(0.2),
      tf.keras.layers.Dense(10, activation='softmax')
    ])
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    return model


  callbacks = [tf.keras.callbacks.ModelCheckpoint(filepath='/tmp/mnist_ckpt')]

  num_workers = argv['numworkers']
  per_worker_batch_size = 64

  global_batch_size = per_worker_batch_size * num_workers

  multi_worker_dataset = get_dataset(global_batch_size)

  with strategy.scope():
      multi_worker_model = get_model()

  multi_worker_model.fit(multi_worker_dataset[0], epochs=5, steps_per_epoch=128, callbacks=callbacks)

if __name__=="__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--workerid", '-w', type=int, default=0)
  parser.add_argument('--numworkers', '-n', type=int, default=3)

  args = parser.parse_args()
  main(**args.__dict__)
