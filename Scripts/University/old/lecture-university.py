from canvasapi import Canvas

API_URL = 'https://poli.instructure.com'
API_KEY = '---'

canvas = Canvas(API_URL, API_KEY)

#get courses
for course in canvas.get_courses():
    print(course.id)
