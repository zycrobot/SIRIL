from pathlib import Path


from .sir import SIR


def make_rm(cfg):
    if cfg.rm_model == 'sir':
        cfg.cfg_path = str(Path(__file__).parents[3]) + cfg.cfg_path
        cfg.ckpt_path = str(Path(__file__).parents[3]) + cfg.ckpt_path
        rm = SIR(cfg=cfg)
    else:
        raise NotImplementedError

    return rm