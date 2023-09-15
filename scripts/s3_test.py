from src.services.aws import AWSClient

aws_client = AWSClient()

key = "image_store/astronaut_rides_horse_refined.png";
aws_client.upload_to_s3(key, key)
aws_client.download_from_s3(key)