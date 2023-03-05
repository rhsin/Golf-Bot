def input_course():
  first_course = input("Enter your most preferred course: ")
  course = first_course.lower()

  if course == 'y':
    return "Bethpage Yellow Course"
  if course == 'b':
    return "Bethpage Blue Course"     
  if course == 'r':
    return "Bethpage Red Course"    
  if course == 'g':
    return "Bethpage Green Course" 
  else:
    return "Bethpage Yellow Course"   

def input_days():
  days_ahead = input("How many days from today? ")

  try: 
    days_ahead = int(days_ahead)
    if 1 <= days_ahead <= 7:
      print(days_ahead)
      return days_ahead
    else: 
      return 1
  except:
    return 1

def order_courses(first_course):
  courses = ["Bethpage Blue Course", "Bethpage Yellow Course", "Bethpage Red Course", "Bethpage Green Course"]

  for course in courses:
    if course == first_course:
      courses.remove(course)      

  courses.insert(0, first_course) 
  print(courses)
  return courses