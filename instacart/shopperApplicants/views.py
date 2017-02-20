from datetime import datetime
from django.core.urlresolvers import reverse
from django.forms.util import ErrorList
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from forms import ShopperRegistrationForm
from instacart.shopperApplicants.forms import ShopperLoginForm
from models import ShopperApplicants
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
from django.contrib.auth.hashers import *


class ShopperApplicantBaseClass(TemplateView):
    #Display messages
    EMAIL_VALIDATION_FAILURE_MSG = "Sorry! This email is already registered with us. Please try again with a different email-id."
    PHONE_VALIDATION_FAILURE_MSG = "Sorry! This phone number is already registered with us. Please try again with a different phone number."
    SHOPPER_NOT_FOUND_ERR_MSG = "Seems like you're not registered with us yet! Please register here!"
    SHOPPER_DETAILS_UPDATED_SUCCESS_MSG = "Thank you! We have successfully edited your information."
    LOGIN_PASSWORD_INCORRECT_MSG = "Sorry the password is incorrect. Please try again."
    LOGIN_EMAIL_INCORRECT_MSG = "Sorry this email is not registered with us. Please try again."

    def get_context_data(self, **kwargs):
        context_data = super(ShopperApplicantBaseClass, self).get_context_data(**kwargs)
        if self.request.session.get("login_name"):
            context_data["login_name"] = self.request.session.get("login_name")
            context_data["login_id"] = self.request.session.get("login_id")
        return context_data

    def validate_email(self, email):
        if ShopperApplicants.objects.filter(email=email).exists():
            return False
        return True

    def validate_phone(self, phone_no):
        if ShopperApplicants.objects.filter(phone=phone_no).exists():
            return False
        return True

    def validate_form(self, form):

        if not self.validate_email(form.get("email")):
            result = {'success': False, "attr": "email",
                      'message': self.EMAIL_VALIDATION_FAILURE_MSG}
        elif not self.validate_phone(form.get("phone_no")):
            result = {'success': False, "attr": "phone_no",
                      'message': self.PHONE_VALIDATION_FAILURE_MSG}
        else:
            result = {"success": True}
        return result


class ShopperLandingPageView(ShopperApplicantBaseClass):
    '''
    View for the first page the shopper encounters. This view apply now button which takes the shopper to the
    registartion page.
    '''
    template_name = "shopper_landing_page.html"

    def get_context_data(self, **kwargs):
        context = super(ShopperLandingPageView, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        context_data = self.get_context_data(**kwargs)
        return super(ShopperLandingPageView, self).render_to_response(context_data)


class ShopperApplicationView(ShopperApplicantBaseClass):
    '''
    View for registering as a shopper. Displays the ShopperRegistrationForm.
    '''
    template_name = "shopper_apply_now.html"

    def get_context_data(self, **kwargs):
        context = super(ShopperApplicationView, self).get_context_data(**kwargs)
        form = ShopperRegistrationForm(self.request.POST or None)
        context["form"] = form
        return context

    def get(self, request, *args, **kwargs):
        context_data = self.get_context_data(**kwargs)
        return super(ShopperApplicationView, self).render_to_response(context_data)

    def post(self, request, *args, **kwargs):
        """
        Validating the ShopperRegistrationForm and creating an entry in ShopperApplicants.
        Sending an edit link to the shopper's email id.
        Redirecting to the ShopperConfirmBackgroundCheckView
        """
        context = self.get_context_data(**kwargs)
        shopper_application_form = context["form"]
        if shopper_application_form.is_valid():
            form_data = shopper_application_form.cleaned_data
            first_name = form_data.get("first_name")
            last_name = form_data.get("last_name")
            email = form_data.get("email")
            zipcode = form_data.get("zipcode")
            phone_no = form_data.get("phone_no")
            password = make_password(form_data.get("password"), None, 'sha1')
            referral_code = None
            if form_data.get("referral_code"):
                referral_code = shopper_application_form.cleaned_data.get("referral_code")

            result = self.validate_form(form_data)
            if not result["success"]:
                #If validate_form returns success=False, set the form attribute to blank so that the applicant
                # clearly understands which field to re-enter

                errors = shopper_application_form._errors.setdefault(result["attr"], ErrorList())
                errors.append(result["message"])
                return super(ShopperApplicationView, self).render_to_response(context)
            else:
                try:
                    #Precautionary measure to avoid ShopperApplicant exception exists error.
                    #Although this has been handled by validate_form.

                    _ = ShopperApplicants.objects.get(first_name=first_name,
                                                      last_name=last_name,
                                                      email=email,
                                                      phone=phone_no, zipcode=zipcode,
                                                      referral_code=referral_code,
                    )
                except ShopperApplicants.DoesNotExist:
                    _ = ShopperApplicants.objects.create(first_name=first_name,
                                                         last_name=last_name,
                                                         email=email,
                                                         phone=phone_no, zipcode=zipcode,
                                                         referral_code=referral_code,
                                                         workflow_state=ShopperApplicants.APPLIED,
                                                         created_at=datetime.now(),
                                                         password=password
                    )
                self.send_email_to_shopper(email, first_name)
                return HttpResponseRedirect(reverse('shopperBckCheck'))
        else:
            return super(ShopperApplicationView, self).render_to_response(context)


    def send_email_to_shopper(self, email_id, first_name):

        subject = "Welcome to the Instacart Family!"
        message = "<p>Hey {0}!</p><br> <p> Thanks for signing up as a Shopper. </p><p> We will be" \
                  " reviewing your application shortly." \
                  "If you need to edit any information in your application please click on the link below to login - " \
                  " </p><p> <a href={1}>{1}</a> " \
                  "<br><p> Cheers, </p>" \
                  "<p>Instacart </p> ".format(first_name, reverse('shopperLogin'))
        msg = EmailMultiAlternatives(subject, "", "instacart@gmail.com", [email_id])
        msg.attach_alternative(message, "text/html")
        success = msg.send()
        return success


class ShopperApplicantsEditView(ShopperApplicantBaseClass):
    '''
    View to edit shopper appliaction. Once a shopper has registered with Instacart a link to the edit page is sent via email.
    The email-id and phone-no are non-editable fields in this form.
    '''
    template_name = 'shopper_application_edit_page.html'

    def get_context_data(self, **kwargs):
        """
        Set the initial values of the form with the saved details of the shopper and set the email
         field to readonly.
        """
        context = super(ShopperApplicantsEditView, self).get_context_data(**kwargs)
        shopper_id = kwargs["id"]
        try:
            shopper = ShopperApplicants.objects.get(id=shopper_id)
            shopper_edit_form = ShopperRegistrationForm(None, initial={'first_name': shopper.first_name,
                                                                       'last_name': shopper.last_name,
                                                                       'email': shopper.email,
                                                                       'zipcode': shopper.zipcode,
                                                                       'phone_no': shopper.phone,
                                                                       'referral_code': shopper.referral_code,
            })
            shopper_edit_form.fields['email'].widget.attrs['readonly'] = True
            context["form"] = shopper_edit_form
            context["login_name"] = shopper.first_name
            context["workflow_state"] = ShopperApplicants.WORKFLOW_STATUS_CHOICES_DICT[shopper.workflow_state]
        except ShopperApplicants.DoesNotExist:
            #If no ShopperApplicant is found for the id, set the form attribute of context to None and handle it in
            #  get()
            context["form"] = None
        return context

    def get(self, request, *args, **kwargs):
        if request.session["login_name"]:
            context_data = self.get_context_data(**kwargs)
            if not context_data["form"]:
                messages.error(request, self.SHOPPER_NOT_FOUND_ERR_MSG)
                return HttpResponseRedirect(reverse('shopperApply'))
            return super(ShopperApplicantsEditView, self).render_to_response(context_data)
        else:
            messages.error(request, "Oops! Please login first!")
            return HttpResponseRedirect(reverse('shopperLogin'))

    def post(self, request, **kwargs):

        shopper_id = kwargs["id"]
        try:
            shopper = ShopperApplicants.objects.get(id=shopper_id)
        except ShopperApplicants.DoesNotExist:
            messages.error(request, self.SHOPPER_NOT_FOUND_ERR_MSG)
            return HttpResponseRedirect(reverse('shopperApply'))

        shopper_application_form = ShopperRegistrationForm(request.POST)
        if shopper_application_form.is_valid():
            form_data = shopper_application_form.cleaned_data
            first_name = form_data.get("first_name")
            last_name = form_data.get("last_name")
            email = form_data.get("email")
            zipcode = form_data.get("zipcode")
            phone_no = form_data.get("phone_no")
            password = make_password(form_data.get("password"), None)
            referral_code = None
            if form_data.get("referral_code"):
                referral_code = shopper_application_form.cleaned_data.get("referral_code")

            if shopper_application_form.has_changed():
                shopper.first_name = first_name
                shopper.last_name = last_name
                shopper.email = email
                shopper.zipcode = zipcode
                shopper.phone = phone_no
                shopper.referral_code = referral_code
                shopper.password = password
                #If the field values have changed then save the model to avoid unnecessary db calls
                shopper.save()
            messages.success(request, self.SHOPPER_DETAILS_UPDATED_SUCCESS_MSG)
        return super(ShopperApplicantsEditView, self).render_to_response({"form": shopper_application_form})


class ShopperConfirmBackgroundCheckView(ShopperApplicantBaseClass):
    '''
    Background check confirmation view. After the shopper fills the registration form, they are redirected to this view
     where they see a dialog box to confirm whether Instacart can conduct a background check.
    '''
    template_name = "shopper_confirm_background_check.html"

    def get(self, request, *args, **kwargs):
        return super(ShopperConfirmBackgroundCheckView, self).render_to_response({})


class ShopperLoginView(ShopperApplicantBaseClass):
    '''
    Login View for shoppers registered with Instacart to view their application status and edit application if required
    Storing the name and id of the logged in shopper in request.session.
    '''
    template_name = "shopper_login_page.html"

    def get_context_data(self, **kwargs):
        context = super(ShopperLoginView, self).get_context_data(**kwargs)
        form = ShopperLoginForm(self.request.POST or None)
        context["form"] = form
        return context

    def get(self, request, *args, **kwargs):
        context_data = self.get_context_data(**kwargs)
        return super(ShopperLoginView, self).render_to_response(context_data)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        shopper_login_form = context["form"]
        if shopper_login_form.is_valid():
            email = shopper_login_form.cleaned_data.get("email")
            password = shopper_login_form.cleaned_data.get("password")
            if ShopperApplicants.objects.filter(email=email).exists():
                shopper = ShopperApplicants.objects.get(email=email)
                try:
                    if check_password(password, shopper.password):
                        request.session["login_name"] = shopper.first_name
                        request.session["login_id"] = shopper.id
                        return HttpResponseRedirect(reverse("shopperEdit", args=(shopper.id, )))
                    else:
                        errors = shopper_login_form._errors.setdefault("password", ErrorList())
                        errors.append(self.LOGIN_PASSWORD_INCORRECT_MSG)
                except ValueError:
                    errors = shopper_login_form._errors.setdefault("password", ErrorList())
                    errors.append(self.LOGIN_PASSWORD_INCORRECT_MSG)

            else:
                errors = shopper_login_form._errors.setdefault("email", ErrorList())
                errors.append(self.LOGIN_EMAIL_INCORRECT_MSG)

        return super(ShopperLoginView, self).render_to_response({"form": shopper_login_form})


class ShopperLogoutView(ShopperApplicantBaseClass):
    '''
    Logout view removes logged-in info from request.session and takes the shopper back to Landing page
    '''
    template_name = 'shopper_landing_page.html'

    def get_context_data(self, **kwargs):
        context = super(ShopperLogoutView, self).get_context_data(**kwargs)
        context["login_name"] = None
        self.request.session["login_name"] = None
        self.request.session["login_id"] = None
        return context

    def post(self, **kwargs):
        self.get_context_data(**kwargs)
        return HttpResponseRedirect(reverse('shopperLand'))


