from typing import Union, List, Dict, Any

def roblox_id_sanitizer(raw_id: Union[str, int]) -> int:
    """Extracts numeric Roblox IDs from various input formats.
    
    Args:
        raw_id: The input identifier as string or integer.
        
    Returns:
        A sanitized integer ID.
    """
    try:
        return int(str(raw_id).split('/')[-1])
    except (ValueError, TypeError):
        return 0

def metadata_formatter(data: Dict[str, Any]) -> str:
    """Converts dictionary objects into Roblox-compatible meta tags.
    
    Args:
        data: Key-value pairs for asset metadata.
        
    Returns:
        Formatted string sequence for API consumption.
    """
    return "&".join([f"{k}={v}" for k, v in data.items()])

def batch_process_assets(assets: List[int], chunk_size: int = 50) -> List[List[int]]:
    """Chunks asset lists for optimized API request payloads.
    
    Args:
        assets: List of asset IDs to process.
        chunk_size: Maximum size per request packet.
        
    Returns:
        A list of lists partitioned by the chunk size.
    """
    return [assets[i:i + chunk_size] for i in range(0, len(assets), chunk_size)]