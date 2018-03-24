from django.shortcuts import render_to_response, get_object_or_404
from django.utils.safestring import mark_safe



def home_page():
    return render_to_response('home.html')
