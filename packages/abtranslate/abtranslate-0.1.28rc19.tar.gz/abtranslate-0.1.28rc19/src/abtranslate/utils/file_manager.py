from zipfile import ZipFile
from pathlib import Path

from .logger import logger 


def extract_package(model_file: str, extract_dir: str) -> Path:
    try:
        # Ensure extract directory exists
        extract_path = Path(extract_dir)
        extract_path.mkdir(parents=True, exist_ok=True)
        
        with ZipFile(model_file, 'r') as zip_ref:
            zip_ref.testzip()
            file_list = zip_ref.namelist()
            
            # Find the package directory (look for one containing metadata.json)
            package_name = None
            for file_path in file_list:
                if file_path.endswith('metadata.json'):
                    # Get the directory containing metadata.json
                    package_name = str(Path(file_path).parent)
                    if package_name == '.':  # metadata.json is in root
                        package_name = Path(model_file).stem  # Use model filename as package name
                    break
            
            if not package_name:
                # Fallback: assume first directory-like entry or use model filename
                if file_list and '/' in file_list[0]:
                    package_name = file_list[0].split('/')[0]
                else:
                    package_name = Path(model_file).stem
            
            # Clean up package name (remove any leading/trailing slashes)
            package_name = package_name.strip('/')
            
            package_path = extract_path / package_name
            
            # Check if files already exist
            all_exist = all(
                (extract_path / name).exists() 
                for name in file_list if name.strip() and not name.endswith('/')
            )
            
            if not all_exist:
                logger.info(f"Extracting model files to {extract_dir}")
                zip_ref.extractall(extract_dir)
            else:
                logger.info("Model files already exist, skipping extraction")
            
            # Verify the package path exists and contains metadata.json
            if not package_path.exists():
                logger.error(f"Package path {package_path} does not exist after extraction")
                logger.error(f"Available paths: {list(extract_path.iterdir())}")
                raise FileNotFoundError(f"Package directory {package_path} not found after extraction")
            
            metadata_path = package_path / "metadata.json"
            if not metadata_path.exists():
                logger.error(f"metadata.json not found in {package_path}")
                logger.error(f"Contents: {list(package_path.iterdir()) if package_path.exists() else 'PATH_NOT_FOUND'}")
                raise FileNotFoundError(f"metadata.json not found in {package_path}")
            
            return package_path
            
    except Exception as e:
        logger.error(f"Model extraction failed: {e}")
        raise Exception(f"Model extraction failed: {e}")