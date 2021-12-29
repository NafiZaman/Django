from django.contrib import messages
from django.shortcuts import render
from django.urls.base import reverse
from django.http.response import HttpResponseRedirect, JsonResponse
from difflib import SequenceMatcher
import math

from .models import *
from .forms import ProductReviewForm
from users.decorators import ajax_allowed_users, ajax_login_required
from user_profile.models import Profile


def get_product(request):
    context = {}

    if request.is_ajax and request.method == 'GET':
        context['product_id'] = request.GET.get('product_id')

    return JsonResponse(context)

def view_product(request, product_id):
    context = {}

    try:
        product = Product.objects.get(pk=int(product_id))
        context['product'] = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'stock_quantity': Stock.objects.get(product=product).quantity,
            'image': product.image,
            'description': product.description,
            'type': product.type_of,
            'ingredients': product.ingredients,
            'region': product.region,
        }
            
        if request.method == 'POST':
            if request.user.is_authenticated == False:
                return HttpResponseRedirect(reverse('users:user_login'))
            if request.user.groups.all()[0].name != 'customer':
                messages.warning(request, 'Admin cannot post product reviews.')
                return HttpResponseRedirect(reverse('product:view_product', kwargs={'product_id': product_id}))
            else:
                form = ProductReviewForm(request.POST)

                if form.is_valid():
                    ProductReview.objects.create(
                        author = NewUser.objects.get(email=request.user),
                        product = Product.objects.get(pk=product_id),
                        review = form.cleaned_data.get('review')
                    )

                    messages.success(request, 'Thank you for your feedback!')
                    return HttpResponseRedirect(reverse('product:view_product', kwargs={'product_id': product_id}))

        context['product_reviews'] = []
        for review in ProductReview.objects.filter(product = product_id).order_by('-date_posted'):
            context['product_reviews'].append(
                {
                    'id': review.id,
                    'author': Profile.objects.get(user=review.author).username,
                    'is_author': True if request.user.is_authenticated and review.author == NewUser.objects.get(email=request.user) else False,
                    'review': review.review,
                    'date_posted': review.date_posted,
                    'num_likes':ProductReviewSentiment.objects.filter(review=review.id, sentiment="like").count(),
                    'num_dislikes':ProductReviewSentiment.objects.filter(review=review.id, sentiment="dislike").count(),
                    'liked': request.user.is_authenticated and ProductReviewSentiment.objects.filter(review=review.id, sentiment='like', user=NewUser.objects.get(email=request.user)).exists(),
                    'disliked': request.user.is_authenticated and ProductReviewSentiment.objects.filter(review=review.id, sentiment='dislike', user=NewUser.objects.get(email=request.user)).exists(),
                }
            )

        # print(context['product_reviews'])

        context['form'] = ProductReviewForm()

    except Exception as e:
        print(e)
        messages.error(request, 'Server error')
        return HttpResponseRedirect(reverse('home:home'))

    return render(request, 'product/view_product.html', context)

@ajax_login_required
@ajax_allowed_users(allowed_roles=['customer'])
def rate_review(request):
    context = {}

    try:
        if request.is_ajax and request.method == 'POST':
            review_id = int(request.POST.get('review_id'))
            user_sentiment = request.POST.get('sentiment')
            user = NewUser.objects.get(email=request.user)
            
            product_review_sentiment, created = ProductReviewSentiment.objects.get_or_create(review=ProductReview.objects.get(pk=review_id), user=user)

            if user_sentiment == 'like':
                if product_review_sentiment.sentiment == 'like':
                    product_review_sentiment.sentiment = None
                    context['action'] = 'unlike'
                elif product_review_sentiment.sentiment == 'dislike' or not product_review_sentiment.sentiment:
                    product_review_sentiment.sentiment = user_sentiment
                    context['action'] = user_sentiment
            
            elif user_sentiment == 'dislike':
                if product_review_sentiment.sentiment == 'dislike':
                    product_review_sentiment.sentiment = None
                    context['action'] = 'undislike'
                elif product_review_sentiment.sentiment == 'like' or not product_review_sentiment.sentiment:
                    product_review_sentiment.sentiment = user_sentiment
                    context['action'] = 'dislike'

            product_review_sentiment.save()
            context['like_count'] = ProductReviewSentiment.objects.filter(sentiment='like', review=ProductReview.objects.get(pk=review_id)).count() 
            context['dislike_count'] = ProductReviewSentiment.objects.filter(sentiment='dislike', review=ProductReview.objects.get(pk=review_id)).count()

    except Exception as e:
        print("Error:", e)
        context['server_error'] = True

    return JsonResponse(context)

def search_product(request):
    context = {'results':[]}

    try:
        if request.method == 'GET' and 'search' in request.GET:
            search_item = request.GET.get('search')

            score_dict = {}
            for name in Product.objects.values_list('name', flat=True):
                similarity_score = math.ceil(SequenceMatcher(None, search_item.lower(), name.lower()).ratio() * 100)
                if similarity_score > 0.0:
                    score_dict[name] = similarity_score

            score_dict = dict(sorted(score_dict.items(), key=lambda item: item[1], reverse=True))
            
            for key in score_dict:
                product = Product.objects.get(name=key)
                context['results'].append(
                    {
                        'id': product.id,
                        'name': product.name,
                        'image': product.image,
                        'price': product.price,
                    }
                )


    except Exception as e:
        print("Error:", e)
        messages.error(request,'Internal server error')

    return render(request, 'product/search_product.html', context)
