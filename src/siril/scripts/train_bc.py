import os
import shutil
import time

import matplotlib
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from siril.models.video_models.videogpt.transformer import \
    VideoGPTTransformer
from siril.models.video_models.videogpt.utils import load_video_data
from siril.models.reward_models.sir import SIR

from torchvision import utils as vutils
from siril.logger import Logger
from tqdm import tqdm
from pathlib import Path

import hydra
import matplotlib.pyplot as plt


class BC:
    def __init__(self, args):
        self.args = args
        # self.work_dir = 'results'
        self.work_dir= Path.cwd()
        print(f'workspace: {self.work_dir}')
        self.model = VideoGPTTransformer(args).to(device=args.device)
        self.optim = self.configure_optimizers()

        self.prepare_training()
        self.logger=Logger(log_dir=self.work_dir,use_tb=False,use_wandb=False)

        self.train(args)

    def prepare_training(self):
        if os.path.exists(f"{self.work_dir}/results"):
            shutil.rmtree(f"{self.work_dir}/results")
        os.makedirs(f"{self.work_dir}/results", exist_ok=True)
        if os.path.exists(f"{self.work_dir}/checkpoints"):
            shutil.rmtree(f"{self.work_dir}/checkpoints") 
        os.makedirs(f"{self.work_dir}/checkpoints", exist_ok=True)


        
    def configure_optimizers(self):
        decay, no_decay = set(), set()
        whitelist_weight_modules = (nn.Linear, )
        blacklist_weight_modules = (nn.LayerNorm, nn.Embedding)

        for mn, m in self.model.transformer.named_modules():
            for pn, p in m.named_parameters():
                fpn = f"{mn}.{pn}" if mn else pn

                if pn.endswith("bias"):
                    no_decay.add(fpn)

                elif pn.endswith("weight") and isinstance(m, whitelist_weight_modules):
                    decay.add(fpn)

                elif pn.endswith("weight") and isinstance(m, blacklist_weight_modules):
                    no_decay.add(fpn)

        no_decay.add("pos_emb")

        param_dict = {pn: p for pn, p in self.model.transformer.named_parameters()}

        optim_groups = [
            {"params": [param_dict[pn] for pn in sorted(list(decay))], "weight_decay": 0.01},
            {"params": [param_dict[pn] for pn in sorted(list(no_decay))], "weight_decay": 0.0},
        ]

        optimizer = torch.optim.AdamW(optim_groups, lr=4.5e-06, betas=(0.9, 0.95))
        return optimizer

    @torch.no_grad()
    def eval(self, val_dataset):
        losses = []
        for imgs in val_dataset:
            loss = self.compute_loss(imgs)
            losses.append(loss.cpu().detach().numpy().item())
        loss = np.array(losses).mean()
        return loss


    def train_bc(self, args):
        skill = SIR(args)
        train_dataset, val_dataset = load_video_data(args)
        best_loss = float('inf')
        
        for epoch in range(args.epochs):
            with tqdm(range(len(train_dataset))) as pbar:
                train_loss = []
                for i, (imgs, past_actions, next_actions) in zip(pbar, train_dataset):
                    imgs = imgs.to(device=self.args.device)
                    past_actions = past_actions.to(device=self.args.device)
                    next_actions = next_actions.to(device=self.args.device)
                    
                    self.optim.zero_grad()
                    loss=self.compute_loss_bc(imgs, past_actions,next_actions)
                    loglikelihood_loss = skill.calc_loss(imgs) 
                    loss += loglikelihood_loss
                    
                    # Backpropagation
                    loss.backward()
                    self.optim.step()
                    
                    # Logging loss
                    pbar.set_postfix(Transformer_Loss=np.round(loss.cpu().detach().numpy().item(), 4))
                    train_loss.append(np.round(loss.cpu().detach().numpy().item(), 5))
                
                train_loss_mean = np.array(train_loss).mean()
                val_loss = self.eval(val_dataset)
                is_best = val_loss < best_loss
                best_loss = min(val_loss, best_loss)
                
                # Logging and checkpointing
                with self.logger.log_and_dump_ctx(epoch, ty='train') as log:
                    log('trainloss', train_loss_mean)
                    log('val_loss', val_loss)
                    log('episode', epoch)
                
                if is_best:
                    print(f'Checkpoint at epoch {epoch} is saved with eval loss {best_loss} !!!')
                    torch.save(self.model.state_dict(), os.path.join(f"{self.work_dir}/checkpoints/siril.pt"))


    def compute_loss_bc(self, imgs, past_actions,next_actions):
        imgs = imgs.to(device=self.args.device)
        past_actions = past_actions.to(device=self.args.device)
        logits, targets, predicted_actions = self.model.output(imgs, past_actions, compute_joint=True)
        
        # Combine video prediction loss and action prediction loss
        ce_loss = F.cross_entropy(logits.reshape(-1, logits.size(-1)), targets.reshape(-1))
        mse_loss = F.mse_loss(predicted_actions, next_actions)
        
        loss = ce_loss + self.args.lambda_bc * mse_loss
        return loss



@hydra.main(config_path="../siril/configs/models/bc/videogpt", config_name="default")
def main(args):
    BC(args)


if __name__ == '__main__':
    main()