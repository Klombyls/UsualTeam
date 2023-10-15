from ultralytics import YOLO

# Load a model
model = YOLO("YOLOv8m.pt")  # l
model.train(data="config.yaml",workers=0, optimizer = 'SGD', batch=14, epochs=1,patience=10,  imgsz=640,iou=0.98, augment=True, pretrained = True,verbose = False, degrees=10, translate=0.1, scale=0.9, shear=0,perspective=0.001,copy_paste=0.1,line_thickness=1)