from kubernetes import client, config


class Container:
    def __init__(self, name, image, container_port, host_port):
        self.name = name
        self.image = image
        self.container_port = container_port
        self.host_port = host_port


def list_all_pods():
    config.load_kube_config()

    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))


def create_deployment_object(container: Container, label: str):
    # Configure Pod template container
    container = client.V1Container(
        name=container.name,
        image=container.image,
        ports=[client.V1ContainerPort(container_port=container.container_port, host_port=container.host_port)],
        # resources=client.V1ResourceRequirements(
        #     requests={"cpu": "100m", "memory": "200Mi"},
        #     limits={"cpu": "500m", "memory": "500Mi"},
        # ),
    )

    # Create and configure a spec section
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": label}),
        spec=client.V1PodSpec(containers=[container]),
    )

    # Create the specification of deployment
    spec = client.V1DeploymentSpec(
        replicas=1, template=template, selector={
            "matchLabels":
                {"app": label}})

    # Instantiate the deployment object
    deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name=label+"-deployment"),
        spec=spec,
    )

    return deployment


def create_deployment(api, deployment):
    # Create deployment
    resp = api.create_namespaced_deployment(
        body=deployment, namespace="default"
    )

    print("\n[INFO] deployment created.\n")
    print("%s\t%s\t\t\t%s\t%s\t%s" % ("NAMESPACE", "NAME", "REVISION", "IMAGE", 'PORTS'))
    print(
        "%s\t\t%s\t%s\t\t%s\t\t%s\n"
        % (
            resp.metadata.namespace,
            resp.metadata.name,
            resp.metadata.generation,
            resp.spec.template.spec.containers[0].image,
            resp.spec.template.spec.containers[0].ports,
        )
    )


def delete_deployment(api, deployment_name: str):
    # Delete deployment
    resp = api.delete_namespaced_deployment(
        name=deployment_name,
        namespace="default",
        body=client.V1DeleteOptions(
            propagation_policy="Foreground", grace_period_seconds=5
        ),
    )
    print("\n[INFO] deployment deleted.")
