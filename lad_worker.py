from kubernetes import client, config
from common.utils import get_random_port
from common.k8s import *

if __name__ == "__main__":

    container_name = "lad-worker-test"
    container_image = "wbq1995/lad_hello_world"
    container_port = 7860
    host_port = get_random_port()
    container = Container(container_name, container_image, container_port, host_port)
    deployment_label = "lad-worker"

    config.load_kube_config()
    apps_v1 = client.AppsV1Api()
    deployment = create_deployment_object(container, deployment_label)
    create_deployment(apps_v1, deployment)



