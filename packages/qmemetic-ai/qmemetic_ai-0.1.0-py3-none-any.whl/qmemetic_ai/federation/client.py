"""
Federated learning client for Q-Memetic AI.

Enables distributed meme evolution across federated nodes using secure
communication protocols and privacy-preserving learning techniques.
"""

import asyncio
import json
import time
import uuid
from typing import List, Dict, Optional, Any, Set
from dataclasses import dataclass, field
import logging

try:
    import grpc
    import grpc.aio
    GRPC_AVAILABLE = True
except ImportError:
    GRPC_AVAILABLE = False
    logging.warning("gRPC not available. Federated features disabled.")

try:
    import flower as fl
    FLOWER_AVAILABLE = True
except ImportError:
    FLOWER_AVAILABLE = False
    logging.warning("Flower not available. Federated learning features limited.")

from ..core.meme import Meme


@dataclass
class FederatedNode:
    """Information about a federated node."""
    
    node_id: str
    address: str
    port: int
    status: str = "unknown"
    last_seen: float = field(default_factory=time.time)
    capabilities: List[str] = field(default_factory=list)
    trust_score: float = 1.0
    latency_ms: float = 0.0
    meme_count: int = 0


@dataclass
class SyncRequest:
    """Request for synchronizing memes between nodes."""
    
    request_id: str
    source_node: str
    target_node: Optional[str]
    sync_type: str  # "push", "pull", "bidirectional"
    meme_filters: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)


@dataclass
class SyncResponse:
    """Response from a synchronization request."""
    
    request_id: str
    success: bool
    memes_sent: int
    memes_received: int
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)


class FederatedClient:
    """
    Client for federated memetic network operations.
    
    Provides:
    - Secure peer-to-peer communication
    - Privacy-preserving meme synchronization
    - Distributed evolution coordination
    - Trust and reputation management
    """
    
    def __init__(
        self,
        node_id: Optional[str] = None,
        listen_address: str = "localhost",
        listen_port: int = 8080,
        discovery_servers: Optional[List[str]] = None,
        encryption_enabled: bool = True,
        max_peers: int = 10
    ):
        """
        Initialize federated client.
        
        Args:
            node_id: Unique identifier for this node
            listen_address: Address to listen on
            listen_port: Port to listen on
            discovery_servers: List of discovery server addresses
            encryption_enabled: Whether to use encryption
            max_peers: Maximum number of peer connections
        """
        self.node_id = node_id or f"node_{uuid.uuid4().hex[:8]}"
        self.listen_address = listen_address
        self.listen_port = listen_port
        self.discovery_servers = discovery_servers or []
        self.encryption_enabled = encryption_enabled
        self.max_peers = max_peers
        
        self.logger = logging.getLogger(f"FederatedClient.{self.node_id}")
        
        # Node registry
        self.known_nodes: Dict[str, FederatedNode] = {}
        self.connected_peers: Set[str] = set()
        
        # Synchronization state
        self.sync_history: List[SyncResponse] = []
        self.pending_requests: Dict[str, SyncRequest] = {}
        
        # Network statistics
        self.stats = {
            "memes_sent": 0,
            "memes_received": 0,
            "sync_requests": 0,
            "connections_established": 0,
            "uptime_start": time.time()
        }
        
        # Server instance
        self.server = None
        self.is_running = False
    
    async def start_server(self):
        """Start the federated server to accept connections."""
        if not GRPC_AVAILABLE:
            self.logger.error("gRPC not available. Cannot start federated server.")
            return
        
        self.server = grpc.aio.server()
        # Add service implementations here
        
        listen_addr = f"{self.listen_address}:{self.listen_port}"
        self.server.add_insecure_port(listen_addr)
        
        await self.server.start()
        self.is_running = True
        
        self.logger.info(f"Federated server started on {listen_addr}")
        
        # Register with discovery servers
        await self._register_with_discovery()
        
        # Start background tasks
        asyncio.create_task(self._peer_discovery_loop())
        asyncio.create_task(self._health_check_loop())
    
    async def stop_server(self):
        """Stop the federated server."""
        if self.server:
            await self.server.stop(grace=5.0)
            self.is_running = False
            self.logger.info("Federated server stopped")
    
    async def discover_peers(self) -> List[FederatedNode]:
        """Discover other federated nodes in the network."""
        discovered_nodes = []
        
        # Discovery via configured servers
        for server_addr in self.discovery_servers:
            try:
                nodes = await self._query_discovery_server(server_addr)
                discovered_nodes.extend(nodes)
            except Exception as e:
                self.logger.warning(f"Failed to query discovery server {server_addr}: {e}")
        
        # Local network discovery (simplified)
        local_nodes = await self._local_network_scan()
        discovered_nodes.extend(local_nodes)
        
        # Update known nodes
        for node in discovered_nodes:
            self.known_nodes[node.node_id] = node
        
        self.logger.info(f"Discovered {len(discovered_nodes)} nodes")
        return discovered_nodes
    
    async def connect_to_peer(self, node_id: str) -> bool:
        """Establish connection to a specific peer node."""
        if node_id not in self.known_nodes:
            self.logger.error(f"Node {node_id} not in known nodes")
            return False
        
        if node_id in self.connected_peers:
            self.logger.info(f"Already connected to {node_id}")
            return True
        
        node = self.known_nodes[node_id]
        
        try:
            # Establish gRPC connection
            channel = grpc.aio.insecure_channel(f"{node.address}:{node.port}")
            
            # Test connection with health check
            health_ok = await self._health_check_peer(channel, node_id)
            
            if health_ok:
                self.connected_peers.add(node_id)
                self.stats["connections_established"] += 1
                self.logger.info(f"Connected to peer {node_id}")
                return True
            
        except Exception as e:
            self.logger.error(f"Failed to connect to {node_id}: {e}")
        
        return False
    
    async def sync_network(
        self,
        local_memes: List[Meme],
        node_id: Optional[str] = None,
        sync_mode: str = "bidirectional"
    ) -> Dict[str, Any]:
        """
        Synchronize memes with the federated network.
        
        Args:
            local_memes: Local memes to potentially share
            node_id: Specific node to sync with (None for all)
            sync_mode: "push", "pull", or "bidirectional"
            
        Returns:
            Synchronization results
        """
        sync_results = {
            "total_sent": 0,
            "total_received": 0,
            "nodes_contacted": 0,
            "errors": [],
            "received_memes": []
        }
        
        target_nodes = [node_id] if node_id else list(self.connected_peers)
        
        for peer_id in target_nodes:
            try:
                peer_result = await self._sync_with_peer(
                    peer_id, local_memes, sync_mode
                )
                
                sync_results["total_sent"] += peer_result.memes_sent
                sync_results["total_received"] += peer_result.memes_received
                sync_results["nodes_contacted"] += 1
                
                if not peer_result.success:
                    sync_results["errors"].extend(peer_result.errors)
                
                # Add received memes
                if "memes" in peer_result.metadata:
                    sync_results["received_memes"].extend(peer_result.metadata["memes"])
                
            except Exception as e:
                error_msg = f"Sync failed with {peer_id}: {e}"
                sync_results["errors"].append(error_msg)
                self.logger.error(error_msg)
        
        self.logger.info(f"Network sync completed: {sync_results['nodes_contacted']} nodes contacted")
        return sync_results
    
    async def _sync_with_peer(
        self,
        peer_id: str,
        local_memes: List[Meme],
        sync_mode: str
    ) -> SyncResponse:
        """Synchronize memes with a specific peer."""
        request_id = f"sync_{uuid.uuid4().hex[:8]}"
        
        sync_request = SyncRequest(
            request_id=request_id,
            source_node=self.node_id,
            target_node=peer_id,
            sync_type=sync_mode
        )
        
        self.pending_requests[request_id] = sync_request
        
        try:
            # Filter memes for sharing (privacy considerations)
            shareable_memes = self._filter_shareable_memes(local_memes)
            
            # Create meme data for transmission
            meme_data = [self._serialize_meme_for_sync(meme) for meme in shareable_memes]
            
            # Send sync request to peer
            if sync_mode in ["push", "bidirectional"]:
                await self._send_memes_to_peer(peer_id, meme_data)
            
            # Request memes from peer
            received_memes = []
            if sync_mode in ["pull", "bidirectional"]:
                received_memes = await self._request_memes_from_peer(peer_id)
            
            response = SyncResponse(
                request_id=request_id,
                success=True,
                memes_sent=len(meme_data) if sync_mode in ["push", "bidirectional"] else 0,
                memes_received=len(received_memes),
                metadata={"memes": received_memes}
            )
            
            self.sync_history.append(response)
            self.stats["sync_requests"] += 1
            
            return response
            
        except Exception as e:
            response = SyncResponse(
                request_id=request_id,
                success=False,
                memes_sent=0,
                memes_received=0,
                errors=[str(e)]
            )
            
            self.sync_history.append(response)
            return response
        
        finally:
            self.pending_requests.pop(request_id, None)
    
    def _filter_shareable_memes(self, memes: List[Meme]) -> List[Meme]:
        """Filter memes that can be shared in federated network."""
        shareable = []
        
        for meme in memes:
            # Privacy check: don't share personal/private memes
            if meme.metadata.tags and "private" in meme.metadata.tags:
                continue
            
            # Content filter: check for sensitive information
            if self._contains_sensitive_content(meme.content):
                continue
            
            # Fitness threshold: only share high-quality memes
            if meme.vector and meme.vector.fitness_score < 0.5:
                continue
            
            shareable.append(meme)
        
        return shareable
    
    def _contains_sensitive_content(self, content: str) -> bool:
        """Check if content contains sensitive information."""
        sensitive_keywords = [
            "password", "secret", "private", "confidential",
            "ssn", "credit card", "personal"
        ]
        
        content_lower = content.lower()
        return any(keyword in content_lower for keyword in sensitive_keywords)
    
    def _serialize_meme_for_sync(self, meme: Meme) -> Dict[str, Any]:
        """Serialize meme for network transmission."""
        # Remove sensitive metadata
        safe_metadata = {
            "domain": meme.metadata.domain,
            "generation": meme.metadata.generation,
            "tags": [tag for tag in meme.metadata.tags if not tag.startswith("private_")],
            "mutation_type": meme.metadata.mutation_type
        }
        
        return {
            "content": meme.content,
            "metadata": safe_metadata,
            "vector": {
                "content_embedding": meme.vector.content_embedding if meme.vector else None,
                "fitness_score": meme.vector.fitness_score if meme.vector else 0,
                "dimension": meme.vector.dimension if meme.vector else 0
            },
            "sync_timestamp": time.time()
        }
    
    async def _send_memes_to_peer(self, peer_id: str, meme_data: List[Dict]) -> bool:
        """Send memes to a specific peer."""
        # Placeholder for actual gRPC implementation
        self.logger.info(f"Sending {len(meme_data)} memes to {peer_id}")
        self.stats["memes_sent"] += len(meme_data)
        
        # Simulate network delay
        await asyncio.sleep(0.1)
        return True
    
    async def _request_memes_from_peer(self, peer_id: str) -> List[Dict]:
        """Request memes from a specific peer."""
        # Placeholder for actual gRPC implementation
        self.logger.info(f"Requesting memes from {peer_id}")
        
        # Simulate network delay and response
        await asyncio.sleep(0.1)
        
        # Return mock memes for demonstration
        mock_memes = [
            {
                "content": f"Federated meme from {peer_id}",
                "metadata": {"domain": "federated", "generation": 1},
                "vector": {"fitness_score": 0.8, "dimension": 384},
                "sync_timestamp": time.time()
            }
        ]
        
        self.stats["memes_received"] += len(mock_memes)
        return mock_memes
    
    async def _register_with_discovery(self):
        """Register this node with discovery servers."""
        node_info = {
            "node_id": self.node_id,
            "address": self.listen_address,
            "port": self.listen_port,
            "capabilities": ["meme_sync", "evolution", "entanglement"],
            "version": "0.1.0"
        }
        
        for server_addr in self.discovery_servers:
            try:
                # Placeholder for actual registration
                self.logger.info(f"Registered with discovery server {server_addr}")
            except Exception as e:
                self.logger.warning(f"Failed to register with {server_addr}: {e}")
    
    async def _query_discovery_server(self, server_addr: str) -> List[FederatedNode]:
        """Query discovery server for available nodes."""
        # Placeholder implementation
        return []
    
    async def _local_network_scan(self) -> List[FederatedNode]:
        """Scan local network for federated nodes."""
        # Placeholder for local discovery
        return []
    
    async def _health_check_peer(self, channel, peer_id: str) -> bool:
        """Perform health check on peer connection."""
        try:
            # Placeholder for gRPC health check
            await asyncio.sleep(0.05)  # Simulate network round trip
            return True
        except:
            return False
    
    async def _peer_discovery_loop(self):
        """Background task for continuous peer discovery."""
        while self.is_running:
            try:
                await self.discover_peers()
                await asyncio.sleep(60)  # Discover every minute
            except Exception as e:
                self.logger.error(f"Peer discovery error: {e}")
                await asyncio.sleep(30)  # Retry after 30 seconds
    
    async def _health_check_loop(self):
        """Background task for peer health monitoring."""
        while self.is_running:
            try:
                disconnected_peers = []
                
                for peer_id in list(self.connected_peers):
                    if peer_id in self.known_nodes:
                        node = self.known_nodes[peer_id]
                        channel = grpc.aio.insecure_channel(f"{node.address}:{node.port}")
                        
                        if not await self._health_check_peer(channel, peer_id):
                            disconnected_peers.append(peer_id)
                        else:
                            node.last_seen = time.time()
                
                # Remove disconnected peers
                for peer_id in disconnected_peers:
                    self.connected_peers.discard(peer_id)
                    self.logger.warning(f"Peer {peer_id} disconnected")
                
                await asyncio.sleep(30)  # Health check every 30 seconds
                
            except Exception as e:
                self.logger.error(f"Health check error: {e}")
                await asyncio.sleep(60)
    
    def get_network_status(self) -> Dict[str, Any]:
        """Get comprehensive network status."""
        return {
            "node_info": {
                "node_id": self.node_id,
                "address": f"{self.listen_address}:{self.listen_port}",
                "running": self.is_running,
                "uptime_seconds": time.time() - self.stats["uptime_start"]
            },
            "network_state": {
                "known_nodes": len(self.known_nodes),
                "connected_peers": len(self.connected_peers),
                "pending_requests": len(self.pending_requests),
                "sync_history_count": len(self.sync_history)
            },
            "statistics": self.stats.copy(),
            "peers": [
                {
                    "node_id": node.node_id,
                    "address": f"{node.address}:{node.port}",
                    "status": node.status,
                    "trust_score": node.trust_score,
                    "last_seen": node.last_seen
                }
                for node in self.known_nodes.values()
            ]
        }
    
    async def disconnect(self):
        """Cleanly disconnect from the federated network."""
        self.logger.info("Disconnecting from federated network")
        
        # Stop background tasks
        self.is_running = False
        
        # Close peer connections
        self.connected_peers.clear()
        
        # Stop server
        await self.stop_server()
        
        self.logger.info("Federated client disconnected")
