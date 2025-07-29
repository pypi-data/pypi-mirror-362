"""Type stubs for py_ark_vrf package."""

from typing import Tuple, List

def secret_from_seed(seed: bytes) -> Tuple[bytes, bytes]:
    """Generate a secret key pair from a seed.
    
    Args:
        seed: The seed bytes to generate the secret from
        
    Returns:
        A tuple of (public_key_bytes, secret_scalar_bytes)
    """
    ...

def public_from_le_secret(secret_scalar: bytes) -> bytes:
    """Derive a public key from a secret scalar.
    
    Args:
        secret_scalar: The secret scalar in little-endian bytes
        
    Returns:
        The public key bytes
    """
    ...

def prove_ietf(secret_scalar_le: bytes, input_data: bytes, aux: bytes) -> bytes:
    """Generate an IETF VRF proof.
    
    Args:
        secret_scalar_le: The secret scalar in little-endian bytes
        input_data: The input data for the VRF
        aux: Auxiliary data
        
    Returns:
        The VRF proof bytes (output + proof concatenated)
    """
    ...

def verify_ietf(pub_key: bytes, proof: bytes, input_data: bytes, aux: bytes) -> bool:
    """Verify an IETF VRF proof.
    
    Args:
        pub_key: The public key bytes
        proof: The VRF proof bytes (output + proof concatenated)
        input_data: The input data for the VRF
        aux: Auxiliary data
        
    Returns:
        True if the proof is valid, False otherwise
    """
    ...

def prove_ring(secret_scalar: bytes, input_data: bytes, ring: List[bytes], aux: bytes) -> bytes:
    """Generate a ring VRF proof.
    
    Args:
        secret_scalar: The secret scalar bytes
        input_data: The input data for the VRF
        ring: List of public keys in the ring
        aux: Auxiliary data
        
    Returns:
        The ring VRF proof bytes (output + proof concatenated)
    """
    ...

def verify_ring(input_data: bytes, proof: bytes, ring: List[bytes], aux: bytes) -> bool:
    """Verify a ring VRF proof.
    
    Args:
        input_data: The input data for the VRF
        proof: The ring VRF proof bytes (output + proof concatenated)
        ring: List of public keys in the ring
        aux: Auxiliary data
        
    Returns:
        True if the proof is valid, False otherwise
    """
    ...

def vrf_output(proof: bytes) -> bytes:
    """Extract the VRF output from a proof.
    
    Args:
        proof: The VRF proof bytes (output + proof concatenated)
        
    Returns:
        The VRF output bytes (first 32 bytes of the proof)
    """
    ...

def get_ring_root(public_keys_bytes: List[bytes]) -> bytes:
    """Compute the ring commitment root from a list of public keys.
    
    Args:
        public_keys_bytes: List of public key bytes
        
    Returns:
        The ring commitment root bytes
    """
    ...

def get_srs_file_path() -> str:
    """Get the path to the SRS file, extracting it from the package if needed.
    
    Returns:
        The path to the SRS file
    """
    ... 