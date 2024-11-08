import face_recognition
import cv2
import numpy as np
import csv
from datetime import datetime
import getpass

print("Its is an Attendence system prototype")
print("press '1' for face recognition and '2' for password attendence.(press 'q' to quit.)")
choice=input("Enter Your Choice : ")
if choice=='1':
    
    video_capture=cv2.VideoCapture(0) #for video capure from lappy webcam

    #load known faces

    dhrubo_image=face_recognition.load_image_file("faces/Dhrubojyoti_Bhattacharjee_12021002001121_Passport (1).jpg")

    #kamal_image=face_recognition.load_image_file("faces/kamal.jpg")


    dhrubo_encoding=face_recognition.face_encodings(dhrubo_image)[0]
    #kamal_encoding=face_recognition.face_encodings(kamal_image)[0]


    known_face_encodings=[dhrubo_encoding]
    known_face_names=["Dhrubojyoti",]

    #list of expected students
    students= known_face_names.copy()


    face_location=[]
    face_encodings=[]


    #Get the current date and time
    now=datetime.now()
    current_date = now.strftime("%Y-%m-%d")

    f=open(f"{current_date}_Present.csv","w+",newline="")

    lnwriter=csv.writer(f)

    while True:
        _, frame=video_capture.read()
        small_frame=cv2.resize(frame,(0,0),fx=0.25,fy=0.25)
        
        rgb_small_frame=cv2.cvtColor(small_frame,cv2.COLOR_BGR2RGB)
        
        #RECOGNITION FACES
        
        face_location=face_recognition.face_locations(rgb_small_frame)
        face_encodings=face_recognition.face_encodings(rgb_small_frame,face_location)
        
        for face_encoding in face_encodings:
            matches=face_recognition.compare_faces(known_face_encodings,face_encoding)
            
            face_ditance=face_recognition.face_distance(known_face_encodings,face_encoding)
            
            best_match_index=np.argmin(face_ditance)
            
            if(matches[best_match_index]):
                name=known_face_names[best_match_index]
                
            #Add the text if the person is present 
            if name in known_face_names:
                font=cv2.FONT_HERSHEY_SIMPLEX
                bottonLeftCornerOfText=(10,100)
                fontScale=1.5
                fontColor=(255,0,0)
                thickness=3
                lineType=2
                cv2.putText(frame,name + " Present ",bottonLeftCornerOfText,font,fontScale,fontColor,thickness,lineType)
                
                if name in students:
                    students.remove(name)
                    current_time=now.strftime("%H-%M-%S")
                    lnwriter.writerow([name,current_time])
            

                    
                    
                
                
        cv2.imshow("Attendance",frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break     

    video_capture.release()
    cv2.destroyAllWindows()
    f.close()

elif choice=='2':
        # Dictionary of passwords mapped to usernames
        user_passwords = {
            "Dhrubojyoti": "123456",
            "Student2": "password2",
            "Student3": "password3",
            # Add more users and passwords as needed
        }

        # List of students who need to mark attendance
        students = list(user_passwords.keys())

        # Get the current date and time
        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d")

        # Create/Open the CSV file for the day
        with open(f"{current_date}_Present(By Password).csv", "w+", newline="") as f:
            lnwriter = csv.writer(f)
            lnwriter.writerow(["Attendance by Password"])  # Header for the CSV file
            lnwriter.writerow(["Name", "Time", "Status"])  # Header for the CSV file

            while students:
                entered_password = getpass.getpass(prompt="Enter password to mark attendance(press 'q' to exit): ")
                
                # Check if the entered password matches any user
                user_found = False
                for user, password in user_passwords.items():
                    if entered_password == password and user in students:
                        user_found = True
                        print(f"Password accepted for {user}. Marking attendance...")
                        
                        # Mark the user as present and remove them from the list of students
                        students.remove(user)
                        current_time = now.strftime("%H-%M-%S")
                        lnwriter.writerow([user, current_time, "Present"])  # Marking as Present in the CSV
                        print(f"{user} marked as present.")
                        
                        break
                    elif entered_password.lower() == 'q':
                        print("Attendance marking ended by user.")
                        exit()  # Exit the program if 'q' is pressed
                        break
                
                if not user_found:
                    print("Incorrect password or attendance already marked. Please try again.")
                
                # Exit if all students have marked their attendance
                if not students:
                    print("All students have marked their attendance.")
                    break
else:
    print('The Process was ended by the user.')
