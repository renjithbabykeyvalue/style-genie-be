from src.services.aws import AWSClient

aws_client = AWSClient()

key = "body_measure_samples/man-standing-upright.jpg";
file = "samples/man-standing-upright.jpg"
aws_client.upload_to_s3(file, key)
# aws_client.download_from_s3(key)
print(f"uploaded to:{aws_client.get_s3_public_url(key)}")