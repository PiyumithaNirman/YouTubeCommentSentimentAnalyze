import difflib
import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import datetime, timedelta
import dateutil.relativedelta
import csv

CLIENT_SECRETS_FILE = "client_secret.json"  # for more information   https://python.gotrained.com/youtube-api-extracting-comments/
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

def get_authenticated_service():
    credentials = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)
    #  Check if the credentials are invalid or do not exist
    if not credentials or not credentials.valid:
        # Check if the credentials have expired
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES)
            credentials = flow.run_console()

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(credentials, token)

    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


def write_to_csv(data_list, date_time):
    list_big = []
    list_add = []
    fields = ["vid", "comment_id", "comment", "channel_id", "like_count", "published_date", "updated_date"]
    # print("coments ",comments)

    for i in range(0, len(data_list)):
        list_add = data_list[i]
        stringList1 = [str(x) for x in list_add]
        print(stringList1)
        for j in range(30):
            date = date_time + dateutil.relativedelta.relativedelta(days=j)
            dateTime = date.strftime("%Y-%m-%d")
            print(dateTime + '*****************************')
            if any(dateTime in s for s in stringList1):
                list_big.append(stringList1)
    print("list big ", len(list_big))

    filename = "comcsv4.csv"
    with open(filename, 'w', newline='', encoding='utf-16') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter='\t')
        csvwriter.writerow(fields)
        csvwriter.writerows(list_big)


#      output file  2mq3pCIN7A0
#       sinahala    4edY1pNRmnI ,kanna = F4OKB86r9BQ

def get_video_comments(service, **kwargs):
    data_list = []
    data_row = []
    publishedDate = []
    results = service.commentThreads().list(**kwargs).execute()
    while results:

        for item in results['items']:
            publisheddate = []
            data_row = []
            print("--------------------------------------------------------------")
            print("item ", item)
            vid = item['snippet']['topLevelComment']['snippet']['videoId']
            data_row.append(vid)

            comment_id = item['snippet']['topLevelComment']['id']
            data_row.append(comment_id)

            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            data_row.append(comment)

            channel_id = item['snippet']['topLevelComment']['snippet']['authorChannelId']['value']
            data_row.append(channel_id)

            like_count = item['snippet']['topLevelComment']['snippet']['likeCount']
            data_row.append(like_count)

            published_date = item['snippet']['topLevelComment']['snippet']['publishedAt']
            data_row.append(published_date)
            publisheddate.append(published_date)

            updated_date = item['snippet']['topLevelComment']['snippet']['updatedAt']
            data_row.append(updated_date)

            publishedDate.append(publisheddate)
            data_list.append(data_row)
        # Check if another page exists
        if 'nextPageToken' in results:
            kwargs['pageToken'] = results['nextPageToken']
            results = service.commentThreads().list(**kwargs).execute()
        else:
            break
    # publishedDate.sort()
    print("*********************************************************")
    print(publishedDate)
    print("*********************************************************")
    publishedDate.sort()
    print(publishedDate[0])
    resDate = str(publishedDate[0])[1:-1]
    print(resDate)
    date_time_str = resDate

    date_time = datetime.strptime(date_time_str, "'%Y-%m-%dT%H:%M:%SZ'")
    print("The date is", date_time)

    # date_time = datetime.strptime(date_time_str, "'%Y-%m-%dT%H:%M:%SZ'")
    # dateIncriment = date_time + dateutil.relativedelta.relativedelta(months=1)
    # print(dateIncriment)
    # dateTime = date_time.strftime("'%Y-%m-%dT%H:%M:%SZ'")
    # dateStr = dateIncriment.strftime("%Y-%m-%dT%H:%M:%SZ")
    # print(dateStr + '**********')
    # reGenerateDate = datetime.strptime(dateIncriment, "'%Y-%m-%dT%H:%M:%SZ'")
    # dateIn = datetime.strptime(dateStr, '%Y-%m-%d %H:%M:%S').strptime('%Y-%m-%dT%H:%M:%SZ')
    print("*********************************************************")
    print(data_list)

    write_to_csv(data_list, date_time)


if __name__ == '__main__':
    # When running locally, disable OAuthlib's HTTPs verification. When
    # running in production *do not* leave this option enabled.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    service = get_authenticated_service()
    videoId = input(
        'Enter Video id : ')  # video id here (the video id of https://www.youtube.com/watch?v=vedLpKXzZqE -> is
    # vedLpKXzZqE)
    get_video_comments(service, part='snippet', videoId=videoId, textFormat='plainText')
# print(len(comments),comments)
# print("my comments ",comments)
