# ec2_mcp_server.py
import asyncio
import logging
from typing import Any, Sequence

import boto3
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.types import Resource, Tool, TextContent, ImageContent, EmbeddedResource
from pydantic import AnyUrl

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the MCP server
server = Server("aws-ec2-mcp")

# Initialize AWS EC2 client
ec2_client = boto3.client('ec2')


@server.list_resources()
async def handle_list_resources() -> list[Resource]:
    """
    List available AWS EC2 resources that the AI can access.
    This is like a table of contents for what data is available.
    """
    try:
        # Get EC2 instances
        instances_response = ec2_client.describe_instances()

        resources = []

        # Create resource entries for each instance
        for reservation in instances_response['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                instance_name = get_instance_name(instance)

                resources.append(Resource(
                    uri=AnyUrl(f"ec2://instance/{instance_id}"),
                    name=f"EC2 Instance: {instance_name} ({instance_id})",
                    description=f"EC2 instance {instance_id} - {instance.get('State', {}).get('Name', 'unknown')}",
                    mimeType="application/json"
                ))

        # Add VPC resources
        vpcs_response = ec2_client.describe_vpcs()
        for vpc in vpcs_response['Vpcs']:
            vpc_id = vpc['VpcId']
            resources.append(Resource(
                uri=AnyUrl(f"ec2://vpc/{vpc_id}"),
                name=f"VPC: {vpc_id}",
                description=f"Virtual Private Cloud {vpc_id}",
                mimeType="application/json"
            ))

        logger.info(f"Listed {len(resources)} EC2 resources")
        return resources

    except Exception as e:
        logger.error(f"Error listing resources: {e}")
        return []


def get_instance_name(instance):
    """Extract instance name from tags"""
    tags = instance.get('Tags', [])
    for tag in tags:
        if tag['Key'] == 'Name':
            return tag['Value']
    return 'Unnamed'


@server.read_resource()
async def handle_read_resource(uri: AnyUrl) -> str:
    """
    Read detailed information about a specific resource.
    This is like opening a file to see its contents.
    """
    try:
        uri_str = str(uri)
        logger.info(f"Reading resource: {uri_str}")

        if uri_str.startswith("ec2://instance/"):
            # Extract instance ID from URI
            instance_id = uri_str.split("/")[-1]
            return await get_instance_details(instance_id)

        elif uri_str.startswith("ec2://vpc/"):
            # Extract VPC ID from URI
            vpc_id = uri_str.split("/")[-1]
            return await get_vpc_details(vpc_id)

        else:
            return f"Unknown resource type: {uri_str}"

    except Exception as e:
        logger.error(f"Error reading resource {uri}: {e}")
        return f"Error reading resource: {e}"


async def get_instance_details(instance_id: str) -> str:
    """Get detailed information about an EC2 instance"""
    try:
        response = ec2_client.describe_instances(InstanceIds=[instance_id])

        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                # Format instance information in a readable way
                instance_info = {
                    'InstanceId': instance['InstanceId'],
                    'InstanceType': instance['InstanceType'],
                    'State': instance['State']['Name'],
                    'PublicIpAddress': instance.get('PublicIpAddress', 'N/A'),
                    'PrivateIpAddress': instance.get('PrivateIpAddress', 'N/A'),
                    'LaunchTime': instance['LaunchTime'].isoformat(),
                    'VpcId': instance.get('VpcId', 'N/A'),
                    'SubnetId': instance.get('SubnetId', 'N/A'),
                    'SecurityGroups': [sg['GroupName'] for sg in instance.get('SecurityGroups', [])],
                    'Tags': {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}
                }

                return f"EC2 Instance Details:\n{json.dumps(instance_info, indent=2, default=str)}"

        return f"Instance {instance_id} not found"

    except Exception as e:
        return f"Error getting instance details: {e}"


async def get_vpc_details(vpc_id: str) -> str:
    """Get detailed information about a VPC"""
    try:
        response = ec2_client.describe_vpcs(VpcIds=[vpc_id])

        if response['Vpcs']:
            vpc = response['Vpcs'][0]
            vpc_info = {
                'VpcId': vpc['VpcId'],
                'State': vpc['State'],
                'CidrBlock': vpc['CidrBlock'],
                'IsDefault': vpc['IsDefault'],
                'Tags': {tag['Key']: tag['Value'] for tag in vpc.get('Tags', [])}
            }

            return f"VPC Details:\n{json.dumps(vpc_info, indent=2)}"

        return f"VPC {vpc_id} not found"

    except Exception as e:
        return f"Error getting VPC details: {e}"
@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """
    List available tools (actions) that the AI can perform.
    These are like commands the AI can execute.
    """
    return [
        Tool(
            name="start_instance",
            description="Start an EC2 instance",
            inputSchema={
                "type": "object",
                "properties": {
                    "instance_id": {
                        "type": "string",
                        "description": "The EC2 instance ID to start"
                    }
                },
                "required": ["instance_id"]
            }
        ),
        Tool(
            name="stop_instance",
            description="Stop an EC2 instance",
            inputSchema={
                "type": "object",
                "properties": {
                    "instance_id": {
                        "type": "string",
                        "description": "The EC2 instance ID to stop"
                    }
                },
                "required": ["instance_id"]
            }
        ),
        Tool(
            name="get_instance_status",
            description="Get the current status and health of an EC2 instance",
            inputSchema={
                "type": "object",
                "properties": {
                    "instance_id": {
                        "type": "string",
                        "description": "The EC2 instance ID to check"
                    }
                },
                "required": ["instance_id"]
            }
        ),
        Tool(
            name="create_snapshot",
            description="Create a snapshot of an EC2 instance's EBS volumes",
            inputSchema={
                "type": "object",
                "properties": {
                    "instance_id": {
                        "type": "string",
                        "description": "The EC2 instance ID to snapshot"
                    },
                    "description": {
                        "type": "string",
                        "description": "Description for the snapshot",
                        "default": "Automated snapshot via MCP"
                    }
                },
                "required": ["instance_id"]
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[TextContent]:
    """
    Execute a tool (perform an action) based on the AI's request.
    This is like running a command with specific parameters.
    """
    try:
        if name == "start_instance":
            return await start_instance_tool(arguments or {})
        elif name == "stop_instance":
            return await stop_instance_tool(arguments or {})
        elif name == "get_instance_status":
            return await get_instance_status_tool(arguments or {})
        elif name == "create_snapshot":
            return await create_snapshot_tool(arguments or {})
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]

    except Exception as e:
        logger.error(f"Error executing tool {name}: {e}")
        return [TextContent(type="text", text=f"Error executing {name}: {e}")]


async def start_instance_tool(arguments: dict) -> list[TextContent]:
    """Start an EC2 instance"""
    instance_id = arguments.get("instance_id")
    if not instance_id:
        return [TextContent(type="text", text="Error: instance_id is required")]

    try:
        # Check current state first
        response = ec2_client.describe_instances(InstanceIds=[instance_id])
        current_state = response['Reservations'][0]['Instances'][0]['State']['Name']

        if current_state == 'running':
            return [TextContent(type="text", text=f"Instance {instance_id} is already running")]

        # Start the instance
        ec2_client.start_instances(InstanceIds=[instance_id])

        result = f"✅ Successfully initiated start for instance {instance_id}\n"
        result += f"Previous state: {current_state}\n"
        result += "Instance is starting up... This may take a few minutes."

        return [TextContent(type="text", text=result)]

    except Exception as e:
        return [TextContent(type="text", text=f"Failed to start instance {instance_id}: {e}")]


async def stop_instance_tool(arguments: dict) -> list[TextContent]:
    """Stop an EC2 instance"""
    instance_id = arguments.get("instance_id")
    if not instance_id:
        return [TextContent(type="text", text="Error: instance_id is required")]

    try:
        # Check current state first
        response = ec2_client.describe_instances(InstanceIds=[instance_id])
        current_state = response['Reservations'][0]['Instances'][0]['State']['Name']

        if current_state in ['stopped', 'stopping']:
            return [TextContent(type="text", text=f"Instance {instance_id} is already {current_state}")]

        # Stop the instance
        ec2_client.stop_instances(InstanceIds=[instance_id])

        result = f"✅ Successfully initiated stop for instance {instance_id}\n"
        result += f"Previous state: {current_state}\n"
        result += "Instance is shutting down... This may take a few minutes."

        return [TextContent(type="text", text=result)]

    except Exception as e:
        return [TextContent(type="text", text=f"Failed to stop instance {instance_id}: {e}")]


async def get_instance_status_tool(arguments: dict) -> list[TextContent]:
    """Get comprehensive status of an EC2 instance"""
    instance_id = arguments.get("instance_id")
    if not instance_id:
        return [TextContent(type="text", text="Error: instance_id is required")]

    try:
        # Get instance status
        status_response = ec2_client.describe_instance_status(
            InstanceIds=[instance_id],
            IncludeAllInstances=True
        )

        # Get instance details
        instances_response = ec2_client.describe_instances(InstanceIds=[instance_id])
        instance = instances_response['Reservations'][0]['Instances'][0]

        status_info = {
            'InstanceId': instance_id,
            'State': instance['State']['Name'],
            'InstanceType': instance['InstanceType'],
            'LaunchTime': instance['LaunchTime'].isoformat(),
            'Monitoring': instance.get('Monitoring', {}).get('State', 'N/A'),
        }

        # Add status checks if available
        if status_response['InstanceStatuses']:
            status = status_response['InstanceStatuses'][0]
            status_info.update({
                'SystemStatus': status['SystemStatus']['Status'],
                'InstanceStatus': status['InstanceStatus']['Status'],
                'SystemStatusDetails': [check['Status'] for check in status['SystemStatus']['Details']],
                'InstanceStatusDetails': [check['Status'] for check in status['InstanceStatus']['Details']]
            })

        result = f"📊 Instance Status Report for {instance_id}:\n"
        result += json.dumps(status_info, indent=2, default=str)

        return [TextContent(type="text", text=result)]

    except Exception as e:
        return [TextContent(type="text", text=f"Failed to get status for instance {instance_id}: {e}")]


async def create_snapshot_tool(arguments: dict) -> list[TextContent]:
    """Create snapshots of all EBS volumes attached to an instance"""
    instance_id = arguments.get("instance_id")
    description = arguments.get("description", "Automated snapshot via MCP")

    if not instance_id:
        return [TextContent(type="text", text="Error: instance_id is required")]

    try:
        # Get instance details to find attached volumes
        response = ec2_client.describe_instances(InstanceIds=[instance_id])
        instance = response['Reservations'][0]['Instances'][0]

        snapshots_created = []

        # Create snapshots for each attached volume
        for block_device in instance.get('BlockDeviceMappings', []):
            volume_id = block_device['Ebs']['VolumeId']
            device_name = block_device['DeviceName']

            snapshot_description = f"{description} - {instance_id} - {device_name}"

            snapshot_response = ec2_client.create_snapshot(
                VolumeId=volume_id,
                Description=snapshot_description
            )

            snapshots_created.append({
                'SnapshotId': snapshot_response['SnapshotId'],
                'VolumeId': volume_id,
                'DeviceName': device_name
            })

        result = f"📸 Successfully initiated snapshots for instance {instance_id}:\n"
        for snap in snapshots_created:
            result += f"  • {snap['DeviceName']} ({snap['VolumeId']}) → {snap['SnapshotId']}\n"
        result += "\n⏳ Snapshots are being created in the background..."

        return [TextContent(type="text", text=result)]

    except Exception as e:
        return [TextContent(type="text", text=f"Failed to create snapshots for instance {instance_id}: {e}")]


import json


async def main():
    """Main entry point for the MCP server"""
    # Import and add the missing import at the top
    from mcp.server.stdio import stdio_server

    try:
        logger.info("Starting AWS EC2 MCP Server...")

        # Run the server using stdio transport
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="aws-ec2-mcp",
                    server_version="1.0.0",
                    capabilities=server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={}
                    )
                )
            )

    except Exception as e:
        logger.error(f"Server error: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())