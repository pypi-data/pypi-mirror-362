import torch.optim as optim

optimizer_dict = {
    "Adam": lambda params, lr=0.001, betas=(0.9, 0.999), eps=1e-08, weight_decay=0, amsgrad=False: 
        optim.Adam(params, lr=lr, betas=betas, eps=eps, weight_decay=weight_decay, amsgrad=amsgrad),

    "SGD": lambda params, lr=0.01, momentum=0.9, weight_decay=0, nesterov=False:
        optim.SGD(params, lr=lr, momentum=momentum, weight_decay=weight_decay, nesterov=nesterov),

    "RMSprop": lambda params, lr=0.01, alpha=0.99, eps=1e-08, weight_decay=0, momentum=0, centered=False:
        optim.RMSprop(params, lr=lr, alpha=alpha, eps=eps, weight_decay=weight_decay, momentum=momentum, centered=centered),

    "Adagrad": lambda params, lr=0.01, lr_decay=0, weight_decay=0, initial_accumulator_value=0, eps=1e-10:
        optim.Adagrad(params, lr=lr, lr_decay=lr_decay, weight_decay=weight_decay, initial_accumulator_value=initial_accumulator_value, eps=eps),

    "Adadelta": lambda params, lr=1.0, rho=0.9, eps=1e-06, weight_decay=0:
        optim.Adadelta(params, lr=lr, rho=rho, eps=eps, weight_decay=weight_decay),

    "AdamW": lambda params, lr=0.001, betas=(0.9, 0.999), eps=1e-08, weight_decay=0, amsgrad=False:
        optim.AdamW(params, lr=lr, betas=betas, eps=eps, weight_decay=weight_decay, amsgrad=amsgrad),

    "Adamax": lambda params, lr=0.002, betas=(0.9, 0.999), eps=1e-08, weight_decay=0:
        optim.Adamax(params, lr=lr, betas=betas, eps=eps, weight_decay=weight_decay),

    "NAdam": lambda params, lr=0.001, betas=(0.9, 0.999), eps=1e-08, weight_decay=0:
        optim.NAdam(params, lr=lr, betas=betas, eps=eps, weight_decay=weight_decay),
    
    # Added optimizers
    "ASGD": lambda params, lr=0.01, lambd=0.0001, alpha=0.75, t0=1000000.0, weight_decay=0:
        optim.ASGD(params, lr=lr, lambd=lambd, alpha=alpha, t0=t0, weight_decay=weight_decay),
    
    "LBFGS": lambda params, lr=1, max_iter=20, max_eval=None, tolerance_grad=1e-05, tolerance_change=1e-09, history_size=100, line_search_fn=None:
        optim.LBFGS(params, lr=lr, max_iter=max_iter, max_eval=max_eval, tolerance_grad=tolerance_grad, tolerance_change=tolerance_change, history_size=history_size, line_search_fn=line_search_fn),
    
    "Rprop": lambda params, lr=0.01, etas=(0.5, 1.2), step_sizes=(1e-06, 50):
        optim.Rprop(params, lr=lr, etas=etas, step_sizes=step_sizes),
}
