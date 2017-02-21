from django.contrib import messages
from django.http import HttpResponse
from django.views.generic.base import TemplateView
import json
from models import Applicants
import datetime
from forms import ApplicantAnalysisForm
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

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
            request_received_time_stamp = datetime.datetime.now()
            start_date = app_analysis_form.cleaned_data.get("start_date")
            end_date = app_analysis_form.cleaned_data.get("end_date")
            json_data = self.compute_applicant_data(start_date, end_date)
        else:
            return super(TemplateView, self).render_to_response({"form": app_analysis_form})
        response = HttpResponse(json.dumps(json_data, sort_keys=True, indent=4), content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename=funnel.json'
        request_fulfilled_time_stamp = datetime.datetime.now()
        time_to_fullfill_request = request_fulfilled_time_stamp - request_received_time_stamp
        logger.debug("Time to fulfill request from {0} to {1} : {2} secs".format(start_date, end_date, time_to_fullfill_request.total_seconds()))
        return response

    def compute_applicant_data(self, start_date, end_date):
        '''
        Computes and returns json data for a given date range.
        '''

        #Fetching all applicants for the given date range as a list of workflow_state and created_at at once so that
        #  there are no more db calls in the rest of the evaluation. Applying list to the queryset for
        # immediate execution. Sorted the list by created_at date for ease in computing data for each week.
        all_applicants_for_date_range = list(
            Applicants.objects.filter(created_at__range=(start_date, end_date)).values_list("workflow_state",
                                                                                            "created_at").order_by(
                "created_at"))

        if all_applicants_for_date_range:
            #If the queryset returns data, update the start_date by the created_at date of the first applicant of the
            # list and the end_date by the created_at of the last applicant in the list since its sorted by created_at
            # to avoid unnecessary searches
            start_date = all_applicants_for_date_range[0][1]
            end_date = all_applicants_for_date_range[-1][1]

            #Set the values of current_startdate and current_enddate for the first week
            current_startdate = start_date
            current_enddate = start_date + datetime.timedelta(days=6)

            final_data = {}
            start = 0
            end = len(all_applicants_for_date_range)
            while current_enddate <= end_date:
                #Looping through for each week till current_enddate reaches end_date

                #created a dict(hashmap) for each workflow_state as a bucket to store the frequency of occurance of each state
                #  for every applicant with a created_at date in the week of computation
                applicant_workflow_count_dict = {"applied": 0, "quiz_started": 0, "quiz_completed": 0,
                                                 "onboarding_requested": 0,
                                                 "onboarding_completed": 0, "hired": 0, "rejected": 0}

                add_to_list = False
                for index in range(start, end):
                    #Looping through the applicants to update applicant_workflow_count_dict for the applicants of the
                    # week of computation
                    applicant = all_applicants_for_date_range[index]
                    if applicant[1] > current_enddate:
                        #If the created_at of an applicant is greater than current_enddate store the index of the
                        # applicant to start with this index for the next week of computation to avoid unecessary
                        # comparisions and break out of the loop.
                        start = index
                        break
                    else:
                        applicant_workflow_count_dict[applicant[0]] += 1
                        add_to_list = True
                if add_to_list:
                    #If there are applicants found for this week of computation create the json data and append it to
                    # final_data with key as date_str and vale as the dict applicant_workflow_count_dict
                    date_str = "{0}-{1}".format(current_startdate.strftime("%Y-%m-%d"),
                                                current_enddate.strftime("%Y-%m-%d"))
                    final_data.update({date_str: applicant_workflow_count_dict})
                current_startdate = current_enddate + datetime.timedelta(days=1)
                current_enddate = current_startdate + datetime.timedelta(days=6)
            if current_startdate <= end_date:
                #If the duration between the start_date and end_date is less than a week then the above loop will not
                # get executed and a single record is generated with the key as start_date-end_date

                applicant_workflow_count_dict = {"applied": 0, "quiz_started": 0, "quiz_completed": 0,
                                                 "onboarding_requested": 0,
                                                 "onboarding_completed": 0, "hired": 0, "rejected": 0}
                add_to_list = False
                for applicant in all_applicants_for_date_range[start:]:
                    if applicant[1] <= end_date:
                        applicant_workflow_count_dict[applicant[0]] += 1
                        add_to_list = True
                if add_to_list:
                    date_str = "{0}-{1}".format(current_startdate.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
                    final_data.update({date_str: applicant_workflow_count_dict})
        else:
            final_data = "No results found for given date range"
            logger.debug("No search results returned for {0} to {1}".format(start_date, end_date))
        return final_data
