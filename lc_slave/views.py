from django.shortcuts import render
import docker
from django.http import JsonResponse
from subprocess import run, PIPE
import json

APP_CONTAINER_PREFIX = "cc_"
client = docker.from_env()


def start_instance(request):
    """
    Creates a new instance in the client.
    :param memory:
    :param cpu:
    :param image:
    :param request:
    :param instance_id:
    :return:
    """

    request = json.loads(request.body.decode('UTF-8'))

    instance_id = str(request['instance_id'])
    image = request['image']
    cpu = int(request['cpu'])
    memory = str(request['memory']) + "m"
    container_name = APP_CONTAINER_PREFIX + instance_id
    try:
        container = client.containers.get(container_name)
    except docker.errors.NotFound:
        pass
    else:
        return JsonResponse({"message": "Instance with the ID already running"}, status=400)

    container = client.containers.run(
        image=image,
        name=container_name,
        cpu_count=cpu,
        mem_limit=memory,
        ports={
            22: None
        },
        detach=True
    )
    ssh_port = container.ports[0]
    return JsonResponse({"message": "Instance Created", "ssh_port": ssh_port})


def stop_instance(request):
    """
    Stops the instance created
    :param request:
    :param instance_id:
    :return:
    """

    request = json.loads(request.body.decode('UTF-8'))
    print(request)

    instance_id = request['instance_id']
    container_name = APP_CONTAINER_PREFIX + instance_id
    try:
        container = client.containers.get(container_name)
    except docker.errors.NotFound:
        return JsonResponse({"message": "Instance not found"}, status=400)
    else:
        container.stop()
    return JsonResponse({"message": "Instance terminated"})


def get_system_resource(request):
    """
    :return: Current system resource of slave
    """
    process = run(["bash", "lc_slave/stats.sh"], stdout=PIPE, stderr=PIPE)
    if process.returncode != 0:
        print(process.stderr.decode("utf-8"))
        return JsonResponse({"message": process.stderr.decode("utf-8")}, status=500)
    stats = process.stdout.decode("utf-8").split()
    print(stats)
    try:
        docker_ram = int(float(stats[0]))
        host_ram = int(float(stats[1]))
        total_ram = int(float(stats[2]))
    except ValueError as err:
        print(err)
        return JsonResponse({"message": err}, status=500)
    return JsonResponse({"host_ram": host_ram, "docker_ram": docker_ram, "total_ram": total_ram})


def get_instance_resource(request, instance_id):
    """
    :param request:
    :param instance_id:
    :return: the resources within the instance
    """
    container_name = APP_CONTAINER_PREFIX + instance_id
    process = run(["bash", "lc_slave/stats_instance.sh", container_name], stdout=PIPE, stderr=PIPE)
    if process.returncode != 0:
        print(process.stderr.decode("utf-8"))
        return JsonResponse({"message": process.stderr.decode("utf-8")}, status=500)
    stats = process.stdout.decode("utf-8").split()
    return JsonResponse({"memory": stats[0], "cpu": stats[1]})
