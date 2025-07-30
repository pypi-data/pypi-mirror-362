import pynvml

pynvml.nvmlInit()


def getFanSpeed(gpu_index: int) -> int:
    """Returns the current fan speed percentage for the specified GPU index."""
    try:
        handle = pynvml.nvmlDeviceGetHandleByIndex(gpu_index)
        fan_speed = pynvml.nvmlDeviceGetFanSpeed(handle)
        return fan_speed  # Already returns as percentage (0-100)
    except pynvml.NVMLError as error:
        print(f"Failed to get fan speed for GPU {gpu_index}: {error}")
        raise  # Re-raise the exception so the caller can handle it


def getFanCount(gpu_index: int) -> int:
    # Get the handle for the GPU
    gpuHandle = pynvml.nvmlDeviceGetHandleByIndex(index=gpu_index)

    # Get the number of fans for this GPU
    fanCount = pynvml.nvmlDeviceGetNumFans(device=gpuHandle)

    return fanCount


def setFanSpeed(gpu_index: int, fan_speed: int) -> None:
    """Sets fan speed for specified GPU using nvidia-settings with X server permissions."""

    fanCount = getFanCount(gpu_index=gpu_index)
    for i in range(fanCount):
        # fansCommand += f" -a '[fan:0]/GPUTargetFanSpeed={fan_speed}'"
        handle = pynvml.nvmlDeviceGetHandleByIndex(i)
        try:
            pynvml.nvmlDeviceSetFanSpeed_v2(handle, i, fan_speed)
        except pynvml.NVMLError as error:
            print(f"Error while controlling GPU fan: {error}")
            print("Please ensure you are running this script with sudo.")
            exit(1)

    if not 0 <= fan_speed <= 100:
        raise ValueError("Fan speed must be between 0 and 100.")


def getTotalDevices() -> int:
    return pynvml.nvmlDeviceGetCount()


def getDeviceName(gpu_index: int) -> str:
    """Retorna o nome da GPU especificada pelo índice."""
    try:
        handle = pynvml.nvmlDeviceGetHandleByIndex(gpu_index)
        name = pynvml.nvmlDeviceGetName(handle)
        return name
    except pynvml.NVMLError as error:
        print(f"Failed to get device name for GPU {gpu_index}: {error}")
        raise  # Re-levanta a exceção para que o chamador possa lidar com ela


def getGpuTemperature(gpu_index: int) -> int:
    """Retorna a temperatura da GPU especificada pelo índice."""
    try:
        handle = pynvml.nvmlDeviceGetHandleByIndex(gpu_index)
        temperature = pynvml.nvmlDeviceGetTemperature(
            handle, pynvml.NVML_TEMPERATURE_GPU
        )
        return temperature
    except pynvml.NVMLError as error:
        print(f"Failed to get temperature for GPU {gpu_index}: {error}")
        raise  # Re-levanta a exceção para que o chamador possa lidar com ela


def getFanDuty(
    currentTemp: int, targetTemps: list[int], targetDuties: list[int]
) -> int:
    if not targetTemps or not targetDuties or len(targetTemps) != len(targetDuties):
        raise ValueError(
            "The targetTemps and targetDuties lists must have the same length and cannot be empty."
        )

    if currentTemp <= targetTemps[0]:
        return targetDuties[0]

    for i in range(1, len(targetTemps)):
        if targetTemps[i - 1] < currentTemp <= targetTemps[i]:
            return targetDuties[i]

    return targetDuties[-1]


if __name__ == "__main__":
    # print(getNvidiaBoardsPresent())
    # print("")
    pass
