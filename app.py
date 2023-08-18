from potassium import Potassium, Request, Response
import os
from transformers import AutoProcessor, BarkModel
import scipy
import uuid
import boto3
import logging

logging.basicConfig(level=logging.INFO)

MODEL = "suno/bark"
AWS_ACCESS = os.getenv('AWS_ACCESS')
AWS_BUCKET = os.getenv('AWS_BUCKET')
AWS_REGION = os.getenv('AWS_REGION')
AWS_SECRET = os.getenv('AWS_SECRET')

app = Potassium("bark")

@app.init
def init():
    """
    Initialize the application with the model and processor.
    This function is called once when the application starts.
    It loads the model and processor from the pretrained model specified by the MODEL constant.
    The model and processor are stored in the context dictionary which is returned.
    """
    model = BarkModel.from_pretrained(MODEL).to("cuda:0")
    processor = AutoProcessor.from_pretrained(MODEL)
    context = {
        "processor": processor,
        "model": model
    }
    return context

@app.handler()
def handler(context: dict, request: Request) -> Response:
    """
    Handle a request to generate audio from a text prompt.
    This function is called for each request the application receives.
    It retrieves the model and processor from the context.
    The text prompt is extracted from the request and processed into a format the model can understand.
    The model generates the audio, which is then converted to a byte array and encoded in base64.
    The base64 audio is returned in the response.
    """
    processor = context.get("processor")
    model = context.get("model")
    prompt = request.json.get("prompt")
    inputs = processor(
        text=[prompt],
        return_tensors="pt",
    )
    inputs = {name: tensor.to("cuda:0") for name, tensor in inputs.items()}
    speech_output = model.generate(**inputs, do_sample=True)
    #*sampling rate from model config
    sampling_rate = 24000
    file_name = f"bark_{uuid.uuid4().hex}.wav"
    scipy.io.wavfile.write(file_name, rate=sampling_rate, data=speech_output[0].cpu().numpy())
    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS,
        aws_secret_access_key=AWS_SECRET,
        region_name=AWS_REGION
    )
    s3 = session.client('s3')
    s3.upload_file(file_name, AWS_BUCKET, file_name)
    logging.info(f"the bucket is: {AWS_BUCKET}")
    url = f"https://{AWS_BUCKET}.s3.amazonaws.com/{file_name}"
    return Response(json={"output": url}, status=200)

if __name__ == "__main__":
    app.serve()