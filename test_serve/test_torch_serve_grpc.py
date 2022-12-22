
import sys
import pyrootutils

root = pyrootutils.setup_root(sys.path[0], pythonpath=True, cwd=True)
sys.path.insert(0,'serve/ts_scripts/')
import unittest
import inference_pb2
import inference_pb2_grpc
import requests
import json
import base64
from requests import Response
from serve.ts_scripts.torchserve_grpc_client import get_inference_stub

def infer(stub, model_name, model_input):
    with open(model_input, 'rb') as f:
        data = f.read()

    input_data = {'data': data}
    response = stub.Predictions(
        inference_pb2.PredictionsRequest(model_name=model_name,
                                         input=input_data))

    try:
        prediction = response.prediction.decode('utf-8')
        return prediction
    except grpc.RpcError as e:
        exit(1)

class TestFargateGradio(unittest.TestCase):
    @classmethod
    def setUpClass(cls):


        cls.image_paths = ['1000_truck.png',  '10011_cat.png',  '10010_airplane.png',  '10008_airplane.png',  '10001_frog.png',  '10003_ship.png',  '10009_frog.png',  '10006_deer.png',  '10005_cat.png',  '10007_frog.png']
        cls.stub = get_inference_stub()
        # convert image to base64
    def test_predict(self):
        for image_path in self.image_paths:
            print(f"testing: {image_path}")

            response = infer(self.stub, 'cifar', 'test_serve/image/' + image_path)
     

            # print(f"response: {response.text}")

            data = json.loads(response)

            predicted_label = list(data)[0]
            act_label = image_path.split(".")[0].split('_')[-1]

            print(f"predicted label: {predicted_label}, actual label: {act_label}")

            self.assertEqual(act_label, predicted_label)

            print(f"done testing: {image_path}")

            print()


if __name__ == '__main__':
    unittest.main()