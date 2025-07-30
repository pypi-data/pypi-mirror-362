import os
import json
import torch

class LoggingManager:
    def __init__(self, instance_params):
        self.instance_params = instance_params
    
    def _format_layer_sequence(self, layer_sequence):
        """Compactly format layer sequence for readability."""
        def fmt(layer):
            if layer["type"] == "MLP":
                return f"MLP({layer.get('units', '?')})"
            elif layer["type"] == "Conv2d":
                return f"Conv2d({layer.get('channel_units', '?')}, k={layer.get('kernel_size', '?')})"
            elif layer["type"] == "CNNBlock":
                return f"CNNBlock({layer.get('channel_units', '?')}, k={layer.get('kernel_size', '?')})"
            elif layer["type"] == "Pooling":
                return f"{layer.get('pooling_type', 'Pool')}({layer.get('kernel_size', '?')})"
            elif layer["type"] == "Transformer":
                return f"Transformer(d={layer.get('d_model', '?')}, h={layer.get('nhead', '?')}, L={layer.get('num_layers', '?')})"
            elif layer["type"] == "Dropout":
                return f"Dropout({layer.get('p', '?'):.2f})"
            elif layer["type"] == "BatchNorm":
                return "BatchNorm1d"
            elif layer["type"] == "BatchNorm2d":
                return "BatchNorm2d"
            else:
                # For complex layer types, show abbreviated version
                if isinstance(layer, dict) and 'type' in layer:
                    return layer['type']
                return str(layer)
        
        return "->".join(fmt(l) for l in layer_sequence)
    
    def _get_changing_keys(self):
        """Get keys that can change between runs."""
        changing = []
        ip = self.instance_params
        # Layer sequence always can change
        changing.append("layer_sequence")
        # Activation sequence only if more than one activation is possible
        if isinstance(ip.get("activation_function"), list) and len(set(ip["activation_function"])) > 1:
            changing.append("activation_sequence")
        # Loss function
        if isinstance(ip.get("loss_function"), list) and len(ip["loss_function"]) > 1:
            changing.append("loss_function")
        # Optimizer
        if isinstance(ip.get("optimizer"), list) and len(ip["optimizer"]) > 1:
            changing.append("optimizer")
        else:
            # Check if optimizer params can change
            opt = ip.get("optimizer", [{}])[0]
            if any(
                isinstance(v, dict) and ("min" in v and "max" in v and v["min"] != v["max"])
                for v in getattr(opt, "params", getattr(opt, "get", lambda k: {})("params")).values()
            ):
                changing.append("optimizer")
        return changing
    
    def _get_changing_optimizer_params(self):
        """Returns a set of optimizer param names that can change."""
        changing = set()
        for opt in self.instance_params.get("optimizer", []):
            for k, v in opt.get("params", {}).items():
                if isinstance(v, dict):
                    if ("min" in v and "max" in v and v["min"] != v["max"]) or ("values" in v and len(v["values"]) > 1):
                        changing.add(k)
        return changing
    
    def log_result(self, model, hyper_params, result, table_filepath, json_filepath, columns, 
                   rows, json_results, changing_keys, changing_opt_params, i, verbose, 
                   output_format, track_train_time=False, track_forward_time=False):
        """Log results to files and terminal."""
        
        # Handle different result formats
        if isinstance(result, tuple):
            result_list = list(result)
            accuracy = result_list[-1]  # Accuracy is always last
            
            # Extract timing data based on what's being tracked
            train_time = None
            forward_time = None
            
            if track_train_time and track_forward_time:
                # Both times tracked: [train_time, forward_time, accuracy]
                train_time = result_list[-3]
                forward_time = result_list[-2]
            elif track_train_time:
                # Only train time tracked: [train_time, accuracy]
                train_time = result_list[-2]
            elif track_forward_time:
                # Only forward time tracked: [forward_time, accuracy]
                forward_time = result_list[-2]
        else:
            # Single accuracy value
            accuracy = result
            train_time = None
            forward_time = None
        
        # Create table row
        row = {"Eval": i + 1}
        if "layer_sequence" in changing_keys:
            layer_seq_str = self._format_layer_sequence(hyper_params["layer_sequence"])
            row["layer_sequence"] = layer_seq_str
        if "activation_sequence" in changing_keys:
            row["activation_sequence"] = ",".join(hyper_params["activation_sequence"])
        if "optimizer" in changing_keys:
            opt = hyper_params["optimizer"]
            opt_str = opt["type"]
            if changing_opt_params:
                params = []
                for k in sorted(list(changing_opt_params)):
                    if k in opt['params']:
                        val = opt['params'][k]
                        if isinstance(val, float):
                            params.append(f"{k}={val:.2e}")
                        else:
                            params.append(f"{k}={val}")
                if params:
                    opt_str += f"({', '.join(params)})"
            row["optimizer"] = opt_str
        if "loss_function" in changing_keys:
            row["loss_function"] = hyper_params["loss_function"]
        
        # Add timing columns if being tracked
        if track_train_time and train_time is not None:
            row["train_time"] = f"{train_time:.2f}s"
        if track_forward_time and forward_time is not None:
            row["avg_forward_time"] = f"{forward_time * 1000:.3f}ms"
        
        row["accuracy"] = f"{accuracy:.4f}"
        rows.append(row)
        
        # Create JSON entry with full hyperparameters
        json_entry = {
            "eval_id": i + 1,
            "hyperparameters": hyper_params,
            "accuracy": accuracy,
            "layer_sequence_formatted": self._format_layer_sequence(hyper_params["layer_sequence"]),
            "activation_sequence_formatted": ",".join(hyper_params.get("activation_sequence", [])),
            "optimizer_formatted": row.get("optimizer", ""),
            "loss_function": hyper_params.get("loss_function", "")
        }
        
        # Add timing data to JSON if being tracked
        if track_train_time and train_time is not None:
            json_entry["training_time_seconds"] = train_time
        if track_forward_time and forward_time is not None:
            json_entry["avg_forward_time_seconds"] = forward_time
        
        json_results.append(json_entry)
        
        # Write files based on output format
        if output_format in ["table", "both"]:
            with open(table_filepath, "w") as f:
                self.write_table(f, columns, rows)
        
        if output_format in ["json", "both"]:
            with open(json_filepath, "w") as f:
                json.dump(json_results, f, indent=2)
        
        # Print to terminal if verbose
        if verbose:
            self.print_table_to_terminal(columns, rows, i)
    
    def write_table(self, f, columns, rows):
        """Write table to file."""
        # Calculate max width for each column based on content
        col_widths = {col: len(col) for col in columns}
        for row in rows:
            for col in columns:
                col_widths[col] = max(col_widths[col], len(str(row.get(col, ''))))

        # Write header
        header = " | ".join(col.ljust(col_widths[col]) for col in columns)
        f.write(header + "\n")
        f.write("-+-".join('-' * col_widths[col] for col in columns) + "\n")

        # Write rows
        for row in rows:
            line = " | ".join(str(row.get(col, '')).ljust(col_widths[col]) for col in columns)
            f.write(line + "\n")
    
    def print_table_to_terminal(self, columns, rows, i, max_col_widths=None):
        """Print table to terminal with consistent formatting."""
        if max_col_widths is None:
            # Fixed column widths to prevent shifting
            max_col_widths = {
                "Eval": 6,
                "layer_sequence": 80, 
                "optimizer": 40, 
                "activation_sequence": 30, 
                "loss_function": 18,
                "train_time": 12,
                "avg_forward_time": 16,
                "accuracy": 8
            }

        # Determine alignment
        alignments = {col: 'left' for col in columns}
        alignments['Eval'] = 'right'
        alignments['train_time'] = 'right'
        alignments['avg_forward_time'] = 'right'
        alignments['accuracy'] = 'right'

        # Use fixed column widths to prevent table shifting
        term_widths = {}
        for col in columns:
            # Use fixed width for this column, or header length if not specified
            if col in max_col_widths:
                term_widths[col] = max_col_widths[col]
            else:
                term_widths[col] = max(len(col), 15)  # Default minimum width

        def format_row(row_dict, is_header=False):
            cells = []
            for col in columns:
                val = col if is_header else str(row_dict.get(col, ''))
                width = term_widths[col]
                # Truncate if necessary
                if len(val) > width:
                    val = val[:width-3] + '...'
                # Align
                if alignments[col] == 'right':
                    cells.append(val.rjust(width))
                else:
                    cells.append(val.ljust(width))
            return " | ".join(cells)

        # Print header and separator on first call
        if i == 0:
            header = format_row({}, is_header=True)
            separator = "-+-".join('-' * term_widths[col] for col in columns)
            print(header)
            print(separator)
        
        # Print the latest row
        if rows:
            print(format_row(rows[-1]))
    
    def save_best_model(self, model, preset_name, log_dir):
        """Save the best model to disk."""
        model_filename = f"best_initial_{preset_name.lower()}_sample.pt"
        torch.save(model.state_dict(), os.path.join(log_dir, model_filename))
        return model_filename
