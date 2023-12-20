from typing import Any, Dict

from chaoslib.exceptions import ActivityFailed
from chaoslib.types import Configuration, Secrets
from google.cloud import compute_v1
from google.cloud.compute_v1.types import Tags
from logzero import logger

from chaosgcp import get_context, load_credentials, wait_on_extended_operation

__all__ =["set_instance_tags","get_fingerprint_of_instance"]

def get_fingerprint_of_instance(instance_name:  str, 
                              configuration: Configuration = None,
                              secrets: Secrets = None):
    
    ctx = get_context(configuration=configuration, secrets=secrets)
    credentials = load_credentials(secrets)
    # Create a client
    client = compute_v1.InstancesClient(credentials=credentials)

    # Initialize request argument(s)
    request = compute_v1.GetInstanceRequest(
        instance=instance_name,
        project=ctx.project_id,
        zone=ctx.zone,
    )

    # Make the request
    response = client.get(request=request)

    # Handle the response
    #print(response)
    return response.tags.fingerprint

def set_instance_tags(instance_name,fgp,tags_list, configuration: Configuration = None,
                              secrets: Secrets = None):
    
    credentials = load_credentials(secrets)
    ctx = get_context(configuration=configuration, secrets=secrets)
    # Create a client
    client = compute_v1.InstancesClient(credentials)
    
    fgp=get_fingerprint_of_instance(instance_name,configuration, secrets)
   
    

    # Initialize request argument(s)
    request = compute_v1.SetTagsInstanceRequest(
        instance=instance_name,
        project=ctx.project_id,
        zone=ctx.zone,
        tags_resource=Tags(fingerprint=fgp,items=tags_list)
                
    )

    # Make the request
    operation = client.set_tags(request=request,tags_resource=Tags())

    # Handle the response
    wait_on_extended_operation(operation)