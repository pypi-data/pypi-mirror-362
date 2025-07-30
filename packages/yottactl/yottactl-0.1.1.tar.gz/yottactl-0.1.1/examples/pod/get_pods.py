#!/usr/bin/env python

import logging

from examples.utils.prepare_env import get_api_key
from yotta.error import ClientError
from yotta.lib.utils import config_logging, none_to_zero
from yotta.pod import PodApi


def format_size(size_in_gb):
    """Format size to appropriate unit"""
    if size_in_gb >= 1024:
        return f"{size_in_gb / 1024:.1f} TB"
    return f"{size_in_gb} GB"


def format_network_speed(speed_mbps):
    """Format network speed to appropriate unit"""
    if float(speed_mbps) >= 1000:
        return f"{float(speed_mbps) / 1000:.1f} Gbps"
    return f"{speed_mbps} Mbps"


def display_pod_summary(pod):
    """Display a single line summary of pod information"""
    # Format status indicator
    status_symbols = {
        0: "⚪",  # Unknown/Initial
        1: "🟢",  # Running
        2: "🟡",  # Warning
        3: "🔴",  # Error
        4: "⚫",  # Stopped
    }
    status_indicator = status_symbols.get(pod['status'], "⚪")

    # Format the line
    logging.info(
        f"{status_indicator} {pod['id']:10} | "
        f"{pod['podName'][:20]:<20} | "
        f"{pod['gpuType'][:15]:<15} x{pod['gpuCount']:<2}"
    )


def display_pods_list(pods):
    """Display a list of pods in a table format"""
    if not pods:
        logging.info("No pods found.")
        return

    # Print header
    logging.info("\nPods List:")
    logging.info("=" * 100)
    logging.info(
        "  ID                  | Name                 | GPU Type"
    )
    logging.info("-" * 100)

    # Sort pods by creation time (newest first)
    sorted_pods = sorted(pods, key=lambda x: x['createdAt'], reverse=True)

    # Print each pod's information
    for pod in sorted_pods:
        display_pod_summary(pod)

    # Print footer with summary
    logging.info("-" * 100)
    logging.info(f"Total Pods: {len(pods)}")

    # Calculate some statistics
    active_pods = sum(1 for pod in pods if pod['status'] == 'RUNNING')  # Assuming 1 is "Running"
    total_gpus = sum(none_to_zero(pod['gpuCount'], 'gpuCount') for pod in pods)

    logging.info(f"Active Pods: {active_pods}")
    logging.info(f"Total GPUs: {total_gpus}")


def main():
    # Configure logging to show debug information
    config_logging(logging, logging.DEBUG)

    # Get API key from environment
    api_key = get_api_key()

    # Initialize client with test environment
    client = PodApi(api_key, base_url="https://api.dev.yottalabs.ai", debug=True)

    try:
        # Get all pods
        response = client.get_pods()

        # Check response
        if response['code'] == 10000:
            logging.info(f"Successfully retrieved pods list")
            logging.info(f"Response message: {response['message']}")

            # Display pods list in a table format
            display_pods_list(response['data'])
        else:
            logging.warning(f"Unexpected response code: {response['code']}")
            logging.warning(f"Response message: {response['message']}")

    except ClientError as error:
        # Handle client-side errors (4XX status codes)
        logging.error(
            "Client error occurred. Status: %s, Error code: %s, Message: %s",
            error.status_code, error.error_code, error.error_message
        )
    except Exception as error:
        # Handle other unexpected errors
        logging.error("An unexpected error occurred: %s", str(error))


if __name__ == "__main__":
    main()
