import os
import sys

import requests
import re


def green_print(text):
    green = '\033[92m'
    regular = '\033[0m'
    print(f"{green}" + text + f"{regular}")

def get_name(str1):
    # if len(string1)<500==True, it means that the profile url in entered.
    if len(str1) < 500:
        name = string1[26:len(string1) - 1]
    else:
        start = ",\"username\":\""
        end = "\""
        pattern = f"{start}(.*?){end}"
        matches = re.findall(pattern, string1)
        name = matches[0]
    return name

def get_links_as_list_from_string(str1, is_url):
    if is_url:
        str1=str1+"?__a=1&__d=dis"
        str1=requests.get(str1).text
    start_substring = "https://instagram.ftlv6-1.fna.fbcdn"
    end_substring = "nc_sid="+str1[str1.rfind("nc_sid=")+len("nc_sid="):str1.find("\"", str1.rfind(start_substring))]+"\""
    #end_substring = "nc_sid=a12345" # manual set "nc_sid "
    pattern = f"{start_substring}(.*?){end_substring}"
    matches = re.findall(pattern, str1)
    for x in range (len(matches)):
        matches[x]= start_substring + matches[x] + end_substring
        #print(matches[x])
    return matches

def save_content(urls, name):
    folder1=name
    if not os.path.exists(folder1):
        os.makedirs(folder1)

    for x in range(len(urls)):
        if (".mp4" in str((urls[x]))):
            # setting the folder name as the target username ('folder1'), and saving the video
            with open(os.path.join(folder1, (x+1).__str__() + ".mp4"), 'wb') as handler:
                sys.stdout.write("video " + (x + 1).__str__() + "/" + len(urls).__str__())
                handler.write(requests.get(urls[x]).content)
                sys.stdout.write("\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b")
                if (x==len(urls)-1):
                    print("video " + (x+1).__str__() + "/" + len(urls).__str__())
        else:
            # setting the folder name as the target username ('folder1'), and saving the image
            with open(os.path.join(folder1, (x+1).__str__() + ".jpg"), 'wb') as handler:
                sys.stdout.write("picture " + (x + 1).__str__() + "/" + len(urls).__str__())
                handler.write(requests.get(urls[x]).content)
                sys.stdout.write("\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b")
                if (x==len(urls)-1):
                    print("picture " + (x + 1).__str__() + "/" + len(urls).__str__())

while True:
    sys.stdout.flush()
    print()
    print()
    string1= input("enter the target profile url (must be public account): https://www.instagram.com/target_profile_name/\nor enter the text which is shown in (if the account is private): https://www.instagram.com/target_profile_name/?__a=1&__d=dis\n\n")
    print()

    # getting the name of the target, the output folder will be named as the target name
    name= "media\\"+get_name(string1)

    # getting the link list
    list1= get_links_as_list_from_string(string1, True if len(string1)<500 else False)

    # saving each link as '.mp4' or as '.jpg'
    save_content(list1, name)

    print()
    green_print("media has been saved to:")
    green_print(os.path.dirname(os.path.realpath(__file__))+"\\"+name)
