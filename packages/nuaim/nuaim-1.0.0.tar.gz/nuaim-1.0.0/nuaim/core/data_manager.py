from nuaim.utils import dataset_dict
import torch
from torch.utils.data import DataLoader, SubsetRandomSampler

class DataManager:
    def __init__(self, instance_params, device=None):
        self.instance_params = instance_params
        self.device = device or torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self._data_loader_cache = {}
    
    def create_or_get_data_loaders(self, batch_size=64, test_split=0.2, valid_split=0.2, dataset_frac=1.0):
        """Create or retrieve cached data loaders."""
        dataset_name = self.instance_params["dataset_name"]
        cache_key = (dataset_name, batch_size, test_split, valid_split, dataset_frac)
        if cache_key in self._data_loader_cache:
            return self._data_loader_cache[cache_key]

        dataset = dataset_dict.get(dataset_name)
        extra_args = self.instance_params.get("dataset_args", {})

        # Handle dataset-specific logic for train/test splits
        if dataset_name == "STL10":
            train_set = dataset(split="train", **extra_args)
            test_set = dataset(split="test", **extra_args)
        elif dataset_name == "SVHN":
            train_set = dataset(split="train", **extra_args)
            test_set = dataset(split="test", **extra_args)
        elif dataset_name == "QMNIST":
            train_set = dataset(what="train", **extra_args)
            test_set = dataset(what="test", **extra_args)
        elif dataset_name == "EMNIST":
            split = self.instance_params.get("split", "balanced")
            train_set = dataset(split=split, train=True, **extra_args)
            test_set = dataset(split=split, train=False, **extra_args)
        elif dataset_name == "LSUN":
            train_set = dataset(classes="train", **extra_args)
            test_set = dataset(classes="test", **extra_args)
        elif dataset_name == "LSUNClass":
            class_label = self.instance_params.get("class_label", "bedroom_train")
            train_set = dataset(class_label=class_label, **extra_args)
            test_set = dataset(class_label=class_label.replace("train", "val"), **extra_args)
        elif dataset_name == "Places365":
            train_set = dataset(split="train-standard", **extra_args)
            test_set = dataset(split="val", **extra_args)
        elif dataset_name == "ImageFolder":
            root = self.instance_params.get("root", "./data")
            train_set = dataset(root=root, **extra_args)
            test_set = dataset(root=root, **extra_args)  # You may want to split manually
        else:
            train_set = dataset(train=True, **extra_args)
            test_set = dataset(train=False, **extra_args)

        # Subsample train set
        total_train = int(len(train_set) * dataset_frac)
        train_indices_full = torch.randperm(len(train_set))[:total_train].tolist()
        valid_size = int(valid_split * total_train)
        train_size = total_train - valid_size
        train_indices = train_indices_full[:train_size]
        valid_indices = train_indices_full[train_size:]

        # Subsample test set
        total_test = int(len(test_set) * dataset_frac)
        test_indices = torch.randperm(len(test_set))[:total_test].tolist()

        train_sampler = SubsetRandomSampler(train_indices)
        valid_sampler = SubsetRandomSampler(valid_indices)
        test_sampler = SubsetRandomSampler(test_indices)

        train_loader = DataLoader(train_set, batch_size=batch_size, sampler=train_sampler)
        valid_loader = DataLoader(train_set, batch_size=batch_size, sampler=valid_sampler)
        test_loader = DataLoader(test_set, batch_size=batch_size, sampler=test_sampler)

        # Dynamically update instance_params based on the dataset
        sample_data, _ = train_set[0]
        if isinstance(sample_data, torch.Tensor):
            self.instance_params["in_features"] = sample_data.numel()
            self.instance_params["dimension"] = sample_data.shape
        else:
            raise ValueError("Dataset input must be a torch.Tensor.")

        all_targets = torch.tensor([target for _, target in train_set])
        min_target = int(all_targets.min().item())
        max_target = int(all_targets.max().item())

        # Calculate out_features based on the range of target values
        if min_target == 0:
            self.instance_params["out_features"] = max_target + 1
        else:
            self.instance_params["out_features"] = max_target

        self._data_loader_cache[cache_key] = (train_loader, valid_loader, test_loader)
        return train_loader, valid_loader, test_loader
