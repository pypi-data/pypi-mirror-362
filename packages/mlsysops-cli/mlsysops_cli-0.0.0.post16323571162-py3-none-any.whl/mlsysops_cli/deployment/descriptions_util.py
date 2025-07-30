import os

import yaml
from jinja2 import Template, Environment, PackageLoader, select_autoescape


def render_template(template_file, context):
    """
    Renders a Jinja template with the provided context.
    """
    with open(template_file, 'r') as file:
        template = Template(file.read())
    return template.render(context)


def create_cluster_yaml(input_file, cluster_name, descriptions_path=""):
    """
    Generates the cluster-level YAML based on a template.
    """
    with open(input_file, 'r') as file:
        inventory = yaml.safe_load(file)

    # Extract data for the target cluster
    cluster = inventory['all']['children'].get(cluster_name, {})
    master_nodes = cluster.get('children', {}).get('master_nodes', {}).get('hosts', {})
    worker_nodes = cluster.get('children', {}).get('worker_nodes', {}).get('hosts', {})

    # Validate master nodes
    master_hostnames = list(master_nodes.keys())
    if not master_hostnames:
        raise ValueError(f"No master hostname found for cluster: {cluster_name}")

    # Update corrected cluster filename logic here
    cluster_yaml_filename = os.path.join(descriptions_path, f"{master_hostnames[0]}.yaml")

    # Create context for the cluster template
    cluster_context = {
        "cluster_name": master_hostnames[0],
        "nodes": list(worker_nodes.keys())
    }

    loader = PackageLoader("mlsysops_cli", "templates")
    env = Environment(
        loader=loader,
        autoescape=select_autoescape(enabled_extensions=("j2"))
    )

    # Load the template
    template = env.get_template("cluster.yaml.j2")

    # Render and write the cluster YAML
    cluster_yaml = template.render(cluster_context)
    with open(cluster_yaml_filename, 'w') as output_file:
        output_file.write(cluster_yaml)
    print(f"Cluster YAML written to {cluster_yaml_filename}")


def create_worker_node_yaml(input_file, cluster_name, descriptions_path=""):
    """
    Generates YAML files for each worker node based on a template.
    """
    with open(input_file, 'r') as file:
        inventory = yaml.safe_load(file)

    # Extract data for the target cluster
    cluster = inventory['all']['children'].get(cluster_name, {})
    master_nodes = cluster.get('children', {}).get('master_nodes', {}).get('hosts', {})
    worker_nodes = cluster.get('children', {}).get('worker_nodes', {}).get('hosts', {})

    # Validate master nodes
    master_hostnames = list(master_nodes.keys())
    if not master_hostnames:
        raise ValueError(f"No master node found for cluster: {cluster_name}")
    cluster_id = master_hostnames[0]

    # Define permitted actions
    permitted_actions = [
        "traffic_redirection",
        "acceleration",
        "cpu_frequency",
        "gpu_frequency",
        "change_container_cpu_set",
        "change_container_image"
    ]

    # Generate YAML for each worker node
    for worker_name, worker_object in worker_nodes.items():
        worker_context = {
            "node_name": worker_name,
            "cluster_id": cluster_id,
            "continuum_layer": worker_object['labels']['mlsysops.eu/continuumLayer'],
            "permitted_actions": permitted_actions
        }

        loader = PackageLoader("mlsysops_cli", "templates")
        env = Environment(
            loader=loader,
            autoescape=select_autoescape(enabled_extensions=("j2"))
        )

        # Load the template
        template = env.get_template("node.yaml.j2")
        worker_yaml = template.render(worker_context)
        worker_yaml_filename = os.path.join(descriptions_path, f"{worker_name}.yaml")
        with open(worker_yaml_filename, 'w') as output_file:
            output_file.write(worker_yaml)
        print(f"Worker YAML written to {worker_yaml_filename}")


def create_app_yaml(input_file):
    """
    Generates the application-level YAML with `cluster_id` and `server_placement_node`.
    """
    with open(input_file, 'r') as file:
        inventory = yaml.safe_load(file)

    management_cluster = inventory['all']['children'].get('management_cluster', {})
    management_nodes = management_cluster.get('hosts', {})

    all_nodes = list(management_nodes.keys())
    if not all_nodes:
        raise ValueError("No nodes found in the management cluster")

    cluster_id = all_nodes[0]  # First management node
    server_placement_node = all_nodes[0]  # Also the first node for placement

    app_context = {
        "cluster_id": cluster_id,
        "server_placement_node": server_placement_node
    }

    loader = PackageLoader("mlsysops_cli", "templates")
    env = Environment(
        loader=loader,
        autoescape=select_autoescape(enabled_extensions=("j2"))
    )

    # Load the template
    template = env.get_template("app.yaml.j2")

    app_yaml = template.render(app_context)
    app_yaml_filename = "mlsysops-test-app-description.yaml"
    with open(app_yaml_filename, 'w') as output_file:
        output_file.write(app_yaml)
    print(f"Application YAML written to {app_yaml_filename}")


def create_continuum_yaml(input_file, descriptions_path=""):
    """
    Generates the continuum-level YAML with `continuum_id` from the first host in management_cluster
    and adds cluster names based on all master nodes in other clusters.
    """
    with open(input_file, 'r') as file:
        inventory = yaml.safe_load(file)

    # Extract the continuum_id from the first host of management_cluster
    management_cluster = inventory['all']['children'].get('management_cluster', {})
    management_hosts = management_cluster.get('hosts', {})

    if not management_hosts:
        raise ValueError("No hosts found in the management cluster")

    # Use the first hostname under management_cluster as the continuum_id
    continuum_id = list(management_hosts.keys())[0]  # e.g., "mls-test-karmada"

    # Collect all cluster names from master_nodes across clusters
    cluster_hostnames = []
    for cluster_name, cluster_data in inventory['all']['children'].items():
        if "master_nodes" in cluster_data.get('children', {}):
            master_nodes = cluster_data['children']['master_nodes']['hosts']
            cluster_hostnames.extend(master_nodes.keys())

    # Create context for the continuum YAML
    continuum_context = {
        "continuum_id": continuum_id,
        "clusters": cluster_hostnames
    }

    loader = PackageLoader("mlsysops_cli", "templates")
    env = Environment(
        loader=loader,
        autoescape=select_autoescape(enabled_extensions=("j2"))
    )

    # Load the template
    template = env.get_template("continuum.yaml.j2")

    # Render and write the continuum YAML
    continuum_yaml_filename = os.path.join(descriptions_path, f"{continuum_id}.yaml")
    continuum_yaml_content = template.render(continuum_context)
    with open(continuum_yaml_filename, 'w') as output_file:
        output_file.write(continuum_yaml_content)
    print(f"Continuum YAML written to {continuum_yaml_filename}")