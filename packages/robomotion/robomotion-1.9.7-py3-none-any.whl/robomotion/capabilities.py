import logging
import sys
import robomotion.runtime  as runtime
from robomotion.utils import Version

MINIMUM_ROBOT_VERSION = "23.12.0"
class Capability:
    CapabilityLMO = 1 << 0

capabilities = []

def IsLMOCapable():
    robot_info = runtime.Runtime.get_robot_info()  
    
    capabilities = robot_info.get("capabilities", {})    
    lmo_enabled = capabilities.get("lmo", False)
    
    version = robot_info.get("version", "")
    if lmo_enabled and not Version.is_version_less_than(version, MINIMUM_ROBOT_VERSION):
        return True

    return False

def add_capability(capability):
    capabilities.append(capability)


def get_capabilities():
    _capabilities = sys.maxsize 
    for cap in capabilities:
        _capabilities &= cap
    return _capabilities

def init_capabilities():
    add_capability(Capability.CapabilityLMO)
    
init_capabilities()