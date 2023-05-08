import os
import openai
# from django.conf import settings
from backend import settings
# Load your API key from an environment variable or secret management service
openai.api_key = os.environ.get('OPENAI_API_KEY')


def generateBlogTopicIdeas(topic, keywords):
    blog_topics = []
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="generate blog topic ideas on the given topic: {}\nkeywords:{} \n*".format(
            topic, keywords),
        temperature=0.5,
        max_tokens=250,
        top_p=1,
        best_of=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    if 'choices' in response:
        if len(response['choices']) > 0:
            res = response['choices'][0]['text']
        else:
            return []
    else:
        return []

    a_list = res.split('*')
    if len(a_list) > 0:
        for blog in a_list:
            blog_topics.append(blog)
    else:
        return []
    return blog_topics


def generateBlogTopic(topic, keywords,words,accuracy):
    blog_topics = []
    words = int(words)
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="write a blog, based on the following topic: {}\nkeywords:{}\nwords: {}\n*".format(topic, keywords,words),
        temperature=accuracy,
        max_tokens=words,
        top_p=1,
        best_of=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    if 'choices' in response:
        if len(response['choices']) > 0:
            res = response['choices'][0]['text']
            # return res
        else:
            return []
    else:
        return []

    a_list = res.split('*')
    if len(a_list) > 0:
        for blog in a_list:
            blog_topics.append(blog)
    else:
        return []
    return blog_topics

def generateStory(topic, keywords,words,accuracy):
    blog_topics = []
    words = int(words)
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="write a story, based on the following topic: {}\nkeywords:{}\nrequirements:heading \n  should contain {} words\n*".format(topic, keywords,words),
        temperature=accuracy,
        max_tokens=words,
        top_p=1,
        best_of=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    if 'choices' in response:
        if len(response['choices']) > 0:
            res = response['choices'][0]['text']
            # return res
        else:
            return []
    else:
        return []

    a_list = res.split('*')
    if len(a_list) > 0:
        for blog in a_list:
            blog_topics.append(blog)
    else:
        return []
    return blog_topics
def generateBlogSections(topic,section,keywords):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Generate detailed blog section write up for '' the following blog section heading, using the blog title, and keywords provided.\nblog title : {}\n Blog section heading: {}\nkeywords: {}\n requirement:maximum words \n".format(topic,section, keywords),
        temperature=0.6,
        max_tokens=200,
        top_p=1,
        best_of=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    if 'choices' in response:
        if len(response['choices']) > 0:
            res = response['choices'][0]['text']
            cleaned_response = res.replace('\n',"*" )
            return cleaned_response
        else:
            return []
    else:
        return []
    

def CountChecker(user,wordCount):
    totalCount = user.wordCount + wordCount
    if totalCount < user.monthlyCount:
        return True
    else:
        return False




def ImageGenerator(topic,keywords,imageQuality):
    response = openai.Image.create(
                prompt="{}. keywords:{}. full view,keep originality".format(topic,keywords),
                n=1,
                size=imageQuality
    )
    image_url = response['data'][0]['url']
    print(image_url)
    return image_url

#256x256, 512x512, or 1024x1024


