#!/usr/bin/env python3
"""
SSH Tunnel Manager - Table Widget Component
"""

from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QMenu
from PySide6.QtCore import QObject, Signal, Qt


class TunnelTableWidget(QObject):
    """Manages the tunnel table widget."""
    
    selection_changed = Signal(bool, str)  # selected, config_name
    context_menu_start = Signal(str)
    context_menu_stop = Signal(str)
    context_menu_browse_files = Signal(str)
    context_menu_browse_remote_files = Signal(str)
    context_menu_launch_rtsp = Signal(str)
    context_menu_launch_rdp = Signal(str)
    context_menu_deploy_ssh_key = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.table = None
        
    def create_table(self) -> QTableWidget:
        """Create and configure the tunnel table."""
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Name", "Status", "Type", "Local Port", "Remote", "SSH Host", "Description"
        ])
        
        # Configure headers
        header = self.table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        
        # Connect signals
        self.table.selectionModel().selectionChanged.connect(self._on_selection_changed)
        
        # Set up context menu
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_context_menu)
        
        return self.table
    
    def _on_selection_changed(self):
        """Handle selection changes."""
        selected = len(self.table.selectedItems()) > 0
        config_name = ""
        
        if selected:
            current_row = self.table.currentRow()
            if current_row >= 0:
                config_name = self.table.item(current_row, 0).text()
        
        self.selection_changed.emit(selected, config_name)
    
    def refresh_table(self, configs: dict, active_tunnels: dict):
        """Refresh table with current configurations."""
        if not self.table:
            return
            
        self.table.setRowCount(len(configs))
        
        for row, (name, config) in enumerate(configs.items()):
            # Name
            self.table.setItem(row, 0, QTableWidgetItem(name))
            
            # Status
            if name in active_tunnels:
                status_text = active_tunnels[name].get_status()
            else:
                status_text = "🔴 Stopped"
            status_item = QTableWidgetItem(status_text)
            self.table.setItem(row, 1, status_item)
            
            # Type
            self.table.setItem(row, 2, QTableWidgetItem(config.tunnel_type.title()))
            
            # Local Port
            self.table.setItem(row, 3, QTableWidgetItem(str(config.local_port)))
            
            # Remote
            if config.tunnel_type == 'dynamic':
                remote_str = "SOCKS Proxy"
            else:
                remote_str = f"{config.remote_host}:{config.remote_port}"
            self.table.setItem(row, 4, QTableWidgetItem(remote_str))
            
            # SSH Host
            ssh_str = f"{config.ssh_user}@{config.ssh_host}:{config.ssh_port}"
            self.table.setItem(row, 5, QTableWidgetItem(ssh_str))
            
            # Description
            self.table.setItem(row, 6, QTableWidgetItem(config.description))
    
    def get_selected_config_name(self) -> str:
        """Get the currently selected configuration name."""
        if not self.table:
            return ""
            
        current_row = self.table.currentRow()
        if current_row >= 0:
            return self.table.item(current_row, 0).text()
        return ""
    
    def show_context_menu(self, position):
        """Show context menu for the table."""
        from PySide6.QtGui import QCursor
        
        config_name = self.get_selected_config_name()
        if not config_name:
            return
            
        menu = QMenu()
        
        # Create menu actions
        start_action = menu.addAction("▶️ Start Tunnel")
        stop_action = menu.addAction("⏹️ Stop Tunnel")
        menu.addSeparator()
        browse_files_action = menu.addAction("📁 Browse SSH Host Files")
        browse_remote_files_action = menu.addAction("🔒 Browse Remote Host Files")
        menu.addSeparator()
        deploy_key_action = menu.addAction("📤 Deploy SSH Key...")
        menu.addSeparator()
        launch_rtsp_action = menu.addAction("📹 Launch RTSP Viewer")
        launch_rdp_action = menu.addAction("🖥️ Launch RDP Client")
        
        # Show the menu and get the selected action
        action = menu.exec(QCursor.pos())
        
        # Process the selected action
        if action == start_action:
            self.context_menu_start.emit(config_name)
        elif action == stop_action:
            self.context_menu_stop.emit(config_name)
        elif action == browse_files_action:
            self.context_menu_browse_files.emit(config_name)
        elif action == browse_remote_files_action:
            self.context_menu_browse_remote_files.emit(config_name)
        elif action == deploy_key_action:
            self.context_menu_deploy_ssh_key.emit(config_name)
        elif action == launch_rtsp_action:
            self.context_menu_launch_rtsp.emit(config_name)
        elif action == launch_rdp_action:
            self.context_menu_launch_rdp.emit(config_name)
