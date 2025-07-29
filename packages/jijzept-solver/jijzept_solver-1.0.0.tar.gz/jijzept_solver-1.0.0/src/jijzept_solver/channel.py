import certifi
import grpc
from grpc._channel import Channel


def ssl_channel_manager(target: str) -> Channel:
    try:
        with open(certifi.where(), "rb") as f:
            root_certificates = f.read()
        credentials = grpc.ssl_channel_credentials(root_certificates=root_certificates)
        return grpc.secure_channel(target, credentials)
    except Exception as e:
        raise RuntimeError(f"Failed to load certs: {e}")


def no_ssl_channel_manager(target: str) -> Channel:
    return grpc.insecure_channel(target)
