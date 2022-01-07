# webcam-face-recognition

## Tools

### opencv-python
https://github.com/opencv/opencv-python

### Milvus vector database
https://milvus.io/docs

### Face Recognition
https://github.com/ageitgey/face_recognition

## Running

```
docker-compose up -d
pip install -r requirements.txt
```

Put the face images in the images directory. Ex:


```
├── images
│   ├── biden.jpg
│   └── obama.jpg
```

Insert the embeddings of the images into the Milvus vector database.
```
python insert_face.py
```
After

```
python main.py
```

## Based on:
- https://github.com/milvus-io/bootcamp/tree/master/solutions/reverse_image_search/quick_deploy/server/src
- https://github.com/ageitgey/face_recognition/blob/master/examples/facerec_from_webcam_faster.py
