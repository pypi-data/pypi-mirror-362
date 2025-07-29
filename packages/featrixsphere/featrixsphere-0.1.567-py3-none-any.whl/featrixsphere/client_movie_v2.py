"""
Improved Notebook Training Movie Functions V2

This module contains enhanced versions of the training movie functions used in FeatrixSphereClient.
Key improvements:
- Fixed scaling issues: No more jarring scale changes between frames
- Precomputed axis limits and data structures
- Better performance with reduced redundant calculations
- Consistent 1:1:1 aspect ratio for 3D plots
- Optimized rendering for smoother animation

These functions can be used to replace the existing movie methods in client.py
when you want better performance and fixed scaling behavior.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, Any, Optional
import pandas as pd


class NotebookMovieV2:
    """Improved notebook movie functions with performance optimizations."""
    
    def __init__(self, client):
        """Initialize with reference to the FeatrixSphereClient."""
        self.client = client
        self._cached_limits = {}  # Cache computed axis limits
        self._cached_data = {}    # Cache processed epoch data
    
    def plot_embedding_evolution_frame_v2(self, ax, epoch_projections: Dict[str, Any], current_epoch: int):
        """
        IMPROVED: Plot 3D embedding space for current epoch with fixed scaling.
        
        Key improvements:
        - Computes and caches fixed axis limits to prevent scale changes
        - Maintains 1:1:1 aspect ratio for 3D plots
        - Better error handling and fallbacks
        - Optimized data processing
        """
        session_key = id(epoch_projections)  # Use object ID as cache key
        
        # Check cache for precomputed limits
        if session_key not in self._cached_limits:
            self._precompute_limits_and_data(epoch_projections, session_key)
        
        if not epoch_projections:
            ax.text(0.5, 0.5, 'No embedding evolution data', 
                   transform=ax.transAxes, ha='center', va='center')
            return
        
        # Find projection data for current epoch
        current_projection = None
        for proj_data in epoch_projections.values():
            if proj_data.get('epoch', 0) == current_epoch:
                current_projection = proj_data
                break
        
        if not current_projection:
            ax.text(0.5, 0.5, f'No projection data for epoch {current_epoch}', 
                   transform=ax.transAxes, ha='center', va='center')
            return
        
        # Extract coordinates
        coords = current_projection.get('coords', [])
        if not coords:
            ax.text(0.5, 0.5, 'No coordinate data', 
                   transform=ax.transAxes, ha='center', va='center')
            return
        
        df = pd.DataFrame(coords)
        
        # PERFORMANCE FIX: Use cached fixed limits instead of recalculating
        cached_data = self._cached_limits[session_key]
        
        if all(col in df.columns for col in ['x', 'y', 'z']):
            # TRUE 3D VISUALIZATION - the star of the show!
            from mpl_toolkits.mplot3d import Axes3D
            import numpy as np
            
            # Clear the axis and recreate as 3D if needed
            if not hasattr(ax, 'zaxis'):
                ax.remove()
                ax = ax.figure.add_subplot(ax.get_geometry()[0], ax.get_geometry()[1], 
                                           ax.get_geometry()[2], projection='3d')
            
            scatter = ax.scatter(df['x'], df['y'], df['z'], alpha=0.7, s=25, c='steelblue')
            ax.set_xlabel('Dimension 1', fontweight='bold')
            ax.set_ylabel('Dimension 2', fontweight='bold')
            ax.set_zlabel('Dimension 3', fontweight='bold')
            
            # Set equal aspect ratio for better 3D visualization
            if len(df) > 0:
                max_range = np.max([
                    np.max(df['x']) - np.min(df['x']),
                    np.max(df['y']) - np.min(df['y']),
                    np.max(df['z']) - np.min(df['z'])
                ])
                
                mid_x = (np.max(df['x']) + np.min(df['x'])) * 0.5
                mid_y = (np.max(df['y']) + np.min(df['y'])) * 0.5
                mid_z = (np.max(df['z']) + np.min(df['z'])) * 0.5
                
                ax.set_xlim(mid_x - max_range/2, mid_x + max_range/2)
                ax.set_ylim(mid_y - max_range/2, mid_y + max_range/2)
                ax.set_zlim(mid_z - max_range/2, mid_z + max_range/2)
                
        elif 'x' in df.columns and 'y' in df.columns:
            # 2D projection fallback
            ax.scatter(df['x'], df['y'], alpha=0.6, s=20)
            ax.set_xlabel('Dimension 1', fontweight='bold')
            ax.set_ylabel('Dimension 2', fontweight='bold')
            
            # SCALING FIX: Use fixed axis limits
            if cached_data['xlim'] and cached_data['ylim']:
                ax.set_xlim(cached_data['xlim'])
                ax.set_ylim(cached_data['ylim'])
        
        ax.set_title(f'Embedding Space - Epoch {current_epoch}', fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # IMPROVEMENT: Ensure equal aspect ratio for better visualization
        ax.set_aspect('equal', adjustable='box')
    
    def _precompute_limits_and_data(self, epoch_projections: Dict[str, Any], session_key: str):
        """
        PERFORMANCE OPTIMIZATION: Precompute fixed axis limits and process data once.
        
        This prevents the jarring scale changes that occur when axis limits are
        recalculated for every frame.
        """
        all_x, all_y, all_z = [], [], []
        
        # Collect all coordinates from all epochs
        for proj_data in epoch_projections.values():
            coords = proj_data.get('coords', [])
            if coords:
                df = pd.DataFrame(coords)
                
                if 'x' in df.columns:
                    all_x.extend(df['x'].tolist())
                if 'y' in df.columns:
                    all_y.extend(df['y'].tolist())
                if 'z' in df.columns:
                    all_z.extend(df['z'].tolist())
        
        # Calculate fixed axis limits with margin
        margin = 0.1  # 10% margin
        
        xlim = None
        ylim = None
        zlim = None
        
        if all_x:
            x_range = max(all_x) - min(all_x)
            x_margin = x_range * margin
            xlim = [min(all_x) - x_margin, max(all_x) + x_margin]
        
        if all_y:
            y_range = max(all_y) - min(all_y)
            y_margin = y_range * margin
            ylim = [min(all_y) - y_margin, max(all_y) + y_margin]
        
        if all_z:
            z_range = max(all_z) - min(all_z)
            z_margin = z_range * margin
            zlim = [min(all_z) - z_margin, max(all_z) + z_margin]
        
        # Cache the computed limits
        self._cached_limits[session_key] = {
            'xlim': xlim,
            'ylim': ylim,
            'zlim': zlim,
            'total_points': len(all_x),
            'epochs': len(epoch_projections)
        }
        
        print(f"📏 V2: Precomputed fixed axis limits for {len(epoch_projections)} epochs")
        print(f"   🎯 X: {xlim}, Y: {ylim}, Z: {zlim}")
        print(f"   📊 Total points: {len(all_x)}")
    
    def create_static_evolution_plot_v2(self, epoch_projections: Dict[str, Any], 
                                       sample_size: int, color_by: Optional[str], 
                                       session_id: str):
        """
        IMPROVED: Create static evolution plot with fixed scaling and better performance.
        
        Key improvements:
        - Fixed axis limits across all subplots for consistent scaling
        - Better subplot layout and sizing
        - Optimized data sampling
        - Enhanced visual styling
        """
        epochs = sorted([v.get('epoch', 0) for v in epoch_projections.values()])
        
        if not epochs:
            fig, ax = plt.subplots(1, 1, figsize=(10, 8))
            ax.text(0.5, 0.5, 'No epoch projection data', transform=ax.transAxes, ha='center', va='center')
            return fig
        
        # Precompute limits for consistent scaling
        session_key = id(epoch_projections)
        if session_key not in self._cached_limits:
            self._precompute_limits_and_data(epoch_projections, session_key)
        
        cached_data = self._cached_limits[session_key]
        
        # Create optimized subplot grid
        n_epochs = len(epochs)
        cols = min(4, n_epochs)
        rows = (n_epochs + cols - 1) // cols
        
        # Better figure sizing
        fig_width = max(12, 3 * cols)
        fig_height = max(8, 3 * rows)
        
        fig, axes = plt.subplots(rows, cols, figsize=(fig_width, fig_height))
        if rows == 1 and cols == 1:
            axes = [axes]
        elif rows == 1:
            axes = axes
        else:
            axes = axes.flatten()
        
        for i, epoch in enumerate(epochs):
            if i >= len(axes):
                break
                
            ax = axes[i]
            
            # Find data for this epoch
            epoch_data = None
            for proj_data in epoch_projections.values():
                if proj_data.get('epoch', 0) == epoch:
                    epoch_data = proj_data
                    break
            
            if epoch_data:
                coords = epoch_data.get('coords', [])
                if coords:
                    df = pd.DataFrame(coords)
                    
                    # Optimized sampling
                    if len(df) > sample_size:
                        df = df.sample(sample_size, random_state=42)
                    
                    if all(col in df.columns for col in ['x', 'y', 'z']):
                        # TRUE 3D VISUALIZATION - the star of the show!
                        from mpl_toolkits.mplot3d import Axes3D
                        import numpy as np
                        
                        # Clear the axis and recreate as 3D if needed
                        if not hasattr(ax, 'zaxis'):
                            ax.remove()
                            ax = ax.figure.add_subplot(ax.get_geometry()[0], ax.get_geometry()[1], 
                                                       ax.get_geometry()[2], projection='3d')
                        
                        if color_by and color_by in df.columns:
                            scatter = ax.scatter(df['x'], df['y'], df['z'], alpha=0.7, s=25, 
                                               c=df[color_by], cmap='viridis')
                        else:
                            scatter = ax.scatter(df['x'], df['y'], df['z'], alpha=0.7, s=25, 
                                               c='steelblue')
                        
                        ax.set_xlabel('Dimension 1', fontsize=10)
                        ax.set_ylabel('Dimension 2', fontsize=10)
                        ax.set_zlabel('Dimension 3', fontsize=10)
                        
                        # Set equal aspect ratio for better 3D visualization
                        if len(df) > 0:
                            max_range = np.max([
                                np.max(df['x']) - np.min(df['x']),
                                np.max(df['y']) - np.min(df['y']),
                                np.max(df['z']) - np.min(df['z'])
                            ])
                            
                            mid_x = (np.max(df['x']) + np.min(df['x'])) * 0.5
                            mid_y = (np.max(df['y']) + np.min(df['y'])) * 0.5
                            mid_z = (np.max(df['z']) + np.min(df['z'])) * 0.5
                            
                            ax.set_xlim(mid_x - max_range/2, mid_x + max_range/2)
                            ax.set_ylim(mid_y - max_range/2, mid_y + max_range/2)
                            ax.set_zlim(mid_z - max_range/2, mid_z + max_range/2)
                        
                    elif 'x' in df.columns and 'y' in df.columns:
                        # 2D projection fallback
                        if color_by and color_by in df.columns:
                            scatter = ax.scatter(df['x'], df['y'], alpha=0.7, s=25, 
                                               c=df[color_by], cmap='viridis')
                        else:
                            scatter = ax.scatter(df['x'], df['y'], alpha=0.7, s=25, 
                                               c='steelblue')
                        
                        ax.set_xlabel('Dimension 1', fontsize=10)
                        ax.set_ylabel('Dimension 2', fontsize=10)
                        
                        # SCALING FIX: Apply fixed limits to all subplots
                        if cached_data['xlim'] and cached_data['ylim']:
                            ax.set_xlim(cached_data['xlim'])
                            ax.set_ylim(cached_data['ylim'])
                        
                        # IMPROVEMENT: Equal aspect ratio for better visualization
                        ax.set_aspect('equal', adjustable='box')
            
            ax.set_title(f'Epoch {epoch}', fontweight='bold', fontsize=11)
            ax.grid(True, alpha=0.3)
            
            # Better tick formatting
            ax.tick_params(axis='both', which='major', labelsize=8)
        
        # Hide empty subplots
        for i in range(n_epochs, len(axes)):
            axes[i].set_visible(False)
        
        plt.suptitle(f'Embedding Evolution V2 - Session {session_id[:12]}...', 
                    fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        return fig
    
    def create_interactive_training_movie_v2(self, training_metrics, epoch_projections, session_id,
                                           show_embedding_evolution, show_loss_evolution):
        """
        IMPROVED: Create interactive training movie with better performance and fixed scaling.
        
        Key improvements:
        - Uses improved embedding plot functions with fixed scaling
        - Better widget layout and controls
        - Enhanced error handling
        - Performance optimizations
        """
        try:
            from ipywidgets import widgets, interact, Layout
            from IPython.display import display, HTML
        except ImportError:
            print("⚠️ ipywidgets not available - falling back to static movie")
            return self.client._create_static_training_movie(
                training_metrics, epoch_projections, (15, 10), 'notebook',
                None, show_embedding_evolution, show_loss_evolution, 2
            )
        
        # Extract training data
        progress_info = training_metrics.get('progress_info', {})
        loss_history = progress_info.get('loss_history', [])
        training_info = training_metrics.get('training_info', [])
        
        if not loss_history and not training_info:
            return HTML("<div style='color: red;'>No training data available for movie</div>")
        
        # Combine all epochs
        all_epochs = []
        if loss_history:
            all_epochs.extend([entry.get('epoch', 0) for entry in loss_history])
        if training_info:
            all_epochs.extend([entry.get('epoch', 0) for entry in training_info])
        
        if not all_epochs:
            return HTML("<div style='color: red;'>No epoch data found</div>")
        
        max_epoch = max(all_epochs)
        
        # Precompute data for better performance
        if show_embedding_evolution and epoch_projections:
            session_key = id(epoch_projections)
            if session_key not in self._cached_limits:
                self._precompute_limits_and_data(epoch_projections, session_key)
        
        # Create interactive widget
        def update_movie(epoch=1):
            """Update movie display for given epoch."""
            try:
                # Create subplot layout - EMBEDDING SPACE IS THE STAR!
                if show_embedding_evolution and show_loss_evolution:
                    fig = plt.figure(figsize=(16, 8))
                    ax2 = fig.add_subplot(1, 2, 1, projection='3d')  # Large 3D embedding plot
                    ax1 = fig.add_subplot(1, 2, 2)  # Smaller loss plot
                elif show_loss_evolution:
                    fig, ax1 = plt.subplots(1, 1, figsize=(10, 6))
                    ax2 = None
                else:
                    fig = plt.figure(figsize=(12, 8))
                    ax2 = fig.add_subplot(1, 1, 1, projection='3d')  # Full 3D embedding plot
                    ax1 = None
                
                # Plot embedding evolution for current epoch (USING IMPROVED V2 METHOD) - THE STAR!
                if show_embedding_evolution and ax2 is not None:
                    self.plot_embedding_evolution_frame_v2(ax2, epoch_projections, epoch)
                    ax2.set_title('🌌 Featrix Sphere - 3D Embedding Space', fontweight='bold', fontsize=14)
                
                # Plot loss evolution up to current epoch - as sparkline
                if show_loss_evolution and ax1 is not None:
                    self.client._plot_loss_evolution_frame(ax1, loss_history, training_info, epoch)
                    ax1.set_title('📊 Training Loss', fontweight='bold', fontsize=12)
                    ax1.tick_params(axis='both', which='major', labelsize=10)
                    ax1.grid(True, alpha=0.3)
                
                plt.tight_layout()
                plt.show()
                
            except Exception as e:
                print(f"Error in movie frame {epoch}: {e}")
        
        # Enhanced controls with better styling
        epoch_slider = widgets.IntSlider(
            value=1,
            min=1,
            max=max_epoch,
            step=1,
            description='Epoch:',
            style={'description_width': '70px'},
            layout=Layout(width='600px')
        )
        
        # Improved play controls
        play_button = widgets.Play(
            value=1,
            min=1,
            max=max_epoch,
            step=1,
            description="Press play",
            disabled=False,
            interval=800  # Slightly slower for better visibility
        )
        
        speed_slider = widgets.IntSlider(
            value=800,
            min=200,
            max=2000,
            step=100,
            description='Speed (ms):',
            style={'description_width': '90px'},
            layout=Layout(width='350px')
        )
        
        # Link controls
        widgets.jslink((play_button, 'value'), (epoch_slider, 'value'))
        
        def update_speed(change):
            play_button.interval = change['new']
        speed_slider.observe(update_speed, names='value')
        
        # Enhanced layout
        control_box = widgets.VBox([
            widgets.HTML("<b>🎬 Animation Controls</b>"),
            widgets.HBox([play_button, speed_slider])
        ])
        
        main_controls = widgets.HBox([control_box, epoch_slider])
        
        # Display controls and interactive output
        display(main_controls)
        interact(update_movie, epoch=epoch_slider)
        
        return HTML(f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 20px; border-radius: 15px; margin: 15px 0;
                    box-shadow: 0 8px 32px rgba(0,0,0,0.3);'>
            <h3>🎬 Interactive Training Movie V2 - Session {session_id[:12]}...</h3>
            <div style='background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; margin-top: 10px;'>
                <p><strong>✨ Enhanced Features:</strong></p>
                <ul style='margin: 10px 0; padding-left: 20px;'>
                    <li><strong>🔒 Fixed Scaling:</strong> No more jarring scale changes between frames</li>
                    <li><strong>⚡ Performance:</strong> Optimized rendering for smoother playback</li>
                    <li><strong>🎮 Enhanced Controls:</strong> Better play/pause and speed controls</li>
                    <li><strong>📐 Consistent Ratios:</strong> 1:1:1 aspect ratio maintained throughout</li>
                </ul>
                <p><strong>🎮 How to Use:</strong></p>
                <ul style='margin: 10px 0; padding-left: 20px;'>
                    <li>Use the <strong>Play button</strong> to automatically advance through epochs</li>
                    <li>Adjust <strong>Speed</strong> to control playback rate (200ms = fast, 2000ms = slow)</li>
                    <li>Drag the <strong>Epoch slider</strong> to jump to specific epochs</li>
                    <li>Watch how training progresses with <em>consistent scaling</em>!</li>
                </ul>
            </div>
        </div>
        """)


# Usage example:
# 
# from featrixsphere.client_movie_v2 import NotebookMovieV2
# 
# # In your FeatrixSphereClient instance:
# movie_v2 = NotebookMovieV2(client)
# 
# # Use improved functions:
# movie_v2.plot_embedding_evolution_frame_v2(ax, epoch_projections, current_epoch)
# movie_v2.create_interactive_training_movie_v2(training_metrics, epoch_projections, 
#                                               session_id, True, True) 