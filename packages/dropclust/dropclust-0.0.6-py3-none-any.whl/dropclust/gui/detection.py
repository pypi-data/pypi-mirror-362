import os
import sys, pathlib

from ultralytics import YOLO
from collections import defaultdict

def detect(gui_self):
    model_path = pathlib.Path.home().joinpath(".dropclust/models", "yolov11_ droplets_custom.pt")

    # if not model_path.is_file():
    #     cp_dir = pathlib.Path.home().joinpath(".dropclust")
    #     cp_dir.mkdir(exist_ok=True)
    #     print("downloading model")
    #     download_url_to_file(
    #         "https://gitlab.com/MeLlamoArroz/DropClustGUI/-/raw/master/logo_gui.png",
    #         model_path, progress=True)

    model = YOLO(model_path)

    results_dir = os.path.splitext(gui_self.filename)[0]

    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    model.predict(source=gui_self.filename, project=results_dir, show=True, save=True, conf=0.6, show_labels=True, show_conf=True, line_width=1, verbose=True)

def track(gui_self):
    from trackers import DeepSORTFeatureExtractor, DeepSORTTracker
    import supervision as sv
    
    model_path = pathlib.Path.home().joinpath(".dropclust/models", "yolov11_ droplets_custom.pt")
    model = YOLO(model_path)

    feature_extractor = DeepSORTFeatureExtractor.from_timm(
    model_name="mobilenetv4_conv_small.e1200_r224_in1k")

    tracker = DeepSORTTracker(feature_extractor=feature_extractor)

    color = sv.ColorPalette.from_hex([
        "#ffff00", "#ff9b00", "#ff8080", "#ff66b2", "#ff66ff", "#b266ff",
        "#9999ff", "#3399ff", "#66ffff", "#33ff99", "#66ff66", "#99ff00"
    ])

    box_annotator = sv.BoxAnnotator(
        color=color,
        color_lookup=sv.ColorLookup.TRACK)

    trace_annotator = sv.TraceAnnotator(
        color=color,
        color_lookup=sv.ColorLookup.TRACK,
        thickness=2,
        trace_length=100)

    label_annotator = sv.LabelAnnotator(
        color=color,
        color_lookup=sv.ColorLookup.TRACK,
        text_color=sv.Color.BLACK,
        text_scale=0.8)

    CONFIDENCE_THRESHOLD = 0.3
    NMS_THRESHOLD = 0.3

    results_dir = os.path.splitext(gui_self.filename)[0]
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    SOURCE_VIDEO_PATH = gui_self.filename
    TARGET_VIDEO_PATH = results_dir + "/out.mp4"

    frame_samples = []

    def callback(frame, i):
        result = model(frame)[0]
        detections = sv.Detections.from_ultralytics(result).with_nms(threshold=NMS_THRESHOLD)
        detections = tracker.update(detections, frame=frame)
        
        # # Get tracker ID's from frame
        # for box, tid in zip(detections.xyxy, detections.tracker_id):
        #     x1, y1, x2, y2 = map(int, box) 
        #     center = ((x1 + x2) // 2, (y1 + y2) // 2)
        #     trajectory_points[tid].append(center)

        # with open('file.pkl', 'wb') as file:
        #     pickle.dump(trajectory_points, file)


        annotated_image = frame.copy()
        annotated_image = box_annotator.annotate(annotated_image, detections)
        annotated_image = trace_annotator.annotate(annotated_image, detections)
        annotated_image = label_annotator.annotate(annotated_image, detections, detections.tracker_id)

        if i % 30 == 0 and i != 0:
            frame_samples.append(annotated_image)

        return annotated_image

    tracker.reset()

    sv.process_video(
        source_path=SOURCE_VIDEO_PATH,
        target_path=TARGET_VIDEO_PATH,
        callback=callback,
        show_progress=True,
    )
