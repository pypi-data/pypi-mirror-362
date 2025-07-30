import torch.nn as nn

loss_func_dict = {
    "CrossEntropyLoss": lambda: nn.CrossEntropyLoss(),
    "MSELoss": lambda: nn.MSELoss(),
    "L1Loss":  lambda: nn.L1Loss(),
    # Added loss functions
    "NLLLoss": lambda: nn.NLLLoss(),
    "PoissonNLLLoss": lambda: nn.PoissonNLLLoss(),
    "GaussianNLLLoss": lambda: nn.GaussianNLLLoss(),
    "KLDivLoss": lambda: nn.KLDivLoss(),
    "BCELoss": lambda: nn.BCELoss(),
    "BCEWithLogitsLoss": lambda: nn.BCEWithLogitsLoss(),
    "MarginRankingLoss": lambda: nn.MarginRankingLoss(),
    "HingeEmbeddingLoss": lambda: nn.HingeEmbeddingLoss(),
    "MultiLabelMarginLoss": lambda: nn.MultiLabelMarginLoss(),
    "HuberLoss": lambda: nn.HuberLoss(),
    "SmoothL1Loss": lambda: nn.SmoothL1Loss(),
    "SoftMarginLoss": lambda: nn.SoftMarginLoss(),
    "MultiLabelSoftMarginLoss": lambda: nn.MultiLabelSoftMarginLoss(),
    "CosineEmbeddingLoss": lambda: nn.CosineEmbeddingLoss(),
    "MultiMarginLoss": lambda: nn.MultiMarginLoss(),
    "TripletMarginLoss": lambda: nn.TripletMarginLoss(),
}
