# # import pyrebase

# import base64


# def image_to_data(image_path):
#     with open(image_path, 'rb') as image_file:
#         encoded_image = base64.b64encode(image_file.read())
#     return encoded_image

# # Example usage:
# image_path = '54545.jpg'
# image_data = image_to_data(image_path)

# config = {
#     "apiKey": "AIzaSyCgyOzGnG59FtmyzpfcFAgW-9MEQpb25IE",
#     "authDomain": "prism-repo.firebaseapp.com",
#     "databaseURL": "https://prism-repo.firebaseio.com",
#     "storageBucket": "prism-repo.appspot.com"
# }

# # firebase = pyrebase.initialize_app(config)
# # storage = firebase.storage()

# class FirebaseStorage:
#     def __init__(self, firebase, storage):
#         self.firebase = firebase
#         self.storage = storage

#     def upload_profile_image(self, image, folder, name):
#         try:
#             path = f'{folder}/{name}.jpg'
#             self.storage.child(path).put(image)
#             return f"{path}"
#         except Exception as e:
#             return f"Error uploading profile image: {e}"

#     def upload_post_images(self, images, post_id):
#         try:
#             urls = []
#             for index, image in enumerate(images):
#                 path = f'post-images/{post_id}_{index + 1}.jpg'
#                 self.storage.child(path).put(image)
#                 urls.append(path)
#             return urls
#         except Exception as e:
#             return f"Error uploading post images: {e}"

#     def get_image_url(self, filename):
#         try:
#             auth = self.firebase.auth()
#             user = auth.sign_in_with_email_and_password('mr.anish.kmr@gmail.com', 'anish50')
#             url = self.storage.child(filename).get_url(user['idToken'])
#             return url
#         except Exception as e:
#             return f"Error getting image URL: {e}"
            

# # Example usage:
# firebase_storage = FirebaseStorage(firebase, storage)

# # image=image_to_data('54545.jpg')

# # # Upload profile image for user
# # result_user_profile = firebase_storage.upload_profile_image(image, 'user-profiles', 'username')

# # # Upload profile image for teacher
# # result_teacher_profile = firebase_storage.upload_profile_image(image, 'teacher-profiles', 'teachername')

# # # Upload post images
# # post_images = [image1, image2, image3]  # List of images for a post
# # result_post_images = firebase_storage.upload_post_images(post_images, 'postid')

# # Get image URL for user profile
# # url_user_profile = firebase_storage.get_image_url('user-profiles/username.jpg', 'mr.anish.kmr@gmail.com', 'anish50')

# # print(result_user_profile)
# # print(result_teacher_profile)
# # print(result_post_images)
# # print(url_user_profile)
