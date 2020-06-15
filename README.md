# Distributed TF learning
## Description
This is a simple example of utilizing distributed training with Tensorflow.
`tf.distribute.experimental.MultiWorkerMirroredStrategy` is used for synchronous training among all workers, and the connection among the workers is established via gRPC with `tf.distribute.experimental.CollectiveCommunication.RING`. Number of workers is preset to 3 for demonstration simplicity. Dataset sharding is automatically handled by the distribute API.

Since the training and distribution is handled within docker containers for each worker, a bridge network is required. After `build.sh` generates the docker container, it creates the shared network bridge - `sk_tfdistnetwork`.

Each container are given unique names (worker0,...) by `run.sh`, so that it is exposed to other containers. `TF_CONFIG` environment variables for each container are set correspondingly.

## Usage
```
git clone https://github.com/skmono/dist_mnistdemo.git
cd dist_mnistdemo
./build.sh
```
This builds and docker image and generates the network bridge.

Note: If sudo is required to run docker commands, run the scripts (`build.sh` and `run.sh` with sudo privileges.)

To test the distributed training, run the first worker with
```
./run.sh 0
```
and other workers in different terminals (2 more required) with
```
./run.sh 1
```
```
./run.sh 2
```
The designated names will be removed after training is complete.


