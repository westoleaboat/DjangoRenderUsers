
from operator import itemgetter
import requests

def hn_articles():

    # Make an API call and store the response.
    url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
    r = requests.get(url)
    # print(f"Status code: {r.status_code}")

    # Process information about each submission.
    submission_ids = r.json()
    submission_dicts = []

    for submission_id in submission_ids[:5]:
        # Make a separate API call for each submission.
        url = f"https://hacker-news.firebaseio.com/v0/item/{submission_id}.json"
        r = requests.get(url)
        # print(f"id: {submission_id}\tstatus: {r.status_code}")
        
        # Check if the response contains the 'descendants' key.
        if 'descendants' in r.json():
            response_dict = r.json()
            submission_dict = {
                'title': response_dict.get('title', 'N/A'),
                'hn_link': f"http://news.ycombinator.com/item?id={submission_id}",
                'comments': response_dict.get('descendants', 0),
            }
            submission_dicts.append(submission_dict)
        else:
            print(f"Submission {submission_id} does not have 'descendants' key.")

    # Sort the submission dictionaries by the number of comments.
    submission_dicts = sorted(submission_dicts, key=itemgetter('comments'), reverse=True)
    # print(submission_dicts)
    # Print the sorted list of submissions.
    # for submission_dict in submission_dicts:
    #     print(f"\nTitle: {submission_dict['title']}")
    #     print(f"Discussion link: {submission_dict['hn_link']}")
    #     print(f"Comments: {submission_dict['comments']}")
        
    return submission_dicts