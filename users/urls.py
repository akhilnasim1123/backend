from django.urls import path
from .views import RegisterView, RetrieveUserView
from . import views



urlpatterns = [
  path('register', RegisterView.as_view()),
  path('me', RetrieveUserView.as_view()),
  path('user-data',views.UserData),
  path('user-details',views.UsersData),
  path('Block',views.Block),
  path('delete',views.Delete),
  path('search',views.Search),
  path('prime-search',views.PrimeSearch),
  path('otp',views.email_login),
  path('email-verify',views.email_verify),
  path('otp-verify',views.otp_verify),
  path('otp-email-verify',views.otp_emailVerify),


  path('blog-ideas-generator',views.BlogTopicIdeas),
  path('blog-generator',views.BlogTopic),
  path('story-generator',views.Story),
  path('save-blog',views.BlogIdeasSave),
  path('generate-blog-sections',views.generateBlogsSect),
  path('user-collection',views.UserCollection),
  path('free-trail',views.FreeTrailData),
  path('beginner',views.Beginner),
  path('edit-prime',views.EditPrime),
  path('prime-data',views.PrimeData),
  path('premium-plans',views.subscriptionPlans),
  path('primium-subscription',views.registerSubscriptions),
  path('update-image',views.UpdateProfileImage),
  path('update-profile',views.UpdateProfile),
  path('image-generator',views.ImageGenerate),
  path('saved-ideas',views.savedIdeas),
  path('delete-idea',views.deleteIdea),
  path('blog-section',views.blogSect),
  path('blog-sections-details',views.blogSectionDetails),
  path('delete-section',views.deleteSection),
  path('blog-details',views.blogDetails),
  path('delete-Blog',views.deleteBlog),
  path('subscribed',views.subscribedDetails),
  

]