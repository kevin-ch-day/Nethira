from dataclasses import dataclass, asdict

@dataclass
class DeviceInfo:
    serial: str
    model: str
    manufacturer: str
    android_version: str
    sdk_version: str
    device_name: str
    build_number: str
    security_patch: str
    fingerprint: str
    bootloader: str
    cpu_abi: str

    def __str__(self) -> str:
        return (
            f"Serial        : {self.serial}\n"
            f"Model         : {self.model}\n"
            f"Manufacturer  : {self.manufacturer}\n"
            f"Android Ver   : {self.android_version}\n"
            f"SDK Version   : {self.sdk_version}\n"
            f"Device Name   : {self.device_name}\n"
            f"Build Number  : {self.build_number}\n"
            f"Security Patch: {self.security_patch}\n"
            f"Fingerprint    : {self.fingerprint}\n"
            f"Bootloader     : {self.bootloader}\n"
            f"CPU ABI        : {self.cpu_abi}"
        )

    def to_dict(self) -> dict:
        return asdict(self)
