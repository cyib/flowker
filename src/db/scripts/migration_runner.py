import os
import sys
current_path = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.abspath(os.path.join(current_path, "../../"))
sys.path.append(root_path)

import importlib.util

def runner(migrationType='up', step=None):
    migrations_dir = os.path.join(os.getcwd(), 'src', 'db', 'migrations')
    reverse = False
    if(migrationType == 'down'):
        reverse = True
    migration_files = sorted([f for f in os.listdir(migrations_dir) if f.endswith('.py')], reverse=reverse)
    print(migration_files)
    for i, migration_file in enumerate(migration_files):
        if(step != None):
            step = int(step)
            if(i >= step):
                break
        if migration_file.endswith('.py'):
            migration_path = os.path.join(migrations_dir, migration_file)

            spec = importlib.util.spec_from_file_location("migrations", migration_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if(migrationType == 'up'):
                if hasattr(module, 'up'):
                    print(f"Running migration {migration_file}...")
                    module.up()
                    print(f"Migration {migration_file} complete.")
                else:
                    print(f"Skipping migration {migration_file} (no up() function found).")
                    
            if(migrationType == 'down'):
                if hasattr(module, 'down'):
                    print(f"Running undoing migration {migration_file}...")
                    module.down()
                    print(f"Undo migration {migration_file} complete.")
                else:
                    print(f"Skipping migration {migration_file} (no down() function found).")

if __name__ == "__main__":
    runner()