import dataclasses
import pathlib

import yaml


@dataclasses.dataclass
class CameraConfig:
    rtsp_url: str
    gpu_id: int
    slice_start_indices: list[int]


@dataclasses.dataclass
class ServerConfig:
    cameras: dict[str, CameraConfig]
    http_port: int
    recording_lifetime_s: int
    close_bbox_diagonal: int
    min_throughput_hz: float

    @property
    def camera_ids(self) -> list[str]:
        return list(self.cameras.keys())


def load(path: pathlib.Path) -> ServerConfig:
    """Loads the server configuration from a YAML file."""
    with open(path, "r") as f:
        loaded_cfg = yaml.safe_load(f)
    cams = {
        cam_id: CameraConfig(**cam_dict)
        for cam_id, cam_dict in loaded_cfg.get("cameras", {}).items()
    }
    server_cfg = ServerConfig(
        cameras=cams,
        recording_lifetime_s=loaded_cfg["recording_lifetime_s"],
        http_port=loaded_cfg["http_port"],
        close_bbox_diagonal=loaded_cfg["close_bbox_diagonal"],
        min_throughput_hz=loaded_cfg["min_throughput_hz"],
    )
    if len(server_cfg.cameras) == 0:
        raise ValueError("Configuration must specify at least one camera.")
    return server_cfg


def save(config: ServerConfig, path: pathlib.Path) -> None:
    """Saves the server configuration to a YAML file."""
    with open(path, "w") as f:
        yaml.dump(dataclasses.asdict(config), f)
