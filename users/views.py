import json
from requests import session
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from .helpers import sent_otp_to_mobile

from .emails import sent_otp_for_emailVerify, sent_otp_via_email


from .serializers import *
from rest_framework.permissions import IsAuthenticated
from .models import BlogIdea, BlogIdeaSave, BlogSection, UserAccount, StoryDetails
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from .functions import *
from django.core import serializers
from django.db.models import Sum
from django.db.models import Q


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        serializer = UserCreateSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.create(serializer.validated_data)

        
        user = UserSerializer(user)
        print(user.data['email'])



        return Response(user.data, status=status.HTTP_201_CREATED)
    

class RetrieveUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_data = UserAccount.objects.get(email=user)
        print(user_data.currentSub)
        user_data = UserSerializer(user_data)
        return Response(user_data.data, status=status.HTTP_200_OK)


# Sherlock@11

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def email_login(request):
    data = request.data
    email = data['email']
    user = UserAccount.objects.filter(email=email).exists()
    print(email)
    print(user)
    if user:
        message="Email Already, please try again"
        return Response(message,status=status.HTTP_401_UNAUTHORIZED)
    else:
        otp = sent_otp_via_email(email)
        print(otp)
        message = "Otp Sended"
        return Response(message,status=status.HTTP_200_OK)
    

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def email_verify(request):
    data = request.data
    email = data['email']
    otp = sent_otp_for_emailVerify(email)
    print(otp)
    message = "Otp Sended"
    return Response(message,status=status.HTTP_200_OK)

# @api_view(['GET', 'POST'])
# @permission_classes([AllowAny])
# def Phone_login(request):
#     data = request.data
#     phone = data.get('phone')
#     user = UserAccount.objects.filter(phone_number=phone).exists()
#     if user:
#         otp = sent_otp_to_mobile(phone)
#         print(otp)
#         return Response(status=status.HTTP_200_OK,message="OTP sended")
#     else:
#         return Response(status=status.HTTP_401_UNAUTHORIZED,message="Invalid email, please try again")
    

    


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def otp_verify(request):
    data = request.data
    otp = data['otp']
    email = data['email']
    otp_verifying = OTP.objects.filter(otp=otp,email=email).exists()
    if otp_verifying:
        message="Verification Success"
        
        return Response(message,status=status.HTTP_200_OK)
    else:
        message="Verification Failure"
        return Response(message,status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def otp_emailVerify(request):
    data = request.data
    otp = data['otp']
    email = data['email']
    otp_verifying = OTP.objects.filter(otp=otp,email=email).exists()
    if otp_verifying:
        message="Verification Success"
        user = UserAccount.objects.get(email=email)
        user.email_verified = True
        user.save()
        return Response(message,status=status.HTTP_200_OK)
    else:
        message="Verification Failure"
        return Response(message,status=status.HTTP_401_UNAUTHORIZED)








@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def UsersData(request):
    if request.method == 'POST':
        user = UserAccount.objects.filter(is_superuser=False).order_by('id')
        user = UserSerializer(user, many=True)
        return Response(user.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def UserData(request):
    if request.method == 'POST':
        data = request.data
        if data is None:
            value = None
        else:
            value = data['value']
        if value:
            user = UserAccount.objects.filter(subscriptionType=value,is_superuser=False).order_by('id')
            user = UserSerializer(user, many=True)
            return Response(user.data, status=status.HTTP_200_OK)
        user = UserAccount.objects.filter(is_superuser=False).order_by('id')
        user = UserSerializer(user, many=True)
        return Response(user.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def Block(request):
    if request.method == 'POST':
        email = request.data
        user = UserAccount.objects.get(email=email)
        if user.is_active == True:
            user.is_active = False
            user.save()
        else:
            user.is_active = True
            user.save()
        all_user = UserAccount.objects.filter(is_superuser=False).order_by()
        all_user = UserSerializer(all_user, many=True)
        return Response(all_user.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def UpdateProfileImage(request):
    if request.method == 'POST':
        data = request.data
        email = data['email']

        url = data['url']
        print(url)
        user = UserAccount.objects.get(email=email)
        user.image_url = url
        user.save()
        user = UserSerializer(user)
        
        return Response(user.data['image_url'],status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def Delete(request):
    if request.method == 'POST':
        data = request.data
        email = data
        user = UserAccount.objects.get(email=email)
        user.delete()
        all_user = UserAccount.objects.filter(is_superuser=False).order_by()
        all_user = UserSerializer(all_user, many=True)
        return Response(all_user.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def Search(request):
    if request.method == 'POST':
        data = request.data
        searchData = UserAccount.objects.filter(
            first_name__icontains=data , is_superuser=False)
        searchData = UserSerializer(searchData, many=True)
        return Response(searchData.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def BlogTopicIdeas(request):
    if request.method == 'POST':
        data = request.data

        topic = data['topic']
        user = data['email']
        request.session['topic'] = topic
        keywords = data['keywords']
        request.session['keywords'] = keywords

        user = UserAccount.objects.get(email=user)
        blog_topic = generateBlogTopicIdeas(topic, keywords)
        word_list = blog_topic[1].split()
        number_of_words = len(word_list)
        wordCountChecker = CountChecker(user, number_of_words)
        print(blog_topic)
        print(number_of_words)
        print(wordCountChecker)
        if wordCountChecker:
            blog = BlogIdea.objects.create(
                title=topic, keywords=keywords, user=user, wordCount=number_of_words)
            request.session['blog_topic'] = blog_topic
            blog = BlogIdeaSerializer(blog)
            user.wordCount += number_of_words
            context = {'blog_topic': blog_topic, 'blog': blog.data}
            return Response(context, status=status.HTTP_200_OK)
        else:
            return Response(user.wordCount, status='words count limit exceeded')   


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def BlogTopic(request):
    if request.method == 'POST':
        data = request.data

        topic = data['topic']
        keywords = data['keywords']
        accuracy = data['accuracy']
        words = data['words']
        email = data['email']
        
        user = UserAccount.objects.get(email=email)
        blog_topic = generateBlogTopic(topic, keywords, words, accuracy)
        word_list = blog_topic[0].split()
        print(word_list)
        print(word_list)
        number_of_words = len(word_list)
        wordCountChecker = CountChecker(user, number_of_words)
        if wordCountChecker:
            blog = BlogCollection.objects.create(
                title = topic,
                blog = blog_topic,
                keywords = keywords,
                accuracy = accuracy,
                user = user,
            )
            user.wordCount += number_of_words
            user.save()
            print(number_of_words)
            print(wordCountChecker)
            return Response(blog_topic, status=status.HTTP_200_OK)
        else:
            return Response(user.wordCount, status='words count limit exceeded')     



@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def Story(request):
    if request.method == 'POST':
        data = request.data
        topic = data['topic']
        keywords = data['keywords']
        accuracy = data['accuracy']
        email = data['email']
        words = data['words']
        user = UserAccount.objects.get(email=email)
        story = generateStory(topic, keywords, words, accuracy)
        word_list = story[1].split()
        number_of_words = len(word_list)
        wordCountChecker = CountChecker(user, number_of_words)
        print(story[0])
        print(number_of_words)
        print(wordCountChecker)
        if wordCountChecker:
            story_save = StoryDetails.objects.create(
                title=topic,
                keywords=keywords,
                accuracy=accuracy,
                user=user,
                story=story,
                wordCount=number_of_words)
            user.wordCount+=number_of_words
            user.save()
            return Response(story, status=status.HTTP_200_OK)
        else:
            error = 'words count limit exceeded'
            return Response(error, status=status.HTTP_507_INSUFFICIENT_STORAGE)            


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def BlogIdeasSave(request):
    data = request.data
    blogTopic = data['content']
    email = data['email']
    keywords = data['keywords']
    title = data['topic']
    unique_id = data['unique_id']
    print(unique_id)
    user = UserAccount.objects.get(email=email)
    blogIdea = BlogIdea.objects.get(unique_id=unique_id)
    blog = BlogIdeaSave.objects.create(
        title=title,
        blog_ideas=blogTopic,
        keywords=keywords,
        user=user,
        idea = blogIdea,
        idea_key = unique_id,
    )
    blog.save()
    blog = BlogIdeaSerializer(blog)
    return Response(blog.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def generateBlogsSect(request):
    data = request.data

    headings = data['checkedList']
    topic = data['topic']
    keywords = data['keywords']
    unique_id = data['unique_id']
    print(headings)
    blog = BlogIdea.objects.get(
        title=topic, keywords=keywords, unique_id=unique_id)
    condition = True
    for heading in headings:
        section = generateBlogSections(topic, heading, keywords)
        word_list = section.split()
        print(word_list)
        number_of_words = len(word_list)
        print(number_of_words,'wordddddddddddd')
        wordCountChecker = CountChecker(blog.user, number_of_words)
        if wordCountChecker:
            blog_section = BlogSection.objects.create(
                title=heading,
                body=section,
                blog=blog,
                user=blog.user
            )
            user = UserAccount.objects.get(email=blog.user.email)
            print(user)
            user.wordCount += number_of_words
            user.save()
            blog_section.save()
        else:
            condition = False
            return condition
    if condition:
        sections = BlogSection.objects.filter(blog=blog)
        sections = BlogSectionSerializer(sections, many=True)
        return Response(sections.data, status=status.HTTP_200_OK)
    else:
        return Response(blog.user.wordCount, status='words count limit exceeded')


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def UserCollection(request):
    wordCount = 0
    data = request.data
    email = data['email']


    BlogIdea_wordCount = 0
    blogIdeaSaveWordCount = 0  
    storyCountWords = 0 


    user = UserAccount.objects.get(email=email)

    blogIdeas = BlogIdea.objects.filter(user=user)
    BlogIdea_wordCount = BlogIdea.objects.filter(
        user=user).aggregate(Sum('wordCount'))
    BlogIdea_wordCount = BlogIdea_wordCount['wordCount__sum']
    blogIdeasCount = BlogIdea.objects.filter(user=user).count()

    blogSection = BlogSection.objects.filter(user=user)
    BlogSection_wordCount = BlogSection.objects.filter(
        user=user).aggregate(Sum('wordCount'))
    blogSectionCount = BlogSection.objects.filter(user=user).count()

    blog_idea_save = BlogIdeaSave.objects.filter(user=user)
    blogIdeaSaveCount = BlogIdea.objects.filter(user=user).count()
    blogIdeaSaveWordCount = BlogIdeaSave.objects.filter(
        user=user).aggregate(Sum('wordCount'))
    blogIdeaSaveWordCount = blogIdeaSaveWordCount['wordCount__sum']
    print(blog_idea_save)

    story = StoryDetails.objects.filter(user=user)
    storyCount = StoryDetails.objects.filter(user=user).count()
    storyCountWords = StoryDetails.objects.filter(
        user=user).aggregate(Sum('wordCount'))
    storyCountWords = storyCountWords['wordCount__sum']

    blogIdeas = BlogIdeaSerializer(blogIdeas, many=True)
    blogSection = BlogSectionSerializer(blogSection, many=True)
    blog_idea_save = BlogIdeaSaveSerializer(blog_idea_save, many=True)
    story = StorySerializer(story, many=True)
    if BlogIdea_wordCount == None:
        BlogIdea_wordCount = 0
    if blogIdeaSaveWordCount == None:
        blogIdeaSaveWordCount = 0
    if storyCountWords == None:
        storyCountWords = 0

    print(BlogIdea_wordCount,blogIdeaSaveWordCount,storyCountWords)
    


    context = {
        'blogIdeas': blogIdeas.data,
        'blogSection': blogSection.data,
        'blog_idea_save': blog_idea_save.data,
        'blogIdeasCount': blogIdeasCount,
        'blogSectionCount': blogSectionCount,
        'blogIdeaSaveCount': blogIdeaSaveCount,
        'story': story.data,
        'storyCount': storyCount,

    }
    return Response(context, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def PrimeSearch(request):
    if request.method == 'POST':
        data = request.data
        searchData = UserAccount.objects.filter(
            Q(first_name__icontains=data) | Q(email__icontains=data) |  Q(subscriptionType__icontains=data) | Q(wordCount__icontains=data), is_superuser=False)
        searchData = UserSerializer(searchData, many=True)
        return Response(searchData.data, status=status.HTTP_200_OK)
    

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def FreeTrailData(request):
    if request.method == 'GET':
        user = UserAccount.objects.filter(is_superuser=False,subscriptionType = 'Free Trail')
        userDetails = UserSerializer(user, many=True)

        freeTrail = Prime.objects.all()
        print(freeTrail)
        freeTrailDet = PrimeSerializer(freeTrail, many=True)
        print(freeTrailDet)
        context = {
            'userDetails':userDetails.data,
            'freeTrailDet':freeTrailDet.data
        }
        return Response(context, status=status.HTTP_200_OK)
    

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def EditPrime(request):
    if request.method == 'POST':
        data = request.data
        words = data['words']
        prize = data['prize']
        key = data['key']
        prime = data['prime']
        month = data['month']

        prime = Prime.objects.get(
            unique_id = key,
            prime = prime,
        )
        prime.words = words
        prime.prize = prize
        prime.month = month
        prime.save()
        prime = Prime.objects.all().order_by('id')
        prime = PrimeSerializer(prime,many=True)

        return Response(prime.data, status=status.HTTP_200_OK)
    



@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def PrimeData(request):
    if request.method == 'GET':
        prime = Prime.objects.all()
        print(prime)
        prime = PrimeNameSerializer(prime, many=True)
        print(prime.data[2])
        return Response(prime.data, status=status.HTTP_200_OK)
    



@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def Beginner(request):
    if request.method == 'GET':
        user = UserAccount.objects.filter(is_superuser=False,subscriptionType = 'Beginner Level')
        userDetails = UserSerializer(user, many=True)

        freeTrail = Prime.objects.all()
        print(freeTrail)
        freeTrailDet = PrimeSerializer(freeTrail, many=True)
        print(freeTrailDet)
        context = {
            'userDetails':userDetails.data,
            'freeTrailDet':freeTrailDet.data
        }
        return Response(context, status=status.HTTP_200_OK)
    


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def subscriptionPlans(request):
    data = request.data
    plans = Prime.objects.all()
    plans = PrimeSerializer(plans,many=True)
    return Response(plans.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def registerSubscriptions(request):
    data = request.data
    email = data.get('email')
    payment_id = data['paymentId']
    plan = data['key']
    amount = data['amount']
    user = UserAccount.objects.get(email=email)
    sub = Prime.objects.get(prime=plan)
    plans = PremiumSubscription.objects.create(
        user=user,
        payment_id=payment_id,
        plan = sub,
        payment=amount,

    )
    planCheck = CurrentSub.objects.filter(user=user).exists()
    if planCheck:
        current = CurrentSub.objects.get(user=user)
        current.delete()
    current = CurrentSub.objects.create(
        user=user,
        premiumPlan=plans
        )
    current.save()
        
    user.premium = True
    user.subscriptions = plan
    user.monthlyCount=sub.words
    user.approve = True
    user.save()
    user = UserSerializer(user)
    return Response(user.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def UpdateProfile(request):
    data = request.data
    first_name = data['first_name']
    last_name = data['last_name']
    email = data['email']
    phone_number = data['phone_number']
    user = UserAccount.objects.get(email=email)
    print(user.first_name, user.last_name)
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.phone_number = phone_number
    user.save()
    user = UserSerializer(user)
    return Response(user.data,status=status.HTTP_200_OK)




@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def ImageGenerate(request):
    data = request.data
    topic = data['topic']
    keywords = data['keywords']
    imageQuality = data['imageQuality']
    print(topic,keywords,imageQuality)
    imageUrl = ImageGenerator(topic,keywords,imageQuality)
    print('heeeeeeeeeeeeeeeey')
    print(imageUrl)
    return Response(imageUrl,status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def savedIdeas(request):
    data = request.data
    email = data['email']
    user = UserAccount.objects.get(email=email)
    ideas = BlogIdeaSave.objects.filter(user=user)
    ideas = BlogIdeaSaveSerializer(ideas,many=True)
    return Response(ideas.data,status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def deleteIdea(request):
    data = request.data
    idea = data['content']
    email = data['email']
    user = UserAccount.objects.get(email=email)
    ideas = BlogIdeaSave.objects.get(user=user,blog_ideas=idea)
    ideas.delete()
    allIdeas = BlogIdeaSave.objects.filter(user=user)
    allIdeas = BlogIdeaSaveSerializer(allIdeas,many=True)
    return Response(allIdeas.data,status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def blogSect(request):
    data = request.data
    contents = []
    headings = data['checkedList']
    print(headings[0]['title'],'first')
    condition = True
    for heading in headings:
        print(heading['idea_key'])
        blog = BlogIdea.objects.get(
        title=heading['title'], keywords=heading['keywords'], unique_id=heading['idea_key'])
        section = generateBlogSections(heading['blog_ideas'], heading, heading['keywords'])
        print(section)
        word_list = section.split()
        number_of_words = len(word_list)
        wordCountChecker = CountChecker(blog.user, number_of_words)
        print(wordCountChecker)
        if wordCountChecker:
            blog_section = BlogSection.objects.create(
                title=heading['blog_ideas'],
                body=section,
                blog=blog,
                user=blog.user
            )
            blog_section.save()
            user = UserAccount.objects.get(email=blog.user.email)
            user.wordCount += number_of_words
            user.save()
        else:
            condition = False
            return condition
        if condition:
            sections = BlogSection.objects.filter(
                title=heading['blog_ideas'],
                body=section,
                blog=blog,
                user=blog.user
            )
            sections = BlogSectionSerializer(sections, many=True)
            contents.append(sections.data)
    if condition:
        print(contents)
        return Response(contents, status=status.HTTP_200_OK)
    else:
        return Response(blog.user.wordCount, status='words count limit exceeded')

    

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def blogSectionDetails(request):
    data = request.data
    email = data['email']
    user = UserAccount.objects.get(email=email)
    section = BlogSection.objects.filter(user=user)
    section = BlogSectionSerializer(section,many=True)
    return Response(section.data,status=status.HTTP_200_OK)



@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def deleteSection(request):
    data = request.data
    body = data['content']
    email = data['email']
    user = UserAccount.objects.get(email=email)
    section = BlogSection.objects.get(user=user,body=body)
    section.delete()
    all_section = BlogSection.objects.filter(user=user)
    all_section = BlogSectionSerializer(all_section,many=True)
    return Response(all_section.data,status=status.HTTP_200_OK)

    

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def blogDetails(request):
    data = request.data
    email = data['email']
    user = UserAccount.objects.get(email=email)
    blog = BlogCollection.objects.filter(user=user)
    print(blog)
    blog = BlogCollectionSerializer(blog,many=True)
    return Response(blog.data,status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def deleteBlog(request):
    data = request.data
    blog = data['content']
    email = data['email']
    user = UserAccount.objects.get(email=email)
    blog = BlogCollection.objects.get(user=user,blog=blog)
    blog.delete()
    all_blog = BlogSection.objects.filter(user=user)
    all_blog = BlogSectionSerializer(all_blog,many=True)
    return Response(all_blog.data,status=status.HTTP_200_OK)

        
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def subscribedDetails(request):
    data = request.data
    email = data['email']
    print(email)
    user = UserAccount.objects.get(email=email)
    plans = PremiumSubscription.objects.filter(user=user)
    plan = CurrentSub.objects.get(user=user)
    planData = Prime.objects.get(prime=plan.premiumPlan.plan.prime)
    print(planData)
    plans = PremiumSubscriptionSerializer(plans,many=True)
    planData = PrimeSerializer(planData)
    plan= CurrentSubSerializer(plan)
    print(plan.data,'plans')
    context = {
        'subscribed':plan.data,
        'plan':planData.data,
        'plans':plans.data
    }
    return Response(context,status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def cancelSubscription(request):
    data = request.data
    email = data['email']
    user = UserAccount.objects.get(email=email)
    plan = CurrentSub.objects.get(user=user)
    subPlans= PremiumSubscription.objects.get(unique_id=plan.premiumPlan.unique_id)
    subPlans.status = False
    subPlans.save()
    plan.delete()
    user.premium = False
    user.save()

    plansDetails = PremiumSubscription.objects.filter(user=user)
    plansDetails = PremiumSubscriptionSerializer(plansDetails,many=True)

    planData = Prime.objects.get(prime=plan.premiumPlan.plan.prime)
    planData = PrimeSerializer(planData)

    plan = CurrentSubSerializer(plan)
    context = {
        'subscribed':plan.data,
        'plan':planData.data,
        'plans':plansDetails.data
    }
    return Response(context,status=status.HTTP_200_OK)