import os
import asyncio
import tempfile
import time
import pandas as pd
from geopandas import GeoDataFrame
from shapely.geometry import mapping
from ..exceptions import APIError, ConfigurationError
from ..helper.bounded_taskgroup import BoundedTaskGroup
from ..helper.tiles import tiles
import uuid
import xarray as xr

async def request_data(
        client,
        gdf: GeoDataFrame,
        expr: str,
        conc: int = 20,
        in_crs: str = "epsg:4326",
        out_crs: str = "epsg:4326",
        resolution: int = -1,
        geom_fix: bool = False,
        max_memory_mb: int = 500,
        stream_to_disk: bool = None,
):
    """
    Request xarray datasets for all geometries in a GeoDataFrame.

    Args:
        client: The AsyncClient instance
        gdf (GeoDataFrame): GeoDataFrame containing geometries
        expr (str): Terrakio expression to evaluate, can include spatial aggregations
        conc (int): Number of concurrent requests to make
        in_crs (str): Input coordinate reference system
        out_crs (str): Output coordinate reference system
        resolution (int): Resolution parameter
        geom_fix (bool): Whether to fix the geometry (default False)
        max_memory_mb (int): Maximum memory threshold in MB (default 500MB)
        stream_to_disk (bool): Whether to stream large datasets to disk. If None, will be determined automatically.

    Returns:
        geopandas.GeoDataFrame: Copy of input GeoDataFrame with additional 'dataset' column
                               containing the xarray Dataset for each geometry.

    Raises:
        ValueError: If concurrency is too high or if data exceeds memory limit without streaming
        APIError: If the API request fails
    """
    if conc > 100:
        raise ValueError("Concurrency (conc) is too high. Please set conc to 100 or less.")
    
    total_geometries = len(gdf)
    
    # First, make a request with the first geometry to estimate total memory usage
    client.logger.info("Estimating total memory usage...")
    first_geom = gdf.geometry.iloc[0]
    feature = {
        "type": "Feature",
        "geometry": mapping(first_geom),
        "properties": {}
    }
    
    try:
        first_result = await client.geoquery(expr=expr, feature=feature,
                                           in_crs=in_crs, out_crs=out_crs, resolution=resolution, geom_fix=geom_fix)
        if isinstance(first_result, dict) and first_result.get("error"):
            error_msg = f"Request failed: {first_result.get('error_message', 'Unknown error')}"
            if first_result.get('status_code'):
                error_msg = f"Request failed with status {first_result['status_code']}: {first_result.get('error_message', 'Unknown error')}"
            raise APIError(error_msg)
        
        if not isinstance(first_result, xr.Dataset):
            raise ValueError(f"Expected xarray Dataset, got {type(first_result)}")
        
        # Estimate total memory usage
        single_dataset_size_bytes = estimate_dataset_size(first_result)
        total_size_bytes = single_dataset_size_bytes * total_geometries
        total_size_mb = total_size_bytes / (1024 * 1024)
        
        client.logger.info(f"Estimated total memory usage: {total_size_mb:.2f} MB for {total_geometries} geometries")
        
        # Check if we need to stream to disk
        if stream_to_disk is None:
            # Auto-determine based on memory usage
            if total_size_mb > max_memory_mb:
                client.logger.warning(f"The data you are requesting exceeds {max_memory_mb} MB, we recommend you to set the stream_to_disk parameter to True")
                raise ValueError(f"The data you are requesting exceeds {max_memory_mb} MB, we recommend you to set the stream_to_disk parameter to True")
        
    except Exception as e:
        if "recommend you to set the stream_to_disk parameter to True" in str(e):
            raise
        client.logger.error(f"Failed to estimate memory usage: {e}")
        raise
    
    client.logger.info(f"Processing {total_geometries} geometries with concurrency {conc}")
    
    completed_count = 0
    lock = asyncio.Lock()
    
    async def process_geometry(geom):
        """Process a single geometry and return the dataset"""
        nonlocal completed_count
        
        try:
            feature = {
                "type": "Feature",
                "geometry": mapping(geom),
                "properties": {}
            }
            # Request xarray dataset
            result = await client.geoquery(expr=expr, feature=feature,
                                        in_crs=in_crs, out_crs=out_crs, resolution=resolution, geom_fix=geom_fix)
            if isinstance(result, dict) and result.get("error"):
                error_msg = f"Request failed: {result.get('error_message', 'Unknown error')}"
                if result.get('status_code'):
                    error_msg = f"Request failed with status {result['status_code']}: {result.get('error_message', 'Unknown error')}"
                raise APIError(error_msg)
            
            # Ensure we got an xarray Dataset
            if not isinstance(result, xr.Dataset):
                raise ValueError(f"Expected xarray Dataset, got {type(result)}")
            
            async with lock:
                completed_count += 1
                if completed_count % max(1, total_geometries // 10) == 0:
                    client.logger.info(f"Progress: {completed_count}/{total_geometries} geometries processed")
            
            return result
            
        except Exception as e:
            async with lock:
                completed_count += 1
            raise
    
    try:
        async with BoundedTaskGroup(max_concurrency=conc) as tg:
            tasks = [
                tg.create_task(process_geometry(gdf.geometry.iloc[idx]))
                for idx in range(len(gdf))
            ]
        all_results = [task.result() for task in tasks]

    except* Exception as eg:
        for e in eg.exceptions:
            if hasattr(e, 'response'):
                raise APIError(f"API request failed: {e.response.text}")
        raise
    
    client.logger.info("All requests completed!")

    if not all_results:
        raise ValueError("No valid results were returned for any geometry")
    
    # Create a copy of the input GeoDataFrame
    result_gdf = gdf.copy()
    
    # Add the dataset column with the xarray datasets
    result_gdf['dataset'] = all_results
    
    return result_gdf


import os
from pathlib import Path

def estimate_dataset_size(dataset):
    """
    Estimate the memory size of an xarray dataset in bytes.
    
    Args:
        dataset: xarray Dataset
        
    Returns:
        int: Estimated size in bytes
    """
    total_size = 0
    for var_name, var in dataset.data_vars.items():
        # Get the dtype size in bytes
        dtype_size = var.dtype.itemsize
        # Get the total number of elements
        total_elements = var.size
        # Calculate total size for this variable
        total_size += dtype_size * total_elements
    
    # Add coordinate sizes
    for coord_name, coord in dataset.coords.items():
        if coord_name not in dataset.dims:  # Don't double count dimension coordinates
            dtype_size = coord.dtype.itemsize
            total_elements = coord.size
            total_size += dtype_size * total_elements
    
    return total_size

def save_dataset_to_file(dataset, filepath):
    """
    Save dataset to NetCDF file.
    
    Args:
        dataset: xarray Dataset
        filepath: Path to save the file
        
    Returns:
        str: Path to saved file
    """
    filepath = Path(filepath)
    
    if not str(filepath).endswith('.nc'):
        filepath = filepath.with_suffix('.nc')
    
    dataset.to_netcdf(filepath)
    return str(filepath)

def post_processing(
        gdf_with_datasets: GeoDataFrame,
        spatial_reduction: str = None,
        temporal_reduction: str = None,
        drop_nan: bool = False,
        inplace: bool = False,
        stream_to_disk: bool = False,
):
    """
    Post-process the GeoDataFrame with datasets to extract variables with optional reductions.

    Args:
        gdf_with_datasets (GeoDataFrame): GeoDataFrame with 'dataset' column containing xarray Datasets
        spatial_reduction (str): Reduction operation for spatial dimensions (x, y). 
                               Options: 'mean', 'median', 'min', 'max', 'std', 'var', 'sum', 'count'
        temporal_reduction (str): Reduction operation for temporal dimension (time).
                                Options: 'mean', 'median', 'min', 'max', 'std', 'var', 'sum', 'count'
        drop_nan (bool): Whether to drop NaN values from the results (default False)
        inplace (bool): Whether to modify the input GeoDataFrame in place
        stream_to_disk (bool): Whether to stream datasets to disk as NetCDF files (default False)

    Returns:
        geopandas.GeoDataFrame: GeoDataFrame with variable dataarrays/values or file paths in separate columns.
                               If stream_to_disk=True, large datasets are saved as NetCDF files with file paths stored.
    """
    if 'dataset' not in gdf_with_datasets.columns:
        raise ValueError("Input GeoDataFrame must contain a 'dataset' column")
    
    # Validate reduction parameters
    valid_reductions = ['mean', 'median', 'min', 'max', 'std', 'var', 'sum', 'count']
    if spatial_reduction and spatial_reduction not in valid_reductions:
        raise ValueError(f"spatial_reduction must be one of {valid_reductions}")
    if temporal_reduction and temporal_reduction not in valid_reductions:
        raise ValueError(f"temporal_reduction must be one of {valid_reductions}")
    
    result_rows = []
    geometries = []
    
    # Process each row (geometry + dataset)
    for i, row in gdf_with_datasets.iterrows():
        dataset = row['dataset']
        
        # Create new row for this geometry
        new_row = {}
        
        # Copy original GeoDataFrame attributes (excluding dataset column)
        for col in gdf_with_datasets.columns:
            if col not in ['geometry', 'dataset']:
                new_row[col] = row[col]
        
        # Process each variable in the dataset
        data_vars = list(dataset.data_vars.keys())
        for var_name in data_vars:
            var_data = dataset[var_name]
            
            # Apply drop_nan if requested
            if drop_nan:
                # Drop spatial dimensions where all values are NaN
                var_data = var_data.dropna(dim='x', how='all').dropna(dim='y', how='all')
                
                # Drop time dimensions where all values are NaN
                if 'time' in var_data.dims:
                    var_data = var_data.dropna(dim='time', how='all')
            
            # Check current dimensions to determine if aggregation is needed
            current_dims = set(var_data.dims)
            has_spatial_dims = bool(current_dims.intersection(['x', 'y']))
            has_temporal_dim = 'time' in current_dims
            
            # Apply spatial reduction only if spatial dimensions exist and reduction is requested
            if spatial_reduction and has_spatial_dims:
                spatial_dims = [dim for dim in ['x', 'y'] if dim in var_data.dims]
                if spatial_dims:
                    if spatial_reduction == 'count':
                        var_data = var_data.count(dim=spatial_dims)
                    else:
                        var_data = getattr(var_data, spatial_reduction)(dim=spatial_dims)
            
            # Apply temporal reduction only if time dimension exists and reduction is requested
            if temporal_reduction and has_temporal_dim:
                if temporal_reduction == 'count':
                    var_data = var_data.count(dim='time')
                else:
                    var_data = getattr(var_data, temporal_reduction)(dim='time')
            
            # Handle streaming to disk if requested
            if stream_to_disk:
                # Create a single-variable dataset for saving
                single_var_dataset = var_data.to_dataset(name=var_name)
                
                # Generate filename based on row index and variable name
                filename = f"geometry_{i}_{var_name}.nc"
                filepath = os.path.join(os.getcwd(), filename)
                
                # Save to disk and store file path
                saved_path = save_dataset_to_file(single_var_dataset, filepath)
                new_row[var_name] = f"file://{saved_path}"
                
                print(f"Dataset for geometry {i}, variable '{var_name}' saved to: {saved_path}")
            else:
                # Keep in memory
                new_row[var_name] = var_data
        
        result_rows.append(new_row)
        geometries.append(row['geometry'])
    
    # Create the result GeoDataFrame with default integer index
    result_gdf = GeoDataFrame(result_rows, geometry=geometries)
    
    if inplace:
        # Clear original gdf and replace with result_gdf content
        gdf_with_datasets.drop(gdf_with_datasets.index, inplace=True)
        gdf_with_datasets.drop(gdf_with_datasets.columns, axis=1, inplace=True)
        
        # Copy all data from result_gdf to gdf
        for col in result_gdf.columns:
            gdf_with_datasets[col] = result_gdf[col].values
        
        # Ensure it remains a GeoDataFrame with correct geometry
        gdf_with_datasets.geometry = result_gdf.geometry
        
        return None
    else:
        return result_gdf


# Updated zonal_stats function that uses both parts
async def zonal_stats(
        client,
        gdf: GeoDataFrame,
        expr: str,
        conc: int = 20,
        inplace: bool = False,
        in_crs: str = "epsg:4326",
        out_crs: str = "epsg:4326",
        resolution: int = -1,
        geom_fix: bool = False,
        drop_nan: bool = False,
        spatial_reduction: str = None,
        temporal_reduction: str = None,
        max_memory_mb: int = 500,
        stream_to_disk: bool = False,
):
    """
    Compute zonal statistics for all geometries in a GeoDataFrame.
    This is a convenience function that combines request_data and post_processing.
    
    Args:
        client: The AsyncClient instance
        gdf (GeoDataFrame): GeoDataFrame containing geometries
        expr (str): Terrakio expression to evaluate, can include spatial aggregations
        conc (int): Number of concurrent requests to make
        inplace (bool): Whether to modify the input GeoDataFrame in place
        in_crs (str): Input coordinate reference system
        out_crs (str): Output coordinate reference system
        resolution (int): Resolution parameter
        geom_fix (bool): Whether to fix the geometry (default False)
        drop_nan (bool): Whether to drop NaN values from the results (default False)
        spatial_reduction (str): Reduction operation for spatial dimensions (x, y). 
                               Options: 'mean', 'median', 'min', 'max', 'std', 'var', 'sum', 'count'
        temporal_reduction (str): Reduction operation for temporal dimension (time).
                                Options: 'mean', 'median', 'min', 'max', 'std', 'var', 'sum', 'count'
        max_memory_mb (int): Maximum memory threshold in MB (default 500MB)
        stream_to_disk (bool): Whether to stream datasets to disk as NetCDF files (default False)
    """
    # Step 1: Request data (with memory estimation)
    gdf_with_datasets = await request_data(
        client=client,
        gdf=gdf,
        expr=expr,
        conc=conc,
        in_crs=in_crs,
        out_crs=out_crs,
        resolution=resolution,
        geom_fix=geom_fix,
        max_memory_mb=max_memory_mb,
        stream_to_disk=stream_to_disk
    )
    
    # Step 2: Post-process with reductions and optional streaming
    result = post_processing(
        gdf_with_datasets=gdf_with_datasets,
        spatial_reduction=spatial_reduction,
        temporal_reduction=temporal_reduction,
        drop_nan=drop_nan,
        inplace=inplace,
        stream_to_disk=stream_to_disk
    )
    
    return result

async def create_dataset_file(
    client,
    aoi: str,
    expression: str,
    output: str,
    in_crs: str = "epsg:4326",
    res: float = 0.0001,
    region: str = "aus",
    to_crs: str = "epsg:4326",
    overwrite: bool = True,
    skip_existing: bool = False,
    non_interactive: bool = True,
    poll_interval: int = 30,
    download_path: str = "/home/user/Downloads",
) -> dict:
    
    name = f"tiles-{uuid.uuid4().hex[:8]}"
    
    body, reqs, groups = tiles(
        name = name, 
        aoi = aoi, 
        expression = expression,
        output = output,
        tile_size = 128,
        crs = in_crs,
        res = res,
        region = region,
        to_crs = to_crs,
        fully_cover = True,
        overwrite = overwrite,
        skip_existing = skip_existing,
        non_interactive = non_interactive
    )
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tempreq:
        tempreq.write(reqs)
        tempreqname = tempreq.name
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tempmanifest:
        tempmanifest.write(groups)
        tempmanifestname = tempmanifest.name

    task_id = await client.mass_stats.execute_job(
        name=body["name"],
        region=body["region"],
        output=body["output"],
        config = {},
        overwrite=body["overwrite"],
        skip_existing=body["skip_existing"],
        request_json=tempreqname,
        manifest_json=tempmanifestname,
    )

    start_time = time.time()
    status = None
    
    while True:
        try:
            taskid = task_id['task_id']
            trackinfo = await client.mass_stats.track_job([taskid])
            client.logger.info("the trackinfo is: ", trackinfo)
            status = trackinfo[taskid]['status']
            
            if status == 'Completed':
                client.logger.info('Tiles generated successfully!')
                break
            elif status in ['Failed', 'Cancelled', 'Error']:
                raise RuntimeError(f"Job {taskid} failed with status: {status}")
            else:
                elapsed_time = time.time() - start_time
                client.logger.info(f"Job status: {status} - Elapsed time: {elapsed_time:.1f}s", end='\r')
                
                await asyncio.sleep(poll_interval)
                
                
        except KeyboardInterrupt:
            client.logger.info(f"\nInterrupted! Job {taskid} is still running in the background.")
            raise
        except Exception as e:
            client.logger.info(f"\nError tracking job: {e}")
            raise

    os.unlink(tempreqname)
    os.unlink(tempmanifestname)

    combine_result = await client.mass_stats.combine_tiles(body["name"], body["overwrite"], body["output"])
    combine_task_id = combine_result.get("task_id")

    combine_start_time = time.time()
    while True:
        try:
            trackinfo = await client.mass_stats.track_job([combine_task_id])
            client.logger.info('client create dataset file track info:', trackinfo)
            if body["output"] == "netcdf":
                download_file_name = trackinfo[combine_task_id]['folder'] + '.nc'
            elif body["output"] == "geotiff":
                download_file_name = trackinfo[combine_task_id]['folder'] + '.tif'
            bucket = trackinfo[combine_task_id]['bucket']
            combine_status = trackinfo[combine_task_id]['status']
            if combine_status == 'Completed':
                client.logger.info('Tiles combined successfully!')
                break
            elif combine_status in ['Failed', 'Cancelled', 'Error']:
                raise RuntimeError(f"Combine job {combine_task_id} failed with status: {combine_status}")
            else:
                elapsed_time = time.time() - combine_start_time
                client.logger.info(f"Combine job status: {combine_status} - Elapsed time: {elapsed_time:.1f}s", end='\r')
                time.sleep(poll_interval)
        except KeyboardInterrupt:
            client.logger.info(f"\nInterrupted! Combine job {combine_task_id} is still running in the background.")
            raise
        except Exception as e:
            client.logger.info(f"\nError tracking combine job: {e}")
            raise

    if download_path:
        await client.mass_stats.download_file(
            job_name=body["name"],
            bucket=bucket,
            file_type='processed',
            page_size=10,
            output_path=download_path,
        )
    else:
        path = f"{body['name']}/outputs/merged/{download_file_name}"
        client.logger.info(f"Combined file is available at {path}")

    return {"generation_task_id": task_id, "combine_task_id": combine_task_id}
