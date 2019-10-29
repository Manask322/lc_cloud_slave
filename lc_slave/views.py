from django.shortcuts import render

from django.http import JsonResponse
# Create your views here.


def start_instance(request, instance_id):
    """
    Creates a new instance in the client.
    :param request:
    :param instance_id:
    :return:
    """
    return JsonResponse({"message": "Instance Created"})


def stop_instance(request, instance_id):
    """
    Stops the instance created
    :param request:
    :param instance_id:
    :return:
    """

    return JsonResponse({"message": "Instance terminated"})


def get_system_resource(request):
    """
    :return: Current system resource of slave
    """

    return JsonResponse({"message": "Return System Resource."})


def get_instance_resource(request, instance_id):
    """
    :param request:
    :param instance_id:
    :return: the resources within the instance
    """

    return JsonResponse({"message":"returns instance resource"})

