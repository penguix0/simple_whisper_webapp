from faster_whisper import WhisperModel
from application import logger

def init_model(model_path, use_gpu, model_size):
    logger.info(f"Initializing faster_whisper, model_size: { model_size }, USE_GPU: { use_gpu }, path: { model_path }")
    model = (
        WhisperModel(model_size, download_root=model_path, device="cuda", compute_type="float16")
        if use_gpu
        else WhisperModel(model_size, download_root=model_path, device="cpu", compute_type="int8")
    )

    return model