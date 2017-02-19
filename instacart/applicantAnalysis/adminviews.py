from django.contrib import messages
from django.db.models.aggregates import Count
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from models import Applicants
import datetime
from forms import ApplicantAnalysisForm
import json


class ApplicantAnalysisView(TemplateView):
    '''
    View to display ApplicantAnalysisForm. The form takes start date and end date as input and computes json of the
    format. The  json is downloaded in a file funnel.json.
    '''
    template_name = "applicant_analysis_form.html"

    def get_context_data(self, **kwargs):
        context = super(ApplicantAnalysisView, self).get_context_data(**kwargs)
        form = ApplicantAnalysisForm(self.request.POST or None)
        context["form"] = form
        return context

    def get(self, request, *args, **kwargs):
        context_data = self.get_context_data(**kwargs)
        return super(TemplateView, self).render_to_response(context_data)

    def post(self, request):
        app_analysis_form = ApplicantAnalysisForm(request.POST)
        json_data = {}
        if app_analysis_form.is_valid():
            # start_date =  datetime.strptime(app_analysis_form.cleaned_data.get("start_date"), "%Y-%m-%d")
            # end_date =  datetime.strptime(app_analysis_form.cleaned_data.get("end_date"), "%Y-%m-%d")
            start_date = app_analysis_form.cleaned_data.get("start_date")
            end_date = app_analysis_form.cleaned_data.get("end_date")
            if end_date <= start_date:
                app_analysis_form._errors["end_date"] = str("End date should be greater than start date.")

            json_data = self.compute_applicant_data(start_date, end_date)
        else:
            return super(TemplateView, self).render_to_response({"form": app_analysis_form})
        response = HttpResponse(json.dumps(json_data), content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename=funnel.json'
        messages.success(request, "Successfully downloaded result as funnel.json!")
        return response

    def compute_applicant_data(self, start_date, end_date):
        '''
        Computes and returns json data for a given date range.
        '''


        current_enddate = start_date + datetime.timedelta(days=6)
        final_data = {}
        while current_enddate <= end_date:
            app_data_list = list(
                Applicants.objects.filter(created_at__range=(start_date, current_enddate)).values_list("workflow_state").annotate(
                    total=Count("workflow_state")))
            date_str = "{0}-{1}".format(start_date.strftime("%Y-%m-%d"), current_enddate.strftime("%Y-%m-%d"))
            final_data.update({date_str: {}})
            for i in app_data_list:
                if i[1] > 0:
                    final_data[date_str].update({str(i[0]): i[1]})
            if not final_data[date_str]:
                final_data.pop(date_str)
            start_date = current_enddate + datetime.timedelta(days=1)
            current_enddate = start_date + datetime.timedelta(days=7)

        current_enddate = end_date
        app_data_list = list(
            Applicants.objects.filter(created_at__range=(start_date, end_date)).values_list("workflow_state").annotate(
                total=Count("workflow_state")))
        date_str = "{0}-{1}".format(start_date.strftime("%Y-%m-%d"), current_enddate.strftime("%Y-%m-%d"))
        final_data.update({date_str: {}})
        for i in app_data_list:
            final_data[date_str].update({str(i[0]): i[1]})
        return final_data
