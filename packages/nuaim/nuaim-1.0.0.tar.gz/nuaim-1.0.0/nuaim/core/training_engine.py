from nuaim.utils import loss_func_dict, optimizer_dict
from .universal_model import UniversalModel

import torch
import torch.optim as optim
import time
from ignite.engine import Engine, Events
from ignite.metrics import Accuracy, Loss
from ignite.contrib.handlers import ProgressBar

class TrainingEngine:
    def __init__(self, instance_params, device=None):
        self.instance_params = instance_params
        self.device = device or torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    def train(self, hyper_params, train_loader, valid_loader, test_loader, max_epochs=100, 
              verbose=True, return_model=False, track_train_time=False, track_forward_time=False):
        """Train a model with given hyperparameters."""
        
        # Generate model
        model = UniversalModel(hyper_params, self.instance_params).to(self.device)

        # Initialize optimizer
        optimizer_config = hyper_params.get("optimizer", self.instance_params.get("optimizer"))
        if isinstance(optimizer_config, list):
            optimizer_config = optimizer_config[0]  # Fallback to the first one
        optimizer_params = optimizer_config["params"]
        optimizer_class = getattr(optim, optimizer_config["type"])
        optimizer = optimizer_class(model.parameters(), **optimizer_params)

        # Initialize loss function
        loss_fn_name = hyper_params.get("loss_function", self.instance_params.get("loss_function"))
        if isinstance(loss_fn_name, list):
            loss_fn_name = loss_fn_name[0]  # Fallback
        if isinstance(loss_fn_name, str):
            loss_fn = loss_func_dict[loss_fn_name]()
        else:
            raise ValueError("loss_function must be a string representing the loss function name.")

        # Define training and evaluation steps
        def train_step(engine, batch):
            model.train()
            inputs, targets = batch
            inputs, targets = inputs.to(self.device), targets.to(self.device)
            optimizer.zero_grad()
            predictions = model(inputs)
            loss = loss_fn(predictions, targets)
            loss.backward()
            optimizer.step()
            return loss.item()

        def eval_step(engine, batch):
            model.eval()
            with torch.no_grad():
                inputs, targets = batch
                inputs, targets = inputs.to(self.device), targets.to(self.device)
                predictions = model(inputs)
                return predictions, targets

        # Create training and evaluation engines
        trainer = Engine(train_step)
        evaluator = Engine(eval_step)

        # Attach metrics
        Accuracy().attach(evaluator, "accuracy")
        if verbose:
            Loss(loss_fn).attach(evaluator, "loss")
            ProgressBar().attach(trainer)
            ProgressBar().attach(evaluator)

        # Early stopping logic
        best_val_acc = 0.0
        best_model_state = None
        epochs_no_improvement = 0
        patience = 10
        
        @trainer.on(Events.EPOCH_COMPLETED)
        def log_and_early_stop(engine):
            nonlocal best_val_acc, best_model_state, epochs_no_improvement
            evaluator.run(valid_loader)
            val_acc = evaluator.state.metrics["accuracy"]
            if val_acc > best_val_acc:
                best_val_acc = val_acc
                best_model_state = model.state_dict()
                epochs_no_improvement = 0
            else:
                epochs_no_improvement += 1
            if epochs_no_improvement >= patience:
                engine.terminate()

        # Start training timing here (after all setup is complete)
        start_time = time.time() if track_train_time else None
        trainer.run(train_loader, max_epochs=max_epochs)
        # Calculate training time immediately after training completes
        training_time = (time.time() - start_time) if track_train_time else None
        
        if best_model_state is not None:
            model.load_state_dict(best_model_state)
        
        # Measure forward propagation time if requested
        avg_forward_time = None
        if track_forward_time:
            model.eval()
            forward_times = []
            with torch.no_grad():
                for batch in test_loader:
                    inputs, targets = batch
                    inputs = inputs.to(self.device)
                    
                    # Time forward pass
                    forward_start = time.time()
                    _ = model(inputs)
                    forward_time = time.time() - forward_start
                    forward_times.append(forward_time / len(inputs))  # Per-sample time
            
            avg_forward_time = sum(forward_times) / len(forward_times) if forward_times else 0.0
        
        # Run final evaluation for accuracy
        evaluator.run(test_loader)
        metrics = evaluator.state.metrics
        
        # Build result tuple based on what's being tracked
        result_data = []
        if track_train_time:
            result_data.append(training_time)
        if track_forward_time:
            result_data.append(avg_forward_time)
        result_data.append(metrics['accuracy'])  # Accuracy is always last
        
        # For backward compatibility, if no timing requested, return as before
        if not track_train_time and not track_forward_time:
            if return_model:
                return metrics['accuracy'], model
            return metrics['accuracy']
        
        if return_model:
            return tuple(result_data), model
        return tuple(result_data)
