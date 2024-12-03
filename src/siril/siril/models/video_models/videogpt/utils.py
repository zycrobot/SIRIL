import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
from PIL import Image
# from termcolor import cprint
from torch.utils.data import DataLoader, Dataset

# --------------------------------------------- #
#                  Module Utils
#            for Encoder, Decoder etc.
# --------------------------------------------- #

def weights_init(m):
    classname = m.__class__.__name__
    if classname.find('Conv') != -1:
        nn.init.normal_(m.weight.data, 0.0, 0.02)
    elif classname.find('BatchNorm') != -1:
        nn.init.normal_(m.weight.data, 1.0, 0.02)
        nn.init.constant_(m.bias.data, 0)


def plot_images(images):
    x = images["input"]
    reconstruction = images["rec"]
    half_sample = images["half_sample"]
    full_sample = images["full_sample"]

    fig, axarr = plt.subplots(1, 4)
    axarr[0].imshow(x.cpu().detach().numpy()[0].transpose(1, 2, 0))
    axarr[1].imshow(reconstruction.cpu().detach().numpy()[0].transpose(1, 2, 0))
    axarr[2].imshow(half_sample.cpu().detach().numpy()[0].transpose(1, 2, 0))
    axarr[3].imshow(full_sample.cpu().detach().numpy()[0].transpose(1, 2, 0))
    plt.show()


class VideoDataset(Dataset):
    def __init__(self, data_path, train=True, frames_per_sample=3, frame_skip=1, random_time=True, total_videos=-1):
        self.data_path = data_path 
        self.train = train
        self.frames_per_sample = frames_per_sample
        self.frame_skip = frame_skip
        self.random_time = random_time
        self.total_videos = total_videos

        self.data_root = str(Path(__file__).parents[4]) + data_path
        self.images = []
        self.task_list = os.listdir(self.data_root)
        if 'clip_embs.npy' in self.task_list:
            self.task_list.remove('clip_embs.npy')
        all_video_paths = []
        for task in self.task_list:
            task_path = os.path.join(self.data_root, task, 'train') if self.train else os.path.join(self.data_root, task, 'test')
            task_videos = [os.path.join(task_path, video) for video in os.listdir(task_path)]
            all_video_paths += task_videos
        self.all_video_paths = all_video_paths
        if self.total_videos > 0:
            self.all_video_paths = np.random.choice(self.all_video_paths, self.total_videos)
        
        self.num_videos = len(all_video_paths)

    def preprocess_image(self, image):
        if not image.mode == "RGB":
            image = image.convert("RGB")
        image = np.array(image).astype(np.uint8)
        image = (image / 127.5 - 1.0).astype(np.float32)
        image = image.transpose(2, 0, 1)
        return image

    def preprocess_trajectory(self, traj_path):
        trajectory = np.load(traj_path).astype(np.float32)  
        return torch.tensor(trajectory, dtype=torch.float32)

    def __len__(self):
        return len(self.all_video_paths) * 100 // self.frames_per_sample

    def __getitem__(self, index):
        video_index = index % len(self.all_video_paths)
        video_path = self.all_video_paths[video_index]
        frame_len = len(os.listdir(video_path))

        # Randomly select a frame window
        if self.random_time and frame_len > (self.frames_per_sample * self.frame_skip):
            start_idx = np.random.randint(0, frame_len - self.frames_per_sample * self.frame_skip)
        else:
            start_idx = 0  # If deterministic behavior is required

        frame_indices = range(start_idx, start_idx + self.frames_per_sample * self.frame_skip, self.frame_skip)
        images = []
        trajectories = []

        for idx in frame_indices:
            img_path = os.path.join(video_path, f"{idx}.png")
            traj_path = os.path.join(video_path, f"{idx}_traj.npy")  
            
            # Preprocess image and trajectory data
            img = Image.open(img_path)
            img = self.preprocess_image(img)
            images.append(torch.tensor(img, dtype=torch.float32))
            
            traj = self.preprocess_trajectory(traj_path)
            trajectories.append(traj)

        # Stack images and trajectories
        images = torch.stack(images)  # Shape: (frames_per_sample, C, H, W)
        trajectories = torch.stack(trajectories)  # Shape: (frames_per_sample, action_dim)

        # Split into past trajectories and next action
        past_actions = trajectories[:-1]  # All except the last
        next_action = trajectories[-1]  # The last action

        return images, past_actions, next_action



class VideoDataLoader(DataLoader):
    def get_video(self, idx):
        return self.dataset.get_video(idx)


def load_video_data(cfg):
    train_data = VideoDataset(
        cfg.dataset_path, 
        frames_per_sample=cfg.num_frames + 1, 
        frame_skip=cfg.frame_skip, 
        train=True
    )
    train_loader = VideoDataLoader(train_data, batch_size=cfg.batch_size, shuffle=True)

    val_data = VideoDataset(
        cfg.dataset_path, 
        frames_per_sample=cfg.num_frames + 1, 
        frame_skip=cfg.frame_skip, 
        train=False
    )
    val_loader = VideoDataLoader(val_data, batch_size=cfg.batch_size, shuffle=False)

    return train_loader, val_loader