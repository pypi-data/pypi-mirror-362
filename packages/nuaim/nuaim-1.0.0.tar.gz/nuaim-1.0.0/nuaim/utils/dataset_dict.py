import torchvision.datasets as datasets
import torchvision.transforms as transforms

dataset_dict = {
    # Handwritten digits datasets
    "MNIST": lambda root="./data", train=True, transform=transforms.ToTensor(), download=True:
        datasets.MNIST(root=root, train=train, transform=transform, download=download),
    "QMNIST": lambda root="./data", what="train", transform=transforms.ToTensor(), download=True:
        datasets.QMNIST(root=root, what=what, transform=transform, download=download),
    "KMNIST": lambda root="./data", train=True, transform=transforms.ToTensor(), download=True:
        datasets.KMNIST(root=root, train=train, transform=transform, download=download),
    "EMNIST": lambda root="./data", split="balanced", train=True, transform=transforms.ToTensor(), download=True:
        datasets.EMNIST(root=root, split=split, train=train, transform=transform, download=download),
    "USPS": lambda root="./data", train=True, transform=transforms.ToTensor(), download=True:
        datasets.USPS(root=root, train=train, transform=transform, download=download),

    # Fashion and object datasets
    "FashionMNIST": lambda root="./data", train=True, transform=transforms.ToTensor(), download=True:
        datasets.FashionMNIST(root=root, train=train, transform=transform, download=download),
    "CIFAR10": lambda root="./data", train=True, transform=transforms.ToTensor(), download=True:
        datasets.CIFAR10(root=root, train=train, transform=transform, download=download),
    "CIFAR100": lambda root="./data", train=True, transform=transforms.ToTensor(), download=True:
        datasets.CIFAR100(root=root, train=train, transform=transform, download=download),
    "STL10": lambda root="./data", split="train", transform=transforms.ToTensor(), download=True:
        datasets.STL10(root=root, split=split, transform=transform, download=download),
    "SVHN": lambda root="./data", split="train", transform=transforms.ToTensor(), download=True:
        datasets.SVHN(root=root, split=split, transform=transform, download=download),

    # Generic folder-based dataset (for custom datasets)
    "ImageFolder": lambda root, transform=transforms.ToTensor():
        datasets.ImageFolder(root=root, transform=transform),
}