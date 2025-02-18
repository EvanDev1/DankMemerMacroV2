import importlib
import os

def load_actions(bot):
    actions_dir = 'actions'
    
    for root, _, files in os.walk(actions_dir):
        for filename in files:
            if not filename.endswith('.py') or filename == '__init__.py':
                continue

            # Convert file path to module path
            module_name = os.path.splitext(os.path.relpath(os.path.join(root, filename), actions_dir))[0].replace(os.sep, '.')
            full_module_name = f'{actions_dir}.{module_name}'
            
            # Import the module
            module = importlib.import_module(full_module_name)

            # Find a class within the module
            action_class = None
            for attr in dir(module):
                attr_value = getattr(module, attr)
                if isinstance(attr_value, type):
                    action_class = attr_value
                    break

            if action_class is None:
                raise AttributeError(f"No class found in module '{full_module_name}'.")

            action_instance = action_class(bot)

            # Bind the run method to the bot instance using the filename as the method name
            setattr(bot, module_name, action_instance.run)

# Example usage:
# Assuming `bot` is an instance of your bot class
# load_actions(bot)
