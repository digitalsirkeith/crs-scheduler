from urllib.request import Request, urlopen
from collections import defaultdict
import bs4 as bs
import pandas as pd

def day_converter(day):
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
    # print(credit)
    # print(slots)
    # print(demand)
    # print(class_type)
    # print(lec_day)
    # print(lab_day)
    # print(lec_time)
    # print(lab_time)
    # print(lec_place)
    # print(lab_place)
    # print(prof)

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
                    #if int(slots[j]) > 0:

                        lecday = None
                        labday = None

                        if (class_type[j] == "TBA"):
                            print("Subject Name: " + classes[j] + " (Unknown)")
                            print("Credit(s): " + credit[j])
                            print("Day: TBA")
                            print("Time: TBA")
                            print("Place: TBA")    
                            print("Instructor: " + prof[j])   

                            for k in range(len(blocks[j])):
                                print("For block "  + blocks[j][k] + " --- Available Slots: " + slots[j][k]  + " | Demand: " + demands[j][k]   + " | Restriction: " + restrictions[j][k] )

                            if remarks.get(j) != None:
                                print("Remarks: " + remarks[j])
                            else:
                                print("Remarks: None")                           
                            print("\n")    

                        #lec or lab
                        elif ( (class_type[j] == "lec") or (class_type[j] == "lab") ):
                            if class_type[j] == "lec":

                                if j < len(lec_day) :
                                    lecday = day_converter(lec_day[j])

                                print("Subject Name: " + classes[j] + " (Lecture only)")
                                print("Credit(s): " + credit[j])
                                print("Day: " + str(lecday))
                                print("Time: " + lec_time[j])
                                print("Place: " + lec_place[j])         
                    
                            elif (class_type[j] == "lab"):  

                                if j < len(lab_day):
                                    labday = day_converter(lab_day[j])                        

                                print("Subject Name: " + classes[j] + " (Lab only)")
                                print("Credit(s): " + credit[j])
                                print("Day: " + str(labday))
                                print("Time: " + lab_time[j])
                                print("Place: " + lab_place[j])    
                             
                            print("Instructor: " + prof[j])    

                            for k in range(len(blocks[j])):
                                print("For block "  + blocks[j][k] + " --- Available Slots: " + slots[j][k]  + " | Demand: " + demands[j][k]   + " | Restriction: " + restrictions[j][k] )
                            
                            if remarks.get(j) != None:
                                print("Remarks: " + remarks[j])
                            else:
                                print("Remarks: None")                        
                            print("\n")    

                        #two day subjects
                        else:

                            if lec_day.get(j) != None:
                                lecday = day_converter(lec_day[j])
                                labday = day_converter(lab_day[j])

                            if class_type[j] == "lablab":
                                print("Subject Name: " + classes[j] + " (Two-Day Lab)")
                                print("Credit(s): " + credit[j])
                                print("Lab Day 1: " + str(lecday))
                                print("Lab Time 1: " + lec_time[j]) 
                                print("Lab Place 1: " + lec_place[j]) 
                                print("Lab Day 2: " + str(labday))
                                print("Lab Time 2: " + lab_time[j]) 
                                print("Lab Place 2: " + lab_place[j])  
                            
                            elif class_type[j] == "leclec":
                                print("Subject Name: " + classes[j] + " (Two-Day Lecture)")
                                print("Credit(s): " + credit[j])
                                print("Lec Day 1: " + str(lecday))
                                print("Lec Time 1: " + lec_time[j]) 
                                print("Lec Place 1: " + lec_place[j])
                                print("Lec Day 1: " + str(labday))
                                print("Lec Time 1: " + lab_time[j]) 
                                print("Lec Place 1: " + lab_place[j])  

                            elif class_type[j] == "leclab":
                                print("Subject Name: " + classes[j] + " (Lecture and Lab)")
                                print("Credit(s): " + credit[j])
                                print("Lec Day: " + str(lecday))
                                print("Lec Time: " + lec_time[j]) 
                                print("Lec Place: " + lec_place[j])
                                print("Lab Day: " + str(labday))
                                print("Lab Time: " + lab_time[j]) 
                                print("Lab Place: " + lab_place[j])  

                            else:
                                print("Subject Name: " + classes[j] + " (Unknown)")
                                print("Credit(s): " + credit[j])
                                print("Unknown Day")   
                                print("Unknown Time")
                                print("Unknown Place")
                        
                            print("Instructor: " + prof[j])

                            for k in range(len(blocks[j])):
                                print("For block "  + blocks[j][k] + " --- Available Slots: " + slots[j][k]  + " | Demand: " + demands[j][k]   + " | Restriction: " + restrictions[j][k] )


                            if remarks.get(j) != None:
                                print("Remarks: " + remarks[j])
                            else:
                                print("Remarks: None")   
                            print("\n")    
                                

#table dictionaries
classes = {}
credit = {}
#slots = {}
#demand = {}
class_type = {}
lec_day = {}
lab_day = {}
lec_time = {}
lab_time = {}
lec_place = {}
lab_place = {}
prof = {}
remarks = {}

blocks = {}
slots = {}
restrictions = {}
demands = {}

dict_ctr = 0


#url = "https://crs.upd.edu.ph/schedule/120191/coe%2023"
#url = "https://crs.upd.edu.ph/schedule/120191/VC%20130"


print("Scraping web please wait.\n")

#scrape data
for i in range(ord('A'), (ord('Z') + 1)):

    #fetch page and html data
    url = "https://crs.upd.edu.ph/schedule/120191/" + (chr(i))

    print("Scraping page " + (chr(i)))

    req = Request(url, headers = {'User-Agent': 'Mozilla/5.0'})
    import ssl
    g = ssl.SSLContext()
    html = urlopen(req, context=g).read()

    soup = bs.BeautifulSoup(html, "html.parser")

    #find table
    table = soup.find(id = "tbl_schedule")
    rows = table.find_all('tbody')

    #populate arrays
    for row in rows:

        #no classes
        if row.find('tr').text == "No classes to display":
            continue

        else:
            row_tr = row.find_all('tr')
            #print(len(row_tr))

            block_list = []
            slot_list = []
            demand_list = []
            restriction_list = []


            for j in range(len(row_tr)):

                cell = row_tr[j].find_all('td')

                #for single-block rows
                if j == 0:

                    #gets class
                    classes[dict_ctr] = cell[1].text
                    #print(classes)

                    #gets number of credit/s
                    credit[dict_ctr] = cell[2].text

                    #gets schedule
                    schedule = cell[3]
                    
                    #gets time and day
                    time_day = schedule.find('br').previous_sibling.strip()
                    lec_lab = time_day.split(";") #checks if lab exists
                    #print(lec_lab)

                    #TBA schedule
                    if lec_lab[0] == "TBA":
                        class_type[dict_ctr] = "TBA"

                    #two-day schedule
                    elif len(lec_lab) > 1:

                        #indicates lab-lab
                        if "lab" in lec_lab[0] and "lab" in lec_lab[1]:
                            class_type[dict_ctr] = "lablab"

                        #indicates lec-lec
                        if "lec" in lec_lab[0] and "lec" in lec_lab[1]:
                            class_type[dict_ctr] = "leclec"
                            
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
                            lab_day[dict_ctr] = sched_info[0] if 0 < len(sched_info) else None
                            lab_time[dict_ctr] = sched_info[1] if 1 < len(sched_info) else None

                            if len(sched_info) > 4:
                                lab_place[dict_ctr] = str(sched_info[3]) + " " + str(sched_info[4])
                            else:
                                lab_place[dict_ctr] = str(sched_info[3] if 3 < len(sched_info) else None)

                    #single day (lec or lab only)
                    else:
                        #tokenize information
                        sched_info = lec_lab[0].split(" ") 
                        
                        if sched_info[0] != "TBA":
                            #check if lec or lab
                            class_type[dict_ctr] = sched_info[2] if 2 < len(sched_info) else None

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
                                lab_day[dict_ctr] = sched_info[0] if 0 < len(sched_info) else None
                                lab_time[dict_ctr] = sched_info[1] if 1 < len(sched_info) else None

                                if len(sched_info) > 4:
                                    lab_place[dict_ctr] = str(sched_info[3]) + " " + str(sched_info[4])
                                else:
                                    lab_place[dict_ctr] = str(sched_info[3] if 3 < len(sched_info) else None) 
                    
                    #gets prof
                    prof[dict_ctr] = schedule.find('br').next_sibling.strip()

                    #gets remarks
                    remark_checker = schedule.find('em')
                    if remark_checker is not None:
                        remarks[dict_ctr] = remark_checker.text

                    #gets enlisting unit/block/block remarks
                    block = cell[4].text
                    block_list.append(block)
                    #print(block)

                    #gets slots
                    total_slots = cell[5]
                    free_slots = total_slots.find('strong').text
                    #print(free_slots)
                    slot_list.append(free_slots)

                    #slots[dict_ctr] = free_slots
                    

                    #gets demand
                    demand = cell[6].text
                    demand_list.append(demand)

                    #demand[dict_ctr] = cell[6].text
                    #print(demand)

                    #gets restriction
                    restriction = cell[7].text if 7 < len(cell) else None
                    restriction_list.append(restriction)

                #for other blocks
                else:
                    block = cell[0].text
                    block_list.append(block)

                    total_slots = cell[1]
                    free_slots = total_slots.find('strong').text
                    slot_list.append(free_slots)

                    demand = cell[2].text
                    demand_list.append(demand)

                    restriction = cell[3].text if 3 < len(cell) else None
                    restriction_list.append(restriction)
                
            blocks[dict_ctr] = block_list
            slots[dict_ctr] = slot_list
            demands[dict_ctr] = demand_list
            restrictions[dict_ctr] = restriction_list

            dict_ctr += 1

# #indicate end of scraping
# print(classes)
# print(blocks)
# print(slots)
# print(demands)
# print(restrictions)

print("Web scraping done. Total classes: %d\n" % (len(classes),))

user_input(classes, credit, slots, demand, class_type, lec_day, lab_day, lec_time, lab_time, lec_place, lab_place, prof)