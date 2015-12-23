from django.shortcuts import render
from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext,Context, Template  
from article.models import *
from django.http import Http404
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.contrib.syndication.views import Feed #订阅RSS
from django.http import JsonResponse
from django.core import serializers
import json
import mptt
from django.http.response import HttpResponse  
# Create your views here.   
#导入包装的csrf请求，对跨站攻击脚本做处理  
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template 
from django.db import transaction
# Create your views here.
def Home(request):
    is_Home=True
    articles = Article.objects.all()#获取所有文章
    paginator = Paginator(articles,6)#每页显示的文章数量
    page_num = request.GET.get('page')#获取页数
   
    try:
         articles = paginator.page(page_num)
    except PageNotAnInteger:
         articles = paginator.page(1)
    except EmptyPage:
         articles = paginator.page(paginator.num_pages)

    classification = Classification.class_list.get_Class_list()#分类,以及对应的数目
    tagCloud = json.dumps(Tag.tag_list.get_Tag_list(),ensure_ascii=False)#标签,以及对应的文章数目
    date_list = Article.date_list.get_Article_onDate()#按月归档,以及对应的文章数目
    #return render(request, 'index.html')
    return render_to_response('index.html',
            locals(), #它返回的字典对所有局部变量的名称与值进行映射。
            context_instance=RequestContext(request))

def detail(request, year,month,day,id):#每篇文章的显示
    try:
      
       article = Article.objects.get(id=str(id))
       article.read_count_num =article.read_count_num+1;
       article.save();
       comment= article.comment_set.order_by("-publish_time")
       #nodes= Comment.objects.all()
       nodes=[]
       tempnode=  Comment.objects.filter(article_id=str(id),level=0).order_by("-publish_time")[0:15]
       for node in tempnode:      
           a=getPath(Comment.objects.filter(tree_id=node.tree_id))
           for nodetemp in a:    
               nodes.append(Comment.objects.filter(pk__in=nodetemp))      
    except Article.DoesNotExist:
       raise Http404

    #ar_newpost = Article.objects.order_by('-publish_time')[:10]
    #nodes.reverse()
    classification = Classification.class_list.get_Class_list()
    tagCloud = json.dumps(Tag.tag_list.get_Tag_list(),ensure_ascii=False)#标签,以及对应的文章数目
    date_list = Article.date_list.get_Article_onDate()
    return render_to_response('content.html',
            locals(),
            context_instance=RequestContext(request))

@csrf_exempt  
def save(request):  
    #response=HttpResponse()  
    #article = Article.objects.get(id=1)
    #Comment(content='asd' , article=article,author='sss').save()  
    article = Article.objects.get(id=request.POST.get('id',None))
    article.comment_count =article.comment_count+1;
    article.save();
    name=request.POST.get('author',None)
    if name=='':
       name='匿名用户'
    if str(request.POST.get('to',None))!="":
        Comment.objects.rebuild()
        comment=Comment.objects.get(id=request.POST.get('commontid',None))
        b = Comment(content=request.POST.get('content',None) , article=article,author=request.POST.get('author',None),parent=comment)
        b.save()
    else :
         Comment.objects.rebuild()
         b = Comment(content=request.POST.get('content',None) , article=article,author=request.POST.get('author',None))
         b.save()
    tempnode=Comment.objects.filter(article_id=str(request.POST.get('id',None)),level=0).order_by("-publish_time")[0:15]
    nodes=[]
    for node in tempnode:      
        a=getPath(Comment.objects.filter(tree_id=node.tree_id))
        for nodetemp in a:
            nodes.append(Comment.objects.filter(pk__in=nodetemp))
    #ar_newpost = Article.objects.order_by('-publish_time')[:10]

    classification = Classification.class_list.get_Class_list()
    tagCloud = json.dumps(Tag.tag_list.get_Tag_list(),ensure_ascii=False)#标签,以及对应的文章数目
    date_list = Article.date_list.get_Article_onDate()
    t=get_template('contentTemplt.html')
    c=Context(locals())
    html=t.render(c)
    name_dict = {'html': html}
    return HttpResponse(json.dumps(name_dict),content_type='application/json')
@csrf_exempt 
def detailNew(request):#每篇文章的显示
    try:
      
       #nodes= Comment.objects.all()
       nodes=[]
       num=str(request.POST.get('num',None))
       begin=15*int(num)+1
       end=15*(int(num)+1)
       tempnode=  Comment.objects.filter(article_id=str(request.POST.get('id',None)),level=0).order_by("-publish_time")[begin:end]
       nodes=[]
       for node in tempnode:      
           a=getPath(Comment.objects.filter(tree_id=node.tree_id))
           for nodetemp in a:    
               nodes.append(Comment.objects.filter(pk__in=nodetemp))        
    except Article.DoesNotExist:
       raise Http404
    nodes.reverse()
    #ar_newpost = Article.objects.order_by('-publish_time')[:10]

    classification = Classification.class_list.get_Class_list()
    tagCloud = json.dumps(Tag.tag_list.get_Tag_list(),ensure_ascii=False)#标签,以及对应的文章数目
    date_list = Article.date_list.get_Article_onDate()
    t=get_template('contentTemplt.html')
    c=Context(locals())
    html=t.render(c)
    name_dict = {'html': html}
    return HttpResponse(json.dumps(name_dict),content_type='application/json')


def getPath(Node):
    all=[] 
    for node in Node:
        seq = []
        if node.is_root_node()==False:
           nodenew=node.get_ancestors()
           seq.append(node.id)
           for nodetemp in nodenew:
                seq.append(nodetemp.id)
           all.append(seq)
        if node.is_root_node():
           seq.append(node.id)
           all.append(seq)
    return all
