from canvasapi import Canvas

token_canvas = '8994~rABkDzmaDzmJNwuF4Y73Zz82fr9QxrEwFW3JcxE7NeXwGaNN4GXBHmBKxuHZ9KRJ'


API_URL = 'https://poli.instructure.com'
API_KEY = '8994~rABkDzmaDzmJNwuF4Y73Zz82fr9QxrEwFW3JcxE7NeXwGaNN4GXBHmBKxuHZ9KRJ'

canvas = Canvas(API_URL, API_KEY)

#get courses
for course in canvas.get_courses():
    print(course.id)
