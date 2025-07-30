"""
Command-line interface for k8s-helper
"""

import typer
from typing import Optional, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
import time
import time

from .core import K8sClient
from .config import get_config
from .utils import (
    format_pod_list,
    format_deployment_list,
    format_service_list,
    format_events,
    format_yaml_output,
    format_json_output,
    validate_name,
    validate_image,
    parse_env_vars,
    parse_labels,
    format_age
)
from . import __version__

def version_callback(value: bool):
    """Version callback for the CLI"""
    if value:
        typer.echo(f"k8s-helper-cli version {__version__}")
        raise typer.Exit()

app = typer.Typer(help="k8s-helper: Simplified Kubernetes operations")
console = Console()

@app.callback()
def main(
    version: Optional[bool] = typer.Option(None, "--version", callback=version_callback, is_eager=True, help="Show version and exit")
):
    """Main callback to handle global options"""
    return

# Global options
namespace_option = typer.Option(None, "--namespace", "-n", help="Kubernetes namespace")
output_option = typer.Option("table", "--output", "-o", help="Output format: table, yaml, json")


@app.command()
def config(
    namespace: Optional[str] = typer.Option(None, help="Set default namespace"),
    output_format: Optional[str] = typer.Option(None, help="Set output format"),
    timeout: Optional[int] = typer.Option(None, help="Set default timeout"),
    verbose: Optional[bool] = typer.Option(None, help="Enable verbose output"),
    show: bool = typer.Option(False, "--show", help="Show current configuration")
):
    """Configure k8s-helper settings"""
    config_obj = get_config()
    
    if show:
        console.print(Panel(format_yaml_output(config_obj.to_dict()), title="Current Configuration"))
        return
    
    if namespace:
        config_obj.set_namespace(namespace)
        console.print(f"✅ Default namespace set to: {namespace}")
    
    if output_format:
        try:
            config_obj.set_output_format(output_format)
            console.print(f"✅ Output format set to: {output_format}")
        except ValueError as e:
            console.print(f"❌ {e}")
            return
    
    if timeout:
        config_obj.set_timeout(timeout)
        console.print(f"✅ Timeout set to: {timeout} seconds")
    
    if verbose is not None:
        config_obj.set_verbose(verbose)
        console.print(f"✅ Verbose mode: {'enabled' if verbose else 'disabled'}")
    
    if any([namespace, output_format, timeout, verbose is not None]):
        config_obj.save_config()
        console.print("✅ Configuration saved")


@app.command()
def create_deployment(
    name: str = typer.Argument(..., help="Deployment name"),
    image: str = typer.Argument(..., help="Container image"),
    replicas: int = typer.Option(1, "--replicas", "-r", help="Number of replicas"),
    port: int = typer.Option(80, "--port", "-p", help="Container port"),
    env: Optional[str] = typer.Option(None, "--env", "-e", help="Environment variables (KEY1=value1,KEY2=value2)"),
    labels: Optional[str] = typer.Option(None, "--labels", "-l", help="Labels (key1=value1,key2=value2)"),
    namespace: Optional[str] = namespace_option,
    wait: bool = typer.Option(False, "--wait", help="Wait for deployment to be ready")
):
    """Create a new deployment"""
    if not validate_name(name):
        console.print(f"❌ Invalid deployment name: {name}")
        return
    
    if not validate_image(image):
        console.print(f"❌ Invalid image name: {image}")
        return
    
    # Parse environment variables and labels
    env_vars = parse_env_vars(env) if env else None
    label_dict = parse_labels(labels) if labels else None
    
    # Get client
    ns = namespace or get_config().get_namespace()
    client = K8sClient(namespace=ns)
    
    # Create deployment
    with console.status(f"Creating deployment {name}..."):
        result = client.create_deployment(
            name=name,
            image=image,
            replicas=replicas,
            container_port=port,
            env_vars=env_vars,
            labels=label_dict
        )
    
    if result:
        console.print(f"✅ Deployment {name} created successfully")
        
        if wait:
            with console.status(f"Waiting for deployment {name} to be ready..."):
                if client.wait_for_deployment_ready(name):
                    console.print(f"✅ Deployment {name} is ready")
                else:
                    console.print(f"❌ Deployment {name} failed to become ready")
    else:
        console.print(f"❌ Failed to create deployment {name}")


@app.command()
def delete_deployment(
    name: str = typer.Argument(..., help="Deployment name"),
    namespace: Optional[str] = namespace_option
):
    """Delete a deployment"""
    ns = namespace or get_config().get_namespace()
    client = K8sClient(namespace=ns)
    
    if typer.confirm(f"Are you sure you want to delete deployment {name}?"):
        with console.status(f"Deleting deployment {name}..."):
            if client.delete_deployment(name):
                console.print(f"✅ Deployment {name} deleted successfully")
            else:
                console.print(f"❌ Failed to delete deployment {name}")


@app.command()
def scale_deployment(
    name: str = typer.Argument(..., help="Deployment name"),
    replicas: int = typer.Argument(..., help="Number of replicas"),
    namespace: Optional[str] = namespace_option
):
    """Scale a deployment"""
    ns = namespace or get_config().get_namespace()
    client = K8sClient(namespace=ns)
    
    with console.status(f"Scaling deployment {name} to {replicas} replicas..."):
        if client.scale_deployment(name, replicas):
            console.print(f"✅ Deployment {name} scaled to {replicas} replicas")
        else:
            console.print(f"❌ Failed to scale deployment {name}")


@app.command()
def list_deployments(
    namespace: Optional[str] = namespace_option,
    output: str = output_option
):
    """List deployments"""
    ns = namespace or get_config().get_namespace()
    client = K8sClient(namespace=ns)
    
    deployments = client.list_deployments()
    
    if output == "table":
        console.print(format_deployment_list(deployments))
    elif output == "yaml":
        console.print(format_yaml_output(deployments))
    elif output == "json":
        console.print(format_json_output(deployments))


@app.command()
def create_pod(
    name: str = typer.Argument(..., help="Pod name"),
    image: str = typer.Argument(..., help="Container image"),
    port: int = typer.Option(80, "--port", "-p", help="Container port"),
    env: Optional[str] = typer.Option(None, "--env", "-e", help="Environment variables"),
    labels: Optional[str] = typer.Option(None, "--labels", "-l", help="Labels"),
    namespace: Optional[str] = namespace_option
):
    """Create a new pod"""
    if not validate_name(name):
        console.print(f"❌ Invalid pod name: {name}")
        return
    
    if not validate_image(image):
        console.print(f"❌ Invalid image name: {image}")
        return
    
    env_vars = parse_env_vars(env) if env else None
    label_dict = parse_labels(labels) if labels else None
    
    ns = namespace or get_config().get_namespace()
    client = K8sClient(namespace=ns)
    
    with console.status(f"Creating pod {name}..."):
        result = client.create_pod(
            name=name,
            image=image,
            container_port=port,
            env_vars=env_vars,
            labels=label_dict
        )
    
    if result:
        console.print(f"✅ Pod {name} created successfully")
    else:
        console.print(f"❌ Failed to create pod {name}")


@app.command()
def delete_pod(
    name: str = typer.Argument(..., help="Pod name"),
    namespace: Optional[str] = namespace_option
):
    """Delete a pod"""
    ns = namespace or get_config().get_namespace()
    client = K8sClient(namespace=ns)
    
    if typer.confirm(f"Are you sure you want to delete pod {name}?"):
        with console.status(f"Deleting pod {name}..."):
            if client.delete_pod(name):
                console.print(f"✅ Pod {name} deleted successfully")
            else:
                console.print(f"❌ Failed to delete pod {name}")


@app.command()
def list_pods(
    namespace: Optional[str] = namespace_option,
    output: str = output_option
):
    """List pods"""
    ns = namespace or get_config().get_namespace()
    client = K8sClient(namespace=ns)
    
    pods = client.list_pods()
    
    if output == "table":
        console.print(format_pod_list(pods))
    elif output == "yaml":
        console.print(format_yaml_output(pods))
    elif output == "json":
        console.print(format_json_output(pods))


@app.command()
def create_service(
    name: str = typer.Argument(..., help="Service name"),
    port: int = typer.Argument(..., help="Service port"),
    target_port: Optional[int] = typer.Option(None, help="Target port (defaults to port)"),
    service_type: str = typer.Option("ClusterIP", help="Service type"),
    selector: Optional[str] = typer.Option(None, help="Selector labels"),
    namespace: Optional[str] = namespace_option
):
    """Create a new service"""
    if not validate_name(name):
        console.print(f"❌ Invalid service name: {name}")
        return
    
    if target_port is None:
        target_port = port
    
    selector_dict = parse_labels(selector) if selector else None
    
    ns = namespace or get_config().get_namespace()
    client = K8sClient(namespace=ns)
    
    with console.status(f"Creating service {name}..."):
        result = client.create_service(
            name=name,
            port=port,
            target_port=target_port,
            service_type=service_type,
            selector=selector_dict
        )
    
    if result:
        console.print(f"✅ Service {name} created successfully")
    else:
        console.print(f"❌ Failed to create service {name}")


@app.command()
def delete_service(
    name: str = typer.Argument(..., help="Service name"),
    namespace: Optional[str] = namespace_option
):
    """Delete a service"""
    ns = namespace or get_config().get_namespace()
    client = K8sClient(namespace=ns)
    
    if typer.confirm(f"Are you sure you want to delete service {name}?"):
        with console.status(f"Deleting service {name}..."):
            if client.delete_service(name):
                console.print(f"✅ Service {name} deleted successfully")
            else:
                console.print(f"❌ Failed to delete service {name}")


@app.command()
def list_services(
    namespace: Optional[str] = namespace_option,
    output: str = output_option
):
    """List services"""
    ns = namespace or get_config().get_namespace()
    client = K8sClient(namespace=ns)
    
    services = client.list_services()
    
    if output == "table":
        console.print(format_service_list(services))
    elif output == "yaml":
        console.print(format_yaml_output(services))
    elif output == "json":
        console.print(format_json_output(services))


@app.command()
def logs(
    pod_name: str = typer.Argument(..., help="Pod name"),
    container: Optional[str] = typer.Option(None, help="Container name"),
    tail: Optional[int] = typer.Option(None, help="Number of lines to tail"),
    namespace: Optional[str] = namespace_option
):
    """Get pod logs"""
    ns = namespace or get_config().get_namespace()
    client = K8sClient(namespace=ns)
    
    logs = client.get_logs(pod_name, container_name=container, tail_lines=tail)
    if logs:
        console.print(logs)
    else:
        console.print(f"❌ Failed to get logs for pod {pod_name}")


@app.command()
def events(
    resource: Optional[str] = typer.Option(None, help="Resource name to filter events"),
    namespace: Optional[str] = namespace_option,
    output: str = output_option
):
    """Get events"""
    ns = namespace or get_config().get_namespace()
    client = K8sClient(namespace=ns)
    
    events = client.get_events(resource_name=resource)
    
    if output == "table":
        console.print(format_events(events))
    elif output == "yaml":
        console.print(format_yaml_output(events))
    elif output == "json":
        console.print(format_json_output(events))


@app.command()
def describe(
    resource_type: str = typer.Argument(..., help="Resource type: pod, deployment, service"),
    name: str = typer.Argument(..., help="Resource name"),
    namespace: Optional[str] = namespace_option,
    output: str = output_option
):
    """Describe a resource"""
    ns = namespace or get_config().get_namespace()
    client = K8sClient(namespace=ns)
    
    if resource_type.lower() == "pod":
        info = client.describe_pod(name)
    elif resource_type.lower() == "deployment":
        info = client.describe_deployment(name)
    elif resource_type.lower() == "service":
        info = client.describe_service(name)
    else:
        console.print(f"❌ Unsupported resource type: {resource_type}")
        return
    
    if info:
        if output == "yaml":
            console.print(format_yaml_output(info))
        elif output == "json":
            console.print(format_json_output(info))
        else:
            console.print(format_yaml_output(info))  # Default to YAML for describe
    else:
        console.print(f"❌ Failed to describe {resource_type} {name}")


@app.command()
def status(
    namespace: Optional[str] = namespace_option
):
    """Show namespace status"""
    ns = namespace or get_config().get_namespace()
    client = K8sClient(namespace=ns)
    
    console.print(f"\n[bold]Namespace: {ns}[/bold]")
    
    # Get resource counts
    resources = client.get_namespace_resources()
    
    table = Table(title="Resource Summary")
    table.add_column("Resource", style="cyan")
    table.add_column("Count", style="magenta")
    
    for resource, count in resources.items():
        table.add_row(resource.capitalize(), str(count))
    
    console.print(table)
    
    # Show recent events
    events = client.get_events()
    if events:
        console.print(f"\n[bold]Recent Events (last 5):[/bold]")
        recent_events = events[:5]
        for event in recent_events:
            event_type = event['type']
            color = "green" if event_type == "Normal" else "red"
            console.print(f"[{color}]{event['type']}[/{color}] {event['reason']}: {event['message']}")


@app.command()
def apply(
    name: str = typer.Argument(..., help="Application name"),
    image: str = typer.Argument(..., help="Container image"),
    replicas: int = typer.Option(1, "--replicas", "-r", help="Number of replicas"),
    port: int = typer.Option(80, "--port", "-p", help="Container port"),
    service_type: str = typer.Option("ClusterIP", help="Service type"),
    env: Optional[str] = typer.Option(None, "--env", "-e", help="Environment variables"),
    labels: Optional[str] = typer.Option(None, "--labels", "-l", help="Labels"),
    init_container: Optional[str] = typer.Option(None, "--init-container", help="Init container (name:image:command)"),
    init_env: Optional[str] = typer.Option(None, "--init-env", help="Init container environment variables"),
    pvc: Optional[str] = typer.Option(None, "--pvc", help="PVC to mount (name:mount_path)"),
    secret: Optional[str] = typer.Option(None, "--secret", help="Secret to mount (name:mount_path)"),
    namespace: Optional[str] = namespace_option,
    wait: bool = typer.Option(True, "--wait/--no-wait", help="Wait for deployment to be ready"),
    show_url: bool = typer.Option(True, "--show-url/--no-show-url", help="Show service URL after deployment")
):
    """Deploy an application (deployment + service) with advanced features"""
    if not validate_name(name):
        console.print(f"❌ Invalid application name: {name}")
        return
    
    if not validate_image(image):
        console.print(f"❌ Invalid image name: {image}")
        return
    
    env_vars = parse_env_vars(env) if env else None
    label_dict = parse_labels(labels) if labels else None
    
    ns = namespace or get_config().get_namespace()
    client = K8sClient(namespace=ns)
    
    console.print(f"🚀 Deploying application: {name}")
    
    # Prepare init containers
    init_containers = []
    if init_container:
        try:
            parts = init_container.split(":")
            if len(parts) >= 2:
                init_name, init_image = parts[0], parts[1]
                init_command = parts[2].split(" ") if len(parts) > 2 else None
                
                init_env_vars = parse_env_vars(init_env) if init_env else None
                
                init_containers.append({
                    'name': init_name,
                    'image': init_image,
                    'command': init_command,
                    'env_vars': init_env_vars
                })
                
                console.print(f"🔧 Init container: {init_name} ({init_image})")
            else:
                console.print(f"❌ Invalid init container format: {init_container}")
                return
        except Exception as e:
            console.print(f"❌ Error parsing init container: {e}")
            return
    
    # Prepare volumes and volume mounts
    volumes = []
    volume_mounts = []
    
    if pvc:
        try:
            pvc_parts = pvc.split(":")
            if len(pvc_parts) == 2:
                pvc_name, mount_path = pvc_parts
                volumes.append({
                    'name': f"{pvc_name}-volume",
                    'type': 'pvc',
                    'claim_name': pvc_name
                })
                volume_mounts.append({
                    'name': f"{pvc_name}-volume",
                    'mount_path': mount_path
                })
                console.print(f"💾 PVC mount: {pvc_name} → {mount_path}")
            else:
                console.print(f"❌ Invalid PVC format: {pvc}")
                return
        except Exception as e:
            console.print(f"❌ Error parsing PVC: {e}")
            return
    
    if secret:
        try:
            secret_parts = secret.split(":")
            if len(secret_parts) == 2:
                secret_name, mount_path = secret_parts
                volumes.append({
                    'name': f"{secret_name}-volume",
                    'type': 'secret',
                    'secret_name': secret_name
                })
                volume_mounts.append({
                    'name': f"{secret_name}-volume",
                    'mount_path': mount_path
                })
                console.print(f"🔐 Secret mount: {secret_name} → {mount_path}")
            else:
                console.print(f"❌ Invalid secret format: {secret}")
                return
        except Exception as e:
            console.print(f"❌ Error parsing secret: {e}")
            return
    
    # Create deployment
    with console.status(f"Creating deployment {name}..."):
        deployment_result = client.create_deployment(
            name=name,
            image=image,
            replicas=replicas,
            container_port=port,
            env_vars=env_vars,
            labels=label_dict,
            init_containers=init_containers if init_containers else None,
            volume_mounts=volume_mounts if volume_mounts else None,
            volumes=volumes if volumes else None
        )
    
    if not deployment_result:
        console.print(f"❌ Failed to create deployment {name}")
        return
    
    # Create service
    with console.status(f"Creating service {name}-service..."):
        service_result = client.create_service(
            name=f"{name}-service",
            port=port,
            target_port=port,
            service_type=service_type,
            selector=label_dict or {"app": name}
        )
    
    if not service_result:
        console.print(f"❌ Failed to create service {name}-service")
        return
    
    console.print(f"✅ Application {name} deployed successfully")
    
    if wait:
        with console.status(f"Waiting for deployment {name} to be ready..."):
            if client.wait_for_deployment_ready(name):
                console.print(f"✅ Application {name} is ready")
            else:
                console.print(f"❌ Application {name} failed to become ready")
    
    # Show service URL if requested
    if show_url:
        console.print(f"\n🔗 Service URL Information:")
        
        # Wait a moment for service to be ready
        time.sleep(2)
        
        url_info = client.get_service_url(f"{name}-service", ns)
        if url_info:
            console.print(f"🔧 Service Type: {url_info['type']}")
            console.print(f"🖥️  Cluster IP: {url_info['cluster_ip']}")
            
            if url_info['type'] == 'LoadBalancer':
                if url_info.get('aws_elb'):
                    console.print(f"🌐 AWS ELB DNS: [green]{url_info['elb_dns_name']}[/green]")
                    console.print(f"🔗 External URL: [blue]{url_info['external_url']}[/blue]")
                elif url_info.get('external_url'):
                    console.print(f"🔗 External URL: [blue]{url_info['external_url']}[/blue]")
                else:
                    console.print(f"⏳ LoadBalancer provisioning... Use 'k8s-helper service-url {name}-service' to check status")
            
            elif url_info['type'] == 'NodePort':
                if url_info.get('external_url'):
                    console.print(f"🔗 NodePort URL: [blue]{url_info['external_url']}[/blue]")
            
            elif url_info['type'] == 'ClusterIP':
                console.print(f"💡 ClusterIP service - accessible within cluster at {url_info['cluster_ip']}:{port}")
        else:
            console.print("❌ Could not retrieve service URL information")


@app.command()
def cleanup(
    name: str = typer.Argument(..., help="Application name"),
    namespace: Optional[str] = namespace_option
):
    """Clean up an application (delete deployment + service)"""
    ns = namespace or get_config().get_namespace()
    client = K8sClient(namespace=ns)
    
    if typer.confirm(f"Are you sure you want to delete application {name} and its service?"):
        console.print(f"🧹 Cleaning up application: {name}")
        
        # Delete deployment
        with console.status(f"Deleting deployment {name}..."):
            deployment_deleted = client.delete_deployment(name)
        
        # Delete service
        with console.status(f"Deleting service {name}-service..."):
            service_deleted = client.delete_service(f"{name}-service")
        
        if deployment_deleted and service_deleted:
            console.print(f"✅ Application {name} cleaned up successfully")
        else:
            console.print(f"⚠️  Partial cleanup completed for application {name}")


# ======================
# EKS COMMANDS
# ======================
@app.command()
def create_eks_cluster(
    name: str = typer.Argument(..., help="Cluster name"),
    region: str = typer.Option("us-west-2", "--region", "-r", help="AWS region"),
    version: str = typer.Option("1.29", "--version", "-v", help="Kubernetes version"),
    node_group: str = typer.Option(None, "--node-group", help="Node group name"),
    instance_types: str = typer.Option("t3.medium", "--instance-types", help="EC2 instance types (comma-separated)"),
    min_size: int = typer.Option(1, "--min-size", help="Minimum number of nodes"),
    max_size: int = typer.Option(3, "--max-size", help="Maximum number of nodes"),
    desired_size: int = typer.Option(2, "--desired-size", help="Desired number of nodes"),
    wait: bool = typer.Option(True, "--wait/--no-wait", help="Wait for cluster to be ready"),
    create_nodegroup: bool = typer.Option(True, "--create-nodegroup/--no-nodegroup", help="Create node group automatically"),
    ami_type: str = typer.Option("AL2_x86_64", "--ami-type", help="AMI type for nodes"),
    capacity_type: str = typer.Option("ON_DEMAND", "--capacity-type", help="Capacity type: ON_DEMAND or SPOT")
):
    """Create an AWS EKS cluster"""
    if not validate_name(name):
        console.print(f"❌ Invalid cluster name: {name}")
        return
    
    try:
        from .core import EKSClient
        
        eks_client = EKSClient(region=region)
        
        # Parse instance types
        instance_type_list = [t.strip() for t in instance_types.split(",")]
        
        scaling_config = {
            "minSize": min_size,
            "maxSize": max_size,
            "desiredSize": desired_size
        }
        
        console.print(f"🚀 Creating EKS cluster: {name}")
        console.print(f"📍 Region: {region}")
        console.print(f"🎯 Version: {version}")
        console.print(f"💻 Instance types: {instance_type_list}")
        console.print(f"📊 Scaling: {min_size}-{max_size} nodes (desired: {desired_size})")
        console.print(f"🛠️  AMI Type: {ami_type}")
        console.print(f"⚡ Capacity Type: {capacity_type}")
        
        # Show what will be created
        console.print("\n🔧 EKS Resources to create:")
        console.print("   • IAM roles for cluster and node groups")
        console.print("   • VPC subnets in at least 2 availability zones")
        console.print("   • Security groups for cluster communication")
        console.print("   • EKS cluster control plane")
        if create_nodegroup:
            if node_group:
                console.print(f"   • Managed node group: {node_group}")
            else:
                console.print(f"   • Managed node group: {name}-nodegroup")
        else:
            console.print("   • ⚠️  No node group (cluster will have no worker nodes)")
        
        with console.status("Creating EKS cluster and required resources..."):
            cluster_info = eks_client.create_cluster(
                cluster_name=name,
                version=version,
                node_group_name=node_group,
                instance_types=instance_type_list,
                scaling_config=scaling_config,
                ami_type=ami_type,
                capacity_type=capacity_type,
                create_nodegroup=create_nodegroup,
                wait_for_cluster=wait
            )
        
        console.print(f"✅ EKS cluster creation initiated")
        console.print(f"📋 Cluster ARN: {cluster_info['cluster_arn']}")
        console.print(f"🕐 Created at: {cluster_info['created_at']}")
        
        if 'subnets' in cluster_info:
            console.print(f"🌐 Subnets: {cluster_info['subnets']}")
        
        # Show node group information
        if create_nodegroup:
            if 'nodegroup_info' in cluster_info:
                nodegroup_info = cluster_info['nodegroup_info']
                console.print(f"\n✅ Node group creation initiated")
                console.print(f"📋 Node group name: {nodegroup_info['nodegroup_name']}")
                console.print(f"📋 Node group ARN: {nodegroup_info['nodegroup_arn']}")
                console.print(f"💻 Instance types: {nodegroup_info['instance_types']}")
                console.print(f"📊 Scaling config: {nodegroup_info['scaling_config']}")
            elif 'nodegroup_error' in cluster_info:
                console.print(f"\n⚠️  Node group creation failed: {cluster_info['nodegroup_error']}")
                console.print(f"💡 You can create it manually later using: k8s-helper create-nodegroup {name}")
            elif 'node_group_name' in cluster_info:
                console.print(f"\n📋 Node group will be created: {cluster_info['node_group_name']}")
                console.print(f"💡 Create it after cluster is active: k8s-helper create-nodegroup {name}")
        
        if wait:
            console.print("⏳ Waiting for cluster to become active...")
            with console.status("Waiting for cluster to be ready..."):
                if eks_client.wait_for_cluster_active(name):
                    console.print("✅ EKS cluster is now active!")
                    
                    # Show cluster status
                    status = eks_client.get_cluster_status(name)
                    console.print(f"🔗 Endpoint: {status['endpoint']}")
                    
                    # If node group was created, wait for it too
                    if create_nodegroup and 'nodegroup_info' in cluster_info:
                        nodegroup_name = cluster_info['nodegroup_info']['nodegroup_name']
                        console.print(f"⏳ Waiting for node group {nodegroup_name} to become active...")
                        with console.status("Waiting for node group to be ready..."):
                            if eks_client.wait_for_nodegroup_active(name, nodegroup_name):
                                console.print("✅ Node group is now active!")
                                console.print("🎉 Cluster is ready with worker nodes!")
                            else:
                                console.print("❌ Timeout waiting for node group to become active")
                    elif create_nodegroup and not wait:
                        # Create node group now that cluster is active
                        nodegroup_name = cluster_info.get('node_group_name') or f"{name}-nodegroup"
                        console.print(f"🔧 Creating node group: {nodegroup_name}")
                        try:
                            with console.status("Creating node group..."):
                                nodegroup_info = eks_client.create_nodegroup(
                                    cluster_name=name,
                                    nodegroup_name=nodegroup_name,
                                    instance_types=instance_type_list,
                                    ami_type=ami_type,
                                    capacity_type=capacity_type,
                                    scaling_config=scaling_config
                                )
                            console.print(f"✅ Node group creation initiated: {nodegroup_name}")
                            console.print(f"📋 Node group ARN: {nodegroup_info['nodegroup_arn']}")
                            
                            console.print(f"⏳ Waiting for node group to become active...")
                            if eks_client.wait_for_nodegroup_active(name, nodegroup_name):
                                console.print("✅ Node group is now active!")
                                console.print("🎉 Cluster is ready with worker nodes!")
                            else:
                                console.print("❌ Timeout waiting for node group to become active")
                        except Exception as e:
                            console.print(f"❌ Failed to create node group: {e}")
                    
                    # Show next steps
                    console.print(f"\n🚀 Next steps:")
                    console.print(f"   1. Configure kubectl: aws eks update-kubeconfig --name {name} --region {region}")
                    if create_nodegroup:
                        console.print(f"   2. Verify nodes: kubectl get nodes")
                        console.print(f"   3. Verify connection: kubectl get svc")
                        console.print(f"   4. Deploy applications: k8s-helper apply <app-name> <image>")
                    else:
                        console.print(f"   2. Create node group: k8s-helper create-nodegroup {name}")
                        console.print(f"   3. Verify connection: kubectl get svc")
                        console.print(f"   4. Deploy applications: k8s-helper apply <app-name> <image>")
                else:
                    console.print("❌ Timeout waiting for cluster to become active")
        else:
            console.print(f"💡 Use 'aws eks update-kubeconfig --name {name} --region {region}' to configure kubectl")
    
    except Exception as e:
        error_message = str(e)
        console.print(f"❌ Failed to create EKS cluster: {error_message}")
        
        # Provide helpful guidance based on error type
        if "Need at least 2 subnets" in error_message:
            console.print("\n🛠️  Troubleshooting:")
            console.print("   • EKS requires subnets in at least 2 availability zones")
            console.print("   • Check your VPC configuration in the AWS Console")
            console.print("   • Ensure you have subnets in different AZs")
            console.print("   • The tool will attempt to create subnets if none exist")
        elif "credentials not found" in error_message:
            console.print("\n🛠️  Troubleshooting:")
            console.print("   • Configure AWS credentials: aws configure")
            console.print("   • Or set environment variables: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY")
            console.print("   • Ensure you have EKS permissions")
        elif "VPC" in error_message:
            console.print("\n🛠️  Troubleshooting:")
            console.print("   • Check your VPC configuration")
            console.print("   • Ensure you have a default VPC or create one")
            console.print("   • Verify subnet CIDR ranges don't overlap")

@app.command()
def create_nodegroup(
    cluster_name: str = typer.Argument(..., help="EKS cluster name"),
    nodegroup_name: str = typer.Argument(..., help="Node group name"),
    region: str = typer.Option("us-west-2", "--region", "-r", help="AWS region"),
    instance_types: str = typer.Option("t3.medium", "--instance-types", help="EC2 instance types (comma-separated)"),
    min_size: int = typer.Option(1, "--min-size", help="Minimum number of nodes"),
    max_size: int = typer.Option(3, "--max-size", help="Maximum number of nodes"),
    desired_size: int = typer.Option(2, "--desired-size", help="Desired number of nodes"),
    ami_type: str = typer.Option("AL2_x86_64", "--ami-type", help="AMI type for nodes"),
    capacity_type: str = typer.Option("ON_DEMAND", "--capacity-type", help="Capacity type: ON_DEMAND or SPOT"),
    wait: bool = typer.Option(True, "--wait/--no-wait", help="Wait for node group to be ready")
):
    """Create an EKS managed node group"""
    if not validate_name(cluster_name):
        console.print(f"❌ Invalid cluster name: {cluster_name}")
        return
    
    if not validate_name(nodegroup_name):
        console.print(f"❌ Invalid node group name: {nodegroup_name}")
        return
    
    try:
        from .core import EKSClient
        
        eks_client = EKSClient(region=region)
        
        # Parse instance types
        instance_type_list = [t.strip() for t in instance_types.split(",")]
        
        scaling_config = {
            "minSize": min_size,
            "maxSize": max_size,
            "desiredSize": desired_size
        }
        
        console.print(f"🚀 Creating node group: {nodegroup_name}")
        console.print(f"📋 For cluster: {cluster_name}")
        console.print(f"📍 Region: {region}")
        console.print(f"💻 Instance types: {instance_type_list}")
        console.print(f"📊 Scaling: {min_size}-{max_size} nodes (desired: {desired_size})")
        console.print(f"🛠️  AMI Type: {ami_type}")
        console.print(f"⚡ Capacity Type: {capacity_type}")
        
        # Check if cluster exists and is active
        try:
            cluster_status = eks_client.get_cluster_status(cluster_name)
            if cluster_status['status'] != 'ACTIVE':
                console.print(f"❌ Cluster {cluster_name} is not active (status: {cluster_status['status']})")
                console.print("💡 Wait for cluster to become active before creating node group")
                return
        except Exception as e:
            console.print(f"❌ Cluster {cluster_name} not found: {e}")
            return
        
        with console.status("Creating node group..."):
            nodegroup_info = eks_client.create_nodegroup(
                cluster_name=cluster_name,
                nodegroup_name=nodegroup_name,
                instance_types=instance_type_list,
                ami_type=ami_type,
                capacity_type=capacity_type,
                scaling_config=scaling_config
            )
        
        console.print(f"✅ Node group creation initiated")
        console.print(f"📋 Node group ARN: {nodegroup_info['nodegroup_arn']}")
        console.print(f"🕐 Created at: {nodegroup_info['created_at']}")
        console.print(f"💻 Instance types: {nodegroup_info['instance_types']}")
        console.print(f"📊 Scaling config: {nodegroup_info['scaling_config']}")
        
        if wait:
            console.print("⏳ Waiting for node group to become active...")
            with console.status("Waiting for node group to be ready..."):
                if eks_client.wait_for_nodegroup_active(cluster_name, nodegroup_name):
                    console.print("✅ Node group is now active!")
                    console.print("🎉 You can now deploy workloads!")
                    
                    # Show next steps
                    console.print(f"\n🚀 Next steps:")
                    console.print(f"   1. Verify nodes: kubectl get nodes")
                    console.print(f"   2. Deploy applications: k8s-helper apply <app-name> <image>")
                else:
                    console.print("❌ Timeout waiting for node group to become active")
        else:
            console.print(f"💡 Use 'kubectl get nodes' to check when nodes are ready")
    
    except Exception as e:
        error_message = str(e)
        console.print(f"❌ Failed to create node group: {error_message}")
        
        # Provide helpful guidance based on error type
        if "Node group role" in error_message:
            console.print("\n🛠️  Troubleshooting:")
            console.print("   • The tool will automatically create required IAM roles")
            console.print("   • Ensure you have IAM permissions to create roles")
            console.print("   • Check AWS IAM console for existing roles")
        elif "subnets" in error_message:
            console.print("\n🛠️  Troubleshooting:")
            console.print("   • Node groups require valid subnets")
            console.print("   • Ensure cluster subnets are properly configured")
            console.print("   • Check VPC and subnet configuration")

@app.command()
def list_nodegroups(
    cluster_name: str = typer.Argument(..., help="EKS cluster name"),
    region: str = typer.Option("us-west-2", "--region", "-r", help="AWS region"),
    output: str = output_option
):
    """List node groups for an EKS cluster"""
    if not validate_name(cluster_name):
        console.print(f"❌ Invalid cluster name: {cluster_name}")
        return
    
    try:
        from .core import EKSClient
        
        eks_client = EKSClient(region=region)
        
        with console.status("Fetching node groups..."):
            nodegroups = eks_client.list_nodegroups(cluster_name)
        
        if not nodegroups:
            console.print(f"📋 No node groups found for cluster: {cluster_name}")
            console.print(f"💡 Create one with: k8s-helper create-nodegroup {cluster_name} <nodegroup-name>")
            return
        
        if output == "table":
            table = Table(title=f"Node Groups for {cluster_name}")
            table.add_column("Name", style="cyan")
            table.add_column("Status", style="green")
            table.add_column("Instance Types", style="blue")
            table.add_column("Capacity Type", style="yellow")
            table.add_column("Scaling Config", style="magenta")
            table.add_column("Created", style="white")
            
            for ng in nodegroups:
                scaling = f"{ng['scaling_config']['minSize']}-{ng['scaling_config']['maxSize']} (desired: {ng['scaling_config']['desiredSize']})"
                table.add_row(
                    ng['name'],
                    ng['status'],
                    ', '.join(ng['instance_types']),
                    ng['capacity_type'],
                    scaling,
                    format_age(ng['created_at'])
                )
            
            console.print(table)
        elif output == "json":
            console.print(format_json_output(nodegroups))
        elif output == "yaml":
            console.print(format_yaml_output(nodegroups))
    
    except Exception as e:
        console.print(f"❌ Failed to list node groups: {e}")
# ======================
# SECRET COMMANDS
# ======================
@app.command()
def create_secret(
    name: str = typer.Argument(..., help="Secret name"),
    data: str = typer.Option(..., "--data", "-d", help="Secret data (key1=value1,key2=value2)"),
    secret_type: str = typer.Option("Opaque", "--type", "-t", help="Secret type"),
    namespace: Optional[str] = namespace_option
):
    """Create a Kubernetes secret"""
    if not validate_name(name):
        console.print(f"❌ Invalid secret name: {name}")
        return
    
    # Parse data
    try:
        data_dict = {}
        for pair in data.split(","):
            if "=" in pair:
                key, value = pair.split("=", 1)
                data_dict[key.strip()] = value.strip()
            else:
                console.print(f"❌ Invalid data format: {pair}")
                return
        
        if not data_dict:
            console.print("❌ No valid data provided")
            return
        
        ns = namespace or get_config().get_namespace()
        client = K8sClient(namespace=ns)
        
        with console.status(f"Creating secret {name}..."):
            result = client.create_secret(name, data_dict, secret_type, ns)
        
        if result:
            console.print(f"✅ Secret {name} created successfully")
            console.print(f"📋 Type: {secret_type}")
            console.print(f"🔑 Keys: {list(data_dict.keys())}")
        else:
            console.print(f"❌ Failed to create secret {name}")
    
    except Exception as e:
        console.print(f"❌ Error creating secret: {e}")


@app.command()
def list_secrets(
    namespace: Optional[str] = namespace_option,
    output: str = output_option
):
    """List secrets"""
    ns = namespace or get_config().get_namespace()
    client = K8sClient(namespace=ns)
    
    secrets = client.list_secrets(ns)
    
    if output == "table":
        table = Table(title=f"Secrets in {ns}")
        table.add_column("Name", style="cyan")
        table.add_column("Type", style="magenta")
        table.add_column("Keys", style="green")
        table.add_column("Age", style="blue")
        
        for secret in secrets:
            age = format_age(secret['created_at'])
            keys = ", ".join(secret['data_keys'])
            table.add_row(secret['name'], secret['type'], keys, age)
        
        console.print(table)
    elif output == "yaml":
        console.print(format_yaml_output(secrets))
    elif output == "json":
        console.print(format_json_output(secrets))


@app.command()
def delete_secret(
    name: str = typer.Argument(..., help="Secret name"),
    namespace: Optional[str] = namespace_option
):
    """Delete a secret"""
    ns = namespace or get_config().get_namespace()
    client = K8sClient(namespace=ns)
    
    if typer.confirm(f"Are you sure you want to delete secret {name}?"):
        with console.status(f"Deleting secret {name}..."):
            if client.delete_secret(name, ns):
                console.print(f"✅ Secret {name} deleted successfully")
            else:
                console.print(f"❌ Failed to delete secret {name}")


# ======================
# PVC COMMANDS
# ======================
@app.command()
def create_pvc(
    name: str = typer.Argument(..., help="PVC name"),
    size: str = typer.Argument(..., help="Storage size (e.g., 10Gi, 100Mi)"),
    access_modes: str = typer.Option("ReadWriteOnce", "--access-modes", "-a", help="Access modes (comma-separated)"),
    storage_class: Optional[str] = typer.Option(None, "--storage-class", "-s", help="Storage class"),
    namespace: Optional[str] = namespace_option
):
    """Create a Persistent Volume Claim"""
    if not validate_name(name):
        console.print(f"❌ Invalid PVC name: {name}")
        return
    
    # Parse access modes
    access_modes_list = [mode.strip() for mode in access_modes.split(",")]
    
    ns = namespace or get_config().get_namespace()
    client = K8sClient(namespace=ns)
    
    with console.status(f"Creating PVC {name}..."):
        result = client.create_pvc(
            name=name,
            size=size,
            access_modes=access_modes_list,
            storage_class=storage_class,
            namespace=ns
        )
    
    if result:
        console.print(f"✅ PVC {name} created successfully")
        console.print(f"💾 Size: {size}")
        console.print(f"🔐 Access modes: {access_modes_list}")
        if storage_class:
            console.print(f"📦 Storage class: {storage_class}")
    else:
        console.print(f"❌ Failed to create PVC {name}")


@app.command()
def list_pvcs(
    namespace: Optional[str] = namespace_option,
    output: str = output_option
):
    """List Persistent Volume Claims"""
    ns = namespace or get_config().get_namespace()
    client = K8sClient(namespace=ns)
    
    pvcs = client.list_pvcs(ns)
    
    if output == "table":
        table = Table(title=f"PVCs in {ns}")
        table.add_column("Name", style="cyan")
        table.add_column("Status", style="magenta")
        table.add_column("Volume", style="green")
        table.add_column("Size", style="blue")
        table.add_column("Access Modes", style="yellow")
        table.add_column("Storage Class", style="red")
        table.add_column("Age", style="blue")
        
        for pvc in pvcs:
            age = format_age(pvc['created_at'])
            status_color = "green" if pvc['status'] == 'Bound' else "yellow"
            table.add_row(
                pvc['name'],
                f"[{status_color}]{pvc['status']}[/{status_color}]",
                pvc['volume_name'] or "N/A",
                pvc['size'],
                ", ".join(pvc['access_modes']),
                pvc['storage_class'] or "N/A",
                age
            )
        
        console.print(table)
    elif output == "yaml":
        console.print(format_yaml_output(pvcs))
    elif output == "json":
        console.print(format_json_output(pvcs))


@app.command()
def delete_pvc(
    name: str = typer.Argument(..., help="PVC name"),
    namespace: Optional[str] = namespace_option
):
    """Delete a Persistent Volume Claim"""
    ns = namespace or get_config().get_namespace()
    client = K8sClient(namespace=ns)
    
    if typer.confirm(f"Are you sure you want to delete PVC {name}?"):
        with console.status(f"Deleting PVC {name}..."):
            if client.delete_pvc(name, ns):
                console.print(f"✅ PVC {name} deleted successfully")
            else:
                console.print(f"❌ Failed to delete PVC {name}")


# ======================
# SERVICE URL COMMAND
# ======================
@app.command()
def service_url(
    name: str = typer.Argument(..., help="Service name"),
    namespace: Optional[str] = namespace_option,
    watch: bool = typer.Option(False, "--watch", "-w", help="Watch for URL changes")
):
    """Get service URL including AWS ELB URLs"""
    ns = namespace or get_config().get_namespace()
    client = K8sClient(namespace=ns)
    
    def show_service_url():
        url_info = client.get_service_url(name, ns)
        if not url_info:
            console.print(f"❌ Service {name} not found")
            return False
        
        console.print(f"\n🔗 Service URL Information for [cyan]{name}[/cyan]")
        console.print(f"📍 Namespace: {url_info['namespace']}")
        console.print(f"🔧 Type: {url_info['type']}")
        console.print(f"🖥️  Cluster IP: {url_info['cluster_ip']}")
        
        # Show ports
        console.print("\n📋 Ports:")
        for port in url_info['ports']:
            console.print(f"  • {port['port']}/{port['protocol']} → {port['target_port']}")
        
        # Show external access
        if url_info['type'] == 'LoadBalancer':
            if url_info.get('aws_elb'):
                console.print(f"\n🌐 AWS ELB DNS: [green]{url_info['elb_dns_name']}[/green]")
                console.print(f"🔗 External URL: [blue]{url_info['external_url']}[/blue]")
            elif url_info.get('external_url'):
                console.print(f"\n🔗 External URL: [blue]{url_info['external_url']}[/blue]")
            elif url_info.get('status'):
                console.print(f"\n⏳ Status: {url_info['status']}")
        
        elif url_info['type'] == 'NodePort':
            if url_info.get('external_url'):
                console.print(f"\n🔗 NodePort URL: [blue]{url_info['external_url']}[/blue]")
                console.print(f"🖥️  Node IP: {url_info['node_ip']}")
                console.print(f"🚪 Node Port: {url_info['node_port']}")
        
        elif url_info['type'] == 'ClusterIP':
            console.print(f"\n💡 ClusterIP service - only accessible within cluster")
        
        return True
    
    if watch:
        console.print("👁️  Watching for service URL changes (Ctrl+C to stop)")
        try:
            while True:
                show_service_url()
                time.sleep(5)
        except KeyboardInterrupt:
            console.print("\n👋 Stopped watching")
    else:
        show_service_url()
