import  face_recognition
im1=face_recognition.load_image_file("/home/emily/Downloads/gakki/gakki.jpg")
im2=face_recognition.load_image_file("/home/emily/Downloads/shiyuan/shiyuan.jpg")
im=face_recognition.load_image_file("/home/emily/Downloads/photos/2.jpg")
try:
    im1_encoding=face_recognition.face_encodings(im1)[0]
    im2_encoding=face_recognition.face_encodings(im2)[0]
    im_encoding=face_recognition.face_encodings(im)[0]
except IndexError:
    print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")
    quit()
    # 这个except不是很了解
known_faces=[im1_encoding, im2_encoding]
results=face_recognition.compare_faces(known_faces, im_encoding)
print("Is the unknown face a picture of gakki? {}".format(results[0]))




