from .py_ark_vrf import *
import importlib.resources
import tempfile
import os

__doc__ = py_ark_vrf.__doc__
if hasattr(py_ark_vrf, "__all__"):
    __all__ = py_ark_vrf.__all__

def get_srs_file_path():
    """Get the path to the SRS file, extracting it from the package if needed."""
    try:
        # Python 3.9+ way
        files = importlib.resources.files('py_ark_vrf')
        srs_file = files / 'bandersnatch_ring.srs'
        
        # Create a temporary file if we need to extract from the package
        if hasattr(srs_file, 'read_bytes'):
            # File is in a package/zip, extract it
            temp_dir = tempfile.mkdtemp()
            temp_srs_path = os.path.join(temp_dir, 'bandersnatch_ring.srs')
            with open(temp_srs_path, 'wb') as f:
                f.write(srs_file.read_bytes())
            return temp_srs_path
        else:
            # File is on filesystem
            return str(srs_file)
    except (ImportError, AttributeError):
        # Fallback for older Python versions
        try:
            import importlib_resources
            files = importlib_resources.files('py_ark_vrf')
            srs_file = files / 'bandersnatch_ring.srs'
            
            temp_dir = tempfile.mkdtemp()
            temp_srs_path = os.path.join(temp_dir, 'bandersnatch_ring.srs')
            with open(temp_srs_path, 'wb') as f:
                f.write(srs_file.read_bytes())
            return temp_srs_path
        except ImportError:
            # Final fallback - look in current directory
            return 'bandersnatch_ring.srs' 