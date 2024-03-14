from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


from django.views.generic import ListView

from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View



from .models import Course
from .forms import ModuleFormSet

# class ManageCourseListView(ListView):
#     """List all courses for a current user"""
#     model = Course
#     template_name = "course/manage/course/list.html"
#     context_object_name = "courses"

#     def get_queryset(self) -> QuerySet[Any]:
#         # override the get_queryset method so that it returns only the courses of the logged in user
#         qs = super().get_queryset()
#         return qs.filter(owner=self.request.user)


# ----------- USING MIXINS ------------------------------
class OwnerMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin:
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin, PermissionRequiredMixin):
    model = Course
    fields = ["subject", "title", "slug", "overview"]
    success_url = reverse_lazy("manage_course_list")
    context_object_name = "courses"


class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = "course/manage/course/list.html"
    permission_required = "course.view_course"


class CourseDeleteView(OwnerCourseMixin, DeleteView):
    template_name = "course/manage/course/delete.html"
    permission_required = "course.delete_course"
    context_object_name = "course"


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    template_name = "course/manage/course/form.html"
    context_object_name = "course"


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    permission_required = "course.add_course"


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    permission_required = "course.change_course"



# ------------ Managing course modules and their contents -----------
class CourseModuleUpdateView(TemplateResponseMixin, View):
    template_name = 'course/manage/module/formset.html'
    course = None
    
    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course, data=data)
    
    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course, id=pk, owner=self.request.user)
        
        return super().dispatch(request, pk)
    
    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'course': self.course, 'formset':formset})
    
    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        else:
            return self.render_to_response({'course': self.course, 'formset':formset})