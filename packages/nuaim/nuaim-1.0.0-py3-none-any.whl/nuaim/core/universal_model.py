from nuaim.utils import layer_dict, activation_func_dict
from nuaim.utils.layer_dict import TransformerBlock

import torch
import torch.nn as nn

class UniversalModel(nn.Module):
    def __init__(self, hyper_params, instance_params):
        super().__init__()
        
        # Validate that required instance_params are present
        if "dimension" not in instance_params:
            raise ValueError("instance_params missing 'dimension' key. This should be set automatically when creating data loaders, or provided manually.")
        
        if "out_features" not in instance_params:
            raise ValueError("instance_params missing 'out_features' key. This should be set automatically when creating data loaders, or provided manually.")
        
        self.layers = nn.ModuleList()
        current_shape = tuple(instance_params["dimension"])
        activations = hyper_params.get("activation_sequence", [])

        for i, layer in enumerate(hyper_params["layer_sequence"]):
            layer_type = layer["type"]

            if layer_type == "MLP":
                if len(current_shape) == 3:
                    self.layers.append(nn.Flatten())
                    in_features = current_shape[0] * current_shape[1] * current_shape[2]
                    current_shape = (in_features,)
                self.layers.append(layer_dict["MLP"]
                        (
                        in_features=current_shape[0], out_features=layer["units"]
                        )
                )
                current_shape = (layer["units"],)

            elif layer_type == "Conv2d":
                if len(current_shape) == 3:
                    c, h, w = current_shape
                    k = layer["kernel_size"]
                    s = layer.get("stride", 1)
                    p = layer.get("padding", 0)
                    
                    self.layers.append(layer_dict["Conv2d"]
                        (
                        in_channels=current_shape[0],
                        out_channels=layer["channel_units"],
                        kernel_size=k,
                        stride=s,
                        padding=p
                        )
                    )
                    h = (h + 2 * p - k) // s + 1
                    w = (w + 2 * p - k) // s + 1
                    current_shape = (layer["channel_units"], h, w)
                else:
                    raise ValueError("Conv2d layers require 3D input shapes (e.g., images). Please provide a valid input shape.")
                    
            elif layer_type == "Pooling":
                if len(current_shape) == 3:
                    pool_type = layer.get("pooling_type", "MaxPool2d")
                    self.layers.append(layer_dict[pool_type]
                        (
                        kernel_size=layer["kernel_size"], stride=layer.get("stride", layer["kernel_size"])
                        )
                    )
                    c, h, w = current_shape
                    k = layer["kernel_size"]
                    s = layer.get("stride", k)
                    h = (h - k) // s + 1
                    w = (w - k) // s + 1
                    current_shape = (c, h, w)
                else:
                    raise ValueError("Pooling layers are only supported for 3D input shapes (e.g., CNN outputs).")

            elif layer_type == "Dropout":
                dropout_p = layer.get("p", 0.5)
                self.layers.append(layer_dict["Dropout"](p=dropout_p))
                # Dropout doesn't change the shape

            elif layer_type == "BatchNorm":
                if len(current_shape) == 1:
                    # Use the actual current shape's feature count, not from layer config
                    num_features = current_shape[0]
                    self.layers.append(layer_dict["BatchNorm"](num_features=num_features))
                else:
                    raise ValueError("BatchNorm (1D) layers require 1D input shapes (e.g., after MLP layers).")
                # BatchNorm doesn't change the shape

            elif layer_type == "BatchNorm2d":
                if len(current_shape) == 3:
                    # Use the actual current shape's channel count, not from layer config
                    num_features = current_shape[0]
                    self.layers.append(layer_dict["BatchNorm2d"](num_features=num_features))
                else:
                    raise ValueError("BatchNorm2d layers require 3D input shapes (e.g., CNN outputs).")
                # BatchNorm2d doesn't change the shape

            elif layer_type == "Transformer":
                layer_params = layer.copy()
                if 'type' in layer_params:
                    del layer_params['type']

                self.layers.append(nn.Flatten())
                
                if len(current_shape) == 3: # (C, H, W)
                    in_features = current_shape[0] * current_shape[1] * current_shape[2]
                elif len(current_shape) == 1: # (Features,)
                    in_features = current_shape[0]
                else:
                    raise ValueError("Transformer layer input shape must be 1D or 3D.")

                d_model = layer.get("d_model")
                if d_model != in_features:
                    self.layers.append(nn.Linear(in_features, d_model))
                
                self.layers.append(layer_dict["Transformer"](**layer_params))
                current_shape = (d_model,)

            elif layer_type == "CNNBlock":
                if len(current_shape) == 3:
                    in_channels = current_shape[0]
                    c, h, w = current_shape
                    
                    layer_params = layer.copy()
                    if 'type' in layer_params:
                        del layer_params['type']
                    if 'channel_units' in layer_params:
                        layer_params['out_channels'] = layer_params.pop('channel_units')

                    self.layers.append(layer_dict["CNNBlock"]
                        (
                        in_channels=in_channels,
                        **layer_params
                        )
                    )
                    # Shape update logic for CNNBlock
                    out_channels = layer["channel_units"]
                    stride = layer.get("stride", 1)
                    kernel_size = layer.get("kernel_size", 3)
                    padding = layer.get("padding", 1)
                    pooling_type = layer.get("pooling_type", None)
                    pool_kernel_size = layer.get("pool_kernel_size", 2)
                    
                    # After conv
                    h = (h + 2 * padding - kernel_size) // stride + 1
                    w = (w + 2 * padding - kernel_size) // stride + 1
                    # After pooling (if any)
                    if pooling_type in ["MaxPool2d", "AvgPool2d"]:
                        h = (h - pool_kernel_size) // pool_kernel_size + 1
                        w = (w - pool_kernel_size) // pool_kernel_size + 1
                    current_shape = (out_channels, h, w)

                    pass # Skips adding activation since CNNBlock handles it internally
                else:
                    raise ValueError("CNNBlock layers require 3D input shapes (e.g., images).")

            else:
                raise ValueError(f"Unknown layer type: {layer_type}")

            # Add activation function for layers that need it (not for CNNBlock, Pooling, Dropout, BatchNorm)
            if layer_type in ["MLP", "Conv2d"] and i < len(activations):
                if activations[i] not in activation_func_dict:
                    raise ValueError(f"Unsupported activation function: {activations[i]}")
                self.layers.append(activation_func_dict[activations[i]]())

        # If the current shape is not 1D, flatten it before the final layer
        if len(current_shape) != 1:
            self.layers.append(nn.Flatten())
            current_shape = (current_shape[0] * current_shape[1] * current_shape[2],)

        # Add the final layer based on the instance parameters
        self.layers.append(nn.Linear(current_shape[0], instance_params["out_features"]))

    def forward(self, x):
        for layer in self.layers:
            # Special handling for Transformer input shape
            if isinstance(layer, TransformerBlock):
                if x.dim() == 2: # (Batch, Features)
                    x = x.unsqueeze(1) # -> (Batch, 1, Features)
            
            x = layer(x)

            # Special handling for Transformer output shape
            if isinstance(layer, TransformerBlock):
                 if x.dim() == 3: # (Batch, SeqLen, Features)
                    x = x.mean(dim=1) # Average over sequence length -> (Batch, Features)

        return x
