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
