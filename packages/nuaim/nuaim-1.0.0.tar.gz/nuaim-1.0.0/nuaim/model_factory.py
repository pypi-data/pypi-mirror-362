from nuaim.benchmark_presets import PRESET_CONFIGS
from .core import (
    UniversalModel, 
    DataManager, 
    HyperparameterManager, 
    TrainingEngine, 
    LoggingManager
)

import torch
import os
import time

class ModelFactory:
    """
    Main interface for the NUAIM framework.
    
    This class provides a streamlined interface for neural architecture search
    and model evaluation with support for custom hyperparameters.
    """
    
    def __init__(self, instance_params, device=None, **overrides):
        """
        Initialize ModelFactory with instance parameters.
        
        Args:
            instance_params: Either a preset name (string) or custom config dict
            device: PyTorch device for training (defaults to auto-detection)
            **overrides: Additional parameters to override in instance_params
        """
        if isinstance(instance_params, str):
            self.preset_name = instance_params
            if instance_params not in PRESET_CONFIGS:
                raise ValueError(f"Unknown preset: {instance_params}")
            self.instance_params = PRESET_CONFIGS[instance_params].copy()
        else:
            self.preset_name = "custom"
            self.instance_params = instance_params.copy()

        # Apply any overrides
        for k, v in overrides.items():
            self.instance_params[k] = v

        # Initialize components
        self.device = device or torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.data_manager = DataManager(self.instance_params, self.device)
        self.hyperparameter_manager = HyperparameterManager(self.instance_params)
        self.training_engine = TrainingEngine(self.instance_params, self.device)
        self.logging_manager = LoggingManager(self.instance_params)
    
    def create_or_get_data_loaders(self, batch_size=64, test_split=0.2, valid_split=0.2, dataset_frac=1.0):
        """
        Create or retrieve cached data loaders.
        
        Args:
            batch_size: Batch size for data loaders
            test_split: Fraction of data for testing
            valid_split: Fraction of data for validation
            dataset_frac: Fraction of total dataset to use
            
        Returns:
            tuple: (train_loader, valid_loader, test_loader)
        """
        return self.data_manager.create_or_get_data_loaders(
            batch_size, test_split, valid_split, dataset_frac
        )
    
    def generate_random_model_dict(self, custom_params=None):
        """
        Generate random hyperparameters for model training.
        
        Args:
            custom_params: Optional dict to override specific hyperparameters
            
        Returns:
            dict: Generated hyperparameters or None if invalid
        """
        hyper_params = self.hyperparameter_manager.generate_random_model_dict()
        
        # Apply custom parameter overrides if provided
        if custom_params and hyper_params:
            hyper_params.update(custom_params)
            
        return hyper_params
    
    def validate_hyperparameters(self, hyper_params):
        """
        Validate hyperparameter structure.
        
        Args:
            hyper_params: Hyperparameters to validate
            
        Raises:
            ValueError: If hyperparameters are invalid
        """
        self.hyperparameter_manager.validate_hyperparameters(hyper_params)
    
    def train(self, hyper_params=None, max_epochs=100, dataset_frac=1, verbose=True, 
              return_model=False, track_train_time=False, track_forward_time=False):
        """
        Train a model with given hyperparameters.
        
        Args:
            hyper_params: Hyperparameters for training (required)
            max_epochs: Maximum training epochs
            dataset_frac: Fraction of dataset to use
            verbose: Whether to show training progress
            return_model: Whether to return the trained model
            track_train_time: Whether to track training time
            track_forward_time: Whether to track forward propagation time
            
        Returns:
            Various formats based on tracking options and return_model flag
        """
        if hyper_params is None:
            raise ValueError("The 'train' method requires the 'hyper_params' argument.")

        # Validate hyperparameters
        self.validate_hyperparameters(hyper_params)

        # Load dataset and create data loaders
        train_loader, valid_loader, test_loader = self.create_or_get_data_loaders(
            dataset_frac=dataset_frac
        )

        # Train the model
        return self.training_engine.train(
            hyper_params, train_loader, valid_loader, test_loader,
            max_epochs=max_epochs, verbose=verbose, return_model=return_model,
            track_train_time=track_train_time, track_forward_time=track_forward_time
        )
    
    def sample_instance(self, dataset_frac=1, num_samples=5, max_epochs=1000, filename=None, 
                       log_dir="logs", verbose=True, output_format="both", 
                       track_train_time=True, track_forward_time=True, custom_params=None):
        """
        Sample and train multiple model instances.
        
        Args:
            dataset_frac: Fraction of dataset to use
            num_samples: Number of models to sample
            max_epochs: Maximum epochs for training
            filename: Base filename for output (without extension)
            log_dir: Directory to save logs
            verbose: Whether to print progress
            output_format: Output format - "table", "json", or "both"
            track_train_time: Whether to track training time
            track_forward_time: Whether to track forward propagation time
            custom_params: Optional dict to override specific hyperparameters
        
        Returns:
            dict: Summary statistics including models_trained, best_accuracy, etc.
        """
        results = []
        os.makedirs(log_dir, exist_ok=True)
        
        # Setup file paths
        if filename is not None:
            base_filename = filename.replace('.txt', '').replace('.json', '')
            table_filepath = os.path.join(log_dir, f"{base_filename}.txt")
            json_filepath = os.path.join(log_dir, f"{base_filename}.json")
        else:
            table_filepath = os.path.join(log_dir, "sample_results.txt")
            json_filepath = os.path.join(log_dir, "sample_results.json")
        
        # Setup for file logging
        rows = []
        json_results = []
        changing_keys = self.logging_manager._get_changing_keys()
        changing_opt_params = self.logging_manager._get_changing_optimizer_params()
        
        # Define columns for output
        columns = ["Eval"]
        if "layer_sequence" in changing_keys:
            columns.append("layer_sequence")
        if "activation_sequence" in changing_keys:
            columns.append("activation_sequence")
        if "optimizer" in changing_keys:
            columns.append("optimizer")
        if "loss_function" in changing_keys:
            columns.append("loss_function")
        if track_train_time:
            columns.append("train_time")
        if track_forward_time:
            columns.append("avg_forward_time")
        columns.append("accuracy")  # Accuracy is always last
        
        # Generate and train models
        i = 0
        attempts = 0
        max_attempts = num_samples * 5
        
        while i < num_samples:
            if attempts >= max_attempts:
                if verbose:
                    print(f"[Error] Failed to generate a valid model after {max_attempts} attempts. Aborting.")
                break
            attempts += 1
            
            try:
                hyper_params = self.generate_random_model_dict(custom_params)
                
                # Check if the generated hyperparameters are valid
                if hyper_params is None:
                    if verbose:
                        print(f"[Warning] Generated invalid hyperparameters (attempt {attempts}), retrying...")
                    continue
                
                # Call train with timing options
                result_data, model = self.train(
                    hyper_params=hyper_params, 
                    max_epochs=max_epochs, 
                    dataset_frac=dataset_frac, 
                    verbose=verbose, 
                    return_model=True,
                    track_train_time=track_train_time,
                    track_forward_time=track_forward_time
                )
                
                # Store results with flexible structure
                if isinstance(result_data, tuple):
                    # Multiple values returned (timing + accuracy)
                    results.append((hyper_params,) + result_data)
                else:
                    # Single accuracy value returned
                    results.append((hyper_params, result_data))
                
                # Log result to files
                self.logging_manager.log_result(
                    model, hyper_params, result_data, table_filepath, json_filepath, 
                    columns, rows, json_results, changing_keys, changing_opt_params, 
                    i, verbose, output_format, track_train_time, track_forward_time
                )
                i += 1
                
            except Exception as e:
                if verbose:
                    print(f"[Warning] Model generation/evaluation failed (attempt {attempts}): {e}")
                continue
        
        # Calculate summary statistics
        if not results:
            return {
                'models_trained': 0,
                'best_accuracy': 0.0,
                'average_accuracy': 0.0,
                'average_training_time': 0.0,
                'average_forward_time': 0.0,
                'status': 'FAILED',
                'error': 'No valid models were generated'
            }
        
        # Extract statistics from results
        accuracies = [result[-1] for result in results]  # Accuracy is always last
        train_times = []
        forward_times = []
        
        # Extract timing data based on what's being tracked
        if track_train_time and track_forward_time:
            train_times = [result[-3] for result in results]
            forward_times = [result[-2] for result in results]
        elif track_train_time:
            train_times = [result[-2] for result in results]
        elif track_forward_time:
            forward_times = [result[-2] for result in results]
        
        # Calculate averages
        best_accuracy = max(accuracies)
        average_accuracy = sum(accuracies) / len(accuracies)
        average_training_time = sum(train_times) / len(train_times) if train_times else 0.0
        average_forward_time = sum(forward_times) / len(forward_times) if forward_times else 0.0
        
        # Save best model
        best_result = max(results, key=lambda x: x[-1])
        best_hyperparams = best_result[0]
        best_model_instance = UniversalModel(best_hyperparams, self.instance_params).to(self.device)
        
        model_filename = self.logging_manager.save_best_model(
            best_model_instance, self.preset_name, log_dir
        )
        
        # Return summary statistics
        return {
            'models_trained': len(results),
            'best_accuracy': best_accuracy,
            'average_accuracy': average_accuracy,
            'average_training_time': average_training_time,
            'average_forward_time': average_forward_time,
            'status': 'SUCCESS'
        }
