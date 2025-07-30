"""
Zero-copy buffer management and memory-efficient data transfer simulation.
Licensed software requiring valid activation.
"""

import asyncio
import mmap
import os
import tempfile
import time
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field
from threading import Lock
import weakref

from .exceptions import BufferError
from .licensing import LicensedClass


@dataclass
class BufferMetadata:
    """Metadata for buffer tracking and optimization."""
    buffer_id: str
    size_bytes: int
    created_at: float = field(default_factory=time.time)
    last_accessed: float = field(default_factory=time.time)
    access_count: int = 0
    is_pinned: bool = False
    memory_type: str = "system"  # system, gpu, quantum, photonic
    compression_ratio: float = 1.0
    checksum: Optional[str] = None


class ZeroCopyBuffer:
    """
    Zero-copy buffer implementation using memory mapping and views.
    
    This class provides high-performance, memory-efficient data transfer
    capabilities suitable for ultra-low-latency interconnects.
    """
    
    def __init__(
        self,
        size_bytes: int,
        buffer_id: Optional[str] = None,
        use_mmap: bool = True,
        pin_memory: bool = False,
    ):
        """
        Initialize a zero-copy buffer.
        
        Args:
            size_bytes: Size of the buffer in bytes
            buffer_id: Unique identifier for the buffer
            use_mmap: Whether to use memory mapping
            pin_memory: Whether to pin memory pages
        """
        self.size_bytes = size_bytes
        self.buffer_id = buffer_id or f"buf_{int(time.time() * 1000000)}"
        self.use_mmap = use_mmap
        self.pin_memory = pin_memory
        
        self._lock = Lock()
        self._metadata = BufferMetadata(
            buffer_id=self.buffer_id,
            size_bytes=size_bytes,
            is_pinned=pin_memory,
        )
        
        # Initialize buffer storage
        self._buffer = None
        self._mmap_file = None
        self._temp_file = None
        self._initialize_buffer()
    
    def _initialize_buffer(self) -> None:
        """Initialize the underlying buffer storage."""
        try:
            if self.use_mmap and self.size_bytes > 1024 * 1024:  # Use mmap for buffers > 1MB
                self._initialize_mmap_buffer()
            else:
                self._initialize_memory_buffer()
        except Exception as e:
            raise BufferError(f"Failed to initialize buffer: {e}")
    
    def _initialize_mmap_buffer(self) -> None:
        """Initialize memory-mapped buffer."""
        self._temp_file = tempfile.NamedTemporaryFile(delete=False)
        self._temp_file.write(b'\x00' * self.size_bytes)
        self._temp_file.flush()
        
        self._mmap_file = mmap.mmap(
            self._temp_file.fileno(),
            self.size_bytes,
            access=mmap.ACCESS_WRITE
        )
        self._buffer = memoryview(self._mmap_file)
        self._metadata.memory_type = "mmap"
    
    def _initialize_memory_buffer(self) -> None:
        """Initialize in-memory buffer."""
        data = bytearray(self.size_bytes)
        self._buffer = memoryview(data)
        self._metadata.memory_type = "system"
    
    def write(self, data: Union[bytes, bytearray, memoryview], offset: int = 0) -> int:
        """
        Write data to the buffer with zero-copy semantics.
        
        Args:
            data: Data to write
            offset: Offset in the buffer to start writing
            
        Returns:
            Number of bytes written
        """
        with self._lock:
            if offset + len(data) > self.size_bytes:
                raise BufferError("Data exceeds buffer size")
            
            # Zero-copy write using memoryview slicing
            self._buffer[offset:offset + len(data)] = data
            self._metadata.last_accessed = time.time()
            self._metadata.access_count += 1
            
            return len(data)
    
    def read(self, size: int, offset: int = 0) -> memoryview:
        """
        Read data from the buffer with zero-copy semantics.
        
        Args:
            size: Number of bytes to read
            offset: Offset in the buffer to start reading
            
        Returns:
            Memory view of the requested data
        """
        with self._lock:
            if offset + size > self.size_bytes:
                raise BufferError("Read exceeds buffer size")
            
            self._metadata.last_accessed = time.time()
            self._metadata.access_count += 1
            
            # Return a view without copying data
            return self._buffer[offset:offset + size]
    
    def get_view(self, start: int = 0, end: Optional[int] = None) -> memoryview:
        """Get a memory view of a buffer section."""
        with self._lock:
            end = end or self.size_bytes
            if start < 0 or end > self.size_bytes or start >= end:
                raise BufferError("Invalid view range")
            
            return self._buffer[start:end]
    
    def copy_to(self, other: "ZeroCopyBuffer", src_offset: int = 0, 
                dst_offset: int = 0, size: Optional[int] = None) -> int:
        """
        Copy data to another buffer with minimal overhead.
        
        Args:
            other: Destination buffer
            src_offset: Source offset
            dst_offset: Destination offset
            size: Number of bytes to copy (default: remaining source)
            
        Returns:
            Number of bytes copied
        """
        size = size or (self.size_bytes - src_offset)
        
        if src_offset + size > self.size_bytes:
            raise BufferError("Source read exceeds buffer size")
        if dst_offset + size > other.size_bytes:
            raise BufferError("Destination write exceeds buffer size")
        
        # Use memoryview for zero-copy transfer
        source_view = self.get_view(src_offset, src_offset + size)
        other.write(source_view, dst_offset)
        
        return size
    
    def clear(self) -> None:
        """Clear the buffer contents."""
        with self._lock:
            self._buffer[:] = b'\x00' * self.size_bytes
            self._metadata.last_accessed = time.time()
    
    def compress(self, algorithm: str = "lz4") -> float:
        """
        Simulate compression (placeholder for real implementation).
        
        Returns:
            Compression ratio achieved
        """
        # This is a simulation - real implementation would use actual compression
        import zlib
        
        with self._lock:
            data = bytes(self._buffer)
            compressed = zlib.compress(data)
            ratio = len(data) / len(compressed)
            self._metadata.compression_ratio = ratio
            return ratio
    
    def get_metadata(self) -> BufferMetadata:
        """Get buffer metadata."""
        return self._metadata
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit with cleanup."""
        self.cleanup()
    
    def cleanup(self) -> None:
        """Clean up resources."""
        try:
            if self._mmap_file:
                self._mmap_file.close()
            if self._temp_file:
                self._temp_file.close()
                try:
                    os.unlink(self._temp_file.name)
                except (OSError, AttributeError):
                    pass
        except Exception:
            pass  # Best effort cleanup
    
    def __del__(self):
        """Destructor for cleanup."""
        self.cleanup()


class BufferPool:
    """Pool of reusable buffers for efficient memory management."""
    
    def __init__(self, initial_size: int = 10, default_buffer_size: int = 1024 * 1024):
        """
        Initialize buffer pool.
        
        Args:
            initial_size: Initial number of buffers in pool
            default_buffer_size: Default size for new buffers
        """
        self.default_buffer_size = default_buffer_size
        self._available_buffers: List[ZeroCopyBuffer] = []
        self._in_use_buffers: Dict[str, ZeroCopyBuffer] = {}
        self._lock = Lock()
        
        # Pre-allocate initial buffers
        for _ in range(initial_size):
            buffer = ZeroCopyBuffer(default_buffer_size)
            self._available_buffers.append(buffer)
    
    def acquire(self, size: int = None) -> ZeroCopyBuffer:
        """Acquire a buffer from the pool."""
        size = size or self.default_buffer_size
        
        with self._lock:
            # Try to find a suitable buffer
            for i, buffer in enumerate(self._available_buffers):
                if buffer.size_bytes >= size:
                    buffer = self._available_buffers.pop(i)
                    self._in_use_buffers[buffer.buffer_id] = buffer
                    return buffer
            
            # Create new buffer if none available
            buffer = ZeroCopyBuffer(size)
            self._in_use_buffers[buffer.buffer_id] = buffer
            return buffer
    
    def release(self, buffer: ZeroCopyBuffer) -> None:
        """Release a buffer back to the pool."""
        with self._lock:
            if buffer.buffer_id in self._in_use_buffers:
                del self._in_use_buffers[buffer.buffer_id]
                buffer.clear()  # Clear for reuse
                self._available_buffers.append(buffer)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get pool statistics."""
        with self._lock:
            return {
                "available_buffers": len(self._available_buffers),
                "in_use_buffers": len(self._in_use_buffers),
                "total_buffers": len(self._available_buffers) + len(self._in_use_buffers),
                "default_buffer_size": self.default_buffer_size,
            }


class BufferManager(LicensedClass):
    """
    Central manager for all buffer operations in the fabric.
    
    Provides high-level buffer management, optimization, and monitoring
    for ultra-low-latency data transfers.
    """
    
    def __init__(self):
        """Initialize the buffer manager."""
        # STRICT LICENSE VALIDATION - NO BYPASS
        super().__init__(required_features=["core"])
        
        self._pools: Dict[int, BufferPool] = {}
        self._global_buffers: Dict[str, ZeroCopyBuffer] = {}
        self._lock = Lock()
        self._stats = {
            "total_allocations": 0,
            "total_deallocations": 0,
            "peak_memory_usage": 0,
            "current_memory_usage": 0,
        }
        
        # Create default pools for common buffer sizes
        self._create_default_pools()
    
    def _create_default_pools(self) -> None:
        """Create default buffer pools for common sizes."""
        common_sizes = [
            1024,           # 1KB - small messages
            64 * 1024,      # 64KB - medium packets
            1024 * 1024,    # 1MB - large transfers
            16 * 1024 * 1024,  # 16MB - GPU memory pages
            256 * 1024 * 1024, # 256MB - large AI model chunks
        ]
        
        for size in common_sizes:
            self._pools[size] = BufferPool(initial_size=5, default_buffer_size=size)
    
    def allocate_buffer(
        self,
        size: int,
        buffer_id: Optional[str] = None,
        use_pool: bool = True,
        **kwargs
    ) -> ZeroCopyBuffer:
        """
        Allocate a buffer with optimal strategy.
        
        Args:
            size: Buffer size in bytes
            buffer_id: Optional buffer identifier
            use_pool: Whether to use buffer pools
            **kwargs: Additional arguments for buffer creation
            
        Returns:
            Allocated buffer
        """
        with self._lock:
            self._stats["total_allocations"] += 1
            self._stats["current_memory_usage"] += size
            self._stats["peak_memory_usage"] = max(
                self._stats["peak_memory_usage"],
                self._stats["current_memory_usage"]
            )
        
        if use_pool:
            # Find the best-fit pool
            pool_size = self._find_best_pool_size(size)
            if pool_size:
                pool = self._pools.get(pool_size)
                if pool:
                    buffer = pool.acquire(size)
                    if buffer_id:
                        buffer.buffer_id = buffer_id
                    return buffer
        
        # Create a standalone buffer
        buffer = ZeroCopyBuffer(size, buffer_id, **kwargs)
        
        if buffer_id:
            with self._lock:
                self._global_buffers[buffer_id] = buffer
        
        return buffer
    
    def _find_best_pool_size(self, size: int) -> Optional[int]:
        """Find the best pool size for the requested buffer size."""
        for pool_size in sorted(self._pools.keys()):
            if pool_size >= size:
                return pool_size
        return None
    
    def deallocate_buffer(self, buffer: ZeroCopyBuffer) -> None:
        """Deallocate a buffer."""
        with self._lock:
            self._stats["total_deallocations"] += 1
            self._stats["current_memory_usage"] -= buffer.size_bytes
            
            # Remove from global buffers if present
            if buffer.buffer_id in self._global_buffers:
                del self._global_buffers[buffer.buffer_id]
        
        # Try to return to pool
        pool_size = self._find_best_pool_size(buffer.size_bytes)
        if pool_size and pool_size in self._pools:
            self._pools[pool_size].release(buffer)
        else:
            buffer.cleanup()
    
    def get_buffer(self, buffer_id: str) -> Optional[ZeroCopyBuffer]:
        """Get a buffer by ID."""
        with self._lock:
            return self._global_buffers.get(buffer_id)
    
    async def transfer_data(
        self,
        source_buffer: ZeroCopyBuffer,
        destination_buffer: ZeroCopyBuffer,
        size: Optional[int] = None,
        chunk_size: int = 64 * 1024,
    ) -> int:
        """
        Asynchronously transfer data between buffers in chunks.
        
        Args:
            source_buffer: Source buffer
            destination_buffer: Destination buffer
            size: Number of bytes to transfer
            chunk_size: Size of each transfer chunk
            
        Returns:
            Number of bytes transferred
        """
        size = size or source_buffer.size_bytes
        bytes_transferred = 0
        
        for offset in range(0, size, chunk_size):
            current_chunk_size = min(chunk_size, size - offset)
            
            # Perform the transfer
            source_buffer.copy_to(
                destination_buffer,
                src_offset=offset,
                dst_offset=offset,
                size=current_chunk_size
            )
            
            bytes_transferred += current_chunk_size
            
            # Yield control to allow other operations
            await asyncio.sleep(0)
        
        return bytes_transferred
    
    def optimize_pools(self) -> None:
        """Optimize buffer pools based on usage patterns."""
        # This could implement more sophisticated optimization logic
        # based on actual usage statistics
        pass
    
    def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive buffer manager statistics."""
        with self._lock:
            pool_stats = {}
            for size, pool in self._pools.items():
                pool_stats[f"pool_{size}"] = pool.get_stats()
            
            return {
                "global_stats": self._stats.copy(),
                "pool_stats": pool_stats,
                "global_buffers_count": len(self._global_buffers),
            }
    
    def cleanup_all(self) -> None:
        """Clean up all buffers and pools."""
        with self._lock:
            # Cleanup global buffers
            for buffer in self._global_buffers.values():
                buffer.cleanup()
            self._global_buffers.clear()
            
            # Cleanup pools
            for pool in self._pools.values():
                for buffer in pool._available_buffers:
                    buffer.cleanup()
                for buffer in pool._in_use_buffers.values():
                    buffer.cleanup()
            
            self._pools.clear()
            self._create_default_pools()  # Recreate default pools
