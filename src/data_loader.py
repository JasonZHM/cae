import glob

import numpy as np
import torch
from PIL import Image
from torch.utils.data import Dataset


class ImageFolder720p(Dataset):
    """
    Image shape is (720, 1280, 3) --> (768, 1280, 3) --> 6x10 128x128 patches
    """


    def __init__(self, folder_path):
        self.files = sorted(glob.glob('%s/*.*' % folder_path))


    def __getitem__(self, index):
        path = self.files[index % len(self.files)]
        img = np.array(Image.open(path))
        h, w, c = img.shape

        pad = ((24, 24), (0, 0), (0, 0))

        # img = np.pad(img, pad, 'constant', constant_values=0) / 255
        img = np.pad(img, pad, mode='edge') / 255.0

        img = np.transpose(img, (2, 0, 1))
        img = torch.from_numpy(img).float()

        patches = np.reshape(img, (3, 6, 128, 10, 128))
        patches = np.transpose(patches, (0, 1, 3, 2, 4))

        return img, patches, path


    def get_random(self):
        i = np.random.randint(0, len(self.files))
        return self[i]


    def __len__(self):
        return len(self.files)
