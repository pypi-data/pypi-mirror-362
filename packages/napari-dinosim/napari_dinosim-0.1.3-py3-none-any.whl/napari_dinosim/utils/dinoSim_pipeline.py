import numpy as np
import torch
from torch.nn import functional as F
from tqdm import tqdm

from .data_utils_biapy import crop_data_with_overlap, merge_data_with_overlap
from .utils import mirror_border, remove_padding, resizeLongestSide


class DINOSim_pipeline:
    """A pipeline for computing and managing DINOSim.

    This class handles the computation of DINOSim, using DINOv2 embeddings, manages reference
    vectors, and computes similarity distances. It supports processing large images through
    a sliding window approach with overlap.

    Args:
        model: The DINOv2 model to use for computing embeddings
        model_patch_size (int): Size of patches used by the DINOv2 model
        device: The torch device to run computations on (CPU or GPU)
        img_preprocessing: Function to preprocess images before computing embeddings
        feat_dim (int): Number of features of the embeddings
        dino_image_size (int, optional): Size of the image to be fed to DINOv2. Images will be resized to that size before computing them with DINOv2. Defaults to 518.
    """

    def __init__(
        self,
        model,
        model_patch_size,
        device,
        img_preprocessing,
        feat_dim,
        dino_image_size=518,
    ):
        self.model = model
        self.dino_image_size = dino_image_size
        self.patch_h = self.patch_w = self.embedding_size = (
            dino_image_size // model_patch_size
        )
        self.img_preprocessing = img_preprocessing
        self.device = device
        self.feat_dim = feat_dim

        self.reference_color = torch.zeros(feat_dim, device=device)
        self.reference_emb = torch.zeros(
            (self.embedding_size * self.embedding_size, feat_dim),
            device=device,
        )
        self.exist_reference = False

        self.embeddings = torch.tensor([])
        self.emb_precomputed = False
        self.original_size = []
        self.overlap = (0.5, 0.5)
        self.padding = (0, 0)
        self.crop_shape = (518, 518, 3)
        self.resized_ds_size, self.resize_pad_ds_size = [], []
        self.embeddings_on_cpu = True
        self.batch_size = 1

    def check_gpu_memory(self, tensor_size):
        """Check if tensor can fit in GPU memory, return True if it can, False otherwise"""
        if self.device.type != "cuda":
            return False  # Always use CPU if device is not CUDA

        try:
            # Get available GPU memory
            torch.cuda.empty_cache()
            total_mem = torch.cuda.get_device_properties(
                self.device
            ).total_memory
            reserved_mem = torch.cuda.memory_reserved(self.device)
            allocated_mem = torch.cuda.memory_allocated(self.device)
            free_mem = total_mem - reserved_mem - allocated_mem

            # Estimate tensor memory requirements (bytes)
            elem_size = 4  # float32 is 4 bytes
            tensor_mem = tensor_size * elem_size

            # Leave some buffer (80% of free memory)
            return tensor_mem < free_mem * 0.8
        except Exception:
            return False  # Use CPU on any error

    def pre_compute_embeddings(
        self,
        dataset,
        overlap=(0.5, 0.5),
        padding=(0, 0),
        crop_shape=(512, 512, 1),
        verbose=True,
        batch_size=1,
    ):
        """Pre-compute DINO embeddings for the entire dataset.

        The dataset is processed in crops with optional overlap. Large images are handled
        through a sliding window approach, and small images are resized.

        Args:
            dataset: Input image dataset with shape (batch, height, width, channels)
            overlap (tuple, optional): Overlap fraction (y, x) between crops. Defaults to (0.5, 0.5).
            padding (tuple, optional): Padding size (y, x) for crops. Defaults to (0, 0).
            crop_shape (tuple, optional): Size of crops (height, width, channels). Defaults to (512, 512, 1).
            verbose (bool, optional): Whether to show progress bar. Defaults to True.
            batch_size (int, optional): Batch size for processing. Defaults to 1.
        """
        print("Precomputing embeddings")
        self.original_size = dataset.shape
        self.overlap = overlap
        self.padding = padding
        self.crop_shape = crop_shape
        b, h, w, c = dataset.shape
        self.resized_ds_size, self.resize_pad_ds_size = [], []
        self.batch_size = batch_size

        # if both image resolutions are smaller than the patch size,
        # resize until the largest side fits the patch size
        if h < crop_shape[0] and w < crop_shape[0]:
            dataset = np.array(
                [
                    resizeLongestSide(np_image, crop_shape[0])
                    for np_image in dataset
                ]
            )
            if len(dataset.shape) == 3:
                dataset = dataset[..., np.newaxis]
            self.resized_ds_size = dataset.shape

        # yet if one of the image resolutions is smaller than the patch size,
        # add mirror padding until smaller side fits the patch size
        if (
            dataset.shape[1] % crop_shape[0] != 0
            or dataset.shape[2] % crop_shape[1] != 0
        ):
            desired_h, desired_w = (
                np.ceil(dataset.shape[1] / crop_shape[0]) * crop_shape[0],
                np.ceil(dataset.shape[2] / crop_shape[1]) * crop_shape[1],
            )
            dataset = np.array(
                [
                    mirror_border(
                        np_image, sizeH=int(desired_h), sizeW=int(desired_w)
                    )
                    for np_image in dataset
                ]
            )
            self.resize_pad_ds_size = dataset.shape

        # needed format: b,h,w,c
        windows = crop_data_with_overlap(
            dataset,
            crop_shape=crop_shape,
            overlap=overlap,
            padding=padding,
            verbose=False,
        )
        windows = torch.tensor(windows, device=self.device)
        windows = self._quantile_normalization(windows.float())

        self.delete_precomputed_embeddings()

        # Estimate memory needed for embeddings
        tensor_shape = (
            len(windows),
            self.patch_h,
            self.patch_w,
            self.feat_dim,
        )
        tensor_size = np.prod(tensor_shape)

        # Decide where to store embeddings based on available memory
        # Default to CPU storage
        storage_device = torch.device("cpu")
        self.embeddings_on_cpu = True

        # Try GPU storage if available
        if self.device.type == "cuda" and self.check_gpu_memory(tensor_size):
            try:
                storage_device = self.device
                self.embeddings = torch.zeros(tensor_shape, device=self.device)
                self.embeddings_on_cpu = False
                if verbose:
                    print("Embeddings will be stored on GPU")
            except torch.cuda.OutOfMemoryError:
                storage_device = torch.device("cpu")
                torch.cuda.empty_cache()
                if verbose:
                    print(
                        "GPU memory exceeded during allocation, embeddings stored on CPU"
                    )

        # Create embeddings tensor if not already created
        if self.embeddings_on_cpu:
            self.embeddings = torch.zeros(tensor_shape, device=storage_device)
            if verbose:
                print(
                    f"Embeddings stored on CPU"
                    + (
                        ": estimated memory exceeds GPU capacity"
                        if self.device.type == "cuda"
                        else ""
                    )
                )

        following_f = tqdm if verbose else lambda aux: aux
        for i in following_f(range(0, len(windows), batch_size)):
            batch_windows = windows[i : i + batch_size]

            prep_batch = self.img_preprocessing(batch_windows)

            with torch.no_grad():
                if self.model is None:
                    raise ValueError("Model is not initialized")
                encoded_window = self.model.forward_features(prep_batch)[
                    "x_norm_patchtokens"
                ]
                encoded_window_reshaped = encoded_window.reshape(
                    encoded_window.shape[0],
                    self.patch_h,
                    self.patch_w,
                    self.feat_dim,
                )

            # Move computed embeddings to storage device
            self.embeddings[i : i + batch_size] = encoded_window_reshaped.to(
                storage_device
            )

            # Clear GPU memory if not storing on GPU
            del (
                batch_windows,
                prep_batch,
                encoded_window,
                encoded_window_reshaped,
            )
            if storage_device.type == "cpu":
                torch.cuda.empty_cache()

        self.emb_precomputed = True
        # Clean up large intermediate tensor
        del windows
        torch.cuda.empty_cache()

    def _quantile_normalization(
        self,
        tensor,
        lower_quantile: float = 0.01,
        upper_quantile: float = 0.99,
    ):
        """Normalize tensor values between quantile bounds.

        Args:
            tensor (torch.Tensor): Input tensor to normalize
            lower_quantile (float): Lower quantile bound (0-1)
            upper_quantile (float): Upper quantile bound (0-1)

        Returns:
            torch.Tensor: Normalized tensor with values between 0 and 1
        """
        is_tensor = isinstance(tensor, torch.Tensor)
        if is_tensor and tensor.numel() > 1e6:  # If tensor is large
            # Convert to numpy for computation
            tensor_np = tensor.cpu().numpy()
            lower_bound = np.quantile(tensor_np, lower_quantile)
            upper_bound = np.quantile(tensor_np, upper_quantile)
            clipped_tensor = np.clip(tensor_np, lower_bound, upper_bound)
            normalized_tensor = (clipped_tensor - lower_bound) / (
                upper_bound - lower_bound + 1e-8
            )
            return (
                torch.from_numpy(normalized_tensor)
                .to(tensor.dtype)
                .to(tensor.device)
            )
        elif is_tensor:
            lower_bound = torch.quantile(tensor, lower_quantile)
            upper_bound = torch.quantile(tensor, upper_quantile)
            clipped_tensor = torch.clamp(tensor, lower_bound, upper_bound)
        else:
            # Use numpy.quantile
            lower_bound = np.quantile(tensor, lower_quantile)
            upper_bound = np.quantile(tensor, upper_quantile)
            clipped_tensor = np.clip(tensor, lower_bound, upper_bound)

        normalized_tensor = (clipped_tensor - lower_bound) / (
            upper_bound - lower_bound + 1e-8
        )
        return normalized_tensor

    def delete_precomputed_embeddings(
        self,
    ):
        del self.embeddings
        self.embeddings = torch.tensor([])
        self.emb_precomputed = False
        torch.cuda.empty_cache()

    def delete_references(
        self,
    ):
        del self.reference_color, self.reference_emb, self.exist_reference
        self.reference_color = torch.zeros(self.feat_dim, device=self.device)
        self.reference_emb = torch.zeros(
            (self.embedding_size * self.embedding_size, self.feat_dim),
            device=self.device,
        )
        self.exist_reference = False
        torch.cuda.empty_cache()

    def set_reference_vector(self, list_coords, filter=None):
        """Set reference vectors from a list of coordinates in the original image space.

        Computes mean embeddings from the specified coordinates to use as reference vectors
        for similarity computation.

        Args:
            list_coords: List of tuples (batch_idx, z, x, y) specifying reference points
            filter: Optional filter to apply to the generated pseudolabels
        """
        self.delete_references()
        if len(self.resize_pad_ds_size) > 0:
            b, h, w, c = self.resize_pad_ds_size
            if len(self.resized_ds_size) > 0:
                original_resized_h, original_resized_w = self.resized_ds_size[
                    1:3
                ]
            else:
                original_resized_h, original_resized_w = self.original_size[
                    1:3
                ]
        elif len(self.resized_ds_size) > 0:
            b, h, w, c = self.resized_ds_size
            original_resized_h, original_resized_w = h, w
        else:
            b, h, w, c = self.original_size
            original_resized_h, original_resized_w = h, w

        n_windows_h = int(np.ceil(h / self.crop_shape[0]))
        n_windows_w = int(np.ceil(w / self.crop_shape[1]))

        # Calculate actual scaling factors
        scale_x = original_resized_w / self.original_size[2]
        scale_y = original_resized_h / self.original_size[1]

        # Calculate padding
        pad_left = (w - original_resized_w) / 2
        pad_top = (h - original_resized_h) / 2

        list_ref_colors, list_ref_embeddings = [], []
        for n, x, y in list_coords:
            # Apply scaling and padding to coordinates
            x_transformed = x * scale_x + pad_left
            y_transformed = y * scale_y + pad_top

            # Calculate crop index and relative position within crop
            n_crop = int(
                np.floor(x_transformed / self.crop_shape[1])
                + np.floor(y_transformed / self.crop_shape[0]) * n_windows_w
            )
            x_coord = (x_transformed % self.crop_shape[1]) / self.crop_shape[1]
            y_coord = (y_transformed % self.crop_shape[0]) / self.crop_shape[0]

            emb_id = int(n_crop + n * n_windows_h * n_windows_w)

            # Validate embedding index
            if emb_id >= len(self.embeddings):
                raise ValueError(
                    f"Invalid embedding index {emb_id} for coordinates ({n}, {x}, {y})"
                )

            # Ensure embeddings are on the computation device (GPU if available)
            emb_slice = self.embeddings[emb_id]
            if self.embeddings_on_cpu:
                emb_slice = emb_slice.to(self.device)

            x_coord = min(
                round(x_coord * self.embedding_size), self.embedding_size - 1
            )
            y_coord = min(
                round(y_coord * self.embedding_size), self.embedding_size - 1
            )

            list_ref_colors.append(emb_slice[y_coord, x_coord])
            list_ref_embeddings.append(emb_slice)

        list_ref_colors, list_ref_embeddings = torch.stack(
            list_ref_colors
        ), torch.stack(list_ref_embeddings)
        assert (
            len(list_ref_colors) > 0
        ), "No binary objects found in given masks"

        self.reference_color = torch.mean(list_ref_colors, dim=0)
        self.reference_emb = list_ref_embeddings
        self.generate_pseudolabels(filter)
        self.exist_reference = True

    def generate_pseudolabels(self, filter=None):
        reference_embeddings = self.reference_emb.view(
            -1, self.reference_emb.shape[-1]
        )
        distances = torch.cdist(
            reference_embeddings, self.reference_color[None], p=2
        )

        if filter != None:
            distances = distances.view(
                (
                    self.reference_emb.shape[0],
                    1,
                    int(self.embedding_size),
                    int(self.embedding_size),
                )
            )
            distances = filter(distances)

        # normalize per image
        distances = self._quantile_normalization(distances)

        self.reference_pred_labels = distances.view(-1, 1)

    def get_ds_distances_sameRef(self, verbose=True, k=5):
        """Compute distances between dataset embeddings and reference embeddings.

        Uses k-nearest neighbors to compute similarity scores.

        Args:
            verbose (bool, optional): Whether to show progress bar. Defaults to True.
            k (int, optional): Number of nearest neighbors to use. Defaults to 5.

        Returns:
            numpy.ndarray: Array of distance scores
        """
        distances = []
        following_f = tqdm if verbose else lambda x: x
        for i in following_f(range(len(self.embeddings))):
            encoded_windows = self.embeddings[i]
            # Move to computation device if stored on CPU
            if self.embeddings_on_cpu:
                encoded_windows = encoded_windows.to(self.device)

            if isinstance(
                encoded_windows, np.ndarray
            ):  # Should not happen now, but keep check
                encoded_windows = torch.tensor(
                    encoded_windows, device=self.device
                )
            total_features = encoded_windows.reshape(
                1, self.patch_h, self.patch_w, self.feat_dim
            ).to(
                device=self.device
            )  # use all dims

            mask = self._get_torch_knn_mask(
                total_features[0], k=k
            )  # get distance map
            distances.append(mask.cpu().numpy())

            # Clear GPU cache if embeddings were moved
            if self.embeddings_on_cpu:
                del encoded_windows, total_features
                torch.cuda.empty_cache()

        return np.array(distances)

    def _get_torch_knn_mask(self, image_representation, k=5):
        old_shape = image_representation.shape
        embs = image_representation.view(-1, old_shape[-1])
        ref = self.reference_emb.view(-1, self.reference_emb.shape[-1])
        distances_knn = torch.cdist(embs, ref, p=2)
        knn_values, knn_indices = torch.topk(
            distances_knn, k=k, largest=False, dim=1
        )
        knn_labels = self.reference_pred_labels[knn_indices]

        predictions = torch.mean(knn_labels.to(torch.float32), dim=1)
        predictions = predictions.view(old_shape[:-1])
        return predictions

    def distance_post_processing(
        self, distances, low_res_filter, upsampling_mode
    ):
        """Post-process computed distances by merging crops and resizing.

        Args:
            distances: Computed distance scores
            low_res_filter: Optional filter to apply to low-resolution distance maps
            upsampling_mode: Mode for upsampling distance maps ('bilinear', 'nearest', etc.)

        Returns:
            numpy.ndarray: Processed distance maps with shape (batch, height, width, 1)
        """
        if len(self.resize_pad_ds_size) > 0:
            ds_shape = self.resize_pad_ds_size
        elif len(self.resized_ds_size) > 0:
            ds_shape = self.resized_ds_size
        else:
            ds_shape = self.original_size
        ds_shape = list(ds_shape)
        ds_shape[-1] = 1  # distances only has 1 channel
        b, h, w, c = ds_shape
        distances = np.array(distances)[..., np.newaxis]
        emb_h, emb_w = (
            (np.array((h, w)) / self.crop_shape[:2]) * self.embedding_size
        ).astype(np.uint16)
        recons_parts = merge_data_with_overlap(
            distances,
            (b, emb_h, emb_w, c),
            overlap=self.overlap,
            padding=self.padding,
            verbose=False,
            out_dir=None,
            prefix="",
        )
        recons_parts = torch.tensor(recons_parts, device=self.device).permute(
            0, 3, 1, 2
        )  # b,c,h,w

        if low_res_filter != None:
            recons_parts = low_res_filter(recons_parts)
            # Ensure 4D tensor (batch, channel, height, width)
            if len(recons_parts.shape) == 3:
                recons_parts = recons_parts.unsqueeze(
                    1 if c == 1 else 0
                )  # Add channel or batch dimension if missing
            elif len(recons_parts.shape) == 2:
                recons_parts = recons_parts.unsqueeze(0).unsqueeze(
                    1
                )  # Add batch and channel dimensions

        if upsampling_mode != None:
            # resize to padded image size or resized image (small images)
            if (
                len(self.resize_pad_ds_size) > 0
                or len(self.resized_ds_size) > 0
            ):
                recons_parts = F.interpolate(
                    recons_parts,
                    size=(h, w),
                    mode=upsampling_mode,
                    align_corners=False,
                )

            # remove padding
            if len(self.resize_pad_ds_size) > 0:
                b, h, w, c = (
                    self.resized_ds_size
                    if len(self.resized_ds_size) > 0
                    else self.original_size
                )
                recons_parts = remove_padding(recons_parts, (h, w))

            # resize to original size
            b, h, w, c = self.original_size
            recons_parts = F.interpolate(
                recons_parts,
                size=(h, w),
                mode=upsampling_mode,
                align_corners=False,
            )

        return recons_parts.permute(0, 2, 3, 1).cpu().numpy()  # b,h,w,c

    def __del__(self):
        self.delete_references()
        self.delete_precomputed_embeddings()
        self.model = None
        torch.cuda.empty_cache()

    def save_reference(self, filepath):
        """Save the current reference color and embeddings to a file.

        Args:
            filepath (str): Path where to save the reference data

        Raises:
            ValueError: If no reference exists to save
        """
        if not self.exist_reference:
            raise ValueError("No reference exists to save")

        torch.save(
            {
                "reference_color": self.reference_color,
                "reference_emb": self.reference_emb,
                "reference_pred_labels": self.reference_pred_labels,
                "embedding_size": self.embedding_size,
                "feat_dim": self.feat_dim,
            },
            filepath,
        )

    def load_reference(self, filepath, filter=None):
        """Load reference color and embeddings from a file.

        Args:
            filepath (str): Path to the saved reference data
            filter: Optional filter to apply when generating pseudolabels

        Raises:
            ValueError: If the loaded reference is incompatible with current settings
        """
        checkpoint = torch.load(
            filepath, map_location=self.device, weights_only=True
        )

        # Verify compatibility
        if checkpoint["embedding_size"] != self.embedding_size:
            raise ValueError(
                f"Incompatible embedding_size: saved {checkpoint['embedding_size']} vs current {self.embedding_size}"
            )
        if checkpoint["feat_dim"] != self.feat_dim:
            raise ValueError(
                f"Incompatible feat_dim: saved {checkpoint['feat_dim']} vs current {self.feat_dim}"
            )

        self.reference_color = checkpoint["reference_color"]
        self.reference_emb = checkpoint["reference_emb"]
        self.reference_pred_labels = checkpoint["reference_pred_labels"]
        self.exist_reference = True

        if filter is not None:
            self.generate_pseudolabels(filter)

        self.emb_precomputed = True
        # Determine if loaded embeddings are on CPU
        self.embeddings_on_cpu = self.embeddings.device.type == "cpu"

        print(f"Embeddings loaded from {filepath}")

    def save_embeddings(self, filepath):
        """Save precomputed embeddings and related variables to a file.

        Args:
            filepath (str): Path where to save the embeddings data

        Raises:
            ValueError: If no embeddings exist to save
        """
        if not self.emb_precomputed or self.embeddings.numel() == 0:
            raise ValueError("No precomputed embeddings exist to save")

        embeddings_to_save = self.embeddings
        # Move to CPU before saving if on GPU
        if (
            not self.embeddings_on_cpu
            and self.embeddings.device.type == "cuda"
        ):
            embeddings_to_save = self.embeddings.cpu()

        torch.save(
            {
                "embeddings": embeddings_to_save,
                "original_size": self.original_size,
                "overlap": self.overlap,
                "padding": self.padding,
                "crop_shape": self.crop_shape,
                "resized_ds_size": self.resized_ds_size,
                "resize_pad_ds_size": self.resize_pad_ds_size,
                "patch_h": self.patch_h,
                "patch_w": self.patch_w,
                "embedding_size": self.embedding_size,
                "feat_dim": self.feat_dim,
            },
            filepath,
        )
        print(f"Embeddings saved to {filepath}")

    def load_embeddings(self, filepath):
        """Load precomputed embeddings and related variables from a file.

        Args:
            filepath (str): Path to the saved embeddings data

        Raises:
            ValueError: If the loaded embeddings are incompatible with current settings
        """
        checkpoint = torch.load(
            filepath, map_location=self.device, weights_only=True
        )

        # Verify compatibility
        if checkpoint["embedding_size"] != self.embedding_size:
            raise ValueError(
                f"Incompatible embedding_size: saved {checkpoint['embedding_size']} vs current {self.embedding_size}"
            )
        if checkpoint["feat_dim"] != self.feat_dim:
            raise ValueError(
                f"Incompatible feat_dim: saved {checkpoint['feat_dim']} vs current {self.feat_dim}"
            )
        if (
            checkpoint["patch_h"] != self.patch_h
            or checkpoint["patch_w"] != self.patch_w
        ):
            raise ValueError(
                f"Incompatible patch dimensions: saved ({checkpoint['patch_h']}, {checkpoint['patch_w']}) vs current ({self.patch_h}, {self.patch_w})"
            )

        # Load state
        loaded_embeddings = checkpoint["embeddings"]
        # Determine if loaded embeddings are on CPU before moving
        self.embeddings_on_cpu = loaded_embeddings.device.type == "cpu"
        self.embeddings = loaded_embeddings.to(self.device)

        self.original_size = checkpoint["original_size"]
        self.overlap = checkpoint["overlap"]
        self.padding = checkpoint["padding"]
        self.crop_shape = checkpoint["crop_shape"]
        self.resized_ds_size = checkpoint["resized_ds_size"]
        self.resize_pad_ds_size = checkpoint["resize_pad_ds_size"]
        self.emb_precomputed = True

        print(f"Embeddings loaded from {filepath}")
