# from django.shortcuts import render
# from django.http import HttpResponse

# def index(request):
#     return HttpResponse("Hello, world. You're at the homepage, which is from the builder app.")

# def builder(request):
#     return HttpResponse("Hello, world. You're at the builder index.")


from django.shortcuts import render
#from .models import Question


def index(request):
    #latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'some_sample_text': 'some sample i typed'}
    return render(request, 'builder/index.html', context)

def builder(request):
    #latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'some_sample_text': 'some sample i typed'}
    return render(request, 'builder/builder.html', context)