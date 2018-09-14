import cv2
import face_recognition
kn_ima=face_recognition.load_image_file("/home/emily/Downloads/gakki/gakki.jpg")
face_loactions = face_recognition.face_locations(kn_ima)
un_ima=face_recognition.load_image_file("/home/emily/Downloads/photos/2.jpg")
biden_encoding=face_recognition.face_encodings("/home/emily/Downloads/gakki/gakki.jpg")
unknown_encoding=face_recognition.face_encodings("/home/emily/Downloads/photos/2.jpg")
results=face_recognition.compare_faces([biden_encoding], unknown_encoding)
print(results)