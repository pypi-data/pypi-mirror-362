import torch.nn as nn

layer_dict = {
    "MLP": lambda in_features=128, out_features=64: 
         nn.Linear(in_features, out_features),

    "Conv2d": lambda in_channels=3, out_channels=16, kernel_size=3, stride=1, padding=1: 
           nn.Conv2d(in_channels, out_channels, kernel_size, stride, padding),
 
    "MaxPool2d": lambda kernel_size=2, stride=2: 
           nn.MaxPool2d(kernel_size, stride),

    "AvgPool2d": lambda kernel_size=2, stride=2: 
           nn.AvgPool2d(kernel_size, stride),

    "BatchNorm": lambda num_features=128: 
         nn.BatchNorm1d(num_features),

    "BatchNorm2d": lambda num_features=16: 
           nn.BatchNorm2d(num_features),

    "Dropout": lambda p=0.5: 
           nn.Dropout(p),

    "Flatten": lambda: nn.Flatten(),
}

class TransformerBlock(nn.Module):
    """
    A Transformer block using nn.TransformerEncoderLayer.
    Note: batch_first=True is used, so input should be (Batch, Seq, Feature).
    """
    def __init__(self, d_model=512, nhead=8, num_layers=6, dim_feedforward=2048, dropout=0.1, batch_first=True):
        super().__init__()
        if not batch_first:
            raise ValueError("TransformerBlock requires batch_first=True.")
        
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model, 
            nhead=nhead, 
            dim_feedforward=dim_feedforward, 
            dropout=dropout,
            batch_first=batch_first
        )
        self.transformer_encoder = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)

    def forward(self, src):
        return self.transformer_encoder(src)

# Add the custom TransformerBlock to the layer_dict
layer_dict['Transformer'] = TransformerBlock

class CNNBlock(nn.Module):
    """A block of Conv2d -> BatchNorm2d -> Activation -> Pooling."""
    def __init__(self, in_channels, out_channels, kernel_size=3, stride=1, padding=1, pooling_type="MaxPool2d", pool_kernel_size=2, activation=nn.ReLU):
        super().__init__()
        self.conv = nn.Conv2d(in_channels, out_channels, kernel_size, stride, padding, bias=False)
        self.bn = nn.BatchNorm2d(out_channels)
        self.act = activation()
        if pooling_type:
            if pooling_type == "MaxPool2d":
                self.pool = nn.MaxPool2d(kernel_size=pool_kernel_size, stride=pool_kernel_size)
            elif pooling_type == "AvgPool2d":
                self.pool = nn.AvgPool2d(kernel_size=pool_kernel_size, stride=pool_kernel_size)
        else:
            self.pool = nn.Identity()

    def forward(self, x):
        x = self.conv(x)
        x = self.bn(x)
        x = self.act(x)
        x = self.pool(x)
        return x

layer_dict["CNNBlock"] = CNNBlock
