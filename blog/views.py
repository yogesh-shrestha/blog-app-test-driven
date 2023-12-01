from django.http import BadHeaderError, HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView, ListView, DetailView, FormView
from django.views.generic.edit import FormMixin
from django.views import View
from django.core.mail import mail_admins
from django.views.decorators.cache import cache_page

from .models import Profile, Post, Category, Comment
from .forms import EditProfileForm, AddPostForm, CommentForm, ContactForm
from core.models import TaggedItem, Tag
from .tasks import send_mail_task



@method_decorator(cache_page(5*60), name='dispatch')
class ListPostView(ListView):
    queryset = Post.objects.filter(status_published=True)                            
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 6


@method_decorator(login_required(login_url=reverse_lazy('core:sign_in_page')), name='dispatch')
class AddPostView(View):

    def get(self, request, *args, **kwargs):
        form = AddPostForm()
        return render(request, 'blog/add_post.html', {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = AddPostForm(self.request.POST, self.request.FILES)
    
        if form.is_valid():
            form.instance.author = self.request.user
            post = form.save()
            tag_labels = form.cleaned_data.get('tags')
            TaggedItem.objects.save_tags_for(object_type=Post, 
                                            object_id=post.id, 
                                            tag_labels = tag_labels)
            return HttpResponseRedirect(reverse('blog:thanks_post_page'))
        return render(request, 'blog/add_post.html', {'form': form}) 


@method_decorator(cache_page(5*60), name='dispatch')
class PostDetailView(FormMixin, DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    form_class = CommentForm
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        tagged_items = TaggedItem.objects.get_tags_for(object_type=Post,
                                                object_id=self.object.id) 
        context['tagged_items'] = tagged_items
        comments = Comment.objects.filter(post_id=self.kwargs['pk'])
        context['comments'] = comments
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
    
    def form_valid(self, form):
        form.instance.post = self.object
        form.save()   
        return super().form_valid(form)
   
    def get_success_url(self):
        return reverse('blog:post_detail_page', args=[self.object.id])
    
    

class PostUpdateView(PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = AddPostForm
    template_name = 'blog/update_post.html'
    login_url = reverse_lazy('core:sign_in_page')

    def get_success_url(self):
        return reverse_lazy('blog:post_detail_page', args=[self.object.id])
    
    def get_initial(self):
        initial = super().get_initial()
        taged_items_queryset = TaggedItem.objects.get_tags_for(object_type=Post, 
                                                            object_id=self.object.id)
        tag_labels = [taged_item.tag.label for taged_item in taged_items_queryset]
        initial['tags'] = ', '.join(tag_labels)
        return initial
    
    def has_permission(self):
        return self.request.user.is_staff or self.request.user == self.get_object().author
    
    def form_valid(self, form):
        TaggedItem.objects.filter(object_id=self.object.id).delete()
        tag_labels = form.cleaned_data.get('tags')
        TaggedItem.objects.save_tags_for(object_type=Post, 
                                        object_id=self.object.id, 
                                        tag_labels = tag_labels)
        return super().form_valid(form)


@method_decorator(cache_page(5*60), name='dispatch')
class ListCategoryPostView(ListView):
    template_name = 'blog/category_post.html'
    paginate_by = 6

    def get_queryset(self):
        return Post.objects.filter(category=self.kwargs['pk'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cat_name'] = get_object_or_404(Category, pk=self.kwargs['pk']).name
        return context

    
@method_decorator(cache_page(5*60), name='dispatch')
class ListTagPostView(ListView):
    template_name = 'blog/tag_post.html'
    paginate_by = 6

    def get_queryset(self):
        post_ids_dict = TaggedItem.objects.get_objects_for(object_type=Post, 
                                                tag_id=self.kwargs.get('pk'))
        post_ids = [dict_.get('object_id') for dict_ in post_ids_dict]
        tag_posts = Post.objects.filter(id__in = tuple(post_ids))
        return tag_posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_label = get_object_or_404(Tag, id=self.kwargs.get('pk')).label        
        context['tag_label'] = tag_label
        return context



@login_required(login_url=reverse_lazy('core:sign_in_page'))
def show_profile(request):
    return render(request, 'blog/show_profile.html', {})



class EditProfileView(PermissionRequiredMixin, UpdateView):
    model = Profile
    form_class = EditProfileForm
    template_name = "blog/edit_profile.html"
    success_url = reverse_lazy('blog:show_profile_page')
    login_url = reverse_lazy('core:sign_in_page')

    def has_permission(self):
        if self.request.user.is_anonymous:
            return False
        return self.request.user.profile.id == self.kwargs['pk']
    

class ContactView(FormView):
    template_name = 'blog/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('blog:thanks_page')

    def form_valid(self, form):
        try:
            send_mail_task.delay(form.cleaned_data.get("name"),
                           form.cleaned_data.get("email"),
                           form.cleaned_data.get("message"))
        except:
            BadHeaderError
        return super().form_valid(form)





    






        