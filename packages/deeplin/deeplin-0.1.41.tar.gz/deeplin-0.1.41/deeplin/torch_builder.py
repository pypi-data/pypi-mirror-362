"""
@date: 2021/11/7
@description: learning rate scheduler factory, optimizer factory
"""
import torch


def create_optimizer(
    opt: str,
    model,
    lr,
    weight_decay,
):
    opt_lower = opt.lower()

    parameters = model.parameters()
    opt_args = dict(lr=lr, weight_decay=weight_decay)

    opt_split = opt_lower.split("_")
    opt_lower = opt_split[-1]
    if opt_lower == "adam":
        optimizer = torch.optim.Adam(parameters, **opt_args)
    elif opt_lower == "adamw":
        optimizer = torch.optim.AdamW(parameters, **opt_args)
    elif opt_lower == "adadelta":
        optimizer = torch.optim.Adadelta(parameters, **opt_args)
    elif opt_lower == "radam":
        optimizer = torch.optim.RAdam(parameters, **opt_args)
    elif opt_lower == "sgd":
        opt_args["momentum"] = 0.9
        optimizer = torch.optim.SGD(parameters, **opt_args)
    else:
        raise "Invalid optimizer"

    return optimizer


def create_scheduler(
    optimizer,
    lr_policy="exp",
    epoch_count=5,
    lr_decay_iters=25,
    niter=100,
    niter_decay=100,
):
    """Return a learning rate scheduler
    Parameters:
    optimizer -- 网络优化器
    lr_policy -- 学习率scheduler的名称: linear | step | plateau | cosine
    """
    if lr_policy == "linear":

        def lambda_rule(epoch):
            lr_l = 1.0 - max(0, epoch + epoch_count - niter) / float(niter_decay + 1)
            return lr_l

        scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda=lambda_rule)
    elif lr_policy == "step":
        scheduler = torch.optim.lr_scheduler.StepLR(
            optimizer, step_size=lr_decay_iters, gamma=0.5
        )
    elif lr_policy == "plateau":
        scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
            optimizer, mode="min", factor=0.2, threshold=0.01, patience=5
        )
    elif lr_policy == "cosine":
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
            optimizer, T_max=niter, eta_min=0
        )
    elif lr_policy == "exp":
        scheduler = torch.optim.lr_scheduler.ExponentialLR(optimizer, gamma=0.98)
    else:
        return NotImplementedError(
            "learning rate policy [%s] is not implemented", lr_policy
        )
    return scheduler
