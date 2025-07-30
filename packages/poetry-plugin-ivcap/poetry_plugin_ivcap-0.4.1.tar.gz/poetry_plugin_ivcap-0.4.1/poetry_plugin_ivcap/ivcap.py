#
# Copyright (c) 2025 Commonwealth Scientific and Industrial Research Organisation (CSIRO). All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file. See the AUTHORS file for names of contributors.
#
import os
import re
import subprocess
import sys
import tempfile
import uuid
import humanize
import subprocess
import requests

from .constants import DEF_POLICY, PLUGIN_NAME, POLICY_OPT, SERVICE_FILE_OPT, SERVICE_ID_OPT

from .docker import docker_cfg, docker_build, docker_push
from .util import command_exists, get_name, string_to_number

def docker_publish(data, line):
    check_ivcap_cmd(line)
    dname = docker_build(data, line, arch="amd64")

    size_cmd = ["docker", "inspect", "--format='{{.Size}}'", dname]
    line(f"<debug>Running: {' '.join(size_cmd)} </debug>")
    size = string_to_number(subprocess.check_output(size_cmd).decode())
    if size is None:
        line("<error>Failed to retrieve image size</error>")
        return
    line(f"<info>INFO: Image size {humanize.naturalsize(size)}</info>")
    pkg_name = docker_push(dname, line)

def service_register(data, line):
    check_ivcap_cmd(line)
    config = data.get("tool", {}).get(PLUGIN_NAME, {})

    service = config.get(SERVICE_FILE_OPT)
    if not service:
        line(f"<error>Missing '{SERVICE_FILE_OPT}' in [tool.{PLUGIN_NAME}]</error>")
        return

    dcfg = docker_cfg(data, line, "amd64")
    pkg_cmd = ["ivcap", "package", "list", dcfg.docker_name]
    line(f"<debug>Running: {' '.join(pkg_cmd)} </debug>")
    pkg = subprocess.check_output(pkg_cmd).decode()
    if not pkg or pkg == "":
        line(f"<error>No package '{dcfg.docker_name}' found. Please build and publish it first.</error>")
        return
    service_id = get_service_id(data, False, line)

    cmd = ["poetry", "run", "python", service, "--print-service-description"]
    line(f"<debug>Running: {' '.join(cmd)} </debug>")
    svc = subprocess.check_output(cmd).decode()

    svc = svc.replace("#DOCKER_IMG#", pkg.strip())\
            .replace("#SERVICE_ID#", service_id)

    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp:
        tmp.write(svc)
        tmp_path = tmp.name  # Save the file name for subprocess

    try:
        policy = get_policy(data, line)
        up_cmd = ["ivcap", "aspect", "update", "--policy", policy, service_id, "-f", tmp_path]
        try:
            line(f"<debug>Running: {' '.join(up_cmd)} </debug>")
            jaid = subprocess.check_output(up_cmd).decode().strip()
            p = re.compile(r'.*(urn:[^"]*)')
            aid = p.search(jaid).group(1)
            line(f"<info>INFO: service definition successfully uploaded - {aid}</info>")
        except Exception as e:
            line(f"<error>ERROR: cannot upload service definitiion: {e}</error>")
            sys.exit(1)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

def tool_register(data, line):
    check_ivcap_cmd(line)
    config = data.get("tool", {}).get(PLUGIN_NAME, {})

    service = config.get("service-file")
    if not service:
        line(f"<error>Missing 'service-file' in [tool.{PLUGIN_NAME}]</error>")
        return

    cmd = ["poetry", "run", "python", service, "--print-tool-description"]
    line(f"<debug>Running: {' '.join(cmd)} </debug>")
    svc = subprocess.check_output(cmd).decode()

    service_id = get_service_id(data, False, line)
    svc = svc.replace("#SERVICE_ID#", service_id)

    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp:
        tmp.write(svc)
        tmp_path = tmp.name  # Save the file name for subprocess

    try:
        policy = get_policy(data, line)
        up_cmd = ["ivcap", "aspect", "update", "--policy", policy, service_id, "-f", tmp_path]
        try:
            line(f"<debug>Running: {' '.join(up_cmd)} </debug>")
            jaid = subprocess.check_output(up_cmd).decode().strip()
            p = re.compile(r'.*(urn:[^"]*)')
            aid = p.search(jaid).group(1)
            line(f"<info>INFO: tool description successfully uploaded - {aid}</info>")
        except Exception as e:
            line(f"<error>ERROR: cannot upload tool description: {e}</error>")
            sys.exit(1)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

def get_service_id(data, is_silent, line):
    service_id = data.get("tool", {}).get(PLUGIN_NAME, {}).get(SERVICE_ID_OPT)
    if not service_id:
        service_id = create_service_id(data, is_silent, line)
    return service_id

def create_service_id(data, is_silent, line):
    check_ivcap_cmd(line, is_silent)
    name = get_name(data)
    account_id = get_account_id(data, line, is_silent)
    id = uuid.uuid5(uuid.NAMESPACE_DNS, f"{name}{account_id}")
    return f"urn:ivcap:service:{id}"

def get_policy(data, line):
    policy = data.get("tool", {}).get(PLUGIN_NAME, {}).get(POLICY_OPT)
    if not policy:
        policy = DEF_POLICY
    return policy

def exec_job(data, args, is_silent, line):
    """
    Execute a job by posting a JSON request to the IVCAP API.

    Returns:
        requests.Response: The response object from the API call.
    """
    # Parse 'args' for run options
    if not isinstance(args, list) or len(args) < 1:
        raise Exception("args must be a list with at least one element")
    file_name = args[0]
    timeout = 20 # default timeout
    if len(args) == 1:
        pass  # only file_name provided
    elif len(args) == 3 and args[1] == '--timeout':
        try:
            timeout = int(args[2])
        except ValueError:
            raise Exception("Timeout value must be an integer")
    else:
        raise Exception("args must be [file_name] or [file_name, '--timeout', value]")

    # Get access token using ivcap CLI
    try:
        token = subprocess.check_output(
            ["ivcap", "--silent", "context", "get", "access-token", "--refresh-token"],
            text=True
        ).strip()
    except Exception as e:
        raise RuntimeError(f"Failed to get IVCAP access token: {e}")

   # Get IVCAP deployment URL
    try:
        ivcap_url = subprocess.check_output(
            ["ivcap", "--silent", "context", "get", "url"],
            text=True
        ).strip()
    except Exception as e:
        raise RuntimeError(f"Failed to get IVCAP deployment URL: {e}")

    # Read the JSON request file
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            json_data = f.read()
    except Exception as e:
        raise RuntimeError(f"Failed to read request file '{file_name}': {e}")

    # Prepare headers
    headers = {
        "content-type": "application/json",
        "Timeout": f"{timeout}",
        "Authorization": f"Bearer {token}"
    }

    # Build URL
    service_id = get_service_id(data, is_silent, line)
    url = f"{ivcap_url}/1/services2/{service_id}/jobs"
    params = {"with-result-content": "true"}

    # 5. POST request
    if not is_silent:
        line(f"<debug>Creating job '{url}'</debug>")
    try:
        response = requests.post(url, headers=headers, params=params, data=json_data)
    except Exception as e:
        raise RuntimeError(f"Job submission failed: {e}")

    # Handle response according to requirements
    import time
    import json

    def handle_response(resp):
        content_type = resp.headers.get("content-type", "")
        if resp.status_code >= 300:
            line(f"<warning>WARNING: Received status code {resp.status_code}</warning>")
            line(f"<info>Headers: {str(resp.headers)}</info>")
            line(f"<info>Body: {str(resp.text)}</info>")
        elif resp.status_code == 200:
            if "application/json" in content_type:
                try:
                    parsed = resp.json()
                    print(json.dumps(parsed, indent=2, sort_keys=True))
                except Exception as e:
                    line(f"<warning>Failed to parse JSON response: {e}</warning>")
                    line(f"<warning>Headers: {str(resp.headers)}</warning>")
            else:
                line(f"<info>Headers: {str(resp.headers)}</info>")
        else:
            line(f"<warning>Received status code {resp.status_code}</warning>")
            line(f"<warning>Headers: {str(resp.headers)}</warning>")

    if response.status_code == 202:
        try:
            payload = response.json()
            # use when ../output is fixed
            # location = f"{payload.get('location')}/output"
            location = f"{payload.get('location')}"
            job_id = payload.get("job-id")
            retry_later = payload.get("retry-later", 10)
            if not is_silent:
                line(f"<debug>Job '{job_id}' accepted, but no result yet. Polling in {retry_later} seconds.</debug>")
            while True:
                time.sleep(retry_later)
                poll_headers = {
                    "Authorization": f"Bearer {token}"
                }
                poll_resp = requests.get(location, headers=poll_headers)
                if poll_resp.status_code == 202:
                    try:
                        poll_payload = poll_resp.json()
                        location = poll_payload.get("location", location)
                        retry_later = poll_payload.get("retry-later", retry_later)
                        if not is_silent:
                            line(f"<debug>Still processing. Next poll in {retry_later} seconds.</debug>")
                    except Exception as e:
                        line(f"<error>Failed to parse polling response: {e}</error>")
                        break
                else:
                    handle_response(poll_resp)
                    break
        except Exception as e:
            line(f"<error>Failed to handle 202 response: {e}</error>")
    else:
        handle_response(response)

def get_account_id(data, line, is_silent=False):
    check_ivcap_cmd(line)
    cmd = ["ivcap", "context", "get", "account-id"]
    if not is_silent:
        line(f"<debug>Running: {' '.join(cmd)} </debug>")
    try:
        account_id = subprocess.check_output(cmd).decode().strip()
        return account_id
    except subprocess.CalledProcessError as e:
        line(f"<error>Error retrieving account ID: {e}</error>")
        sys.exit(1)

def check_ivcap_cmd(line, is_silent=False):
    if not command_exists("ivcap"):
        line("<error>'ivcap' command not found. Please install the IVCAP CLI tool.</error>")
        line("<error>... see https://github.com/ivcap-works/ivcap-cli?tab=readme-ov-file#install-released-binaries for instructions</error>")
        os.exit(1)
