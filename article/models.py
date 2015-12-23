from django.db import models
from mptt.models import MPTTModel
# Create your models here.
class Author(models.Model):#作者实体
      name = models.CharField(u'名字',max_length=30)
      email = models.EmailField(u'邮箱',blank=True)
      website = models.URLField(u'网站',blank=True)

      class Meta:
        verbose_name = '作者'
        verbose_name_plural = '作者'
      def __str__(self):
          return self.name

class TagManager(models.Manager):
      def get_Tag_list(self):#返回文章标签列表, 每个标签以及对应的文章数目
          tags = Tag.objects.all()#获取所有标签
          tag_list = []
          for i in range(len(tags)):
              tag_list.append([])
          for i in range(len(tags)):
              temp = Tag.objects.get(name = tags[i]) #获取当前标签 
              posts = temp.article_set.all() #获取当前标签下的所有文章
              tag_list[i].append(tags[i].name)
              tag_list[i].append(len(posts))
          return tag_list 

class Tag(models.Model):
      name = models.CharField(u'标签名称',max_length=20,blank=True)#标签
      creat_time = models.DateTimeField(auto_now_add=True)
      
      objects = models.Manager()#默认的管理器
      tag_list = TagManager()#自定义的管理器

      @models.permalink#装饰器 用来简化url
      def get_absolute_url(self):
          return('tagDetail', (), {
          'tag':self.name})
      class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'
      def __str__(self):
          return self.name

class ClassManager(models.Manager):
      def get_Class_list(self):#返回文章分类列表, 每个分类以及对应的文章数目
          classf = Classification.objects.all() #获取所有的分类
          class_list = []
          for i in range(len(classf)):
              class_list.append([])
          for i in range(len(classf)):
              temp = Classification.objects.get(name = classf[i]) #获取当前分类
              posts = temp.article_set.all() #获取当前分类下的所有文章
              class_list[i].append(classf[i])
              class_list[i].append(len(posts))
          return class_list

class Classification(models.Model):#文章分类

      name = models.CharField(u'分类名称',max_length=25)

      objects = models.Manager()#默认的管理器
      class_list = ClassManager()#自定义的管理器
      class Meta:
        verbose_name = '文章分类'
        verbose_name_plural = '文章分类'

      def __str__(self):
          return self.name

class ArticleManager(models.Manager):
      def get_Article_onDate(self):  #实现文章的按月归档, 返回 月份以及对应的文章数  如: [[2015.5,5],[2015.4,5]] ,
          post_date = Article.objects.dates('publish_time','month')
          #post_date = post_date.reverse() #将post_date逆置,使之按月份递减的顺序排布
          date_list=[]       
          for i in range(len(post_date)):
              date_list.append([])
          for i in range(len(post_date)):
              curyear = post_date[i].year
              curmonth = post_date[i].month
              tempArticle = Article.objects.filter(publish_time__year=curyear).filter(publish_time__month=curmonth)
              tempNum = len(tempArticle)
              date_list[i].append(post_date[i])
              date_list[i].append(tempNum)
          return date_list
      def get_Article_OnArchive(self): #返回一个字典,一个时间点,对应一个文章列表
          post_date = Article.objects.dates('publish_time','month')
          #post_date = post_date.reverse() 

          post_date_article=[]
          for i in range(len(post_date)):
              post_date_article.append([])

          for i in range(len(post_date)):
              curyear = post_date[i].year
              curmonth = post_date[i].month
              tempArticle = Article.objects.filter(publish_time__year=curyear).filter(publish_time__month=curmonth)
              post_date_article[i] = tempArticle
      
          dicts=OrderedDict()
          for i in range(len(post_date)):
              dicts.setdefault(post_date[i],post_date_article[i]) 
          return dicts
      
      
      
class Article(models.Model):#文章
      title = models.CharField(u'文章名称',max_length = 100)
      author = models.ForeignKey(Author,verbose_name='作者')
      tags = models.ManyToManyField(Tag,blank=True,verbose_name='标签') #标签
      classification = models.ForeignKey(Classification,verbose_name='分类') #分类
      content = models.TextField(verbose_name='内容',blank=True, null = True)
      publish_time = models.DateField(auto_now_add=True)
      publish_time_new = models.DateTimeField(auto_now_add=True)
      read_count_num = models.IntegerField(u'点击数量',default = 0)#文章点击数,但未实现统计文章点击数的功能
      comment_count = models.IntegerField(u'评论数',default=0)

 
      objects = models.Manager()#默认的管理器
      date_list = ArticleManager()#自定义的管理器
       
      @models.permalink
      def get_absolute_url(self):
          return ('detail', (), {
           'year': self.publish_time.year,
           'month': self.publish_time.strftime('%m'),
           'day': self.publish_time.strftime('%d'),
           'id': self.id})
     
      def get_tags(self):#返回一个文章对应的所有标签
          tag = self.tags.all()
          return tag
           
      def get_before_article(self):#返回当前文章的前一篇文章
          temp = Article.objects.order_by('id')
          cur = Article.objects.get(id=self.id)
          count=0
          for i in temp:
              if i.id==cur.id:
                  index=count
                  break
              else:
                  count=count+1
          if index!=0:
              return temp[index-1]

      def get_after_article(self):#返回当前文章的后一篇文章
          temp = Article.objects.order_by('id')
          max =  len(temp)-1
          cur = Article.objects.get(id=self.id)
          count=0
          for i in temp:
              if i.id==cur.id:
                  index=count
                  break
              else:
                  count=count+1
          if index != max:
           return temp[index+1]
      

      

      def __str__(self):
           return self.title
      class Meta: #按时间下降排序
           verbose_name = '文章'
           verbose_name_plural = '文章'
           ordering = ['-publish_time']  


class Comment(MPTTModel):
      content = models.TextField(verbose_name='内容',blank=True, null = True)
      publish_time = models.DateTimeField(auto_now_add=True)
      author = models.CharField(u'名字',max_length=30)
      article = models.ForeignKey(Article,verbose_name='文章')
      parent = models.ForeignKey("self", blank=True, null=True, related_name="children")
      class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'
      def __str__(self):
         return self.content

class CommentReply(models.Model):
      content = models.TextField(verbose_name='内容',blank=True, null = True)
      publish_time = models.DateTimeField(auto_now_add=True)
      author = models.CharField(max_length=100, default="匿名网友")  
      comment = models.ForeignKey(Comment, null=True, blank=True)
      to = models.CharField(max_length=100, default='匿名网友')
      def __str__(self):
            return self.content
      
     

