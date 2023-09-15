from body_matrix import load, measure, draw
from PIL import Image
from src.services.aws import AWSClient
from src.utils.file_utils import download_file

def _format_response(measurements):
    height, leg, hip, shoulder, markers, _ = measurements
    return {
        "height": height,
        "inseamLength": leg,
        "hipSize": hip,
        "shoulder": shoulder,
        "chestSize": 0.8 * (shoulder or 42)
    }

def get_body_measurements(file_url):    
    
    device = "cpu"
    keypoints_model, keypoints_transform = load.keypoints_model(device)
    segment_model, segment_transform = load.segment_model(device)        
    local_file_path = download_file(file_url=file_url)
    print(local_file_path)
    frame = Image.open(local_file_path)
    results = measure.find_real_measures(
        image_frame=frame,
        device=device,
        keypoints_model=keypoints_model,
        keypoints_transform=keypoints_transform,
        segment_model=segment_model,
        segment_transform=segment_transform
    )
    # height, leg, hip, shoulder, markers, _ = results
    print(f"Extracted measurements:{results}")
    return _format_response(results)
    
    
def _visualise(measure_result, frame):
    
    height, leg, hip, shoulder, markers, _ = measure_result
    font_path = "fonts/Roboto-Bold.ttf"
    visualized_frame: Image = draw.visualize_measures(
        height, leg, hip, shoulder, markers, 
        frame, font_path
    )
    visualized_frame.save('out.png')
