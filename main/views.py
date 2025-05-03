from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import HealthCard
from .forms import HealthCardForm
import pandas as pd
from .tools import Generate_Audio_explanation, Whatsapp_notification, Whatsapp_send_file
from django.http import JsonResponse

def my_python_function(request):
    if request.method == "GET":
        print(phonenumber, filename)
        Whatsapp_send_file(phonenumber, filename)
        # Your logic here (e.g., validation, processing)
        message = f"Received phone: {phonenumber}, file path: {filename}"
        return JsonResponse({"message": message})

class MainCreateView(CreateView):
    model = HealthCard
    form_class = HealthCardForm
    template_name = 'main/main_form.html'
    success_url = reverse_lazy('add_main')
    def form_valid(self, form):
        """Save form and redirect to avoid resubmission issues"""
        self.object = form.save(commit=False)  # Save instance but don't 
        form_data = {field: form.cleaned_data[field] for field in form.cleaned_data}
        df = pd.DataFrame([form_data])
        file = Generate_Audio_explanation(df)
        Whatsapp_notification("91"+str(int(df['mobile_number'])))
        self.object.save()  # Now commit to DB
        global phonenumber
        phonenumber = "91"+str(int(df.iloc[0]['mobile_number']))
        global filename
        filename = file
        # Whatsapp_send_file("91"+str(int(df['mobile_number'])), file)
        return render(self.request, self.template_name, {'form': form, 'success': True, 'farmer_name': self.object.farmer_name ,'file': file, 'phonenumber': "91"+str(int(df['mobile_number']))})

class MainListView(ListView):
    model = HealthCard
    template_name = 'main/main_list.html'
    context_object_name = 'items'
