from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from datetime import datetime
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

cityorigin = "Surabaya"
citydest = "YK"
date = "2026-04-25"
minimumtime = "00:00"

print(f"{len(cityorigin)} {len(citydest)}")

if(len(cityorigin)>3 and len(citydest)>3):
    #print("both are full names")
    link = f"https://www.tiket.com/en-id/kereta-api/cari?d={cityorigin}&dlabel={cityorigin}+%28Semua%29&dt=CITY&a={citydest}&alabel={citydest}+%28Semua%29&at=CITY&date={date}&adult=1&infant=0&productType=train"
elif(len(cityorigin)>3 and len(citydest)<=3):
    #print("name and code")
    link = f"https://www.tiket.com/en-id/kereta-api/cari?d={cityorigin}&dlabel={cityorigin}+%28Semua%29&dt=CITY&a={citydest}&at=STATION&date={date}&adult=1&infant=0&productType=train"
    print(link)
elif(len(cityorigin)<=3 and len(citydest)>3):
    #print("code and name")
    link = f"https://www.tiket.com/en-id/kereta-api/cari?d={cityorigin}&dt=STATION&a={citydest}&alabel={citydest}+%28Semua%29&at=CITY&date={date}&adult=1&infant=0&productType=train"
else:
    #print("both short")
    link = f"https://www.tiket.com/en-id/kereta-api/cari?d={cityorigin}&dt=STATION&a={citydest}&at=STATION&date={date}&adult=1&infant=0&productType=train"


options = Options()
options.add_argument("--headless=new")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

driver = webdriver.Chrome(options=options)  # pass options here
driver.get(link)
time.sleep(2)
html = driver.page_source

print("source gotten")


soup = BeautifulSoup(html, "html.parser")  # parse the string into BeautifulSoup
divs = soup.find_all("div", class_="Text_text__kfEOs Text_variant_highEmphasis__mWW7X Text_size_b1__FYbK7 Text_weight_bold__vY26O") #time
class1 = soup.find_all("div", class_="ScheduleList_train_class__uW0OQ Text_text__kfEOs Text_variant_highEmphasis__mWW7X Text_size_b3__KUyjB") #class
code = soup.find_all("div", class_="ScheduleList_journey_location_station_container__HfQ83") # destination&arrival
mone = soup.find_all("div", class_="Text_text__kfEOs Text_variant_price__41B0u Text_size_b1__FYbK7 Text_weight_bold__vY26O") #price
which = soup.find_all("div", class_="ScheduleList_train_name__2tupS Text_text__kfEOs Text_variant_highEmphasis__mWW7X Text_size_b3__KUyjB Text_weight_bold__vY26O") #e.g Sembrani, dharmawangsa

print("found classes")
cm = []
with open("output.txt", "w") as file:
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
    print(count)
    print(text)
#departure and arrival destinations
r = []
row = []
count1 = 0
for c in code:
    
    if count1 % 2 == 0:
        text1 = c.get_text()
        r.append(text1)
    else:
        text1 = c.get_text()
        row.append(text1)
    print(text1)
    count1 = count1+1
    print(count1)
    

# class e.g. economy/excecutive
cplas = []
for e in class1:
    classes = e.get_text()
    cplas.append(classes)

train = []

for f in which:
    trainy = f.get_text()
    train.append(trainy)

print("checkpoint2 finished doing the fuckton of for loops")

combined = []
print(len(train))
for a, b, c, d, e, f, g in zip(time1, time2, r, row, cplas, cm, train):
    combined.append([a, b, c, d, e, f, g])
    print(a)
    

timenow = ""
x = 0
for item in combined:
    
    if(datetime.strptime(item[0], "%H:%M").time()<datetime.strptime(minimumtime, "%H:%M").time()):
        pass
        print("passing")
        x = x+1

    else:
        if(timenow != item[0]):
            print("")
        print(
            item[0], item[2],
            "-->",
            item[1], item[3],
            "|", item[4],
            "|", item[5],
            "|", item[6]
        )
        timenow = item[0]
        
        
print(x)


#for i in range(len(time1)):
    #print(time1[i]+" "+time2[i]+" "+r[i]+" "+row[i]+" "+cplas[i]+" "+cm[i]+" "+typer[i])
    #r[i].append(cplas[i])
            

#for obj in r:
    #print(obj[0] + obj[1]+" --> "+ obj[2] + obj[3])



