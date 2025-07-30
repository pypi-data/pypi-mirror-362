import rich_click as click
from novara.constants import __version__
from novara.utils import logger, test_ssh_connection
from novara.config import config
from novara.request import request
from novara.constants import SOCKET_FILE
from novara.commands.docker import forward_docker_socket, cleanup_docker_socket, docker
import requests
import time
import docker
import subprocess
import re
import os
import docker.errors

def get_latest_version():
    url = f"https://pypi.org/pypi/novara/json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        latest_version = data['info']['version']
        return latest_version
    else:
        raise Exception(f"Failed to fetch package information: {response.status_code}")

@click.command()
def info():
    logger.debug('fetching version of the cli from pypi...')
    latest_version = get_latest_version()

    logger.debug("check connectivity to the backend...")
    r = request.get("api/up")
    is_up = r.status_code == 200

    if is_up:
        logger.debug("time response of the backend...")
        start_time = time.time()
        r = request.get("api/up")
        time_elapsed = time.time() - start_time
    else:
        time_elapsed = None

    logger.debug('Testing ssh connection...')
    test_ssh_connection()

    logger.debug('Testing connection to docker daemon...')
    ssh = forward_docker_socket()

    time.sleep(0.5)

    docker_version_string = None
    docker_error = None
    try:
        # Set DOCKER_HOST to point to the forwarded socket
        os.environ["DOCKER_HOST"] = f'unix://{SOCKET_FILE}'
        result = subprocess.run(
            ["docker", "version", "--format", "{{.Server.Version}}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version_output = result.stdout.strip()
            # Try to get platform name as well
            platform_result = subprocess.run(
                ["docker", "version", "--format", "{{.Server.Platform.Name}}"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=5
            )
            platform_name = platform_result.stdout.strip() if platform_result.returncode == 0 else "Docker Engine"
            docker_version_string = f"{platform_name} {version_output}"
        else:
            raise Exception(result.stderr.strip())
    except Exception as e:
        docker_error = str(e)

    cleanup_docker_socket(ssh)

    # All logger.info calls at the end
    logger.info("=" * 40)
    logger.info(f"Novara CLI Version:      {__version__}")
    logger.info(f"Latest Available:        {latest_version}")
    if __version__ != latest_version:
        logger.warning(
            "You are using an older version of the CLI.\n"
            "Consider upgrading:\n"
            "    pip install --upgrade novara"
        )

    logger.info("-" * 40)
    logger.info(f"Backend Server:          {config.server_url}")
    logger.info(f"Author:                  {config.author}")
    if is_up and time_elapsed is not None:
        logger.info(f"Backend Status:          Reachable ({time_elapsed:.2f}s response)")
    else:
        logger.warning("Backend Status:          Unreachable")

    logger.info("-" * 40)
    if docker_version_string:
        logger.info(f"Docker Daemon:           {docker_version_string}")
    elif docker_error:
        logger.error(f"Docker Daemon:           Failed to connect ({docker_error})")
    logger.info("=" * 40)