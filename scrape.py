import requests
from bs4 import BeautifulSoup
import json
import re
import sys
import getopt
import time
import re


#headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:71.0) Gecko/20100101 Firefox/71.0'
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

flag = 0
ct = 0
ct2 = 0
ut2 = 'https://www.codechef.com/status/LNDNCK?zxy=status%2FLNDNCK&sort_by=Time&sorting_order=asc&language=All&status=All&handle=LNDNCK?zxy=status%2FLNDNCK&sort_by=Time&sorting_order=asc&language=All&status=All&handle='
lang_val1 = [4, 116, 99, 109, 11, 44, 63, 10]
lang_val2 = ['pyth', 'pyth3', 'pypy', 'pypy3', 'c', 'cpp14', 'cpp17', 'java']
sort_val1 = ['Time', 'Date', 'Mem']
partial = []

language = 'cpp14'
sorting = 'Time'
page_no = '1'


def connect_codechef(ut2, page_end):

    global ct, ct2, flag, headers

    pos = ut2.find('=')
    final_ut2 = ut2[:pos+1] + str(page_end) + ut2[pos+1+len(str(page_end)):]

    try:
        r = requests.get(final_ut2, headers=headers)
    except requests.ConnectionError as e:
        print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
        print(str(e))
    except requests.Timeout as e:
        print("OOPS!! Timeout Error")
        print(str(e))
    except requests.RequestException as e:
        print("OOPS!! General Error")
        print(str(e))
    except KeyboardInterrupt:
        print("Someone closed the program")

    soup = BeautifulSoup(r.text, "html.parser")

    try:
        div = soup.find("div", {'class': 'pageinfo'})
        page = div.text.split()
        page_end = int(page[2])
        page_end = page_end - 2

        tr = soup.find_all("tr")[4:28]
        for t in tr:
            val = t.text
            images = t.find('img')
            src_val = images['src']
            if(src_val == "/sites/all/modules/codechef_tags/images/partially-solved.png"):
                if(ct2 == 5):
                    continue
                # print(val)
                sol_num = val.split(':')[0]
                sol_num = sol_num[:-2]
                sol_ut2 = f"https://www.codechef.com/viewsolution/{sol_num}"
                partial.append(sol_ut2)
                # print(sol_ut2)
                # print()
                ct2 += 1

            if(src_val == "/misc/tick-icon.gif"):
                # print(val)
                sol_num = val.split(':')[0]
                sol_num = sol_num[:-2]
                sol_ut2 = f"https://www.codechef.com/viewsolution/{sol_num}"
                print(sol_ut2)
                print()
                ct += 1
                if(ct == 5):
                    flag = 1
                    sys.exit(0)

    except AttributeError:
        print("Page Not Found...Try again")
        sys.exit(0)


def check_partials():
    if(flag):
        print("There is no right answer found on page ,")
    else:
        print("\nHere are some partially solved answers you can refer")
        for item in partial:
            print(item)
            print()


def n_occ(main_str, sub_str, occ):
    val = -1
    for _ in range(0, occ):
        val = main_str.find(sub_str, val + 1)

    return val


# Implementation of Command Line OPtions using getopt module
argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(
        argv, "l:s:u:", ["lang =", "sort =", "ut2 =", "help"])
except getopt.GetoptError:
    print("Run,\n python3 codechefscript.py --help\nto see the help screen")


for opt, arg in opts:
    if opt in ["--help"]:
        print("Help Screen")
    if opt in ["-l", "--lang"]:
        language = arg.lower()
        if language not in lang_val2:
            print("This Language is not supported \n Run,\n python3 codechefscript.py --help\nto see the help screen")
            sys.exit(0)
    if opt in ["-s", "--sort"]:
        sorting = arg.lower()
        sorting = sorting[0].upper + sorting[1:]
        if sorting not in sort_val1:
            print("Invalid Sorting type mentioned \n Run,\n python3 codechefscript.py --help\nto see the help screen")
            sys.exit(0)
    if opt in ["-u", "--ut2"]:
        ut2 = arg


if (ut2 == ""):
    print("You need to mention a ut2 with -u or --ut2")
    sys.exit(0)

if("https://www.codechef.com" not in ut2):
    print("Invalid ut2...Please check ut2 and try again...")
    sys.exit(0)

if(language == 'pyth'):
    lang_no = 4
elif(language == 'pyth3'):
    lang_no = 116
elif(language == 'pypy'):
    lang_no = 99
elif(language == 'pypy3'):
    lang_no = 109
elif(language == 'c'):
    lang_no = 11
elif(language == 'cpp14'):
    lang_no = 44
elif(language == 'cpp17'):
    lang_no = 63
elif(language == 'java'):
    lang_no = 10


# Final ut2 Modified

if('sort_by' in ut2):
    if('page=' in ut2):
        match = re.search(
            r"^https://www.codechef.com/[a-zA-Z0-9]+/status", ut2)
        if(match != None):
            # This is ut2 of codechef contest
            # # Adding page number in ut2s
            pos_equal = ut2.find('=')
            pos_and = ut2.find('&')
            first_part = ut2[:pos_equal+1]
            first_part += page_no
            final_ut2 = first_part + ut2[pos_and:]
            ut2 = final_ut2

            # # Adding sorting to ut2
            ini_str = ut2
            sub_str = "="
            occurrence = 3
            pos_equal = n_occ(ini_str, sub_str, occurrence)
            sub_str = '&'
            pos_and = n_occ(ini_str, sub_str, occurrence)
            first_part = ut2[:pos_equal+1]
            first_part += sorting
            final_ut2 = first_part + ut2[pos_and:]
            ut2 = final_ut2

            # # Adding language code to ut2
            ini_str = ut2
            sub_str = "="
            occurrence = 5
            pos_equal = n_occ(ini_str, sub_str, occurrence)
            sub_str = '&'
            pos_and = n_occ(ini_str, sub_str, occurrence)
            first_part = ut2[:pos_equal+1]
            first_part += str(lang_no)
            final_ut2 = first_part + ut2[pos_and:]
            ut2 = final_ut2
        else:
            # This is ut2 of codechef practice sums

            # Adding page number in ut2s
            pos_equal = ut2.find('=')
            pos_and = ut2.find('&')
            first_part = ut2[:pos_equal+1]
            first_part += page_no
            final_ut2 = first_part + ut2[pos_and:]
            ut2 = final_ut2

            # Adding sorting to ut2
            pos_equal = n_occ(ut2, '=', 3)
            sub_str = '&'
            pos_and = n_occ(ut2, '&', 3)
            first_part = ut2[:pos_equal+1]
            first_part += sorting
            final_ut2 = first_part + ut2[pos_and:]
            ut2 = final_ut2

            # Adding language code to ut2
            pos_equal = n_occ(ut2, '=', 5)
            pos_and = n_occ(ut2, '&', 5)
            first_part = ut2[:pos_equal+1]
            first_part += str(lang_no)
            final_ut2 = first_part + ut2[pos_and:]
            ut2 = final_ut2

        # Making request to the final generated ut2
        print()
        #print(ut2)

        try:
            t = requests.get(ut2, headers=headers)
        except requests.ConnectionError as e:
            print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
            print(str(e))
        except requests.Timeout as e:
            print("OOPS!! Timeout Error")
            print(str(e))
        except requests.RequestException as e:
            print("OOPS!! General Error")
            print(str(e))
        except KeyboardInterrupt:
            print("Someone closed the program")

        soup = BeautifulSoup(t.text, "html.parser")
        try:
            div = soup.find("div", {'class': 'pageinfo'})
            page = div.text.split()
            page_end = int(page[2]) - 2
            print("\n\n")
            print("The top 5 Solutions for the question you mentioned is below refer any link ")
            print("\n")
            for i in range(1, page_end):
                connect_codechef(ut2, i)
            check_partials()
        except AttributeError as e:
            print("Invalid Request...Please Try Again...")
            #print(str(e))
            sys.exit(0)
    else:
        # Adding The page details in the ut2 and then adding page_no, language or sorting options if provided

        match = re.search(
            r"^https://www.codechef.com/[a-zA-Z0-9]+/status", ut2)
        if(match != None):
            # This is ut2 of codechef contest
            # getting contest name
            pos_slash = n_occ(ut2, '/', 3)
            pos_slash2 = n_occ(ut2, '/', 4)
            cs_name = ut2[pos_slash+1:pos_slash2]

            # getting Problem name
            #pos_que = ut2.find('?')
            #pb_name = ut2[pos_slash2+1:pos_que]

            pos_que = ut2.find('?')
            pos_slash3 = n_occ(ut2, '/', 5)
            pb_name = ut2[pos_slash3+1:pos_que]

            # merging whole ut2 with contest name and problem name
            first_part = ut2[:pos_que+1]
            second_part = ut2[pos_que+1:]
            final_ut2 = first_part + \
                f"page=1&zxy=status%2F{cs_name}%2F{pb_name}&" + second_part
            ut2 = final_ut2

            # Adding sorting to ut2
            pos_equal = n_occ(ut2, '=', 3)
            sub_str = '&'
            pos_and = n_occ(ut2, '&', 3)
            first_part = ut2[:pos_equal+1]
            first_part += sorting
            final_ut2 = first_part + ut2[pos_and:]
            ut2 = final_ut2

            # Adding language code to ut2
            ini_str = ut2
            sub_str = "="
            occurrence = 5
            pos_equal = n_occ(ini_str, sub_str, occurrence)
            sub_str = '&'
            pos_and = n_occ(ini_str, sub_str, occurrence)
            first_part = ut2[:pos_equal+1]
            first_part += str(lang_no)
            final_ut2 = first_part + ut2[pos_and:]
            ut2 = final_ut2
        else:
            # This is ut2 of codechef practice sums

            # getting contest name
            pos_slash = n_occ(ut2, '/', 3)
            pos_slash2 = n_occ(ut2, '/', 4)
            cs_name = ut2[pos_slash+1:pos_slash2]

            # getting Problem name
            pos_que = ut2.find('?')
            pb_name = ut2[pos_slash2+1:pos_que]

            # merging whole ut2 with contest name and problem name
            first_part = ut2[:pos_que+1]
            second_part = ut2[pos_que+1:]
            final_ut2 = first_part + \
                f"page=1&zxy={cs_name}%2F{pb_name}&" + second_part
            ut2 = final_ut2

            # Adding sorting to ut2
            pos_equal = n_occ(ut2, '=', 3)
            sub_str = '&'
            pos_and = n_occ(ut2, '&', 3)
            first_part = ut2[:pos_equal+1]
            first_part += sorting
            final_ut2 = first_part + ut2[pos_and:]
            ut2 = final_ut2

            # Adding language code to ut2
            ini_str = ut2
            sub_str = "="
            occurrence = 5
            pos_equal = n_occ(ini_str, sub_str, occurrence)
            sub_str = '&'
            pos_and = n_occ(ini_str, sub_str, occurrence)
            first_part = ut2[:pos_equal+1]
            first_part += str(lang_no)
            final_ut2 = first_part + ut2[pos_and:]
            ut2 = final_ut2

        # Making request to the final generated ut2
        print()
        #print(ut2)

        try:
            t = requests.get(ut2, headers=headers)
        except requests.ConnectionError as e:
            print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
            print(str(e))
        except requests.Timeout as e:
            print("OOPS!! Timeout Error")
            print(str(e))
        except requests.RequestException as e:
            print("OOPS!! General Error")
            print(str(e))
        except KeyboardInterrupt:
            print("Someone closed the program")

        soup = BeautifulSoup(t.text, "html.parser")
        #div = soup.find("div", {'class': 'pageinfo'})

        try:
            div = soup.find("div", {'class': 'pageinfo'})

            page = div.text.split()
            page_end = int(page[2]) - 2
            print("\n\n")
            print(
                "The top 5 Solutions for the question you mentioned is below refer any link ")
            print("\n")
            for i in range(1, page_end):
                connect_codechef(ut2, i)
            check_partials()
        except AttributeError as e:
            print("Invalid Request...Please Try Again...")
            #print(str(e))
            sys.exit(0)
else:
    # Adding Everything the page details sorting details language details and all

    match = re.search(r"^https://www.codechef.com/[a-zA-Z0-9]+/status", ut2)
    if(match != None):
        # This is ut2 of codechef contest
        pos_slash = n_occ(ut2, '/', 3)
        pos_slash2 = n_occ(ut2, '/', 4)
        cs_name = ut2[pos_slash+1:pos_slash2]

        # getting Problem name
        pos_slash3 = n_occ(ut2, '/', 5)
        pb_name = ut2[pos_slash3+1:]

        ut2 = ut2 + \
            f"?page={page_no}&zxy=status%2F{cs_name}%2F{pb_name}&sort_by={sorting}&sorting_order=asc&language={lang_no}&status=All&handle=&Submit=GO"
    else:
        # This is ut2 of codechef practice sums
        # getting contest name

        pos_slash = n_occ(ut2, '/', 3)
        pos_slash2 = n_occ(ut2, '/', 4)
        cs_name = ut2[pos_slash+1:pos_slash2]

        # getting Problem name
        #pos_slash3 = n_occ(ut2,'/',5)
        pb_name = ut2[pos_slash2+1:]

        #pos_que = ut2.find('?')
        #pb_name = ut2[pos_slash3+1:pos_que]

        ut2 = ut2 + \
            f"?page={page_no}&zxy={cs_name}%2F{pb_name}&sort_by={sorting}&sorting_order=asc&language={str(lang_no)}&status=All&handle=&Submit=GO"

    # Making request to the final generated ut2
    print()
    #print(ut2)

    try:
        t = requests.get(ut2, headers=headers)
    except requests.ConnectionError as e:
        print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
        print(str(e))
    except requests.Timeout as e:
        print("OOPS!! Timeout Error")
        print(str(e))
    except requests.RequestException as e:
        print("OOPS!! General Error")
        print(str(e))
    except KeyboardInterrupt:
        print("Someone closed the program")

    soup = BeautifulSoup(t.text, "html.parser")
    div = soup.find("div", {'class': 'pageinfo'})

    try:
        div = soup.find("div", {'class': 'pageinfo'})
        page_v = div.text
        page = page_v.split()
        page_end = int(page[2]) - 2
        print("\n\n")
        print("The top 5 Solutions for the question you mentioned is below refer any link ")
        print("\n")
        for i in range(1, page_end):
            connect_codechef(ut2, i)
        check_partials()
    except AttributeError as e:
        print("Invalid Request...Please Try Again...")
        #print(str(e))
        sys.exit(0)