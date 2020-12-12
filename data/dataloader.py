import data
import os
from glob import glob
from torch.utils.data import DataLoader
from .dataset import AutoEncoderDataset, DraftModelDataset, ColorizationModelDataset

__DATASET_CANDIDATE__ = ['draft', 'colorization', 'autoencoder']


def create_data_loader(hyperparameters: dict,
                       dataset: str):

    assert dataset in __DATASET_CANDIDATE__, \
        "Dataset {} is not in {}".format(
            dataset, str(__DATASET_CANDIDATE__))

    image_path = hyperparameters['image_path']
    batch_size = hyperparameters['draft_stage']['batch_size']

    image_paths = sorted(glob(os.path.join(image_path, '*')))
    assert len(image_paths) != 0,\
        "Image path {} is Empty".format(image_path)

    image_paths = sorted(glob(os.path.join(image_path, '*')))
    pivot = int(len(image_paths) * 0.1)
    train_image_paths = image_paths[:-pivot]
    test_image_paths = image_paths[-pivot:]

    train_ds = DraftModelDataset(train_image_paths,
                                 training=True)

    test_ds = DraftModelDataset(test_image_paths,
                                training=False)

    train_dl = DataLoader(train_ds,
                          batch_size=batch_size,
                          shuffle=True,
                          num_workers=min(batch_size, 12),
                          pin_memory=hyperparameters['pin_memory'])

    test_dl = DataLoader(test_ds,
                         batch_size=8,
                         shuffle=True,
                         num_workers=min(batch_size, 12),
                         pin_memory=hyperparameters['pin_memory'])

    return train_dl, test_dl