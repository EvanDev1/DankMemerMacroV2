import os
import importlib

def import_commands(bot):
    cmds_dir = 'commands'
    cmds = {}

    for root, _, files in os.walk(cmds_dir):
        for filename in files:
            if not filename.endswith('.py'):
                continue

            # Convert file path to module path
            module_path = os.path.join(root, filename)
            module_name = module_path.replace(os.sep, ".").replace("/", ".").replace("\\", ".")[:-3]

            try:
                module = importlib.import_module(module_name)
            except Exception as e:
                raise ImportError(f"Error importing module {module_name}: {e}")

            valid_class_name = False

            # Check for classes ending with 'Command' and having a 'run' method
            for name in dir(module):
                obj = getattr(module, name)
                if isinstance(obj, type) and name.endswith('Command'):
                    valid_class_name = True
                    cmd_name = name[:-len("Command")].lower()

                    if not hasattr(obj, 'run') or not callable(getattr(obj, 'run')):
                        raise TypeError(f"Class '{name}' in module '{module_name}' does not have a 'run' method.")

                    cmd_instance = obj(bot)
                    cmds[cmd_name] = {
                        'run': cmd_instance.run
                    }

                    if hasattr(obj, 'on_message') and callable(getattr(obj, 'on_message')):
                        cmds[cmd_name]['on_message'] = cmd_instance.on_message

            if not valid_class_name:
                raise TypeError(f"Error importing module {module_name}: Commands must have 'Command' in their classname.")

    return cmds