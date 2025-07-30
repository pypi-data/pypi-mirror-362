PRESET_CONFIGS = {
    # --- Basic Presets ---
    "BasicMLP": {
        "dataset_name": "FashionMNIST",
        "layer_search_space": [
            {"type": "MLP", "units": [32, 64, 128]},
        ],
        "activation_function": ["ReLU"],
        "loss_function": ["CrossEntropyLoss"],
        "optimizer": [
            {
                "type": "Adam", 
                "min_layers": 1, 
                "max_layers": 3,
                "params": {"lr": {"min": 1e-4, "max": 1e-1}, "betas": (0.9, 0.999), "eps": 1e-8, "weight_decay": 0.0}
            },
            {
                "type": "SGD", 
                "min_layers": 1, 
                "max_layers": 3,
                "params": {"lr": {"min": 1e-4, "max": 1e-1}, "momentum": 0.9, "weight_decay": 0.0}
            }
        ]
    },
    "BasicCNN": {
        "dataset_name": "FashionMNIST",
        "layer_search_space": [
            {
                "type": "CNNBlock", 
                "channel_units": [16, 32], 
                "kernel_size": [3], 
                "stride": 1, 
                "padding": 1,
                "pooling_type": ["MaxPool2d"],
                "pool_kernel_size": 2
            },
        ],
        "activation_function": ["ReLU"],
        "loss_function": ["CrossEntropyLoss"],
        "optimizer": [
            {
                "type": "Adam", 
                "min_layers": 1, 
                "max_layers": 3,
                "params": {
                    "lr": {"min": 1e-4, "max": 1e-1},
                    "betas": (0.9, 0.999),
                    "eps": 1e-8,
                    "weight_decay": 0.0
                }
            },
            {
                "type": "SGD", 
                "min_layers": 1, 
                "max_layers": 3,
                "params": {"lr": {"min": 1e-4, "max": 1e-1}, "momentum": 0.9, "weight_decay": 0.0}
            }
        ]
    },
    "BasicTransformer": {
        "dataset_name": "FashionMNIST",
        "layer_search_space": [
            {
                "type": "Transformer", 
                "d_model": [32, 64, 128], 
                "nhead": [4], 
                "num_layers": [1],
                "dropout": 0.1
            },
        ],
        "activation_function": ["GELU"],
        "loss_function": ["CrossEntropyLoss"],
        "optimizer": [
            {
                "type": "AdamW", 
                "min_layers": 1, 
                "max_layers": 2,
                "params": {"lr": {"min": 1e-5, "max": 1e-3}, "weight_decay": {"min": 1e-4, "max": 1e-2}}
            },
            {
                "type": "Adam", 
                "min_layers": 1, 
                "max_layers": 2,
                "params": {"lr": {"min": 1e-5, "max": 1e-3}, "betas": (0.9, 0.999), "eps": 1e-8, "weight_decay": 0.0}
            }
        ]
    },

    # --- Advanced Presets ---
    "AdvancedMLP": {
        "dataset_name": "FashionMNIST",
        "layer_search_space": [
            {"type": "MLP", "units": [64, 128, 256, 512]},
            {"type": "BatchNorm"},
            {"type": "Dropout", "p": {"min": 0.1, "max": 0.3}},
        ],
        "activation_function": ["ReLU", "GELU", "SiLU"],
        "loss_function": ["CrossEntropyLoss"],
        "optimizer": [
            {
                "type": "Adam", 
                "min_layers": 3, 
                "max_layers": 6,
                "params": {
                    "lr": {"min": 1e-4, "max": 1e-3}, 
                    "betas": {"values": [[0.8, 0.9], [0.9, 0.999]]},
                    "eps": 1e-8,
                    "weight_decay": 0.0
                }
            },
            {
                "type": "SGD", 
                "min_layers": 2, 
                "max_layers": 5,
                "params": {
                    "lr": {"min": 1e-3, "max": 1e-2}, 
                    "momentum": {"values": [0.9, 0.95]},
                    "weight_decay": {"min": 1e-5, "max": 1e-3},
                    "nesterov": False
                }
            }
        ]
    },
    "AdvancedCNN": {
        "dataset_name": "FashionMNIST",
        "layer_search_space": [
            {
                "type": "CNNBlock", 
                "channel_units": [32, 64], 
                "kernel_size": [3, 5], 
                "stride": 1,
                "padding": 1,
                "pooling_type": ["MaxPool2d", "AvgPool2d"],
                "pool_kernel_size": [2, 3]
            },
            {
                "type": "Conv2d", 
                "channel_units": [16, 32, 64], 
                "kernel_size": [3, 5],
                "stride": 1,
                "padding": 1
            },
            {
                "type": "Pooling", 
                "pooling_type": ["MaxPool2d", "AvgPool2d"], 
                "kernel_size": [2, 3],
                "stride": 2
            },
            {"type": "BatchNorm2d"},
        ],
        "activation_function": ["ReLU", "GELU", "SiLU"],
        "loss_function": ["CrossEntropyLoss"],
        "optimizer": [
            {
                "type": "AdamW", 
                "min_layers": 3, 
                "max_layers": 6,
                "params": {
                    "lr": {"min": 1e-4, "max": 1e-3}, 
                    "weight_decay": {"min": 1e-4, "max": 1e-3},
                    "betas": (0.9, 0.999),
                    "eps": 1e-8
                }
            },
            {
                "type": "Adam", 
                "min_layers": 2, 
                "max_layers": 4,
                "params": {
                    "lr": {"min": 1e-4, "max": 1e-3},
                    "betas": (0.9, 0.999),
                    "eps": 1e-8,
                    "weight_decay": 0.0
                }
            },
            {
                "type": "SGD", 
                "min_layers": 2, 
                "max_layers": 5,
                "params": {
                    "lr": {"min": 1e-3, "max": 1e-2},
                    "momentum": 0.9,
                    "weight_decay": {"min": 1e-4, "max": 1e-3},
                    "nesterov": True
                }
            }
        ]
    },
    "AdvancedTransformer": {
        "dataset_name": "FashionMNIST",
        "layer_search_space": [
            {
                "type": "Transformer", 
                "d_model": [128, 256], 
                "nhead": [4, 8], 
                "num_layers": [1, 2],
                "dropout": {"min": 0.0, "max": 0.3}
            },
        ],
        "activation_function": ["GELU", "SiLU"],
        "loss_function": ["CrossEntropyLoss"],
        "optimizer": [
            {
                "type": "AdamW", 
                "min_layers": 1, 
                "max_layers": 4,
                "params": {
                    "lr": {"min": 1e-5, "max": 1e-3}, 
                    "weight_decay": {"min": 1e-4, "max": 1e-2},
                    "betas": (0.9, 0.999),
                    "eps": 1e-8
                }
            },
            {
                "type": "Adam", 
                "min_layers": 1, 
                "max_layers": 3,
                "params": {
                    "lr": {"min": 1e-5, "max": 1e-3},
                    "betas": (0.9, 0.999),
                    "eps": 1e-8,
                    "weight_decay": 0.0
                }
            },
            {
                "type": "NAdam", 
                "min_layers": 1, 
                "max_layers": 2,
                "params": {
                    "lr": {"min": 1e-5, "max": 1e-3},
                    "betas": (0.9, 0.999),
                    "eps": 1e-8,
                    "weight_decay": {"min": 1e-5, "max": 1e-3}
                }
            }
        ]
    },

    # --- Hard Presets ---
    "HardMLP": {
        "dataset_name": "FashionMNIST",
        "layer_search_space": [
            {"type": "MLP", "units": [128, 256, 512, 1024]},
            {"type": "BatchNorm"},
            {"type": "Dropout", "p": {"min": 0.1, "max": 0.5}},
        ],
        "activation_function": ["ReLU", "GELU", "SiLU", "LeakyReLU", "ELU", "SELU"],
        "loss_function": ["CrossEntropyLoss", "NLLLoss"],
        "optimizer": [
            {
                "type": "AdamW", 
                "min_layers": 4, 
                "max_layers": 8,
                "params": {
                    "lr": {"min": 1e-5, "max": 1e-3}, 
                    "weight_decay": {"min": 1e-4, "max": 1e-2},
                    "betas": (0.9, 0.999),
                    "eps": 1e-8
                }
            },
            {
                "type": "SGD", 
                "min_layers": 3, 
                "max_layers": 6,
                "params": {
                    "lr": {"min": 1e-4, "max": 1e-2}, 
                    "momentum": {"min": 0.8, "max": 0.95},
                    "weight_decay": {"min": 1e-5, "max": 1e-3},
                    "nesterov": {"values": [True, False]}
                }
            },
            {
                "type": "RMSprop", 
                "min_layers": 3, 
                "max_layers": 7,
                "params": {
                    "lr": {"min": 1e-4, "max": 1e-2}, 
                    "alpha": {"values": [0.9, 0.95, 0.99]},
                    "eps": 1e-8,
                    "weight_decay": {"min": 1e-5, "max": 1e-3},
                    "momentum": 0.0
                }
            }
        ]
    },
    "HardCNN-MLP": {
        "dataset_name": "FashionMNIST",
        "layer_search_space": [
            {
                "type": "CNNBlock", 
                "channel_units": [32, 64, 128], 
                "kernel_size": [3, 5], 
                "stride": 1,
                "padding": 1,
                "pooling_type": ["MaxPool2d", "AvgPool2d"],
                "pool_kernel_size": 2
            },
            {
                "type": "Conv2d", 
                "channel_units": [16, 32, 64, 128], 
                "kernel_size": [3, 5],
                "stride": {"values": [1, 2]},
                "padding": {"values": [1, 2]}
            },
            {
                "type": "Pooling", 
                "pooling_type": ["MaxPool2d", "AvgPool2d"], 
                "kernel_size": [2, 3],
                "stride": {"values": [2, 3]}
            },
            {"type": "MLP", "units": [256, 512, 1024]},
            {"type": "BatchNorm2d"},
            {"type": "BatchNorm"},
            {"type": "Dropout", "p": {"min": 0.1, "max": 0.5}},
        ],
        "activation_function": ["ReLU", "GELU", "SiLU", "LeakyReLU"],
        "loss_function": ["CrossEntropyLoss", "NLLLoss"],
        "optimizer": [
            {
                "type": "AdamW", 
                "min_layers": 4, 
                "max_layers": 10,
                "params": {
                    "lr": {"min": 1e-5, "max": 1e-3}, 
                    "weight_decay": {"min": 1e-4, "max": 1e-2},
                    "betas": (0.9, 0.999),
                    "eps": 1e-8
                }
            },
            {
                "type": "Adam", 
                "min_layers": 3, 
                "max_layers": 8,
                "params": {
                    "lr": {"min": 1e-5, "max": 1e-3},
                    "betas": (0.9, 0.999),
                    "eps": 1e-8,
                    "weight_decay": 0.0
                }
            },
            {
                "type": "SGD", 
                "min_layers": 3, 
                "max_layers": 7,
                "params": {
                    "lr": {"min": 1e-4, "max": 1e-2},
                    "momentum": {"values": [0.8, 0.9, 0.95]},
                    "weight_decay": {"min": 1e-5, "max": 1e-3},
                    "nesterov": {"values": [True, False]}
                }
            }
        ]
    },
    "HardTransformer": {
        "dataset_name": "FashionMNIST",
        "layer_search_space": [
            {
                "type": "Transformer", 
                "d_model": [128, 256, 512], 
                "nhead": [4, 8, 16], 
                "num_layers": [2, 4, 6],
                "dropout": {"min": 0.1, "max": 0.4}
            },
            {"type": "MLP", "units": [256, 512, 1024]},
            {"type": "Dropout", "p": {"min": 0.1, "max": 0.5}},
            {"type": "BatchNorm"},
        ],
        "activation_function": ["GELU", "SiLU", "Mish"],
        "loss_function": ["CrossEntropyLoss", "NLLLoss"],
        "optimizer": [
            {
                "type": "AdamW", 
                "min_layers": 2, 
                "max_layers": 6,
                "params": {
                    "lr": {"min": 1e-5, "max": 1e-3}, 
                    "weight_decay": {"min": 1e-4, "max": 1e-2},
                    "betas": (0.9, 0.999),
                    "eps": 1e-8
                }
            },
            {
                "type": "Adam", 
                "min_layers": 2, 
                "max_layers": 5,
                "params": {
                    "lr": {"min": 1e-5, "max": 1e-3},
                    "betas": (0.9, 0.999),
                    "eps": 1e-8,
                    "weight_decay": 0.0
                }
            },
            {
                "type": "NAdam", 
                "min_layers": 1, 
                "max_layers": 4,
                "params": {
                    "lr": {"min": 1e-5, "max": 1e-3},
                    "betas": (0.9, 0.999),
                    "eps": 1e-8,
                    "weight_decay": {"min": 1e-5, "max": 1e-3}
                }
            }
        ]
    },

    # --- Complete Preset ---
    "Complete": {
        "dataset_name": "FashionMNIST",
        "layer_search_space": [
            {
                "type": "CNNBlock", 
                "channel_units": [16, 32, 64], 
                "kernel_size": [3, 5], 
                "stride": 1,
                "padding": 1,
                "pooling_type": ["MaxPool2d", "AvgPool2d"],
                "pool_kernel_size": 2
            },
            {
                "type": "Conv2d", 
                "channel_units": [16, 32, 64], 
                "kernel_size": [3, 5],
                "stride": {"values": [1, 2]},
                "padding": {"values": [1, 2]}
            },
            {
                "type": "Pooling", 
                "pooling_type": ["MaxPool2d", "AvgPool2d"], 
                "kernel_size": [2, 3],
                "stride": {"values": [2, 3]}
            },
            {"type": "BatchNorm2d"},
            {"type": "MLP", "units": [128, 256, 512]},
            {"type": "BatchNorm"},
            {"type": "Dropout", "p": {"min": 0.1, "max": 0.5}},
            {
                "type": "Transformer", 
                "d_model": [128, 256], 
                "nhead": [2, 4, 8], 
                "num_layers": [1, 2]
            }
        ],
        "activation_function": ["ReLU", "GELU", "SiLU", "LeakyReLU", "ELU", "SELU", "Mish"],
        "loss_function": ["CrossEntropyLoss", "NLLLoss"],
        "optimizer": [
            {
                "type": "AdamW", 
                "min_layers": 3, 
                "max_layers": 8,
                "params": {
                    "lr": {"min": 1e-5, "max": 1e-3}, 
                    "weight_decay": {"min": 1e-4, "max": 1e-2},
                    "betas": (0.9, 0.999),
                    "eps": 1e-8
                }
            },
            {
                "type": "Adam", 
                "min_layers": 3, 
                "max_layers": 7,
                "params": {
                    "lr": {"min": 1e-5, "max": 1e-3},
                    "betas": (0.9, 0.999),
                    "eps": 1e-8,
                    "weight_decay": 0.0
                }
            },
            {
                "type": "SGD", 
                "min_layers": 2, 
                "max_layers": 6,
                "params": {
                    "lr": {"min": 1e-4, "max": 1e-2}, 
                    "momentum": {"min": 0.8, "max": 0.95},
                    "weight_decay": {"min": 1e-5, "max": 1e-3},
                    "nesterov": {"values": [True, False]}
                }
            },
            {
                "type": "RMSprop", 
                "min_layers": 2, 
                "max_layers": 6,
                "params": {
                    "lr": {"min": 1e-4, "max": 1e-2},
                    "alpha": {"values": [0.9, 0.95, 0.99]},
                    "eps": 1e-8,
                    "weight_decay": {"min": 1e-5, "max": 1e-3},
                    "momentum": 0.0
                }
            },
            {
                "type": "NAdam", 
                "min_layers": 2, 
                "max_layers": 5,
                "params": {
                    "lr": {"min": 1e-5, "max": 1e-3},
                    "betas": (0.9, 0.999),
                    "eps": 1e-8,
                    "weight_decay": {"min": 1e-5, "max": 1e-3}
                }
            }
        ]
    }
}