import platform
import os

def get_flags_from_int(value, enum):
    set_flags = [flag for flag in enum if value & flag.value]
    return set_flags

# determine the path to the AIMMS executable by looking for the aimms folder
# based on the given version number
def find_aimms_path(aimms_version: str = None) -> str:
    """
    Finds the path to the AIMMS executable based on the given version number.

    Args:
        aimms_version (str): The version of AIMMS to find. If None, it will look for the default installation path on Linux.

    Returns:
        str: The path to the folder that contains libaimms3.dll or libaimms3.so.
    """
    aimms_folder = None
    if not aimms_version and platform.system() == "Linux":
        # check if /usr/local/Aimms/Lib exists
        default_folder = os.path.join("/usr", "local", "Aimms", "Lib")
        if os.path.exists(default_folder):
            aimms_folder = default_folder
        else:
            raise FileNotFoundError("AIMMS version not specified and /usr/local/Aimms/Lib does not exist.")
    elif platform.system() == "Windows":
        base_path = os.path.join(os.getenv("LOCALAPPDATA"), "AIMMS", "IFA", "Aimms")
        #find a folder that starts with the given version number
        version_folders = [d for d in os.listdir(base_path) if d.startswith(aimms_version)]
        if not version_folders:
            raise FileNotFoundError(f"AIMMS version {aimms_version} not found in {base_path}")
        aimms_folder = os.path.join(base_path, version_folders[0], "Bin")
    else:
        base_path = os.path.join(os.getenv("HOME"), ".Aimms")
        #find a folder that starts with the given version number
        version_folders = [d for d in os.listdir(base_path) if d.startswith(aimms_version)]
        if not version_folders:
            raise FileNotFoundError(f"AIMMS version {aimms_version} not found in {base_path}")
        aimms_folder = os.path.join(base_path, version_folders[0], "Lib")
    
    # Check if the dynamic library exists
    if platform.system() == "Windows":
        lib_name = "libaimms3.dll"
    else:
        lib_name = "libaimms3.so"
    lib_path = os.path.join(aimms_folder, lib_name)
    if not os.path.exists(lib_path):
        raise FileNotFoundError(f"AIMMS dynamic library {lib_name} not found in {aimms_folder}")
    return aimms_folder