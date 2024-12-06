import yaml
import os

# Function to modify the YAML configuration
def modify_yaml(file_path, updates, output_dir, i):
    # Read the YAML file
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)

    # Apply updates
    for field, value in updates.items():
        nested_fields = field.split('.')
        nested_data = config
        for nested_field in nested_fields[:-1]:
            if isinstance(nested_data, list):
                index = int(nested_field)
                nested_data = nested_data[index]
            else:
                nested_data = nested_data.get(nested_field, {})
        last_field = nested_fields[-1]
        if isinstance(nested_data, list) and last_field.isdigit():
            index = int(last_field)
            nested_data[index] = value
        else:
            nested_data[last_field] = value

    # Save the modified file
    modified_file_path = os.path.join(output_dir, f"{i}.yaml")
    with open(modified_file_path, 'w') as file:
        yaml.dump(config, file)

    return modified_file_path

input_yaml = "timing.yaml"
output_dir = "./all_test_yaml"
os.makedirs(output_dir, exist_ok=True)

# Generate experiments
for i in range(256):
    updates = {
        "Frontend.latency_path": f"../traces/all_test_latency/latency{i}.out",
        "Frontend.traces.0": f"../ramulator/trace_generator/all_tests/{i}.trace",
        "MemorySystem.BHDRAMController.plugins.1.ControllerPlugin.path": \
            f"../traces/all_test_controller/{i}"
    }
    new_file = modify_yaml(input_yaml, updates, output_dir, i)
    print(f"Generated: {new_file}")