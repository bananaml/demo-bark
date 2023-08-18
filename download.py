from transformers import AutoProcessor, BarkModel

MODEL = "suno/bark"

def download_model():
    """Load model and processor"""
    processor = AutoProcessor.from_pretrained(MODEL)
    model = BarkModel.from_pretrained(MODEL)

if __name__ == "__main__":
    download_model()