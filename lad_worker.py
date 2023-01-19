from kubernetes import client, config, dynamic
from kubernetes.client import api_client


def list_all_pods():
    config.load_kube_config()

    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))


def create_deployment_object():
    # Configureate Pod template container
    container = client.V1Container(
        name="lad-worker",
        image="wbq1995/lad_hello_world",
        ports=[client.V1ContainerPort(container_port=7860, host_port=17860)],
        # resources=client.V1ResourceRequirements(
        #     requests={"cpu": "100m", "memory": "200Mi"},
        #     limits={"cpu": "500m", "memory": "500Mi"},
        # ),
    )

    # Create and configure a spec section
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": "lad-worker"}),
        spec=client.V1PodSpec(containers=[container]),
    )

    # Create the specification of deployment
    spec = client.V1DeploymentSpec(
        replicas=1, template=template, selector={
            "matchLabels":
                {"app": "lad-worker"}})

    # Instantiate the deployment object
    deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name="lad-worker-deployment"),
        spec=spec,
    )

    return deployment


def create_deployment(api, deployment):
    # Create deployement
    resp = api.create_namespaced_deployment(
        body=deployment, namespace="default"
    )

    print("\n[INFO] deployment `lad-worker-deployment` created.\n")
    print("%s\t%s\t\t\t%s\t%s" % ("NAMESPACE", "NAME", "REVISION", "IMAGE"))
    print(
        "%s\t\t%s\t%s\t\t%s\n"
        % (
            resp.metadata.namespace,
            resp.metadata.name,
            resp.metadata.generation,
            resp.spec.template.spec.containers[0].image,
        )
    )


if __name__ == "__main__":
    config.load_kube_config()
    apps_v1 = client.AppsV1Api()
    deployment = create_deployment_object()
    create_deployment(apps_v1, deployment)
