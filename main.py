from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import service_pb2, resources_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2

stub = service_pb2_grpc.V2Stub(ClarifaiChannel.get_grpc_channel())

YOUR_CLARIFAI_API_KEY = "d27f608cf946432a9701a897b45c087d"
YOUR_APPLICATION_ID = "dephlate_capstone_test"
SAMPLE_URL = "https://assets.epicurious.com/photos/57a8a45db10b4fb03f234f34/1:1/w_1920,c_limit/southern-fried-chicken.jpg"

# This is how you authenticate.
metadata = (("authorization", f"Key {YOUR_CLARIFAI_API_KEY}"),)

# Open an image and convert to bytes
with open("borgir_fries.jpg", "rb") as image:
  f = image.read()
  b = bytes(f)

request = service_pb2.PostModelOutputsRequest(
    # This is the model ID of a publicly available General model. You may use any other public or custom model ID.
    model_id="food-item-recognition",
    user_app_id=resources_pb2.UserAppIDSet(app_id=YOUR_APPLICATION_ID),
    inputs=[
        resources_pb2.Input(
            # Use "url=" for publicly hosted image, or "base64=" for a stream of bytes of a local image
            data=resources_pb2.Data(image=resources_pb2.Image(base64=b))
        )
    ],
)
response = stub.PostModelOutputs(request, metadata=metadata)

if response.status.code != status_code_pb2.SUCCESS:
    print(response)
    raise Exception(f"Request failed, status code: {response.status}")

for concept in response.outputs[0].data.concepts:
    print("%12s: %.2f" % (concept.name, concept.value))