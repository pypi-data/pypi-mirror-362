if __loader__.name == '__main__':
    import sys
    sys.path.append(sys.path[0] + '/..')

import os
import inspect
from letterboxdpy import user, movie, films, members, list
from letterboxdpy import search

def get_class_methods(cls, seen_classes=None):
    """Returns a list of methods for a given class, including inherited methods, preventing recursion."""
    if seen_classes is None:
        seen_classes = set()

    methods = []
    
    if cls in seen_classes:
        return methods

    seen_classes.add(cls)
    
    for name, obj in inspect.getmembers(cls):
        if inspect.isfunction(obj) or inspect.ismethod(obj):
            if not name.startswith('__') and not name.endswith('__'):
                methods.append((cls.__name__, name))  # Return method with class name
        elif inspect.isclass(obj) and obj.__module__ == cls.__module__:
            methods.extend(get_class_methods(obj, seen_classes))
    
    return methods

def get_defined_functions(module):
    """Returns a list of function names and class methods defined in the given module."""
    functions = []
    for name, obj in inspect.getmembers(module):
        if inspect.isfunction(obj) and inspect.getmodule(obj) == module:
            if not name.startswith('__') and not name.endswith('__'):  # Skip dunder functions
                functions.append((None, name))  # Global function
        elif inspect.isclass(obj) and inspect.getmodule(obj) == module:
            functions.extend(get_class_methods(obj))  # Class methods
    return functions

def get_existing_md_files(directory):
    """Returns a list of .md files in the given directory without extension."""
    md_files = [f[:-3] for f in os.listdir(directory) if f.endswith('.md')]
    return md_files

def check_missing_md_files(functions, md_files):
    """Compares functions and .md files, returning functions without corresponding .md files."""
    missing_md = [(cls, func) for cls, func in functions if func not in md_files]
    return missing_md

# Global function template
def create_md_for_global_function(func_name, func_signature, docstring, file_path):
    """Creates an MD file for global functions."""
    with open(file_path, 'w') as file:
        file.write(f'<h2 id="{func_name}">{func_name}{func_signature}</h2>\n\n')
        file.write(f'**Documentation:**\n\n{docstring}\n\n')
        file.write(f'[To be documented.](https://github.com/search?q=repo:nmcassa/letterboxdpy+{func_name})\n')

# Class method template
def create_md_for_class_method(class_name, func_name, func_signature, docstring, file_path):
    """Creates an MD file for class methods."""
    with open(file_path, 'w') as file:
        file.write(f'<h2 id="{class_name}.{func_name}">{class_name}.{func_name}{func_signature}</h2>\n\n')
        file.write(f'**Class:** `{class_name}`\n\n')
        file.write(f'**Documentation:**\n\n{docstring}\n\n')
        file.write(f'[To be documented.](https://github.com/search?q=repo:nmcassa/letterboxdpy+{class_name}.{func_name})\n')

def create_md_file_for_missing_function(class_name, func_name, module, directory):
    """Creates a .md file for a missing function with its signature."""
    file_path = os.path.join(directory, f"{func_name}.md")
    
    # If it's a class method, get the class object
    if class_name:
        cls = getattr(module, class_name, None)
        if cls is None:
            return
        func = getattr(cls, func_name, None)
    else:
        func = getattr(module, func_name, None)

    if func is None:
        return

    signature = str(inspect.signature(func))
    docstring = inspect.getdoc(func) or "No documentation provided."
    
    if class_name:
        create_md_for_class_method(class_name, func_name, signature, docstring, file_path)
    else:
        create_md_for_global_function(func_name, signature, docstring, file_path)

def check_modules_for_missing_md(modules):
    """Checks each module for missing .md files and prints the results."""
    base_directory = "."
    for module_name, module in modules.items():
        print(f"{module_name}:")
        function_names = get_defined_functions(module)
        md_directory = os.path.join(base_directory, module_name, 'funcs')
        
        if not os.path.exists(md_directory):
            print(f"Directory {md_directory} does not exist. Creating...")
            os.makedirs(md_directory, exist_ok=True)
        
        md_files = get_existing_md_files(md_directory)
        missing_md_files = check_missing_md_files(function_names, md_files)
        
        for class_name, func in missing_md_files:
            create_md_file_for_missing_function(class_name, func, module, md_directory)
            print(f"✗ {func}.md missing and created.")
        
        for _, func in function_names:
            if func in md_files:
                print(f"✓ {func}.md exists")
        
        if not missing_md_files:
            print("All functions have corresponding .md files.")
        print()

if __name__ == "__main__":
    modules = {
        'user': user,
        'movie': movie,
        'films': films,
        'members': members,
        'search': search,
        'list': list
    }
    check_modules_for_missing_md(modules)
