from omegaconf import OmegaConf

# def apply_overrides(config):
#     """ Apply CLI overrides to OmegaConf """
#     base = OmegaConf.structured(config)

#     # Get CLI args up to '--' if present, otherwise all args
#     args = sys.argv[1:sys.argv.index("--")] if "--" in sys.argv else sys.argv[1:]
#     cli_args = [arg.lstrip("-") for arg in args]

#     # Merge overrides
#     overrides = OmegaConf.from_cli(cli_args)
#     merged = OmegaConf.merge(base, overrides)
#     return OmegaConf.to_object(merged)


def apply_overrides(config):
    """Apply CLI overrides to OmegaConf"""
    base = OmegaConf.structured(config)

    # Allow dynamic key creation
    OmegaConf.set_struct(base, False)

    # Parse all remaining arguments after the three main ones
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--tasks", nargs="+", required=True)
    parser.add_argument("-m", "--model", default="mock")
    parser.add_argument("-b", "--backend", default="mock")

    # Parse known args to separate main args from overrides
    known_args, remaining_args = parser.parse_known_args()

    # Process remaining args as overrides
    i = 0
    while i < len(remaining_args):
        arg = remaining_args[i]
        if arg.startswith("--"):
            key = arg[2:]  # Remove '--' prefix

            # Check if next arg is a value (not starting with --)
            if i + 1 < len(remaining_args) and not remaining_args[i + 1].startswith("--"):
                value = remaining_args[i + 1]
                # Try to convert to appropriate type
                try:
                    if value.lower() == "true":
                        value = True
                    elif value.lower() == "false":
                        value = False
                    elif value.isdigit():
                        value = int(value)
                    elif "." in value and value.replace(".", "").isdigit():
                        value = float(value)
                except Exception:
                    pass  # Keep as string
                i += 2
            else:
                # Boolean flag
                value = True
                i += 1

            # Handle tasks.* overrides - apply to all tasks
            if key.startswith("tasks."):
                task_key = key[6:]  # Remove 'tasks.' prefix
                for task_idx in range(len(config.tasks)):
                    nested_key = f"tasks.{task_idx}.{task_key}"
                    # Use setattr for nested access
                    keys = nested_key.split(".")
                    current = base
                    for k in keys[:-1]:
                        if k.isdigit():
                            current = current[int(k)]
                        else:
                            current = current[k]
                    setattr(current, keys[-1], value)
            else:
                # For non-nested keys, use direct assignment
                keys = key.split(".")
                current = base
                for k in keys[:-1]:
                    if k.isdigit():
                        current = current[int(k)]
                    else:
                        current = current[k]
                setattr(current, keys[-1], value)
        else:
            i += 1

    return OmegaConf.to_object(base)
