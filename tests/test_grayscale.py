import os
import tempfile
import unittest

import cv2
import numpy as np

from src.grayscale_converter import convert_to_grayscale, convert_to_grayscale_bytes


class TestGrayscaleConverter(unittest.TestCase):
    def test_convert_to_grayscale(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = os.path.join(temp_dir, "input.jpg")
            output_path = os.path.join(temp_dir, "output.jpg")

            image = np.zeros((20, 20, 3), dtype=np.uint8)
            image[:, :, 0] = 255
            cv2.imwrite(input_path, image)

            convert_to_grayscale(input_path, output_path)

            grayscale_image = cv2.imread(output_path, cv2.IMREAD_GRAYSCALE)
            self.assertIsNotNone(grayscale_image)
            self.assertEqual(len(grayscale_image.shape), 2)

    def test_convert_to_grayscale_bytes(self):
        image = np.zeros((20, 20, 3), dtype=np.uint8)
        image[:, :, 0] = 255
        image_bytes = cv2.imencode(".jpg", image)[1].tobytes()

        grayscale_bytes = convert_to_grayscale_bytes(image_bytes)

        self.assertGreater(len(grayscale_bytes), 0)
        decoded = cv2.imdecode(np.frombuffer(grayscale_bytes, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
        self.assertIsNotNone(decoded)
        self.assertEqual(decoded.ndim, 2)


if __name__ == "__main__":
    unittest.main()