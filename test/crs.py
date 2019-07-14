from urllib.request import Request, urlopen
import bs4 as bs
import pandas as pd

def Day_Converter(day):
    if day == "M":
        return "Monday"

    elif day == "T":
        return "Tuesday"

    elif day == "W":
        return "Wednesday"

    elif day == "Th":
        return "Thursday"

    elif day == "F":
        return "Friday"

    elif day == "S":
        return "Saturday"
    
    elif day == "TTh":
        return "Tuesday and Thursday"

    elif day == "WF":
        return "Wednesday and Friday"

def user_input(classes, credit, slots, demand, class_type, lec_day, lab_day, lec_time, lab_time, lec_place, lab_place, prof):
    
    #print(classes)
    
    while 1:
        #narrow search
        class_desired = input("Please enter the subject desired: ")

        #exit code
        if class_desired == "exit" or class_desired == "EXIT":
            break

        #filters subjects
        indices = []
        for keys in classes:
            if class_desired in classes[keys]:
               indices.append(keys)

        #subject doesnt exist
        if not indices:
            print("\nNo subject found")

        #results
        else:
            print("\nSections with available slots:")
            for j in indices:
                if slots[j] != "DISSOLVED":
                    if int(slots[j]) > 0:
                        #lec or lab
                        if ( (class_type[j] == "lec") or (class_type[j] == "lab") ):
                            if class_type[j] == "lec":
                                lecday = Day_Converter(lec_day[j])

                                print("Subject Name: " + classes[j] + " (Lecture only)")
                                print("Credit(s): " + credit[j])
                                print("Day: " + str(lecday))
                                print("Time: " + lec_time[j])
                                print("Place: " + lec_place[j])         
                    
                            elif (class_type[j] == "lab"):  
                                labday = Day_Converter(lab_day[j])      
                                                          
                                print("Subject Name: " + classes[j] + " (Lab only)")
                                print("Credit(s): " + credit[j])
                                print("Day: " + str(labday))
                                print("Time: " + lab_time[j])
                                print("Place: " + lab_place[j])    
                             
                            print("Instructor: " + prof[j])    
                            print("Available Slots: " + slots[j])
                            print("Demand: " + demand[j])
                            print("Remarks: " + remarks[j])                            
                            print("\n")    

                        #lab-lab subjects
                        #lec-lab subjects
                        else:
                            lecday = Day_Converter(lec_day[j])
                            labday = Day_Converter(lab_day[j])

                            if class_type[j] == "lablab":
                                print("Subject Name: " + classes[j] + " (Two-Day Lab)")
                                print("Credit(s): " + credit[j])
                                print("Lab Day 1: " + str(lecday))
                                print("Lab Time 1: " + lec_time[j]) 
                                print("Lab Place 1: " + lec_place[j]) 
                                print("Lab Day: " + str(labday))
                                print("Lab Time: " + lab_time[j]) 
                                print("Lab Place: " + lab_place[j])  

                            else:
                                print("Subject Name: " + classes[j] + " (Lecture and Lab)")
                                print("Credit(s): " + credit[j])
                                print("Lec Day: " + str(lecday))
                                print("Lec Time: " + lec_time[j]) 
                                print("Lec Place: " + lec_place[j])
                                print("Lab Day: " + str(labday))
                                print("Lab Time: " + lab_time[j]) 
                                print("Lab Place: " + lab_place[j])  
                        
                            print("Instructor: " + prof[j])
                            print("Available Slots: " + slots[j])
                            print("Demand: " + demand[j])
                            print("Remarks: " + remarks[j])
                            print("\n")    

#table dictionaries
classes = {}
credit = {}
slots = {}
demand = {}
class_type = {}
lec_day = {}
lab_day = {}
lec_time = {}
lab_time = {}
lec_place = {}
lab_place = {}
prof = {}
remarks = {}

dict_ctr = 0

print("Scraping web please wait.\n")

#scrape data
for i in range(ord('A'), (ord('A') + 1)):
#for i in range(0,1):

    #fetch page and html data
    #url = "https://crs.upd.edu.ph/schedule/120181/" + (chr(i))
    url = "https://crs.upd.edu.ph/schedule/120181/EEE"
    # url = "https://crs.upd.edu.ph/"
    #url = "https://crs.upd.edu.ph/schedule/120172/EEE%2035"

    req = Request(url, headers = {'User-Agent': 'Mozilla/5.0'})

    html = urlopen(req).read()

    soup = bs.BeautifulSoup(html, "html.parser")

    #find table
    table = soup.find(id = "tbl_schedule")
    rows = table.find_all('tbody')

    #populate arrays
    for row in rows:

        #no classes
        if row.find('tr').text == "No classes to display":
            continue

        #subjects found
        else:
            cell = row.find_all('td')

            #gets class
            classes[dict_ctr] = cell[1].text

            #gets number of credit/s
            credit[dict_ctr] = cell[2].text

            #gets schedule
            schedule = cell[3]
            
            #gets time and day
            time_day = schedule.find('br').previous_sibling.strip()
            lec_lab = time_day.split(";") #checks if lab exists

            #lec and lab
            if len(lec_lab) > 1:

                 #indicates lab-lab
                if "lab" in lec_lab[0] and "lab" in lec_lab[1]:
                    class_type[dict_ctr] = "lablab"
                    
                #indicates lec-lab
                else:
                    class_type[dict_ctr] = "leclab"

                #tokenize lec information
                sched_info = lec_lab[0].split(" ") 
                
                if sched_info[0] != "TBA":
                    lec_day[dict_ctr] = sched_info[0]
                    lec_time[dict_ctr] = sched_info[1]

                    if len(sched_info) > 4:
                        lec_place[dict_ctr] = str(sched_info[3]) + " " + str(sched_info[4])
                    else:
                        lec_place[dict_ctr] = str(sched_info[3])

                    #tokenize lab information
                    sched_info = lec_lab[1].split(" ")
                    sched_info.pop(0) #removes erroneous white space
                    lab_day[dict_ctr] = sched_info[0]
                    lab_time[dict_ctr] = sched_info[1]

                    if len(sched_info) > 4:
                        lab_place[dict_ctr] = str(sched_info[3]) + " " + str(sched_info[4])
                    else:
                        lab_place[dict_ctr] = str(sched_info[3])

            #lec or lab
            else:
                #tokenize information
                sched_info = lec_lab[0].split(" ") 
                
                if sched_info[0] != "TBA":
                    #check if lec or lab
                    class_type[dict_ctr] = (sched_info[2])

                    #lecture
                    if class_type[dict_ctr] == "lec":
                        lec_day[dict_ctr] = sched_info[0]
                        lec_time[dict_ctr] = sched_info[1]

                        if len(sched_info) > 4:
                            lec_place[dict_ctr] = str(sched_info[3]) + " " + str(sched_info[4])
                        else:
                            lec_place[dict_ctr] = str(sched_info[3])

                    #lab
                    else:
                        lab_day[dict_ctr] = sched_info[0]
                        lab_time[dict_ctr] = sched_info[1]

                        if len(sched_info) > 4:
                            lab_place[dict_ctr] = str(sched_info[3]) + " " + str(sched_info[4])
                        else:
                            lab_place[dict_ctr] = str(sched_info[3])
            
            #gets prof
            prof[dict_ctr] = schedule.find('br').next_sibling.strip()

            #gets remarks
            remark_checker = schedule.find('em')
            if remark_checker is not None:
                remarks[dict_ctr] = remark_checker.text
                

            #gets slots
            total_slots = cell[5]
            free_slots = total_slots.find('strong').text
            slots[dict_ctr] = free_slots

            #gets demand
            demand[dict_ctr] = cell[6].text
                        
            dict_ctr += 1

#indicate end of scraping
print("Web scraping done. Total classes: %d\n" % (len(classes),))

user_input(classes, credit, slots, demand, class_type, lec_day, lab_day, lec_time, lab_time, lec_place, lab_place, prof)