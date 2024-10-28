import sqlite3
import os
from datetime import datetime
# from upload_image import firebase_storage



#________________________________________________________________________________________________________________________________

def connection():
    conn = sqlite3.connect('Prism.db')
    cursor = conn.cursor()
    return cursor,conn


def disconnect(conn):
    conn.commit()
    conn.close()

# cursor,conn=connection()

# table_name='post_images'
# print(f"table_name: {table_name}():")

# try:        # Execute a query to get the table schema
#     cursor.execute(f"PRAGMA table_info({table_name});")
#     schema_info = cursor.fetchall()

#     if schema_info:
#             # Print or process the schema information
#         for column_info in schema_info:
#             print(f"Column Name: {column_info[1]}, Type: {column_info[2]}")
#     else:
#         print(f"Table '{table_name}' not found or has no schema information.")
# except sqlite3.Error as e:
#     print(f"Error getting table schema: {e}")
# disconnect(conn)



#user
#_________________________________________________________________________________________________________________________________
def check_data_existed(username=None, email=None):
    cursor, conn = connection()
    if username:
        cursor.execute('''
            SELECT * FROM User WHERE username=?
        ''', (username,))
        rows = cursor.fetchall()
    if email:
        cursor.execute('''
            SELECT * FROM User WHERE email=?
        ''', (email,))
        rows = cursor.fetchall()
    disconnect(conn)
    if rows:
        return True
    else:
        return False
    




# print(check_data_existed(email="john@example.com"))


def createuser(username, password, email, full_name, points, phone_number, school_college, photo, group_id=None, group_role=None):
    try:
        cursor, conn = connection()
        image_path = firebase_storage.upload_profile_image(photo, 'user-profiles', username)

        # Insert user data into SQLite database
        cursor.execute('''
            INSERT INTO User (
                username, email, password, full_name,
                points, phone_number, school_college, group_id, group_role, profile_picture
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (username, email, password, full_name, points, phone_number, school_college, group_id, group_role, image_path))

        disconnect(conn)

        print(f'User created: {username}')
    except Exception as e:
        print(f"Error creating user: {e}")
    
    
def get_user_details(username):
    try:
        cursor, conn = connection()

        # Retrieve user details from the SQLite database
        cursor.execute('''
            SELECT * FROM User WHERE username=?
        ''', (username,))
        
        user_details = cursor.fetchone()  # Fetch one row

        disconnect(conn)
        url=firebase_storage.get_image_url(user_details[10])

        if user_details:
            return {
                'user_id': user_details[0],
                'username': user_details[1],
                'email': user_details[2],
                'password': user_details[3],
                'full_name': user_details[4],
                'points': user_details[5],
                'phone_number': user_details[6],
                'school_college': user_details[7],
                'group_id': user_details[8],
                'group_role': user_details[9],
                'profile_picture': url
            }
        else:
            return None

    except Exception as e:
        print(f"Error getting user details: {e}")
        return None

# Example usage:
# username_to_search = 'himanshu'
# user_details = get_user_details(username_to_search)

# if user_details:
#     print(f"User Details for {username_to_search}:\n")
#     print(f"User ID: {user_details['user_id']}")
#     print(f"Username: {user_details['username']}")
#     print(f"Email: {user_details['email']}")
#     print(f"Full Name: {user_details['full_name']}")
#     print(f"Points: {user_details['points']}")
#     print(f"Phone Number: {user_details['phone_number']}")
#     print(f"School/College: {user_details['school_college']}")
#     print(f"Group ID: {user_details['group_id']}")
#     print(f"Group Role: {user_details['group_role']}")
#     print(f"Profile Picture: {user_details['profile_picture']}")
# else:
#     print(f"User not found: {username_to_search}")


# print(get_user('ab'))




def deleteuser(username):
    try:
        cursor, conn = connection()
        cursor.execute("DELETE FROM user WHERE username=?", (username,))
        disconnect(conn)
        return True
    except Exception as e:
        print(f"Error deleting user: {e}")
        return False

# print(deleteuser('ab'))


def update_user(username, newusername=None, password=None, email=None, full_name=None, phone_number=None, school_college=None, group_id=None, group_role=None, photo=None, bio=None, point=None):
    user_exists= get_user_details(username)

    if not user_exists:
        return False

    cursor, conn = connection()
    userid = user_exists['user_id']
    username=user_exists['username']

    if password is not None:
        cursor.execute("UPDATE User SET password=? WHERE user_id=?", (password, userid))
    if email is not None:
        cursor.execute("UPDATE User SET email=? WHERE user_id=?", (email, userid))
    if newusername is not None:
        cursor.execute("UPDATE User SET username=? WHERE user_id=?", (newusername, userid))
    if full_name is not None:
        cursor.execute("UPDATE User SET full_name=? WHERE user_id=?", (full_name, userid))
    if bio is not None:
        cursor.execute("UPDATE User SET bio=? WHERE user_id=?", (bio, userid))
    if photo is not None:
        image_path=firebase_storage.upload_profile_image(photo, 'user-profiles', username)
        cursor.execute("UPDATE User SET profile_picture=? WHERE user_id=?", (bio, userid))
    if point is not None:
        cursor.execute("UPDATE User SET points=? WHERE user_id=?", (point, userid))
    if phone_number is not None:
        cursor.execute("UPDATE User SET phone_number=? WHERE user_id=?", (phone_number, userid))
    if school_college is not None:
        cursor.execute("UPDATE User SET school_college=? WHERE user_id=?", (school_college, userid))
    if group_id is not None:
        cursor.execute("UPDATE User SET group_id=? WHERE user_id=?", (group_id, userid))
    if group_role is not None:
        cursor.execute("UPDATE User SET group_role=? WHERE user_id=?", (group_role, userid))

    disconnect(conn)
    return True

# Example usage:
# update_user('john_doe', newusername='john_doe_updated', password='new_password', email='new_email@example.com', full_name='John Updated', point=150,school_college="delhimodel public school")
        
# update_user('anishwa',password="xyz")
        

#group
#_________________________________________________________________________________________________________________________________

def checkgroupexist(name):
    cursor,conn=connection()
    cursor.execute("SELECT count(*) from UserGroup WHERE group_name = ?",(name,))
    result=cursor.fetchall()
    disconnect(conn)
    if result[0][0]>0:
        return False
    else:
        return True

# print(checkgroupexist("ybs"))


def creategroup(name,description,group_profile,stacks,username):
    user_exists= get_user_details(username)
    userid = user_exists['user_id']
    if checkgroupexist(name):
        cursor,conn=connection()
        image_path=firebase_storage.upload_profile_image(group_profile, 'group_profile', username)
        cursor.execute('''INSERT INTO UserGroup (group_name,group_bio,group_stacks,profile_picture)
                        VALUES (?, ?, ?, ?)''',
                    (f'{name}', f'{description}', f'{stacks}',image_path))
        print(f'group created {name}')

        cursor.execute('''select group_id from UserGroup where group_name=?  ''',(name,))
        result=cursor.fetchall()
        cursor.execute("UPDATE User SET group_id = ?, group_role = ? WHERE username = ?", (result[0][0],'admin', username))
        disconnect(conn)
        return True
    else:
        return False
# print(creategroup("ybs","yaar mera super","54545.jpg","hip hop","anish"))

def getgroup_id(name):
    cursor,conn=connection()
    cursor.execute("SELECT group_id from UserGroup WHERE group_name =?",(name,))
    result=cursor.fetchall()
    disconnect(conn)
    return result[0][0]

# print(getgroup_id("ybs"))

def addusergroup(name,username):
    cursor,conn=connection()
    if checkgroupexist(name)==False:
        cursor.execute('''select group_id from UserGroup where group_name=?  ''',(name,))
        result=cursor.fetchall()
        update_user(username,group_id=result[0][0],group_role='member')
        disconnect(conn)
        return True
    else:
        return False


# addusergroup("ybs","john_doe")

def getGroup_details(group_name):
    cursor, conn = connection()
    cursor.execute('''
        SELECT * FROM UserGroup WHERE group_name=?
    ''', (group_name,))
    rows = cursor.fetchall()
    if rows:
        group = True
        photo_path = None
        details = None
        with open(f'static/group-profile-pic/{rows[0][1]}.jpg', 'wb') as photo:
            photo.write(rows[0][3])
        photo_path = f'static/group-profile-pic/{rows[0][1]}.jpg'
        conn.commit()
        conn.close()
        details = list(rows[0])
        details.pop(3)  # Removing the profile_picture column from details
        return group, photo_path, details

# group,photo_path,details=getGroup_details("ybs")
# print(group,photo_path,details)

def remove_usergroup(group_name,username):
    if checkgroupexist(group_name)==False:
        cursor,conn=connection()
        cursor.execute('''select group_id from UserGroup where group_name=?  ''',(group_name,))
        result=cursor.fetchall()
        cursor.execute("UPDATE User SET group_id = ?, group_role = ? WHERE username = ?", (None,None,username))
        disconnect(conn)
        return True
    else:
        return False
    
# remove_usergroup("ybs","john_doe")

def updategroup(name,newname=None,group_point=None,group_picture=None,group_bio=None,group_stacks=None):
    cursor,conn=connection()
    cursor.execute('''select group_id from UserGroup where group_name=?  ''',(name,))
    if checkgroupexist(name)==False:
        if newname is not None:
            cursor.execute("UPDATE UserGroup SET group_name=? WHERE group_id=?", (newname,getgroup_id(name)))
        if group_point is not None:
            cursor.execute("UPDATE UserGroup SET group_point=? WHERE group_id=?", (group_point,getgroup_id(name)))
        if group_bio is not None:
            cursor.execute("UPDATE UserGroup SET group_bio=? WHERE group_id=?", (group_bio,getgroup_id(name)))
        if group_picture is not None:
            with open(group_picture, 'rb') as f:
                photo_data = bytes(f.read())
            cursor.execute("UPDATE UserGroup SET group_picture=? WHERE group_id=?", (photo_data,getgroup_id(name))) 
        if group_stacks is not None:
            cursor.execute("UPDATE UserGroup SET group_stacks=? WHERE group_id=?", (group_stacks,getgroup_id(name)))
        disconnect(conn)
        return True
    else:
        return False

# print(updategroup("ybs","ybs_updated","12","54545.jpg","yaar tera super","pop hop"))


def deletegroup(name):
    if checkgroupexist(name)==False:
        cursor,conn=connection()
        cursor.execute('''select group_id from UserGroup where group_name=?  ''',(name,))
        result=cursor.fetchall()
        cursor.execute("UPDATE User SET group_id = ?, group_role = ? WHERE group_id = ?", (None,None,result[0][0]))
        cursor.execute(f"Delete from UserGroup where group_name=?",(name,))
        disconnect(conn)
        return(True)
    else:
        return False
    
# print(deletegroup('ybs','john_doe'))

#post
#_________________________________________________________________________________________________________________________________

def upload_post_images(db_path, post_id, image_urls):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Insert the image information into the 'images' table for each URL
        for image_url in image_urls:
            insert_query = '''
            INSERT INTO images (post_id, url) VALUES (?, ?);
            '''
            cursor.execute(insert_query, (post_id, image_url))

        conn.commit()
        print(f"Images uploaded successfully for Post ID {post_id}.")
    except sqlite3.Error as e:
        print(f"Error uploading images: {e}")
    finally:
        # Close the database connection
        conn.close()

# # Example usage
# database_path = 'your_database.db'
# post_id_example = 1  # Replace with the actual post_id
# image_urls_example = [
#     'https://example.com/image1.jpg',
#     'https://example.com/image2.jpg',
#     'https://example.com/image3.jpg'
# ]  # Replace with the actual image URLs

# Call the function to upload the images
# upload_post_images(database_path, post_id_example, image_urls_example)


def get_images_by_post_id(db_path, post_id):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Retrieve all images for the specified post_id
        select_query = '''
        SELECT url FROM images WHERE post_id = ?;
        '''
        cursor.execute(select_query, (post_id,))
        images = cursor.fetchall()

        if images:
            return [image[0] for image in images]
        else:
            print(f"No images found for Post ID {post_id}.")
            return []
    except sqlite3.Error as e:
        print(f"Error retrieving images: {e}")
        return []
    finally:
        # Close the database connection
        conn.close()

# Example usage
# database_path = 'your_database.db'
# post_id_example = 1  # Replace with the actual post_id

# # Call the function to get all images for the specified post_id
# images_for_post = get_images_by_post_id(database_path, post_id_example)

# # Print the result
# print(f"Images for Post ID {post_id_example}:")
# for image_url in images_for_post:
#     print(image_url)

def createpost_byuser(username, title, content, photo_path):
    cursor, conn = connection()
    user_id = get_user(username)[2][0]

    with open(photo_path, 'rb') as f:
        photo_data = f.read()

    # Get the current timestamp
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute('''
        INSERT INTO Post (user_id, title, content, image, created_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, title, content, photo_data, created_at))
    
    disconnect(conn)

# createpost_byuser('john_doe', 'My Post', 'This is my post content.', 'photo.jpg')



def createpost_bygroup(username, title, content, photo_path):
    cursor, conn = connection()
    _,_,details=getGroup_details("ybs_updated")
    print(details[0])

    with open(photo_path, 'rb') as f:
        photo_data = f.read()

    # Get the current timestamp
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # cursor.execute('''
    #     INSERT INTO Post (group_id, title, content, image, created_at)
    #     VALUES (?, ?, ?, ?, ?)
    # ''', (user_id, title, content, photo_data, created_at))
    
    disconnect(conn)

    
   

def getpost():
    pass

def updatepost():
    pass

def deletepost():
    pass

#comment
#_________________________________________________________________________________________________________________________________

def creatcomment():
    pass

def getcommentforpost():
    pass

def updatecomment():
    pass

def deletecomment():
    pass

#like
#_________________________________________________________________________________________________________________________________

def addlike():
    pass

def getlikeforpost():
    pass

def unlike():
    pass









