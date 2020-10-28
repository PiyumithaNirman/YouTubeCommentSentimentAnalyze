import csv
import time
import os
import sys

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

timer = 2
count = 0

fresult = {"positivenum": 0, "negativenum": 0, "neutralnum": 0}

commentbot = SentimentIntensityAnalyzer()

CLIENT_SECRETS_FILE = "client_secrets.json"

YOUTUBE_READ_WRITE_SSL_SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0
To make this sample run you will need to populate the client_secrets.json file
found at:
   %s
with information from the APIs Console
https://console.developers.google.com
For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))


def csv_writer(percent):
    fileName = ["Positive", "Negative", "Nutral"]
    with open("Resul.csv", 'a', newline='', encoding='utf-16') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(fileName)
        wr.writerow(percent)


if __name__ == "__main__":

    percentage = []
    gen = ' ********************* YOUTUBE COMMENT ANALYZER *********************'
    for i in gen:
        print(i, end='')
        sys.stdout.flush()
        time.sleep(0.05)
    print("\n")

    gen = ' ********************************************************************'
    for i in gen:
        print(i, end='')
        sys.stdout.flush()
        time.sleep(0.05)

    time.sleep(timer)

with open("gujikguu.csv", "r", errors='ignore') as csvfile:
    for line in csvfile.read().split('\n'):
        vs = commentbot.polarity_scores(line)
        count += 1
        if vs['compound'] >= 0.05:
            fresult["positivenum"] += 1
        elif vs['compound'] <= - 0.05:
            fresult["negativenum"] += 1
        else:
            fresult["neutralnum"] += 1

print("\n")

gen = ' ************************ GENERATING REPORT *************************'
for i in gen:
    print(i, end='')
    sys.stdout.flush()
    time.sleep(0.05)
print("\n")
time.sleep(1)
print("\n ==> READING THROUGH A TOTAL OF", count, "LINES...\n")

time.sleep(1)
print(" ==> AFTER ANALYZING THE SENTIMENT OF", count, "LINES..\n")

positivenum = fresult["positivenum"]
time.sleep(1)
print(" ==> NUMBER OF POSITIVE COMMENTS ARE : ", positivenum, "\n")

negativenum = fresult["negativenum"]
time.sleep(1)
print(" ==> NUMBER OF NEGATIVE COMMENTS ARE : ", negativenum, "\n")

neutralnum = fresult["neutralnum"]
time.sleep(1)
print(" ==> NUMBER OF NEUTRAL COMMENTS ARE : ", neutralnum, "\n")

positive_percentage = positivenum / count * 100

negative_percentage = negativenum / count * 100

neutral_percentage = neutralnum / count * 100

size1 = positive_percentage / 100 * 360

size2 = negative_percentage / 100 * 360

size3 = neutral_percentage / 100 * 360
time.sleep(1)
print(" ==> PERCENTAGE OF COMMENTS THAT ARE POSITIVE : ", positive_percentage, "%\n")
time.sleep(1)
print(" ==> PERCENTAGE OF COMMENTS THAT ARE NEGATIVE : ", negative_percentage, "%\n")
time.sleep(1)
print(" ==> PERCENTAGE OF COMMENTS THAT ARE NEUTRAL  : ", neutral_percentage, "%\n")
time.sleep(1)
print(" ==> CALCULATING FINAL RESULT.. :-\n")
time.sleep(3)
print(" ********************************************************************\n")

percentage.append(positive_percentage)
percentage.append(negative_percentage)
percentage.append(neutral_percentage)

print(percentage)
csv_writer(percentage)

if positive_percentage >= (neutral_percentage + negative_percentage + 10):
    print(" ==> GREAT JOB!! You got positive feeback.")

elif negative_percentage >= (neutral_percentage + positive_percentage + 10):
    print(" ==> SORRY!! You got negative feedback.")

else:
    print(" ==> NICE TRY!! You got neutral feedback.")

print("\n ********************************************************************\n")

labels = 'Positive', 'Negative ', 'Neutral'

sizes = [size1, size2, size3]

colors = ['Green', 'Red', 'gold']

explode = (0.01, 0.01, 0.01)

patches, texts = plt.pie(sizes, explode=explode, colors=colors
                         , startangle=120)

plt.legend(patches, labels, loc="best")

plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', startangle=120, textprops={'fontsize': 10})

plt.tight_layout()

plt.axis('equal')

plt.show()
