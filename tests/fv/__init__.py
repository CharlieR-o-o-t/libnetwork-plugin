import os
import sh
from sh import docker
from docker_host import DockerHost


def setup_package():
    """
    Sets up docker images and host containers for running the STs.
    """
    containers = docker.ps("-qa").split()
    for container in containers:
        DockerHost.delete_container(container)
    print "Host containers removed."

    # Pull and save each image, so we can use them inside the host containers.
    print sh.bash("./build_node.sh").stdout
    docker.save("--output", "calico-node.tar", "calico/node")
    if not os.path.isfile("busybox.tar"):
        docker.pull("busybox:latest")
        docker.save("--output", "busybox.tar", "busybox:latest")
    if not os.path.isfile("nsenter.tar"):
        docker.pull("jpetazzo/nsenter:latest")
        docker.save("--output", "nsenter.tar", "jpetazzo/nsenter:latest")
    if not os.path.isfile("etcd.tar"):
        docker.pull("quay.io/coreos/etcd:v2.0.10")
        docker.save("--output", "etcd.tar", "quay.io/coreos/etcd:v2.0.10")

    # Create the calicoctl binary here so it will be in the volume mounted on the hosts.
    print sh.bash("./create_binary.sh")
    print "Calicoctl binary created."

    host1 = DockerHost('host1')
    DockerHost('host2')
    host1.start_etcd()


def teardown_package():
    pass
