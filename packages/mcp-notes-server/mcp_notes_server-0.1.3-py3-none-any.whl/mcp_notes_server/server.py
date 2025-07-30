#!/usr/bin/env python3
"""
MCP Notes Server - A note-taking server for developers implementing project features.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.types import (
    Tool,
    TextContent,
    Resource,
    ResourceContents,
    ResourceTemplate,
)
from pydantic import BaseModel, Field


class Note(BaseModel):
    """Model for a single note."""
    id: str
    feature: str
    content: str
    timestamp: datetime
    tags: List[str] = Field(default_factory=list)
    status: str = "in_progress"  # in_progress, completed, blocked
    priority: str = "medium"  # low, medium, high


class NotesStorage:
    """Handles storage and retrieval of notes."""
    
    def __init__(self, storage_path: Optional[Path] = None):
        self.storage_path = storage_path or Path.home() / ".mcp_notes" / "notes.json"
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.notes: Dict[str, Note] = self._load_notes()
    
    def _load_notes(self) -> Dict[str, Note]:
        """Load notes from storage."""
        if self.storage_path.exists():
            try:
                with open(self.storage_path, 'r') as f:
                    data = json.load(f)
                    return {k: Note(**v) for k, v in data.items()}
            except Exception as e:
                print(f"Error loading notes: {e}", file=sys.stderr)
        return {}
    
    def _save_notes(self):
        """Save notes to storage."""
        try:
            data = {k: v.model_dump(mode='json') for k, v in self.notes.items()}
            with open(self.storage_path, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving notes: {e}", file=sys.stderr)
    
    def add_note(self, feature: str, content: str, tags: List[str] = None, 
                 status: str = "in_progress", priority: str = "medium") -> Note:
        """Add a new note."""
        note_id = f"note_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        note = Note(
            id=note_id,
            feature=feature,
            content=content,
            timestamp=datetime.now(),
            tags=tags or [],
            status=status,
            priority=priority
        )
        self.notes[note_id] = note
        self._save_notes()
        return note
    
    def update_note(self, note_id: str, **kwargs) -> Optional[Note]:
        """Update an existing note."""
        if note_id in self.notes:
            note = self.notes[note_id]
            for key, value in kwargs.items():
                if hasattr(note, key) and value is not None:
                    setattr(note, key, value)
            self._save_notes()
            return note
        return None
    
    def delete_note(self, note_id: str) -> bool:
        """Delete a note."""
        if note_id in self.notes:
            del self.notes[note_id]
            self._save_notes()
            return True
        return False
    
    def get_notes(self, feature: Optional[str] = None, 
                  tags: Optional[List[str]] = None,
                  status: Optional[str] = None) -> List[Note]:
        """Get notes with optional filtering."""
        notes = list(self.notes.values())
        
        if feature:
            notes = [n for n in notes if feature.lower() in n.feature.lower()]
        
        if tags:
            notes = [n for n in notes if any(tag in n.tags for tag in tags)]
        
        if status:
            notes = [n for n in notes if n.status == status]
        
        return sorted(notes, key=lambda x: x.timestamp, reverse=True)


class NotesServer:
    """MCP Server for note-taking functionality."""
    
    def __init__(self):
        self.server = Server("mcp-notes-server")
        self.storage = NotesStorage()
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Set up all server handlers."""
        
        @self.server.list_tools()
        async def handle_list_tools() -> List[Tool]:
            """List available tools."""
            return [
                Tool(
                    name="add_note",
                    description="Add a new development note for a feature",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "feature": {
                                "type": "string",
                                "description": "The feature being implemented"
                            },
                            "content": {
                                "type": "string",
                                "description": "The note content"
                            },
                            "tags": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Optional tags for categorization"
                            },
                            "status": {
                                "type": "string",
                                "enum": ["in_progress", "completed", "blocked"],
                                "description": "Status of the feature",
                                "default": "in_progress"
                            },
                            "priority": {
                                "type": "string",
                                "enum": ["low", "medium", "high"],
                                "description": "Priority level",
                                "default": "medium"
                            }
                        },
                        "required": ["feature", "content"]
                    }
                ),
                Tool(
                    name="list_notes",
                    description="List notes with optional filtering",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "feature": {
                                "type": "string",
                                "description": "Filter by feature name (partial match)"
                            },
                            "tags": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Filter by tags"
                            },
                            "status": {
                                "type": "string",
                                "enum": ["in_progress", "completed", "blocked"],
                                "description": "Filter by status"
                            }
                        }
                    }
                ),
                Tool(
                    name="update_note",
                    description="Update an existing note",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "note_id": {
                                "type": "string",
                                "description": "The ID of the note to update"
                            },
                            "content": {
                                "type": "string",
                                "description": "New content (optional)"
                            },
                            "status": {
                                "type": "string",
                                "enum": ["in_progress", "completed", "blocked"],
                                "description": "New status (optional)"
                            },
                            "priority": {
                                "type": "string",
                                "enum": ["low", "medium", "high"],
                                "description": "New priority (optional)"
                            },
                            "tags": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "New tags (optional)"
                            }
                        },
                        "required": ["note_id"]
                    }
                ),
                Tool(
                    name="delete_note",
                    description="Delete a note",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "note_id": {
                                "type": "string",
                                "description": "The ID of the note to delete"
                            }
                        },
                        "required": ["note_id"]
                    }
                ),
                Tool(
                    name="export_notes",
                    description="Export notes to markdown format",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "feature": {
                                "type": "string",
                                "description": "Filter by feature before export"
                            },
                            "format": {
                                "type": "string",
                                "enum": ["markdown", "json"],
                                "description": "Export format",
                                "default": "markdown"
                            }
                        }
                    }
                )
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Any) -> List[TextContent]:
            """Handle tool calls."""
            
            if name == "add_note":
                note = self.storage.add_note(
                    feature=arguments["feature"],
                    content=arguments["content"],
                    tags=arguments.get("tags", []),
                    status=arguments.get("status", "in_progress"),
                    priority=arguments.get("priority", "medium")
                )
                return [TextContent(
                    type="text",
                    text=f"Note added successfully!\nID: {note.id}\nFeature: {note.feature}\nStatus: {note.status}"
                )]
            
            elif name == "list_notes":
                notes = self.storage.get_notes(
                    feature=arguments.get("feature"),
                    tags=arguments.get("tags"),
                    status=arguments.get("status")
                )
                
                if not notes:
                    return [TextContent(type="text", text="No notes found.")]
                
                result = []
                for note in notes:
                    result.append(
                        f"**[{note.id}] {note.feature}**\n"
                        f"Status: {note.status} | Priority: {note.priority}\n"
                        f"Tags: {', '.join(note.tags) if note.tags else 'None'}\n"
                        f"Time: {note.timestamp.strftime('%Y-%m-%d %H:%M')}\n"
                        f"Content: {note.content}\n"
                        f"{'─' * 40}"
                    )
                
                return [TextContent(type="text", text="\n".join(result))]
            
            elif name == "update_note":
                note = self.storage.update_note(
                    note_id=arguments["note_id"],
                    content=arguments.get("content"),
                    status=arguments.get("status"),
                    priority=arguments.get("priority"),
                    tags=arguments.get("tags")
                )
                
                if note:
                    return [TextContent(
                        type="text",
                        text=f"Note {note.id} updated successfully!"
                    )]
                else:
                    return [TextContent(
                        type="text",
                        text=f"Note {arguments['note_id']} not found."
                    )]
            
            elif name == "delete_note":
                if self.storage.delete_note(arguments["note_id"]):
                    return [TextContent(
                        type="text",
                        text=f"Note {arguments['note_id']} deleted successfully!"
                    )]
                else:
                    return [TextContent(
                        type="text",
                        text=f"Note {arguments['note_id']} not found."
                    )]
            
            elif name == "export_notes":
                notes = self.storage.get_notes(feature=arguments.get("feature"))
                format_type = arguments.get("format", "markdown")
                
                if format_type == "json":
                    export_data = [n.model_dump(mode='json') for n in notes]
                    return [TextContent(
                        type="text",
                        text=json.dumps(export_data, indent=2, default=str)
                    )]
                else:  # markdown
                    md_content = ["# Development Notes\n"]
                    
                    # Group by feature
                    features = {}
                    for note in notes:
                        if note.feature not in features:
                            features[note.feature] = []
                        features[note.feature].append(note)
                    
                    for feature, feature_notes in features.items():
                        md_content.append(f"\n## {feature}\n")
                        for note in feature_notes:
                            md_content.append(
                                f"### {note.timestamp.strftime('%Y-%m-%d %H:%M')} "
                                f"[{note.status.upper()}] [{note.priority.upper()}]\n"
                                f"{note.content}\n"
                            )
                            if note.tags:
                                md_content.append(f"**Tags:** {', '.join(note.tags)}\n")
                    
                    return [TextContent(type="text", text="\n".join(md_content))]
            
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
        
        @self.server.list_resources()
        async def handle_list_resources() -> List[Resource]:
            """List available resources."""
            return [
                Resource(
                    uri="notes://all",
                    name="All Notes",
                    description="View all development notes",
                    mimeType="application/json"
                )
            ]
        
        @self.server.read_resource()
        async def handle_read_resource(uri: str) -> ResourceContents:
            """Read resource contents."""
            if uri == "notes://all":
                notes = self.storage.get_notes()
                data = {
                    "total": len(notes),
                    "notes": [n.model_dump(mode='json') for n in notes]
                }
                return ResourceContents(
                    uri=uri,
                    mimeType="application/json",
                    text=json.dumps(data, indent=2, default=str)
                )
            raise ValueError(f"Unknown resource: {uri}")
    
    async def run(self):
        """Run the server."""
        async with self.server.run_stdio():
            await self.server.wait_for_shutdown()


def main():
    """Main entry point."""
    import asyncio
    
    server = NotesServer()
    asyncio.run(server.run())


if __name__ == "__main__":
    main()