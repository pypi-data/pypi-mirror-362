def generate_script(cloud, script_type):
    if script_type == 'terraform':
        return f'Terraform script for {cloud}'
    elif script_type == 'arm':
        return f'ARM template for {cloud}'
    return '# Unsupported'
