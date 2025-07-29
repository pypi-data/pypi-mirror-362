"""
Taskspace storage - Business logic layer for taskspace management.

Handles business concepts like execution plans, messages, artifacts, etc.
Uses the filesystem abstraction layer underneath.
"""

import json
import uuid
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Union

from .interfaces import FileStorage, StorageResult
from ..utils.logger import get_logger

logger = get_logger(__name__)


class TaskspaceStorage:
    """
    Taskspace storage that handles business concepts.

    Manages execution plans, messages, artifacts, and other taskspace
    content using a filesystem abstraction underneath.
    """

    def __init__(
        self,
        taskspace_path: Union[str, Path] = None,
        file_storage: FileStorage = None,
        use_git_artifacts: bool = True,
        base_path: Union[str, Path] = None,
        task_id: str = None,
        user_id: str = None
    ):
        # Support both old API (taskspace_path) and new API (base_path + task_id + optional user_id)
        if taskspace_path is not None:
            # Old API: taskspace_path directly
            self.taskspace_path = Path(taskspace_path)
        elif base_path is not None and task_id is not None:
            # New API: base_path + optional user_id + task_id for taskspace isolation
            if user_id is not None:
                # Multi-tenant: taskspace/{user_id}/{task_id}
                self.taskspace_path = Path(base_path) / user_id / task_id
                self.user_id = user_id
            else:
                # Single-tenant (backward compatibility): taskspace/{task_id}
                self.taskspace_path = Path(base_path) / task_id
            self.task_id = task_id
        else:
            raise ValueError("Either taskspace_path or (base_path + task_id) must be provided")

        self.file_storage = file_storage
        self.use_git_artifacts = use_git_artifacts

        # Initialize artifact storage
        self._init_artifact_storage()

        logger.info(f"TaskspaceStorage initialized: {self.taskspace_path} (Git artifacts: {use_git_artifacts})")

    def _init_artifact_storage(self):
        """Initialize artifact storage (Git-based or simple file-based)."""

        # If file_storage is already a GitArtifactStorage, use it for artifacts too
        if hasattr(self.file_storage, 'store_artifact'):
            self.artifact_storage = self.file_storage
            logger.info("Using provided GitArtifactStorage for artifacts")
            return

        # Otherwise, initialize separate artifact storage if requested
        if self.use_git_artifacts:
            try:
                from .git_storage import GitArtifactStorage

                # Use new API if task_id is available, otherwise fall back to old API
                if hasattr(self, 'task_id'):
                    # New API: use task_id for taskspace isolation
                    base_path = self.taskspace_path.parent
                    self.artifact_storage = GitArtifactStorage(base_path=base_path, task_id=self.task_id)
                else:
                    # Old API: use taskspace_path directly
                    self.artifact_storage = GitArtifactStorage(taskspace_path=self.taskspace_path)

                logger.info("Using Git-based artifact storage")
            except ImportError:
                logger.warning("GitPython not available, falling back to simple artifact storage")
                self.artifact_storage = None
                self.use_git_artifacts = False
        else:
            self.artifact_storage = None

    async def _ensure_directory(self, path: str) -> None:
        """Ensure a directory exists."""
        if not await self.file_storage.exists(path):
            await self.file_storage.create_directory(path)

    def get_taskspace_path(self) -> Path:
        """Get the taskspace path."""
        return self.taskspace_path

    # Artifact Management
    async def store_artifact(
        self,
        name: str,
        content: Union[str, bytes],
        content_type: str = "text/plain",
        metadata: Optional[Dict[str, Any]] = None,
        commit_message: Optional[str] = None
    ) -> StorageResult:
        """Store an artifact with versioning."""
        if self.use_git_artifacts and self.artifact_storage:
            # Use Git-based storage
            return await self.artifact_storage.store_artifact(
                name, content, content_type, metadata, commit_message
            )
        else:
            # Fall back to simple file-based versioning
            return await self._store_artifact_simple(name, content, content_type, metadata)

    async def get_artifact(self, name: str, version: Optional[str] = None) -> Optional[str]:
        """Get artifact content."""
        if self.use_git_artifacts and self.artifact_storage:
            return await self.artifact_storage.get_artifact(name, version)
        else:
            return await self._get_artifact_simple(name, version)

    async def list_artifacts(self) -> List[Dict[str, Any]]:
        """List all artifacts."""
        if self.use_git_artifacts and self.artifact_storage:
            return await self.artifact_storage.list_artifacts()
        else:
            return await self._list_artifacts_simple()

    async def get_artifact_versions(self, name: str) -> List[str]:
        """Get all versions of an artifact."""
        if self.use_git_artifacts and self.artifact_storage:
            return await self.artifact_storage.get_artifact_versions(name)
        else:
            return await self._get_artifact_versions_simple(name)

    async def delete_artifact(self, name: str, version: Optional[str] = None) -> StorageResult:
        """Delete an artifact or specific version."""
        if self.use_git_artifacts and self.artifact_storage:
            return await self.artifact_storage.delete_artifact(name, version)
        else:
            return await self._delete_artifact_simple(name, version)

    async def get_artifact_diff(self, name: str, version1: str, version2: str) -> Optional[str]:
        """Get diff between two versions of an artifact (Git only)."""
        if self.use_git_artifacts and self.artifact_storage:
            return await self.artifact_storage.get_artifact_diff(name, version1, version2)
        else:
            return "Diff not available with simple artifact storage. Enable Git artifacts for diff support."

    # Simple artifact storage fallback methods
    async def _store_artifact_simple(
        self,
        name: str,
        content: Union[str, bytes],
        content_type: str = "text/plain",
        metadata: Optional[Dict[str, Any]] = None
    ) -> StorageResult:
        """Store artifact using simple file-based versioning."""
        try:
            await self._ensure_directory("artifacts")

            # Generate version ID
            version = datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + str(uuid.uuid4())[:8]

            # Create artifact metadata
            artifact_metadata = {
                "name": name,
                "version": version,
                "content_type": content_type,
                "created_at": datetime.now().isoformat(),
                "size": len(content) if isinstance(content, (str, bytes)) else 0,
                "metadata": metadata or {}
            }

            # Store artifact content
            artifact_path = f"artifacts/{name}_{version}.data"
            if isinstance(content, str):
                result = await self.file_storage.write_text(artifact_path, content)
            else:
                result = await self.file_storage.write_bytes(artifact_path, content)

            if not result.success:
                return result

            # Store artifact metadata
            metadata_path = f"artifacts/{name}_{version}.meta"
            metadata_result = await self.file_storage.write_text(
                metadata_path,
                json.dumps(artifact_metadata, indent=2)
            )

            if not metadata_result.success:
                return metadata_result

            # Update artifact index
            await self._update_artifact_index(name, version, artifact_metadata)

            return StorageResult(
                success=True,
                path=artifact_path,
                size=result.size,
                data={"version": version},
                metadata=artifact_metadata
            )

        except Exception as e:
            logger.error(f"Failed to store artifact {name}: {e}")
            return StorageResult(
                success=False,
                error=str(e)
            )

    async def _get_artifact_simple(self, name: str, version: Optional[str] = None) -> Optional[str]:
        """Get artifact using simple storage."""
        try:
            if version is None:
                # Get latest version
                versions = await self._get_artifact_versions_simple(name)
                if not versions:
                    return None
                version = versions[-1]  # Latest version

            artifact_path = f"artifacts/{name}_{version}.data"

            if not await self.file_storage.exists(artifact_path):
                return None

            return await self.file_storage.read_text(artifact_path)

        except Exception as e:
            logger.error(f"Failed to get artifact {name}: {e}")
            return None

    async def _list_artifacts_simple(self) -> List[Dict[str, Any]]:
        """List artifacts using simple storage."""
        try:
            await self._ensure_directory("artifacts")

            index_path = "artifacts/.index"
            if not await self.file_storage.exists(index_path):
                return []

            index_content = await self.file_storage.read_text(index_path)
            index_data = json.loads(index_content)

            artifacts = []
            for name, versions in index_data.items():
                for version_info in versions:
                    artifacts.append(version_info)

            # Sort by creation time (newest first)
            artifacts.sort(key=lambda x: x.get("created_at", ""), reverse=True)
            return artifacts

        except Exception as e:
            logger.error(f"Failed to list artifacts: {e}")
            return []

    async def _get_artifact_versions_simple(self, name: str) -> List[str]:
        """Get artifact versions using simple storage."""
        try:
            await self._ensure_directory("artifacts")

            index_path = "artifacts/.index"
            if not await self.file_storage.exists(index_path):
                return []

            index_content = await self.file_storage.read_text(index_path)
            index_data = json.loads(index_content)

            if name not in index_data:
                return []

            versions = [v["version"] for v in index_data[name]]
            versions.sort()  # Sort chronologically
            return versions

        except Exception as e:
            logger.error(f"Failed to get versions for artifact {name}: {e}")
            return []

    async def _delete_artifact_simple(self, name: str, version: Optional[str] = None) -> StorageResult:
        """Delete artifact using simple storage."""
        try:
            if version is None:
                # Delete all versions
                versions = await self._get_artifact_versions_simple(name)
                for v in versions:
                    await self._delete_artifact_version(name, v)

                # Remove from index
                await self._remove_from_artifact_index(name)

                return StorageResult(
                    success=True,
                    metadata={"deleted_versions": len(versions)}
                )
            else:
                # Delete specific version
                success = await self._delete_artifact_version(name, version)
                if success:
                    await self._remove_from_artifact_index(name, version)
                    return StorageResult(success=True)
                else:
                    return StorageResult(success=False, error="Version not found")

        except Exception as e:
            logger.error(f"Failed to delete artifact {name}: {e}")
            return StorageResult(
                success=False,
                error=str(e)
            )

    # Message Management
    async def store_message(self, message: Dict[str, Any], conversation_id: str = "default") -> StorageResult:
        """Store a conversation message."""
        try:
            await self._ensure_directory("messages")

            timestamp = datetime.now().isoformat()
            message_id = str(uuid.uuid4())[:8]

            message_data = {
                "id": message_id,
                "conversation_id": conversation_id,
                "timestamp": timestamp,
                **message
            }

            message_path = f"messages/{conversation_id}_{timestamp}_{message_id}.json"
            result = await self.file_storage.write_text(
                message_path,
                json.dumps(message_data, indent=2)
            )

            return result

        except Exception as e:
            logger.error(f"Failed to store message: {e}")
            return StorageResult(success=False, error=str(e))

    async def get_conversation_history(self, conversation_id: str = "default") -> List[Dict[str, Any]]:
        """Get conversation history."""
        try:
            await self._ensure_directory("messages")

            files = await self.file_storage.list_directory("messages")
            conversation_files = [
                f for f in files
                if f.path.startswith(f"messages/{conversation_id}_") and f.path.endswith(".json")
            ]

            messages = []
            for file_info in conversation_files:
                try:
                    content = await self.file_storage.read_text(file_info.path)
                    message = json.loads(content)
                    messages.append(message)
                except Exception as e:
                    logger.warning(f"Failed to read message file {file_info.path}: {e}")

            # Sort by timestamp
            messages.sort(key=lambda x: x.get("timestamp", ""))
            return messages

        except Exception as e:
            logger.error(f"Failed to get conversation history: {e}")
            return []

    # Plan Management
    async def store_plan(self, plan: Dict[str, Any]) -> StorageResult:
        """Store the taskspace plan as plan.json."""
        try:
            result = await self.file_storage.write_text(
                "plan.json",
                json.dumps(plan, indent=2)
            )
            return result

        except Exception as e:
            logger.error(f"Failed to store plan: {e}")
            return StorageResult(success=False, error=str(e))

    async def get_plan(self) -> Optional[Dict[str, Any]]:
        """Get the taskspace plan from plan.json."""
        try:
            if not await self.file_storage.exists("plan.json"):
                return None

            content = await self.file_storage.read_text("plan.json")
            return json.loads(content)

        except Exception as e:
            logger.error(f"Failed to get plan: {e}")
            return None

    # Directory Management
    async def list_directory(self, path: str = "") -> Dict[str, Any]:
        """List contents of a directory in the taskspace."""
        try:
            # Use direct filesystem operations for simplicity
            full_path = self.taskspace_path / path if path else self.taskspace_path
            if not full_path.exists():
                return {
                    "success": False,
                    "error": f"Directory '{path}' not found"
                }

            items = []
            for item in full_path.iterdir():
                items.append({
                    "name": item.name,
                    "type": "directory" if item.is_dir() else "file",
                    "size": item.stat().st_size if item.is_file() else None
                })

            return {
                "success": True,
                "path": path,
                "items": items,
                "count": len(items)
            }
        except Exception as e:
            logger.error(f"Error listing directory '{path}': {e}")
            return {
                "success": False,
                "error": str(e)
            }

    # Taskspace Summary
    async def get_taskspace_summary(self) -> Dict[str, Any]:
        """Get a summary of taskspace contents."""
        try:
            files = await self.file_storage.list_directory()
            artifacts = await self.list_artifacts()

            total_files = len(files)
            total_size = sum(f.size for f in files)
            total_artifacts = len(artifacts)

            return {
                "taskspace_path": str(self.taskspace_path),
                "total_files": total_files,
                "total_size_bytes": total_size,
                "total_artifacts": total_artifacts,
                "artifact_storage": "git" if self.use_git_artifacts else "simple",
                "files": [{"path": f.path, "size": f.size} for f in files[:10]],
                "artifacts": [{"name": a["name"], "version": a["version"]} for a in artifacts[:10]]
            }

        except Exception as e:
            logger.error(f"Failed to get taskspace summary: {e}")
            return {
                "taskspace_path": str(self.taskspace_path),
                "error": str(e)
            }

    # Helper methods for simple storage
    async def _update_artifact_index(self, name: str, version: str, metadata: Dict[str, Any]):
        """Update the artifact index."""
        try:
            index_path = "artifacts/.index"

            # Load existing index
            index_data = {}
            if await self.file_storage.exists(index_path):
                index_content = await self.file_storage.read_text(index_path)
                index_data = json.loads(index_content)

            # Add new artifact version
            if name not in index_data:
                index_data[name] = []

            index_data[name].append(metadata)

            # Save updated index
            await self.file_storage.write_text(
                index_path,
                json.dumps(index_data, indent=2)
            )

        except Exception as e:
            logger.error(f"Failed to update artifact index: {e}")

    async def _remove_from_artifact_index(self, name: str, version: Optional[str] = None):
        """Remove artifact from index."""
        try:
            index_path = "artifacts/.index"

            if not await self.file_storage.exists(index_path):
                return

            index_content = await self.file_storage.read_text(index_path)
            index_data = json.loads(index_content)

            if name not in index_data:
                return

            if version is None:
                # Remove entire artifact
                del index_data[name]
            else:
                # Remove specific version
                index_data[name] = [
                    v for v in index_data[name]
                    if v.get("version") != version
                ]

                # Remove artifact if no versions left
                if not index_data[name]:
                    del index_data[name]

            # Save updated index
            await self.file_storage.write_text(
                index_path,
                json.dumps(index_data, indent=2)
            )

        except Exception as e:
            logger.error(f"Failed to remove from artifact index: {e}")

    async def _delete_artifact_version(self, name: str, version: str) -> bool:
        """Delete a specific artifact version."""
        try:
            artifact_path = f"artifacts/{name}_{version}.data"
            metadata_path = f"artifacts/{name}_{version}.meta"

            success = True

            if await self.file_storage.exists(artifact_path):
                result = await self.file_storage.delete(artifact_path)
                success = success and result.success

            if await self.file_storage.exists(metadata_path):
                result = await self.file_storage.delete(metadata_path)
                success = success and result.success

            return success

        except Exception as e:
            logger.error(f"Failed to delete artifact version {name}_{version}: {e}")
            return False
