import asyncio
import functools
import inspect
from typing import Optional, Dict, Any, Union
from geopandas import GeoDataFrame
from shapely.geometry.base import BaseGeometry as ShapelyGeometry
from .async_client import AsyncClient


class SyncWrapper:
    """
    Generic synchronous wrapper with __dir__ support for runtime autocomplete.
    """
    
    def __init__(self, async_obj, sync_client):
        self._async_obj = async_obj
        self._sync_client = sync_client
    
    def __dir__(self):
        """
        Return list of attributes for autocomplete in interactive environments.
        This enables autocomplete in Jupyter/iPython after instantiation.
        """
        # Get all public attributes from the wrapped async object
        async_attrs = [attr for attr in dir(self._async_obj) if not attr.startswith('_')]
        
        # Get all attributes from this wrapper instance
        wrapper_attrs = [attr for attr in object.__dir__(self) if not attr.startswith('_')]
        
        # Combine and return unique attributes
        return list(set(async_attrs + wrapper_attrs))
    
    def __getattr__(self, name):
        """
        Dynamically wrap any method call to convert async to sync.
        """
        attr = getattr(self._async_obj, name)
        
        if callable(attr):
            @functools.wraps(attr)
            def sync_wrapper(*args, **kwargs):
                result = attr(*args, **kwargs)
                if hasattr(result, '__await__'):
                    return self._sync_client._run_async(result)
                return result
            return sync_wrapper
        
        return attr


class SyncClient:
    """
    Synchronous wrapper with __dir__ support for runtime autocomplete.
    Works best in interactive environments like Jupyter/iPython.
    """
    
    def __init__(self, url: Optional[str] = None, api_key: Optional[str] = None, verbose: bool = False):
        self._async_client = AsyncClient(url=url, api_key=api_key, verbose=verbose)
        self._context_entered = False
        self._closed = False
        
        # Initialize endpoint managers
        self.datasets = SyncWrapper(self._async_client.datasets, self)
        self.users = SyncWrapper(self._async_client.users, self)
        self.mass_stats = SyncWrapper(self._async_client.mass_stats, self)
        self.groups = SyncWrapper(self._async_client.groups, self)
        self.space = SyncWrapper(self._async_client.space, self)
        self.model = SyncWrapper(self._async_client.model, self)
        self.auth = SyncWrapper(self._async_client.auth, self)
        
        # Register cleanup
        import atexit
        atexit.register(self._cleanup)
    
    def __dir__(self):
        """
        Return list of attributes for autocomplete in interactive environments.
        This includes all methods from the async client plus the endpoint managers.
        """
        # Get default attributes from this class
        default_attrs = [attr for attr in object.__dir__(self) if not attr.startswith('_')]
        
        # Get all public methods from the async client
        async_client_attrs = [attr for attr in dir(self._async_client) if not attr.startswith('_')]
        
        # Add endpoint managers
        endpoint_attrs = ['datasets', 'users', 'mass_stats', 'groups', 'space', 'model', 'auth']
        
        # Combine all attributes
        all_attrs = default_attrs + async_client_attrs + endpoint_attrs
        
        return list(set(all_attrs))
    
    def geoquery(
        self,
        expr: str,
        feature: Union[Dict[str, Any], ShapelyGeometry],
        in_crs: str = "epsg:4326",
        out_crs: str = "epsg:4326",
        resolution: int = -1,
        geom_fix: bool = False,
        **kwargs
    ):
        """Compute WCS query for a single geometry (synchronous version)."""
        coro = self._async_client.geoquery(
            expr=expr,
            feature=feature,
            in_crs=in_crs,
            out_crs=out_crs,
            output="netcdf",
            resolution=resolution,
            geom_fix=geom_fix,
            **kwargs
        )
        return self._run_async(coro)

    def zonal_stats(
            self,
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
        Compute zonal statistics for all geometries in a GeoDataFrame (synchronous version).
        
        Args:
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

        Returns:
            geopandas.GeoDataFrame: GeoDataFrame with added columns for results, or None if inplace=True
                                If stream_to_disk=True, large datasets are saved as NetCDF files with file paths stored.

        Raises:
            ValueError: If concurrency is too high or if data exceeds memory limit without streaming
            APIError: If the API request fails
        """
        coro = self._async_client.zonal_stats(
            gdf=gdf,
            expr=expr,
            conc=conc,
            inplace=inplace,
            in_crs=in_crs,
            out_crs=out_crs,
            resolution=resolution,
            geom_fix=geom_fix,
            drop_nan=drop_nan,
            spatial_reduction=spatial_reduction,
            temporal_reduction=temporal_reduction,
            max_memory_mb=max_memory_mb,
            stream_to_disk=stream_to_disk
        )
        return self._run_async(coro)
    
    def create_dataset_file(
        self,
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
        """Create a dataset file using mass stats operations (synchronous version)."""
        coro = self._async_client.create_dataset_file(
            aoi=aoi,
            expression=expression,
            output=output,
            in_crs=in_crs,
            res=res,
            region=region,
            to_crs=to_crs,
            overwrite=overwrite,
            skip_existing=skip_existing,
            non_interactive=non_interactive,
            poll_interval=poll_interval,
            download_path=download_path,
        )
        return self._run_async(coro)

    # Rest of the methods remain the same...
    async def _ensure_context(self):
        """Ensure the async client context is entered."""
        if not self._context_entered and not self._closed:
            await self._async_client.__aenter__()
            self._context_entered = True
    
    async def _exit_context(self):
        """Exit the async client context."""
        if self._context_entered and not self._closed:
            await self._async_client.__aexit__(None, None, None)
            self._context_entered = False
    
    def _run_async(self, coro):
        """Run an async coroutine and return the result synchronously."""
        async def run_with_context():
            await self._ensure_context()
            return await coro
        
        try:
            loop = asyncio.get_running_loop()
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, run_with_context())
                return future.result()
        except RuntimeError:
            return asyncio.run(run_with_context())
    
    def close(self):
        """Close the underlying async client session."""
        if not self._closed:
            async def close_async():
                await self._exit_context()
            
            try:
                loop = asyncio.get_running_loop()
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, close_async())
                    future.result()
            except RuntimeError:
                asyncio.run(close_async())
            
            self._closed = True
    
    def _cleanup(self):
        """Internal cleanup method called by atexit."""
        if not self._closed:
            try:
                self.close()
            except Exception:
                pass
    
    def __enter__(self):
        """Context manager entry."""
        async def enter_async():
            await self._ensure_context()
        
        try:
            loop = asyncio.get_running_loop()
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, enter_async())
                future.result()
        except RuntimeError:
            asyncio.run(enter_async())
        
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
    
    def __del__(self):
        """Destructor to ensure session is closed."""
        if not self._closed:
            try:
                self._cleanup()
            except Exception:
                pass