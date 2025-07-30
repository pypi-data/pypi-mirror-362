import pickle
import torch
from torch.utils.data import Dataset, DataLoader
import torch.nn.functional as F
from tqdm.auto import tqdm
from typing import Tuple
import math
import numpy as np
import time
import math
from functools import reduce
from operator import mul
from typing import Sequence, Tuple




# -----------------------------------------------------------------------------
#                  D a t a s e t   f o r   s l i d i n g   p a t c h e s
# -----------------------------------------------------------------------------


class SlidingWindowND(Dataset):
    """Iterate over a 2-D or 3-D Numpy array with a sliding window.

    Parameters
    ----------
    volume : np.ndarray
        A 2-D array (H, W) or a 3-D array (D, H, W).
    window : Sequence[int]
        Window size per axis.  Length must equal `volume.ndim`.
    stride : Sequence[int]
        Step size per axis.  Length must equal `volume.ndim`.
    """

    def __init__(
        self,
        volume: np.ndarray,
        *,
        window: Sequence[int],
        stride: Sequence[int],
    ):
        if volume.ndim not in (2, 3):
            raise ValueError("Only 2-D and 3-D volumes are supported.")
        if len(window) != volume.ndim or len(stride) != volume.ndim:
            raise ValueError("`window` and `stride` must match volume.ndim.")

        self.volume = volume
        self.window = tuple(window)
        self.stride = tuple(stride)

        # How many windows along each axis?
        self.grid_shape: Tuple[int, ...] = tuple(
            math.floor((sz - win) / st) + 1
            for sz, win, st in zip(volume.shape, self.window, self.stride)
        )
        self._n_patches = reduce(mul, self.grid_shape)

    # ---------------------------------------------------------------- required
    def __len__(self) -> int:
        return self._n_patches

    def __getitem__(self, idx: int) -> torch.Tensor:
        # Convert 1-D idx → N-D grid indices (little unravel_index)
        coords = []
        for dim in reversed(self.grid_shape):
            coords.append(idx % dim)
            idx //= dim
        coords = coords[::-1]  # now in correct order

        # Upper-left/front corner of the patch
        offset = tuple(c * st for c, st in zip(coords, self.stride))

        # Construct slice objects per axis
        slices = tuple(slice(o, o + w) for o, w in zip(offset, self.window))
        patch = self.volume[slices]

        # Add a channel dim so downstream models always see [C, ...]
        if patch.ndim == 2:  # (H, W)  → (1, H, W)
            patch = patch[np.newaxis, ...]
        else:                # (D, H, W) → (1, D, H, W)
            patch = patch[np.newaxis, ...]

        return torch.from_numpy(patch).float()





class TraverseDataset2d(Dataset):
    def __init__(self, img: np.ndarray, stride: int, win_size: int, v: bool = False):
        """
        Args:
            img (np.ndarray): RGB image of shape [H, W, 3]
            stride (int): Sliding window stride
            win_size (int): Size of the square window
            v (bool): Verbose flag
        """
        assert img.ndim == 3 and img.shape[2] == 3, "Input must be an RGB image with shape [H, W, 3]"
        
        self.img = img
        self.v = v
        self.stride = stride
        self.win_size = win_size

        if v:
            print(f"init TraverseDataset2d with image of shape {img.shape}, stride = {stride}, win_size = {win_size}")

        self.patches = self._generate_patches()

    def _generate_patches(self):
        img = self.img
        patches = []
        for y in range(0, img.shape[0] - self.win_size + 1, self.stride):
            for x in range(0, img.shape[1] - self.win_size + 1, self.stride):
                patch = img[
                    y:y + self.win_size,
                    x:x + self.win_size,
                    :
                ]
                patches.append(patch)

        self.sample_shape = np.array([
            (img.shape[0] - self.win_size) // self.stride + 1,
            (img.shape[1] - self.win_size) // self.stride + 1,
        ])
        if self.v:
            print(f"sample shape = {self.sample_shape}")
        return patches

    def _get_sample_shape(self):
        return self.sample_shape

    def __len__(self):
        return len(self.patches)

    def __getitem__(self, idx):
        patch = self.patches[idx]
        patch = torch.tensor(patch, dtype=torch.float32).permute(2, 0, 1)  # Convert to [C, H, W]
        return patch

class TraverseDataset3d(Dataset):
    def __init__(self, img, stride: int, win_size, verbose=False):
        """
        Traverse a 3D volume using a sliding window.

        Args:
            img (ndarray): 3D input image of shape (Z, Y, X).
            stride (int): Stride for the sliding window.
            win_size (int or tuple/list of 3 ints): Size of the window in (Z, Y, X).
            verbose (bool): Print debug info if True.
        """
        self.img = img
        self.stride = stride
        self.win_size = self._normalize_win_size(win_size)
        self.verbose = verbose

        if self.verbose:
            print(f"Initializing TraverseDataset3d with shape {img.shape}, "
                  f"stride={stride}, win_size={self.win_size}")

        self.patches, self.sample_shape = self._generate_patches()

        if self.verbose:
            print(f"Sample shape: {self.sample_shape}, Total patches: {len(self.patches)}")

    def _normalize_win_size(self, win_size):
        """Ensure win_size is a tuple of 3 ints."""
        if isinstance(win_size, int):
            return (win_size,) * 3
        if isinstance(win_size, (list, tuple)) and len(win_size) == 3:
            return tuple(win_size)
        raise ValueError("win_size must be an int or a list/tuple of 3 ints.")

    def _generate_patches(self):
        """Extract 3D patches from the input image."""
        wz, wy, wx = self.win_size
        sz = (self.img.shape[0] - wz) // self.stride + 1
        sy = (self.img.shape[1] - wy) // self.stride + 1
        sx = (self.img.shape[2] - wx) // self.stride + 1

        patches = [
            self.img[z:z+wz, y:y+wy, x:x+wx]
            for z in range(0, self.img.shape[0] - wz + 1, self.stride)
            for y in range(0, self.img.shape[1] - wy + 1, self.stride)
            for x in range(0, self.img.shape[2] - wx + 1, self.stride)
        ]

        return patches, np.array([sz, sy, sx])

    def __len__(self):
        return len(self.patches)

    def __getitem__(self, idx):
        """Return a patch as a 1xD x H x W torch tensor."""
        patch = torch.from_numpy(self.patches[idx]).float().unsqueeze(0)
        return patch

    def get_sample_shape(self):
        return self.sample_shape

import numpy as np
import torch
from torch.utils.data import Dataset

class TraverseDataset3d_overlap(Dataset):
    def __init__(self, img, win_size, overlap=0, verbose=False):
        """
        Args:
            img (np.ndarray): 3D input image, shape (Z, Y, X)
            win_size (int or tuple/list of 3 ints): size of the 3D patch
            overlap (int or tuple/list of 3 ints): overlap between patches
            verbose (bool): if True, prints info during initialization
        """
        self.img = img
        self.verbose = verbose

        # Normalize win_size and overlap to 3-element lists
        self.win_size = self._expand_to_3d(win_size)
        self.overlap = self._expand_to_3d(overlap)

        # Compute stride
        self.stride = [w - o for w, o in zip(self.win_size, self.overlap)]
        if any(s <= 0 for s in self.stride):
            raise ValueError("Overlap must be smaller than win_size in all dimensions.")

        if self.verbose:
            print(f"Init TraverseDataset3d: img shape={img.shape}, win_size={self.win_size}, overlap={self.overlap}, stride={self.stride}")

        self.patches, self.roi_nums = self._generate_patches()

    def _expand_to_3d(self, val):
        if isinstance(val, int):
            return [val] * 3
        elif isinstance(val, (list, tuple)) and len(val) == 3:
            return list(val)
        else:
            raise ValueError("win_size and overlap must be either int or list/tuple of 3 ints")

    def _generate_patches(self):
        patches = []
        Z, Y, X = self.img.shape
        wz, wy, wx = self.win_size
        sz, sy, sx = self.stride

        for z in range(0, Z - wz + 1, sz):
            for y in range(0, Y - wy + 1, sy):
                for x in range(0, X - wx + 1, sx):
                    patch = self.img[z:z + wz, y:y + wy, x:x + wx]
                    patches.append(patch)

        roi_nums = [(img_dim - win + stride) // stride
                        for img_dim, win, stride in zip(self.img.shape, self.win_size, self.stride)]
        
        if self.verbose:
            print(f"Generated {len(patches)} patches with sample shape {roi_nums}")

        return patches, roi_nums

    def __len__(self):
        return len(self.patches)

    def __getitem__(self, idx):
        patch = torch.from_numpy(self.patches[idx]).float().unsqueeze(0)
        return patch

    def get_roi_nums(self):
        return self.roi_nums

def extract_feats(img_vol,win_size,cnn,mlp,stride,batch_size):
    """
    img_vol: need to be precropped
    """

    draw_border_dataset = TraverseDataset3d(img_vol,stride=stride,win_size=win_size)  
    border_draw_loader = DataLoader(draw_border_dataset,batch_size,shuffle=False,drop_last=False)
    print(f"len of dataset is {len(draw_border_dataset)}")

    current = time.time()
    feats_lst = get_feature_list('cuda',cnn,mlp,border_draw_loader,save_path=None)
    out_shape = draw_border_dataset.sample_shape

    print(f"extracting feature from image consume {time.time()-current} seconds")
    return feats_lst,out_shape


def get_feature_list(device,encoder,test_loader,extract_layer_name=None,save_path=None,adaptive_pool=False)->np.ndarray:
    """
    encoder inference on a single input 2d-image
    
    input(numpy)--> test_dataset
    collect feats during inference
    return the feats as shape of N*n_dim

    """
    print(f"device is {device}")


    # a dict to store the activations
    activation = {}
    def getActivation(name):
        # the hook signature
        def hook(model, input, output):
            activation[name] = output.detach()
        return hook

    #register the forward hook at layer"layer_name"
    if extract_layer_name:
        hook1 = getattr(encoder,extract_layer_name).register_forward_hook(getActivation(extract_layer_name))

    feats_list = []
    for i, imgs in enumerate(tqdm(test_loader,desc="extracting features")):
        outs=encoder(imgs.to(device))
        if adaptive_pool:
            outs = F.adaptive_avg_pool3d(outs, output_size=(1, 1, 1))
        B = outs.shape[0]
        if extract_layer_name:
            feats_list.append( np.squeeze(activation[extract_layer_name].cpu().detach().numpy().reshape(B,-1)))
        else:
            feats_list.append( np.squeeze(outs.cpu().detach().numpy().reshape(B,-1)))
    #detach the hook
    if extract_layer_name:
        hook1.remove()

    feats_array = np.concatenate([ arr for arr in feats_list], axis=0)
    print(f"fests_arry shape {feats_array.shape}")

    if save_path :
        with open(save_path, 'wb') as file:
            pickle.dump(feats_array, file)
    
    return feats_array






def get_feature_map(device,encoder,img = None,extract_layer_name=None,loader=None, overlap_i =32 ,roi_nums=None)->np.ndarray:
    """
    encoder inference on a single input 2d-image
    
    input(numpy)--> test_dataset
    collect feats during inference
    return the feats as shape of N*n_dim

    """
    print(f"device is {device}")


    # a dict to store the activations
    activation = {}
    def getActivation(name):
        # the hook signature
        def hook(model, input, output):
            activation[name] = output.detach()
        return hook

    #register the forward hook at layer"layer_name"
    if extract_layer_name:
        hook1 = getattr(encoder,extract_layer_name).register_forward_hook(getActivation(extract_layer_name))

    if isinstance(img, np.ndarray) : 
        input = torch.from_numpy(img).float().unsqueeze(0).to(device)
        outs=encoder(input)
        B = outs.shape[0]
        if extract_layer_name:
            feats_map =  np.squeeze(activation[extract_layer_name].cpu().detach().numpy())
        else:
            feats_map =  np.squeeze(outs.cpu().detach().numpy())
        #detach the hook
        if extract_layer_name:
            hook1.remove()

        return feats_map 
    else:

        test_batch_input = next(iter(loader)) 
        test_out = encoder(test_batch_input.to(device))
        # B should be 1
        C,H,W = np.squeeze(test_out.cpu().detach().numpy()).shape
        input_H = 1024
        input_W = 1024
        margin =int( np.ceil( overlap_i* H / input_H)) # cut margin at both side of H and W

        final_chunk_shape = (1,int((H-2*margin)),int((W-2*margin)),C )
        chunk_H = final_chunk_shape[1]
        chunk_W = final_chunk_shape[2]
        final_feats_shape = (1,final_chunk_shape[1]*roi_nums[1],final_chunk_shape[2]*roi_nums[2],C)
        final_feats_map = np.zeros(shape=final_feats_shape)


        for i, imgs in enumerate(tqdm(loader, desc='extracting features')):
            # batch =1

            outs=encoder(imgs.to(device))
            if extract_layer_name:
                feats_map =np.moveaxis( np.squeeze(activation[extract_layer_name].cpu().detach().numpy()), 0,-1)
            else:
                feats_map = np.moveaxis( np.squeeze(outs.cpu().detach().numpy()), 0,-1)

            feats_map = np.expand_dims(feats_map,axis=0) #(1,H,W,C)
            # Handle cropping depending on margin
            if margin > 0:
                feats_map_cropped = feats_map[:, margin:-margin, margin:-margin, :]
            else:
                feats_map_cropped = feats_map

            y = i // roi_nums[2]
            x = i % roi_nums[2]

            index = (
                slice(None),
                slice(y * chunk_H, (y + 1) * chunk_H),
                slice(x * chunk_W, (x + 1) * chunk_W),
                slice(None)
            )
            final_feats_map[index] = feats_map_cropped

        if extract_layer_name:
            hook1.remove()


        return np.squeeze(final_feats_map)
