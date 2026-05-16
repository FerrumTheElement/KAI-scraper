from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta
import argparse
import subprocess
import os


"""
stations = [
    ["GMR", "Gambir"],
    ["PSE", "Pasar Senen"],
    ["MRI", "Manggarai"],
    ["JNG", "Jatinegara"],
    ["BKS", "Bekasi"],
    ["CKR", "Cikarang"],

    ["BD", "Bandung"],
    ["KAC", "Kiaracondong"],
    ["TSM", "Tasikmalaya"],
    ["CN", "Cirebon"],
    ["CNP", "Cirebon Prujakan"],

    ["PWT", "Purwokerto"],
    ["KTA", "Kutoarjo"],
    ["SMT", "Semarang Tawang"],
    ["SMC", "Semarang Poncol"],
    ["SLO", "Solo Balapan"],
    ["PWS", "Purwosari"],

    ["YK", "Yogyakarta"],
    ["LPN", "Lempuyangan"],
    ["WT", "Wates"],

    ["SGU", "Surabaya Gubeng"],
    ["SBI", "Surabaya Pasarturi"],
    ["WO", "Wonokromo"],
    ["ML", "Malang"],
    ["MN", "Madiun"],
    ["JR", "Jember"],
    ["KTG", "Ketapang"],

    ["MDN", "Medan"],
    ["KPT", "Kertapati"],
    ["TNK", "Tanjungkarang"]
]
"""

parser = argparse.ArgumentParser(description="Search for train tickets on tiket.com")
parser.add_argument("-co", required=True, help="Origin station code or city name (e.g. SGU or Surabaya)")
parser.add_argument("-cd",   required=True, help="Destination station code or city name (e.g. YK or Yogyakarta)")
parser.add_argument("-d",       default=datetime.today().strftime("%Y-%m-%d"), help="Travel date in YYYY-MM-DD format (default: today)")
parser.add_argument("-t",       default="00:00", help="Minimum departure time in HH:MM format (default: 00:00)")
parser.add_argument("-c",      default="", help="Train class: Economy or Executive (default: Economy)")
parser.add_argument("-mp",   default=float('inf'), type=int, help="Maximum price filter (default: no limit)")
args = parser.parse_args()

cityorigin  = args.co
citydest    = args.cd
date        = args.d
minimumtime = args.t
trainclass  = args.c
minnum      = args.mp

def find(cityorigin, citydest, date):
    
    if(len(cityorigin)>3 and len(citydest)>3):
        #print("both are full names")
        link = f"https://www.tiket.com/en-id/kereta-api/cari?d={cityorigin}&dlabel={cityorigin}+%28Semua%29&dt=CITY&a={citydest}&alabel={citydest}+%28Semua%29&at=CITY&date={date}&adult=1&infant=0&productType=train"
    elif(len(cityorigin)>3 and len(citydest)<=3):
        #print("name and code") 
        link = f"https://www.tiket.com/en-id/kereta-api/cari?d={cityorigin}&dlabel={cityorigin}+%28Semua%29&dt=CITY&a={citydest}&at=STATION&date={date}&adult=1&infant=0&productType=train"
    elif(len(cityorigin)<=3 and len(citydest)>3):
        #print("code and name")
        link = f"https://www.tiket.com/en-id/kereta-api/cari?d={cityorigin}&dt=STATION&a={citydest}&alabel={citydest}+%28Semua%29&at=CITY&date={date}&adult=1&infant=0&productType=train"
    else:
        #print("both short")
        link = f"https://www.tiket.com/en-id/kereta-api/cari?d={cityorigin}&dt=STATION&a={citydest}&at=STATION&date={date}&adult=1&infant=0&productType=train"

    print(link)
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=options)  # pass options here
    driver.get(link)
    time.sleep(1)
    html = driver.page_source
    #print("source acquired")


    soup = BeautifulSoup(html, "html.parser")  # parse the string into BeautifulSoup
    divs = soup.find_all("div", class_="Text_text__8LH6H Text_variant_highEmphasis___v_nG Text_size_b1__Fa2O2 Text_weight_bold__g5r8s") #time
    class1 = soup.find_all("div", class_="ScheduleList_train_class__uW0OQ Text_text__8LH6H Text_variant_highEmphasis___v_nG Text_size_b3__KuewH") #class
    code = soup.find_all("div", class_="ScheduleList_journey_location_station_container__HfQ83") # destination&arrival Text_text__8LH6H Text_variant_lowEmphasis__lKDdj Text_size_b3__KuewH
    mone = soup.find_all("div", class_="Text_text__8LH6H Text_variant_price__SSGCS Text_size_b1__Fa2O2 Text_weight_bold__g5r8s") #price
    which = soup.find_all("div", class_="ScheduleList_train_name__2tupS Text_text__8LH6H Text_variant_highEmphasis___v_nG Text_size_b3__KuewH Text_weight_bold__g5r8s") #e.g Sembrani, dharmawangsa
    test1 = soup.find_all("div", class_="ScheduleList_part_bottom__J41Zy")  
    #dont touch this is for type of train e.g. premium, newgen, blablabla
    
    driver.quit()

    t1 = []
    for testing in test1:
        typet = testing.get_text()
        t1.append(typet)
    
    #print("found classes")
    cm = []

    with open("another.txt", "w", encoding="utf-8") as file:
        file.write(str(soup))
    for a in mone:
        money = a.get_text()    
        cm.append(money)

    #departure and arrival time
    time1 = []
    time2 = []

    count = 0
    for b in divs:
        if count % 2 == 0:
            text = b.get_text()
            time1.append(text)
        else:
            text = b.get_text()
            time2.append(text)
        
        count = count+1
    
    #departure and arrival destinations
    r = []
    row = []
    count1 = 0
    for c in code:
        if count1 % 2 == 0:
            text1 = c.get_text()
            r.append(text1)
            #print(text1)
        else:
            text1 = c.get_text()
            row.append(text1)
            #print(text1)
        count1 = count1+1
        
    # class e.g. economy/excecutive
    cplas = []
    for e in class1:
        classes = e.get_text()
        #print(classes)
        cplas.append(classes)

    #type of train e.g. Sembrani, Sancaka etc
    train = []
    for f in which:
        trainy = f.get_text()
        train.append(trainy)

    #print("checkpoint2 finished doing the fuckton of for loops")

    combined = []
    
    for a, b, c, d, e, f, g, h in zip(time1, time2, r, row, cplas, cm, train, t1):
        combined.append([a, b, c, d, e, f, g, h])
   
    return combined #returns the combined list
        


#loop to print all the output
def loop(combined):
    timenow = ""
    for item in combined:
        
        if(datetime.strptime(item[0], "%H:%M").time()<datetime.strptime(minimumtime, "%H:%M").time()): #filters out minimumtime
            continue   
            
        #print(f"{item[4]} {trainclass}")
        #print(item[4].find(trainclass))

        if(item[4].find(trainclass) == -1):
            continue
        
        #print(f"{minnum} and {int("".join(c for c in item[5] if c.isdigit()))}")
        if int("".join(c for c in item[5] if c.isdigit())) > minnum:
            continue

        else:
            if(timenow != item[0]): #adds space based on time
                print("")
            print(
                item[0], item[2],
                "-->",
                item[1], item[3],
                "|", item[4],
                "|", item[5],
                "|", item[6],
                "|", item[7]
            )
            timenow = item[0]
counter = 0
#result = find(cityorigin, citydest, date)
print(date)
loop(find(cityorigin, citydest, date))

while True:
    b = ""
    b = input("TIME: ")
    if b == ">>":
        counter += 1
        date = (datetime.strptime(args.d, "%Y-%m-%d") + timedelta(days=counter)).strftime("%Y-%m-%d")
        print(date)
        loop(find(cityorigin, citydest, date))

    if b == "<<":
        counter -= 1
        date = (datetime.strptime(args.d, "%Y-%m-%d") + timedelta(days=counter)).strftime("%Y-%m-%d")
        print(date)
        loop(find(cityorigin, citydest, date))

    if b == "clear":
        subprocess.run("cls" if os.name == "nt" else "clear", shell=True)

    else:
        pass




