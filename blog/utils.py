import requests
import json
from plotly.graph_objs import Bar
from plotly import offline
import plotly
# import python_repos.json
from plotly.subplots import make_subplots


# 1
def get_visual():
    url = 'https://api.github.com/search/repositories?q=language:python&sort=stars'
    headers = {'Accept': 'application/vnd.github.v3+json'}
    r = requests.get(url, headers=headers)
    print(f'Status code: {r.status_code}')

    # Process results.
    response_dict = r.json()
    repo_dicts = response_dict['items'][:10]
    repo_links, stars, labels = [], [], []
    for repo_dict in repo_dicts:

        # repo_names.append(repo_dict['name'])
        repo_name = repo_dict['name']
        repo_url = repo_dict['html_url']
        repo_link = f"<a href='{repo_url}'>{repo_name}</a>"
        repo_links.append(repo_link)
        stars.append(repo_dict['stargazers_count'])

        owner = repo_dict['owner']['login']
        description = repo_dict['description']
        label = f"{owner}<br />{description}"
        labels.append(label)

    # Make visualization.
    data = [{
    'type': 'bar',
    'x': repo_links,
    'y': stars,
    'hovertext': labels,
    'marker': {
    'color': 'rgb(60, 100, 150)',
    'line': {'width': 1.5, 'color': 'rgb(25, 25, 25)'}
    },
    'opacity': 0.6,
    }]

    my_layout = {
    'title': 'Most-Starred Python Projects on GitHub',
    'titlefont': {'size': 28},
    'xaxis': {
    'title': 'Repository',
    'titlefont': {'size': 24},
    'tickfont': {'size': 14},
    },
    'yaxis': {
    'title': 'Stars',
    'titlefont': {'size': 24},
    'tickfont': {'size': 14},
    },
    #  'xaxis': {'title': 'Repository'},
    #  'yaxis': {'title': 'Stars'},
    }

    fig = {'data': data, 'layout': my_layout}
    
    return fig


def generate_visual():
    data = {
    "data": [
        {
            "type": "bar",
            "x": [
                "<a href='https://github.com/public-apis/public-apis'>public-apis</a>",
                "<a href='https://github.com/vinta/awesome-python'>awesome-pyth...</a>",
                "<a href='https://github.com/pallets/flask'>flask</a>",
                "<a href='https://github.com/tiangolo/fastapi'>fastapi</a>",
                "<a href='https://github.com/langchain-ai/langchain'>langchain</a>",
                "<a href='https://github.com/josephmisiti/awesome-machine-learning'>awesome-machi...</a>",
                "<a href='https://github.com/keras-team/keras'>keras</a>",
                "<a href='https://github.com/bregman-arie/devops-exercises'>devops-exercises</a>",
                "<a href='https://github.com/scikit-learn/scikit-learn'>scikit-learn</a>",
                "<a href='https://github.com/python/cpython'>cpython</a>"
            ],
            "y": [
                253162,
                178719,
                63983,
                61911,
                60183,
                59854,
                59090,
                56919,
                55525,
                55368
            ],
            "hovertext": [
                "public-apis<br />A collective list of free APIs",
                "vinta<br />A curated list of awesome Python frameworks, libraries, software and resources",
                "pallets<br />The Python micro framework for building web applications.",
                "tiangolo<br />FastAPI framework, high performance, easy to learn, fast to code, ready for production",
                "langchain-ai<br />⚡ Building applications with LLMs through composability ⚡",
                "josephmisiti<br />A curated list of awesome Machine Learning frameworks, libraries and software.",
                "keras-team<br />Deep Learning for humans",
                "bregman-arie<br />Linux, Jenkins, AWS, SRE, Prometheus, Docker, Python, Ansible, Git, Kubernetes<br>, Terraform, OpenStack, SQL, NoSQL, Azure, GCP, DNS, Elastic,<br> Network, Virtualization. DevOps Interview Questions",
                "scikit-learn<br />scikit-learn: machine learning in Python",
                "python<br />The Python programming language"
            ],
            "marker": {
                "color": "rgb(60, 100, 150)",
                "line": {
                    "width": 1.5,
                    "color": "rgb(25, 25, 25)"
                }
            },
            "opacity": 0.6
        }
    ],
    "layout": {
        "title": "Most-Starred Python Projects on GitHub",
        "titlefont": {
            "size": 28
        },
        "xaxis": {
            "title": "Repository",
            "titlefont": {
                "size": 24
            },
            "tickfont": {
                "size": 14
            }
        },
        "yaxis": {
            # "title": "Stars",
            "titlefont": {
                "size": 24
            },
            "tickfont": {
                "size": 14
            }
        }
    }
    }

     # Shortened labels for the x-axis
    # short_x_labels = [label.split('>')[1].split('<')[0][:5] for label in data["data"][0]["x"]]

    # Make visualization.
    data = [{
    'type': 'bar',
    'x': data["data"][0]["x"],
    'y': data["data"][0]["y"],
    'text': [f'{y / 1000:.0f}K' for y in data["data"][0]["y"]],
    'hovertext': data["data"][0]["hovertext"],
    'marker': {
    'color': 'rgb(60, 100, 150)',
    'line': {'width': 1.5, 'color': 'rgb(25, 25, 25)'}
    },
    'opacity': 0.6,
    }]

   

    my_layout = {
    'margin': {
        'l':5,
        'r':5,
    },
    'title': 'Most-Starred Python Projects on GitHub',
    'titlefont': {'size': 20},
    'xaxis': {
    # 'title': 'Repository',
    'titlefont': {'size': 24},
    'tickfont': {'size': 14},
    'automargin': True,
    'tickangle': 90,
    # 'ticktext':short_x_labels,
    },
    'yaxis': {
    'showticklabels': False,
    # 'title': 'Stars',
    # 'titlefont': {'size': 24},
    'tickfont': {'size': 14},
    'automargin': True,
    },
    #  'xaxis': {'title': 'Repository'},
    #  'yaxis': {'title': 'Stars'},
    }

    

    fig2 = {'data': data, 'layout': my_layout}
    
    return fig2
    
    
    
    
    # # Create a subplot
    # fig2 = make_subplots(rows=1, cols=1)

    # # Add a bar trace to the subplot
    # trace = plotly.graph_objs.Bar(
    #     x=data["data"][0]["x"],
    #     y=data["data"][0]["y"],
    #     # hovertext=data["data"][0]["hovertext"],
    #     marker=data["data"][0]["marker"],
    #     opacity=data["data"][0]["opacity"],
    # )

    # # Update the layout
    # layout = plotly.graph_objs.Layout(
    #     title=data["layout"]["title"],
    #     titlefont=data["layout"]["titlefont"],
    #     xaxis=data["layout"]["xaxis"],
    #     yaxis=data["layout"]["yaxis"],
    # )

    # fig2.add_trace(trace)
    # fig2.update_layout(layout)
    # # return offline.plot(fig, filename='python_repos.html')
    # return fig2
    

# offline.plot(fig, filename='python_repos.html')
if __name__ == "__main__":
    # Call the get_visual function to generate the figure
    fig = get_visual()

    # Convert the figure data to JSON
    fig_json = json.dumps(fig, indent=4, ensure_ascii=False)  # Convert to JSON format with indentation

    # Define the filename where you want to save the JSON file
    json_filename = 'python_repos.json'

    # Save the JSON data to the specified file
    with open(json_filename, 'w', encoding='utf-16') as json_file:
        json_file.write(fig_json)