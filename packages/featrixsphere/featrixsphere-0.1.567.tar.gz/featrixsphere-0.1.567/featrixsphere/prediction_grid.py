
class PredictionGrid:
    """
    Grid-based prediction batch with automatic matrix building and visualization.
    
    Perfect for exploring prediction surfaces across 1-3 dimensions with automatic plotting.
    Collects all predictions and batches them for efficiency.
    
    Usage:
        # 2D parameter sweep with automatic plotting
        grid = client.predict_grid(session_id, degrees_of_freedom=2)
        
        # Fill grid (records are collected, not predicted yet)
        for i, spend in enumerate([100, 250, 500]):
            for j, campaign in enumerate(["search", "display"]):
                record = {"spend": spend, "campaign_type": campaign}
                grid.predict(record, grid_position=(i, j))
        
        # Process all predictions in one batch
        grid.process_batch()
        
        # Now plot results
        grid.plot_heatmap()  # Automatic heatmap
        grid.plot_3d()       # 3D surface plot
    """
    
    def __init__(self, session_id: str, client: 'FeatrixSphereClient', degrees_of_freedom: int, 
                 grid_shape: tuple = None, target_column: str = None):
        self.session_id = session_id
        self.client = client
        self.degrees_of_freedom = degrees_of_freedom
        self.target_column = target_column
        
        # Initialize grid matrix based on degrees of freedom
        if grid_shape:
            self.grid_shape = grid_shape
        else:
            # Default grid sizes
            default_sizes = {1: (20,), 2: (10, 10), 3: (8, 8, 8)}
            self.grid_shape = default_sizes.get(degrees_of_freedom, (10,) * degrees_of_freedom)
        
        # Initialize matrices for different data types
        self._prediction_matrix = {}  # class_name -> matrix
        self._confidence_matrix = None
        self._filled_positions = set()
        
        # Batch collection system
        self._pending_records = {}  # grid_position -> record
        self._position_to_index = {}  # grid_position -> batch_index
        self._batch_processed = False
        
        # Metadata for plotting
        self._axis_labels = [f"Param {i+1}" for i in range(degrees_of_freedom)]
        self._axis_values = [[] for _ in range(degrees_of_freedom)]
        self._colormap = 'viridis'
        
        # Statistics
        self._stats = {'predictions': 0, 'batched': 0, 'errors': 0}
        
    def predict(self, record: Dict[str, Any], grid_position: tuple) -> Dict[str, str]:
        """
        Add record to grid for batch processing.
        
        Args:
            record: Record to predict
            grid_position: Tuple of grid coordinates (i,) for 1D, (i,j) for 2D, (i,j,k) for 3D
            
        Returns:
            Status message about queuing for batch processing
        """
        if len(grid_position) != self.degrees_of_freedom:
            error_msg = f"Grid position must have {self.degrees_of_freedom} dimensions, got {len(grid_position)}"
            raise ValueError(self.client._format_error_with_version(error_msg, f"predict_grid_session_{self.session_id}"))
        
        # Check bounds
        for i, pos in enumerate(grid_position):
            if pos >= self.grid_shape[i]:
                error_msg = f"Grid position {pos} exceeds dimension {i} size {self.grid_shape[i]}"
                raise ValueError(self.client._format_error_with_version(error_msg, f"predict_grid_session_{self.session_id}"))
        
        # Store record for batch processing
        self._pending_records[grid_position] = record
        
        return {
            "status": "queued_for_batch",
            "grid_position": grid_position,
            "total_queued": len(self._pending_records),
            "message": f"Record queued at position {grid_position}. Call process_batch() to run predictions."
        }
    
    def process_batch(self, show_progress: bool = True) -> Dict[str, Any]:
        """
        Process all queued records in a single batch prediction.
        
        Args:
            show_progress: Whether to show progress during batch processing
            
        Returns:
            Batch processing results
        """
        if not self._pending_records:
            return {"message": "No records to process", "processed": 0}
        
        if self._batch_processed:
            return {"message": "Batch already processed", "processed": len(self._filled_positions)}
        
        # Convert grid records to list for batch processing
        records_list = []
        position_mapping = {}
        
        for grid_pos, record in self._pending_records.items():
            batch_index = len(records_list)
            records_list.append(record)
            position_mapping[batch_index] = grid_pos
            self._position_to_index[grid_pos] = batch_index
        
        if show_progress:
            print(f"🚀 Processing {len(records_list)} grid positions in batch...")
        
        # Use existing batch prediction system
        try:
            batch_results = self.client.predict_records(
                session_id=self.session_id,
                records=records_list,
                target_column=self.target_column,
                show_progress_bar=show_progress
            )
            
            # Process results and populate matrices
            predictions = batch_results.get('predictions', [])
            successful = 0
            failed = 0
            
            for prediction in predictions:
                row_index = prediction.get('row_index', 0)
                if row_index in position_mapping:
                    grid_pos = position_mapping[row_index]
                    
                    if 'prediction' in prediction and prediction['prediction']:
                        prediction_probs = prediction['prediction']
                        
                        # Initialize matrices if first successful prediction
                        if not self._prediction_matrix:
                            self._initialize_matrices(prediction_probs.keys())
                        
                        # Store prediction results in matrices
                        for class_name, probability in prediction_probs.items():
                            self._prediction_matrix[class_name][grid_pos] = probability
                        
                        # Store confidence (highest probability)
                        max_class = max(prediction_probs, key=prediction_probs.get)
                        confidence = prediction_probs[max_class]
                        self._confidence_matrix[grid_pos] = confidence
                        
                        # Mark position as filled
                        self._filled_positions.add(grid_pos)
                        successful += 1
                    else:
                        failed += 1
                        self._stats['errors'] += 1
            
            self._stats['predictions'] = successful
            self._stats['batched'] = len(records_list)
            self._batch_processed = True
            
            # Clear pending records
            self._pending_records.clear()
            
            if show_progress:
                print(f"✅ Batch processing complete: {successful} successful, {failed} failed")
                print(f"📊 Grid filled: {len(self._filled_positions)} positions")
            
            return {
                "processed": len(records_list),
                "successful": successful,
                "failed": failed,
                "batch_results": batch_results
            }
            
        except Exception as e:
            self._stats['errors'] += len(records_list)
            raise Exception(f"Error processing grid batch: {str(e)}")
    
    def _initialize_matrices(self, class_names: list):
        """Initialize prediction matrices for each class."""
        import numpy as np
        
        for class_name in class_names:
            self._prediction_matrix[class_name] = np.full(self.grid_shape, np.nan)
        
        self._confidence_matrix = np.full(self.grid_shape, np.nan)
    
    def set_axis_labels(self, labels: list):
        """Set custom labels for axes."""
        if len(labels) != self.degrees_of_freedom:
            raise ValueError(f"Must provide {self.degrees_of_freedom} labels")
        self._axis_labels = labels
    
    def set_axis_values(self, axis_index: int, values: list):
        """Set actual values for an axis (for proper tick labels)."""
        if axis_index >= self.degrees_of_freedom:
            raise ValueError(f"Axis index {axis_index} exceeds degrees of freedom {self.degrees_of_freedom}")
        self._axis_values[axis_index] = values
    
    def plot_heatmap(self, class_name: str = None, figsize: tuple = (10, 8), title: str = None):
        """
        Plot 2D heatmap of prediction probabilities.
        
        Args:
            class_name: Specific class to plot (default: highest probability class)
            figsize: Figure size
            title: Custom title
        """
        if self.degrees_of_freedom != 2:
            raise ValueError("Heatmap plotting only supports 2D grids")
        
        if not self._batch_processed:
            raise ValueError("Must call process_batch() first")
        
        try:
            import matplotlib.pyplot as plt
            import numpy as np
        except ImportError:
            raise ImportError("matplotlib required for plotting. Install with: pip install matplotlib")
        
        if not self._prediction_matrix:
            raise ValueError("No predictions processed yet. Call process_batch() first.")
        
        # Choose class to plot
        if class_name is None:
            # Use the class with highest average probability
            avg_probs = {}
            for cls, matrix in self._prediction_matrix.items():
                avg_probs[cls] = np.nanmean(matrix)
            class_name = max(avg_probs, key=avg_probs.get)
        
        matrix = self._prediction_matrix[class_name]
        
        # Create plot
        fig, ax = plt.subplots(figsize=figsize)
        
        # Transpose matrix for correct matplotlib display orientation
        # matplotlib imshow: first dimension = Y-axis (vertical), second = X-axis (horizontal)
        # So we need to transpose to get axis 0 on X-axis and axis 1 on Y-axis
        display_matrix = matrix.T
        
        # Plot heatmap with transposed matrix
        im = ax.imshow(display_matrix, cmap=self._colormap, aspect='auto', origin='lower')
        
        # Set labels (axis 0 = X-axis, axis 1 = Y-axis after transpose)
        ax.set_xlabel(self._axis_labels[0])
        ax.set_ylabel(self._axis_labels[1])
        
        # Set tick labels if axis values provided (adjusted for transpose)
        if self._axis_values[0]:
            ax.set_xticks(range(len(self._axis_values[0])))
            ax.set_xticklabels(self._axis_values[0])
        if self._axis_values[1]:
            ax.set_yticks(range(len(self._axis_values[1])))
            ax.set_yticklabels(self._axis_values[1])
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label(f'Probability of {class_name}')
        
        # Set title
        if title is None:
            title = f'Prediction Heatmap: {class_name}'
        ax.set_title(title)
        
        plt.tight_layout()
        return fig, ax
    
    def plot_3d(self, class_name: str = None, figsize: tuple = (12, 9), title: str = None,
                 value_filter: tuple = None, opacity: float = 0.8, show_wireframe: bool = False):
        """
        Plot 3D surface of prediction probabilities with filtering and opacity controls.
        
        Args:
            class_name: Specific class to plot (default: highest probability class)
            figsize: Figure size
            title: Custom title
            value_filter: Tuple (min_value, max_value) to filter displayed predictions
            opacity: Surface opacity (0.0 = transparent, 1.0 = opaque)
            show_wireframe: Whether to show wireframe overlay for better shape visibility
        """
        if self.degrees_of_freedom != 2:
            raise ValueError("3D surface plotting only supports 2D grids")
        
        if not self._batch_processed:
            raise ValueError("Must call process_batch() first")
        
        try:
            import matplotlib.pyplot as plt
            import numpy as np
            from mpl_toolkits.mplot3d import Axes3D
        except ImportError:
            raise ImportError("matplotlib required for plotting. Install with: pip install matplotlib")
        
        if not self._prediction_matrix:
            raise ValueError("No predictions processed yet. Call process_batch() first.")
        
        # Choose class to plot
        if class_name is None:
            avg_probs = {}
            for cls, matrix in self._prediction_matrix.items():
                avg_probs[cls] = np.nanmean(matrix)
            class_name = max(avg_probs, key=avg_probs.get)
        
        matrix = self._prediction_matrix[class_name].copy()
        
        # Apply value filter if specified
        if value_filter is not None:
            min_val, max_val = value_filter
            # Mask values outside the filter range
            mask = (matrix < min_val) | (matrix > max_val)
            matrix[mask] = np.nan
        
        # Create meshgrid with proper axis orientation
        x = np.arange(matrix.shape[0])  # axis 0
        y = np.arange(matrix.shape[1])  # axis 1
        X, Y = np.meshgrid(x, y, indexing='ij')
        
        # Create 3D plot
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111, projection='3d')
        
        # Plot surface with specified opacity
        surf = ax.plot_surface(X, Y, matrix, cmap=self._colormap, alpha=opacity)
        
        # Add wireframe if requested (helps see shape)
        if show_wireframe:
            ax.plot_wireframe(X, Y, matrix, alpha=0.3, color='black', linewidth=0.5)
        
        # Set labels (axis 0 = X-axis, axis 1 = Y-axis)
        ax.set_xlabel(self._axis_labels[0])
        ax.set_ylabel(self._axis_labels[1])
        ax.set_zlabel(f'Probability of {class_name}')
        
        # Set tick labels if axis values provided
        if self._axis_values[0]:
            ax.set_xticks(range(len(self._axis_values[0])))
            ax.set_xticklabels(self._axis_values[0])
        if self._axis_values[1]:
            ax.set_yticks(range(len(self._axis_values[1])))
            ax.set_yticklabels(self._axis_values[1])
        
        # Add colorbar
        cbar = fig.colorbar(surf, ax=ax, shrink=0.5)
        cbar.set_label(f'Probability of {class_name}')
        
        # Set title with filter info
        if title is None:
            title = f'3D Prediction Surface: {class_name}'
            if value_filter:
                title += f' (filtered: {value_filter[0]:.3f}-{value_filter[1]:.3f})'
        ax.set_title(title)
        
        return fig, ax
    
    def plot_3d_interactive(self, class_name: str = None, figsize: tuple = (12, 9)):
        """
        Create interactive 3D plot with sliders for filtering and opacity control.
        
        Perfect for Jupyter notebooks - provides sliders to explore the prediction surface.
        
        Args:
            class_name: Specific class to plot (default: highest probability class)
            figsize: Figure size
            
        Returns:
            Interactive widget (in Jupyter) or regular plot (elsewhere)
        """
        if self.degrees_of_freedom != 2:
            raise ValueError("Interactive 3D plotting only supports 2D grids")
        
        if not self._batch_processed:
            raise ValueError("Must call process_batch() first")
        
        # Check if we're in a Jupyter environment
        try:
            from IPython.display import display
            from ipywidgets import interact, FloatSlider, FloatRangeSlider, Checkbox
            import numpy as np
            jupyter_available = True
        except ImportError:
            print("⚠️ Interactive widgets require Jupyter and ipywidgets")
            print("   Install with: pip install ipywidgets")
            print("   Falling back to static 3D plot...")
            return self.plot_3d(class_name=class_name, figsize=figsize)
        
        if not self._prediction_matrix:
            raise ValueError("No predictions processed yet. Call process_batch() first.")
        
        # Choose class to plot
        if class_name is None:
            avg_probs = {}
            for cls, matrix in self._prediction_matrix.items():
                avg_probs[cls] = np.nanmean(matrix)
            class_name = max(avg_probs, key=avg_probs.get)
        
        matrix = self._prediction_matrix[class_name]
        
        # Get value range for sliders
        min_val = float(np.nanmin(matrix))
        max_val = float(np.nanmax(matrix))
        value_range = max_val - min_val
        
        print(f"🎛️ Interactive 3D Surface Explorer: {class_name}")
        print(f"   Value range: {min_val:.4f} to {max_val:.4f}")
        print("   Use sliders below to filter and adjust opacity")
        
        # Create interactive plot function
        def update_plot(value_range=(min_val, max_val), opacity=0.8, wireframe=False):
            """Update the 3D plot based on slider values."""
            import matplotlib.pyplot as plt
            plt.close('all')  # Close previous plots
            
            fig, ax = self.plot_3d(
                class_name=class_name,
                figsize=figsize,
                value_filter=value_range,
                opacity=opacity,
                show_wireframe=wireframe
            )
            
            # Show current filter stats
            filtered_matrix = matrix.copy()
            mask = (filtered_matrix < value_range[0]) | (filtered_matrix > value_range[1])
            filtered_matrix[mask] = np.nan
            
            visible_count = np.sum(~np.isnan(filtered_matrix))
            total_count = np.sum(~np.isnan(matrix))
            visible_percent = (visible_count / total_count) * 100 if total_count > 0 else 0
            
            print(f"📊 Showing {visible_count}/{total_count} points ({visible_percent:.1f}%)")
            plt.show()
        
        # Create interactive widgets
        value_slider = FloatRangeSlider(
            value=(min_val, max_val),
            min=min_val,
            max=max_val,
            step=value_range / 100,
            description='Value Filter:',
            continuous_update=False,
            style={'description_width': 'initial'}
        )
        
        opacity_slider = FloatSlider(
            value=0.8,
            min=0.1,
            max=1.0,
            step=0.1,
            description='Opacity:',
            continuous_update=False,
            style={'description_width': 'initial'}
        )
        
        wireframe_checkbox = Checkbox(
            value=False,
            description='Show Wireframe',
            style={'description_width': 'initial'}
        )
        
        # Create interactive widget
        return interact(
            update_plot,
            value_range=value_slider,
            opacity=opacity_slider,
            wireframe=wireframe_checkbox
        )
    
    def plot_1d(self, class_name: str = None, figsize: tuple = (10, 6), title: str = None):
        """
        Plot 1D line plot of prediction probabilities.
        
        Args:
            class_name: Specific class to plot (default: highest probability class)
            figsize: Figure size
            title: Custom title
        """
        if self.degrees_of_freedom != 1:
            raise ValueError("1D plotting only supports 1D grids")
        
        if not self._batch_processed:
            raise ValueError("Must call process_batch() first")
        
        try:
            import matplotlib.pyplot as plt
            import numpy as np
        except ImportError:
            raise ImportError("matplotlib required for plotting. Install with: pip install matplotlib")
        
        if not self._prediction_matrix:
            raise ValueError("No predictions processed yet. Call process_batch() first.")
        
        # Choose class to plot
        if class_name is None:
            avg_probs = {}
            for cls, matrix in self._prediction_matrix.items():
                avg_probs[cls] = np.nanmean(matrix)
            class_name = max(avg_probs, key=avg_probs.get)
        
        matrix = self._prediction_matrix[class_name]
        
        # Create plot
        fig, ax = plt.subplots(figsize=figsize)
        
        # X values
        x = self._axis_values[0] if self._axis_values[0] else range(len(matrix))
        
        # Plot line
        ax.plot(x, matrix, marker='o', linewidth=2, markersize=6)
        
        # Set labels
        ax.set_xlabel(self._axis_labels[0])
        ax.set_ylabel(f'Probability of {class_name}')
        
        # Set title
        if title is None:
            title = f'Prediction Curve: {class_name}'
        ax.set_title(title)
        
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        
        return fig, ax
    
    def get_optimal_position(self, class_name: str = None) -> tuple:
        """
        Find grid position with highest probability for a class.
        
        Args:
            class_name: Class to optimize for (default: highest average probability)
            
        Returns:
            Grid position tuple with highest probability
        """
        import numpy as np
        
        if not self._batch_processed:
            raise ValueError("Must call process_batch() first")
        
        if not self._prediction_matrix:
            raise ValueError("No predictions processed yet. Call process_batch() first.")
        
        if class_name is None:
            avg_probs = {}
            for cls, matrix in self._prediction_matrix.items():
                avg_probs[cls] = np.nanmean(matrix)
            class_name = max(avg_probs, key=avg_probs.get)
        
        matrix = self._prediction_matrix[class_name]
        optimal_idx = np.unravel_index(np.nanargmax(matrix), matrix.shape)
        
        return optimal_idx
    
    def get_stats(self) -> Dict[str, Any]:
        """Get grid statistics."""
        import numpy as np
        
        total_positions = int(np.prod(self.grid_shape))
        filled_ratio = len(self._filled_positions) / total_positions if total_positions > 0 else 0
        
        return {
            'grid_shape': self.grid_shape,
            'degrees_of_freedom': self.degrees_of_freedom,
            'total_positions': total_positions,
            'filled_positions': len(self._filled_positions),
            'fill_ratio': filled_ratio,
            'pending_records': len(self._pending_records),
            'batch_processed': self._batch_processed,
            'predictions_made': self._stats['predictions'],
            'errors': self._stats['errors'],
            'available_classes': list(self._prediction_matrix.keys()) if self._prediction_matrix else []
        }
    
    def export_data(self) -> Dict[str, Any]:
        """Export grid data for external analysis."""
        import numpy as np
        
        if not self._batch_processed:
            raise ValueError("Must call process_batch() first")
        
        return {
            'prediction_matrices': {cls: matrix.tolist() for cls, matrix in self._prediction_matrix.items()},
            'confidence_matrix': self._confidence_matrix.tolist() if self._confidence_matrix is not None else None,
            'grid_shape': self.grid_shape,
            'axis_labels': self._axis_labels,
            'axis_values': self._axis_values,
            'filled_positions': list(self._filled_positions),
            'stats': self.get_stats()
        }

    def _is_resource_blocking_error(self, job: Dict[str, Any]) -> bool:
        """
        Check if a job failed due to resource blocking/conflicts.
        
        Args:
            job: Job information dictionary
            
        Returns:
            True if the job failed due to resource blocking, False otherwise
        """
        # Check for common resource blocking patterns
        error_indicators = [
            job.get('error', '').lower(),
            job.get('message', '').lower(),
            job.get('failure_reason', '').lower()
        ]
        
        blocking_patterns = [
            'already running',
            'resource conflict',
            'another job is running',
            'blocked by',
            'queue conflict',
            'job conflict',
            'resource busy',
            'concurrent execution not allowed'
        ]
        
        for indicator in error_indicators:
            if indicator and any(pattern in indicator for pattern in blocking_patterns):
                return True
        
        return False

