from nuaim.utils import layer_dict, activation_func_dict, loss_func_dict, optimizer_dict
import random
import math

class HyperparameterManager:
    def __init__(self, instance_params):
        self.instance_params = instance_params
        self.verify_instance_params()
    
    def verify_instance_params(self):
        """Validate instance parameters."""
        required_keys = [
            "dataset_name", "layer_search_space",
            "activation_function", "loss_function", "optimizer"
        ]
        for k in required_keys:
            if k not in self.instance_params:
                raise ValueError(f"Missing required key in instance_params: '{k}'")

        # Validate activation functions
        valid_act_func = list(activation_func_dict.keys())
        for act in self.instance_params["activation_function"]:
            if act not in valid_act_func:
                raise ValueError(f"Unsupported activation_function: '{act}'. Available: {valid_act_func}")

        # Validate loss functions
        valid_loss_func = list(loss_func_dict.keys())
        for loss in self.instance_params["loss_function"]:
            if loss not in valid_loss_func:
                raise ValueError(f"Unsupported loss function: '{loss}'. Available: {valid_loss_func}")

        # Validate optimizers
        valid_optimizer = list(optimizer_dict.keys())
        for opt in self.instance_params["optimizer"]:
            if opt["type"] not in valid_optimizer:
                raise ValueError(f"Unsupported optimizer type: '{opt['type']}'. Available: {valid_optimizer}")
            
            # Validate that each optimizer has min_layers and max_layers
            if "min_layers" not in opt:
                raise ValueError(f"Optimizer '{opt['type']}' missing 'min_layers' field")
            if "max_layers" not in opt:
                raise ValueError(f"Optimizer '{opt['type']}' missing 'max_layers' field")
            
            # Validate min/max layers for each optimizer
            if opt["min_layers"] > opt["max_layers"]:
                raise ValueError(f"Optimizer '{opt['type']}': min_layers ({opt['min_layers']}) cannot be greater than max_layers ({opt['max_layers']})")
            
            if opt["min_layers"] < 1:
                raise ValueError(f"Optimizer '{opt['type']}': min_layers must be at least 1")

        # Validate layer types in search space
        valid_layer_types = set(layer_dict.keys())
        valid_layer_types.update(["MLP", "Dropout", "BatchNorm", "BatchNorm2d", "Transformer", "CNNBlock", "Pooling"])
        valid_layer_types = sorted(list(valid_layer_types))

        for layer_template in self.instance_params["layer_search_space"]:
            if layer_template["type"] not in valid_layer_types:
                raise ValueError(f"Unsupported layer type: '{layer_template['type']}'. Available: {valid_layer_types}")

    def validate_hyperparameters(self, hyper_params):
        """Validate the structure of hyperparameters passed to training."""
        required_hp_keys = ["layer_sequence", "activation_sequence", "optimizer", "loss_function"]
        for key in required_hp_keys:
            if key not in hyper_params:
                raise ValueError(f"Missing required key in hyper_params: '{key}'")
        
        # Validate layer sequence
        if not isinstance(hyper_params["layer_sequence"], list) or len(hyper_params["layer_sequence"]) == 0:
            raise ValueError("layer_sequence must be a non-empty list")
        
        # Validate activation sequence
        if not isinstance(hyper_params["activation_sequence"], list):
            raise ValueError("activation_sequence must be a list")
        
        # Check if activation sequence length matches layer sequence (for layers that need activations)
        layers_needing_activation = sum(1 for layer in hyper_params["layer_sequence"] 
                                      if layer["type"] in ["MLP", "Conv2d"])
        if len(hyper_params["activation_sequence"]) < layers_needing_activation:
            raise ValueError(f"activation_sequence length ({len(hyper_params['activation_sequence'])}) "
                           f"must be at least {layers_needing_activation} to cover all layers that need activations")
        
        # Validate each layer has required parameters
        for i, layer in enumerate(hyper_params["layer_sequence"]):
            if "type" not in layer:
                raise ValueError(f"Layer {i} missing 'type' field")
            
            layer_type = layer["type"]
            
            # Check required parameters for each layer type
            if layer_type == "MLP" and "units" not in layer:
                raise ValueError(f"MLP layer {i} missing 'units' parameter")
            elif layer_type == "Conv2d":
                if "channel_units" not in layer:
                    raise ValueError(f"Conv2d layer {i} missing 'channel_units' parameter")
                if "kernel_size" not in layer:
                    raise ValueError(f"Conv2d layer {i} missing 'kernel_size' parameter")
            elif layer_type == "Pooling" and "kernel_size" not in layer:
                raise ValueError(f"Pooling layer {i} missing 'kernel_size' parameter")
            elif layer_type == "CNNBlock":
                if "channel_units" not in layer:
                    raise ValueError(f"CNNBlock layer {i} missing 'channel_units' parameter")
                if "kernel_size" not in layer:
                    raise ValueError(f"CNNBlock layer {i} missing 'kernel_size' parameter")
            elif layer_type == "Transformer":
                required_transformer_params = ["d_model", "nhead", "num_layers"]
                for param in required_transformer_params:
                    if param not in layer:
                        raise ValueError(f"Transformer layer {i} missing '{param}' parameter")
        
        # Validate CNN layer compatibility with current shape (only if input_shape is available)
        if "input_shape" in self.instance_params:
            self._validate_cnn_layers(hyper_params["layer_sequence"])
        
        # Validate optimizer structure
        optimizer = hyper_params["optimizer"]
        if not isinstance(optimizer, dict) or "type" not in optimizer or "params" not in optimizer:
            raise ValueError("optimizer must be a dict with 'type' and 'params' keys")
        
        # Validate that optimizer type exists
        if optimizer["type"] not in optimizer_dict:
            available_optimizers = list(optimizer_dict.keys())
            raise ValueError(f"Unsupported optimizer type: '{optimizer['type']}'. Available: {available_optimizers}")
        
        # Validate loss function
        loss_function = hyper_params["loss_function"]
        if not isinstance(loss_function, str):
            raise ValueError("loss_function must be a string")
        
        if loss_function not in loss_func_dict:
            available_losses = list(loss_func_dict.keys())
            raise ValueError(f"Unsupported loss function: '{loss_function}'. Available: {available_losses}")
        
        # Validate activation functions
        for i, activation in enumerate(hyper_params["activation_sequence"]):
            if activation not in activation_func_dict:
                available_activations = list(activation_func_dict.keys())
                raise ValueError(f"Unsupported activation function '{activation}' at position {i}. Available: {available_activations}")

    def _validate_cnn_layers(self, layer_sequence):
        """Validate CNN layer configurations by simulating forward pass."""
        current_shape = self.instance_params.get("input_shape", (3, 32, 32))
        
        for i, layer in enumerate(layer_sequence):
            layer_type = layer["type"]
            
            if layer_type == "Conv2d":
                if len(current_shape) == 3:
                    c, h, w = current_shape
                    k = layer["kernel_size"]
                    s = layer.get("stride", 1)
                    p = layer.get("padding", 0)
                    new_h = (h + 2 * p - k) // s + 1
                    new_w = (w + 2 * p - k) // s + 1
                    
                    if new_h <= 0 or new_w <= 0:
                        raise ValueError(f"Conv2d layer {i} would result in invalid output shape: {new_h}x{new_w}")
                    
                    current_shape = (layer["channel_units"], new_h, new_w)
                else:
                    raise ValueError(f"Conv2d layer {i}: Invalid input shape {current_shape}")
            
            elif layer_type == "Pooling":
                if len(current_shape) == 3:
                    c, h, w = current_shape
                    k = layer["kernel_size"]
                    s = layer.get("stride", k)
                    new_h = (h - k) // s + 1
                    new_w = (w - k) // s + 1
                    
                    if new_h <= 0 or new_w <= 0:
                        raise ValueError(f"Pooling layer {i} would result in invalid output shape: {new_h}x{new_w}")
                    
                    current_shape = (c, new_h, new_w)
                else:
                    raise ValueError(f"Pooling layer {i}: Invalid input shape {current_shape}")
            
            elif layer_type == "MLP":
                # MLP layers flatten the input, so transition to 1D
                if len(current_shape) == 3:
                    current_shape = (current_shape[0] * current_shape[1] * current_shape[2],)
                elif len(current_shape) == 1:
                    current_shape = (layer["units"],)
                else:
                    raise ValueError(f"MLP layer {i}: Unsupported input shape {current_shape}")
            
            # Other layer types (Dropout, BatchNorm, etc.) don't change shape significantly

    def generate_random_model_dict(self):
        """Generate random hyperparameters based on instance parameters."""
        # First select an optimizer to determine layer constraints
        optimizer_sample = random.choice(self.instance_params["optimizer"])
        min_layers = optimizer_sample["min_layers"]
        max_layers = optimizer_sample["max_layers"]
        
        n_layers = random.randint(min_layers, max_layers)
        layer_search_space = self.instance_params["layer_search_space"]
        activation_choices = self.instance_params["activation_function"]

        layer_sequence = []
        activation_sequence = []

        shape_type = "3d"  # Start with 3D (image input)
        current_shape = self.instance_params.get("input_shape", (3, 32, 32))

        for _ in range(n_layers):
            # Filter possible layers based on current shape type
            if shape_type == "1d":
                # After MLP or Transformer, can add MLP, Dropout, BatchNorm, or another Transformer
                possible_layers = [l for l in layer_search_space if l["type"] in ["MLP", "Dropout", "BatchNorm", "Transformer"]]
            else: # shape_type == "3d"
                # In 3D space, can add any layer type except 1D-specific ones
                possible_layers = [l for l in layer_search_space if l["type"] not in ["BatchNorm"]]

            if not possible_layers:
                break
            
            layer_sample = random.choice(possible_layers)
            layer_config = {"type": layer_sample["type"]}

            # Special handling for BatchNorm layers to avoid feature count mismatches
            if layer_sample["type"] == "BatchNorm":
                if shape_type == "3d":
                    continue
                layer_config = {"type": "BatchNorm"}
            elif layer_sample["type"] == "BatchNorm2d":
                if shape_type == "1d":
                    continue
                layer_config = {"type": "BatchNorm2d"}
            else:
                # Handle other layer parameters with CNN-aware constraints
                for param, values in layer_sample.items():
                    if param == "type":
                        continue
                    
                    # Apply CNN-aware constraints for kernel_size
                    if param == "kernel_size" and layer_sample["type"] in ["Conv2d", "CNNBlock", "Pooling"]:
                        if len(current_shape) == 3:
                            c, h, w = current_shape
                            max_kernel = min(h, w)
                            
                            if isinstance(values, list):
                                # Filter valid kernel sizes from the list
                                valid_kernels = [k for k in values if k <= max_kernel]
                                if valid_kernels:
                                    layer_config[param] = random.choice(valid_kernels)
                                else:
                                    # If no valid kernels, use the maximum valid size
                                    layer_config[param] = max(1, max_kernel)
                            elif isinstance(values, dict):
                                if "min" in values and "max" in values:
                                    min_val = max(values["min"], 1)
                                    max_val = min(values["max"], max_kernel)
                                    if max_val >= min_val:
                                        layer_config[param] = random.randint(min_val, max_val)
                                    else:
                                        layer_config[param] = max(1, max_kernel)
                                elif "values" in values:
                                    valid_kernels = [k for k in values["values"] if k <= max_kernel]
                                    if valid_kernels:
                                        layer_config[param] = random.choice(valid_kernels)
                                    else:
                                        layer_config[param] = max(1, max_kernel)
                            else:
                                # Single value, check if it's valid
                                if values <= max_kernel:
                                    layer_config[param] = values
                                else:
                                    layer_config[param] = max(1, max_kernel)
                        else:
                            # Handle non-3D case normally
                            if isinstance(values, list):
                                layer_config[param] = random.choice(values)
                            elif isinstance(values, dict):
                                if "min" in values and "max" in values:
                                    layer_config[param] = random.randint(values["min"], values["max"])
                                elif "values" in values:
                                    layer_config[param] = random.choice(values["values"])
                            else:
                                layer_config[param] = values
                    else:
                        # Handle non-kernel parameters normally
                        if isinstance(values, list):
                            layer_config[param] = random.choice(values)
                        elif isinstance(values, dict):
                            if "min" in values and "max" in values:
                                if isinstance(values["min"], int) and isinstance(values["max"], int):
                                    layer_config[param] = random.randint(values["min"], values["max"])
                                else:
                                    layer_config[param] = random.uniform(values["min"], values["max"])
                            elif "values" in values:
                                layer_config[param] = random.choice(values["values"])
                        else:
                            layer_config[param] = values
            
            layer_sequence.append(layer_config)
            activation_sequence.append(random.choice(activation_choices))

            # Update current shape based on the layer added
            try:
                new_shape = self._simulate_layer_output_shape(layer_config, current_shape)
                current_shape = new_shape
            except ValueError:
                # If this layer would create invalid dimensions, remove it and try again
                layer_sequence.pop()
                activation_sequence.pop()
                continue

            # Update shape_type based on layer added
            if layer_sample["type"] in ["MLP", "Transformer"]:
                shape_type = "1d"
            elif layer_sample["type"] in ["Conv2d", "Pooling", "CNNBlock"]:
                shape_type = "3d"
            # Dropout, BatchNorm, BatchNorm2d layers don't change shape type

        # Generate optimizer parameters
        optimizer_params = {}
        for param, value in optimizer_sample["params"].items():
            if isinstance(value, dict):
                if "min" in value and "max" in value:
                    if param == "lr":
                        # Log-uniform sampling for learning rate
                        min_lr = value["min"]
                        max_lr = value["max"]
                        lr = math.exp(random.uniform(math.log(min_lr), math.log(max_lr)))
                        optimizer_params[param] = lr
                    elif isinstance(value["min"], int) and isinstance(value["max"], int):
                        optimizer_params[param] = random.randint(value["min"], value["max"])
                    else:
                        optimizer_params[param] = random.uniform(value["min"], value["max"])
                elif "values" in value:
                    sampled_value = random.choice(value["values"])
                    # Convert lists to tuples for parameters like betas
                    if param == "betas" and isinstance(sampled_value, list):
                        optimizer_params[param] = tuple(sampled_value)
                    else:
                        optimizer_params[param] = sampled_value
            elif isinstance(value, list):
                # Handle direct list values (like the old format)
                sampled_value = random.choice(value)
                # Convert lists to tuples for parameters like betas
                if param == "betas" and isinstance(sampled_value, list):
                    optimizer_params[param] = tuple(sampled_value)
                else:
                    optimizer_params[param] = sampled_value
            else:
                optimizer_params[param] = value

        optimizer = {
            "type": optimizer_sample["type"],
            "params": optimizer_params
        }

        loss_function = random.choice(self.instance_params["loss_function"])

        hyper_params = {
            "layer_sequence": layer_sequence,
            "activation_sequence": activation_sequence,
            "optimizer": optimizer,
            "loss_function": loss_function,
        }
        
        # Final validation to ensure the configuration is valid
        try:
            if "input_shape" in self.instance_params:
                self.validate_hyperparameters(hyper_params)
        except ValueError:
            return None
        
        return hyper_params

    def _simulate_layer_output_shape(self, layer_config, input_shape):
        """Simulate the output shape of a layer given its configuration and input shape."""
        layer_type = layer_config["type"]
        
        if layer_type == "Conv2d":
            c, h, w = input_shape
            k = layer_config.get("kernel_size", 3)
            s = layer_config.get("stride", 1)
            p = layer_config.get("padding", 0)
            
            new_h = (h + 2 * p - k) // s + 1
            new_w = (w + 2 * p - k) // s + 1
            
            # Reject if dimensions become too small
            if new_h <= 0 or new_w <= 0:
                raise ValueError(f"Conv2d would result in invalid output shape: {new_h}x{new_w}")
            
            return (layer_config.get("channel_units", c), new_h, new_w)
        
        elif layer_type == "Pooling":
            c, h, w = input_shape
            k = layer_config.get("kernel_size", 2)
            s = layer_config.get("stride", k)
            new_h = (h - k) // s + 1
            new_w = (w - k) // s + 1
            
            # Reject if dimensions become too small
            if new_h <= 0 or new_w <= 0:
                raise ValueError(f"Pooling would result in invalid output shape: {new_h}x{new_w}")
            
            return (c, new_h, new_w)
        
        elif layer_type == "MLP":
            # MLP flattens input to 1D
            if len(input_shape) == 3:
                return (input_shape[0] * input_shape[1] * input_shape[2],)
            else:
                return (layer_config.get("units", input_shape[0]),)
        
        # For other layer types, return unchanged shape
        return input_shape
