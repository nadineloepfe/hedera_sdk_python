import os
import subprocess
import shutil
import sys

# Constants
HAPI_VERSION = "v0.57.3"
PROTOS_DIR = ".protos"
SERVICES_DIR = "src/hiero-sdk-python/hapi/services"
MIRROR_DIR = "src/hiero-sdk-python/hapi/mirror"

def main():
    # Use Python from the virtual environment to run commands
    venv_python = os.path.join('.', '.venv', 'bin', 'python')
    if not os.path.exists(venv_python):
        print("Virtual environment Python not found. Please ensure your virtual environment is set up correctly.")
        sys.exit(1)

    # Step 1: Prepare directories
    print("Setting up directories...")
    for directory in [PROTOS_DIR, SERVICES_DIR, MIRROR_DIR]:
        os.makedirs(directory, exist_ok=True)

    # Clean up old files
    for directory in [PROTOS_DIR, SERVICES_DIR, MIRROR_DIR]:
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isfile(item_path):
                os.unlink(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)

    # Create subdirectories
    for subdir in ["auxiliary/tss", "event"]:
        os.makedirs(os.path.join(SERVICES_DIR, subdir), exist_ok=True)

    # Touch __init__.py files
    for directory in [SERVICES_DIR, MIRROR_DIR]:
        open(os.path.join(directory, "__init__.py"), 'a').close()

    # Step 2: Download and extract protobuf files
    print(f"Downloading Hedera protobufs version {HAPI_VERSION}...")
    try:
        subprocess.run(f"curl -sL 'https://github.com/hashgraph/hedera-protobufs/archive/refs/tags/{HAPI_VERSION}.tar.gz' | tar -xz -C {PROTOS_DIR} --strip-components=1", shell=True, check=True)

        # Keep 'platform', 'services', and 'mirror', remove everything else
        for item in os.listdir(PROTOS_DIR):
            if item not in ['platform', 'services', 'mirror']:
                item_path = os.path.join(PROTOS_DIR, item)
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)  # Remove directories
                elif os.path.isfile(item_path):
                    os.remove(item_path)     # Remove files
    except subprocess.CalledProcessError as e:
        print(f"Error downloading or extracting protobufs: {e}")
        sys.exit(1)

    # Step 3: Compile service and platform protobuf files
    print("Compiling service and platform protobuf files...")
    protoc_cmd = f"python -m grpc_tools.protoc --proto_path={PROTOS_DIR}/platform --proto_path={PROTOS_DIR}/services --pyi_out=./{SERVICES_DIR} --python_out=./{SERVICES_DIR} --grpc_python_out=./{SERVICES_DIR} {PROTOS_DIR}/services/*.proto {PROTOS_DIR}/services/auxiliary/tss/*.proto {PROTOS_DIR}/platform/event/*.proto"
    subprocess.run(protoc_cmd, shell=True, check=True)

    # Step 4: Adjust imports for service and platform protobuf files
    print("Adjusting imports for service and platform protobuf files...")
    adjust_imports(SERVICES_DIR, [
        (r'^import .*_pb2 as .*__pb2', r'from . \g<0>'),
        (r'^from auxiliary\.tss', 'from .auxiliary.tss'),
        (r'^from event', 'from .event')
    ])

    # Step 5: Compile mirror protobuf files
    print("Compiling mirror protobuf files...")
    protoc_cmd = f"python -m grpc_tools.protoc --proto_path={PROTOS_DIR}/mirror --proto_path={PROTOS_DIR}/services --python_out={MIRROR_DIR} --grpc_python_out={MIRROR_DIR} {PROTOS_DIR}/mirror/*.proto"
    subprocess.run(protoc_cmd, shell=True, check=True)

    # Step 6: Adjust imports for mirror protobuf files
    print("Adjusting imports for mirror protobuf files...")
    adjust_imports(MIRROR_DIR, [
        (r'^import basic_types_pb2 as', r'import hiero-sdk-python.hapi.services.basic_types_pb2 as'),
        (r'^import timestamp_pb2 as', r'import hiero-sdk-python.hapi.services.timestamp_pb2 as'),
        (r'^import consensus_submit_message_pb2 as', r'import hiero-sdk-python.hapi.services.consensus_submit_message_pb2 as'),
        (r'^import consensus_service_pb2 as', r'import hiero-sdk-python.hapi.mirror.consensus_service_pb2 as'),
        (r'^import mirror_network_service_pb2 as', r'import hiero-sdk-python.hapi.mirror.mirror_network_service_pb2 as')
    ])

    # Step 7: Confirm success
    if os.listdir(SERVICES_DIR) and os.listdir(MIRROR_DIR):
        print("All protobuf files have been generated and adjusted successfully!")
    else:
        print("Error: Protobuf file generation or adjustment failed.")
        sys.exit(1)

def adjust_imports(directory, replacements):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    content = f.read()
                for pattern, repl in replacements:
                    content = re.sub(pattern, repl, content, flags=re.MULTILINE)
                with open(file_path, 'w') as f:
                    f.write(content)

if __name__ == "__main__":
    import re
    main()