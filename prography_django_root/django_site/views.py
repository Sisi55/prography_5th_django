from django.shortcuts import render,redirect

from django.http import HttpResponse
from django.utils import timezone
from firebase_admin import firestore
from .models import Post,Info
# Create your views here.

#전역?
#post_number=0
# post_past = firestore.client().collection(u'posts').where(u'number',u'==', int(post_number)).get()
# for p in post_past:
#     print(p.id, p.to_dict(), type(p))
#     post_id = p.id



def home_list(request, page_number=1):
    if page_number < 1:
        page_number=1

    #데이터 임시 생성
    # for i in range(50,-1,-1):
    #     print(i)

    #     transaction = firestore.client().transaction()
    #     info_ref = firestore.client().collection(u'info').document(u'posting_info')

    #     @firestore.transactional # 단순 1 증가하는 함수
    #     def update_in_transaction(transaction, info_ref):
    #         snapshot = info_ref.get(transaction=transaction)
    #         transaction.update(info_ref, {
    #                 u'number': snapshot.get(u'number') + 1
    #         })
    #         post_number = info_ref.get().to_dict().get('number')
    #     #doc = doc_ref.get()
        
    #     # 데이터 저장
    #         now = timezone.localtime()
    #         post = Post(title=str(i), contents=str(i), time=now, n=post_number)
    #         firestore.client().collection(u'posts').add(post.to_dict())


    #     update_in_transaction(transaction, info_ref)



# transaction = firestore.client().transaction()

    # 일단 데이터 전부 가져온다
#cities_ref = db.collection(u'cities')
# query = cities_ref.order_by(u'name', direction=firestore.Query.DESCENDING).get()

    docs = firestore.client().collection(u'posts').order_by(u'time', direction=firestore.Query.DESCENDING).get()

    context = {'posts':[]}
    context['page_n']=[page_number-1,page_number,page_number+1] #3페이지만 보여준다
    for doc in docs:
        #print(u'{}\n'.format(doc.to_dict()))
        #doc_dict = doc.to_dict()
        # print(type(doc.to_dict()['contents']))
        # doc.to_dict()['contents'] = str(list(doc.to_dict()['contents'])[0:10])
        # if '\n' in doc.to_dict()['contents']:
        #     print('   개행처리 필요')
            
        context['posts'].append(doc.to_dict())
    
    print(context['posts'][:20])
    # post 분할해서 가져다주기
    post_n = len(context['posts'])
    
    page_n = int(post_n / 5 +1) #
    print('전체 post 개수', post_n, '\n', 'page 개수', page_n)

    # 1 누르면 1~5
    # 2 누르면 6~10 ( , page*5)
    n = (page_number)*5 #데이터 개수인거지
    if n > page_n*5:
        print("n>page_n")
        context['posts'] = context['posts'][n-5:]
    else:
        context['posts'] = context['posts'][n-5:n] #인덱스 에러나기 쉽겠다

    print(context['page_n'], len(context['posts']))
    #return HttpResponse("i am sisi")
    return render(request, 'list.html',context)#, context)


def read_view(request, post_number):
    print(post_number)
# cities_ref = db.collection(u'cities')
# query = cities_ref.where(u'capital', u'==', True)
    post_iter = firestore.client().collection(u'posts').where(u'number',u'==',int(post_number)).get()#.to_dict()
    post = {}
    
    for p in post_iter:
        print("  read_view: ",p)
        post = p.to_dict()
    # post['contents'] = post['contents'].strip()
    context = {'post':post}
    print("  read_view: ",context)
    return render(request, "read.html", context)


def delete_view(request, post_number):

    post_iter = firestore.client().collection(u'posts').where(u'number',u'==',int(post_number)).get()#.delete()#.get()#.to_dict()
    for p in post_iter:
        p.reference.delete()

    return redirect('/')

def write_view(request, post_number=-1):

    context = {}
    if post_number != -1: #수정하는 로직
        print(post_number)
        post = firestore.client().collection(u'posts').where(u'number',u'==',int(post_number)).get()#.to_dict()
        post = list(post)[0].to_dict()
        context['post'] = post

    
    return render(request, 'write.html', context)



def save_view(request): #수정하면 포스트 넘버는 그대로, 날짜는 수정
    if request.method == 'POST':
        # print(request.POST.get("title",""))
        # print(request.POST.get("contents",""))
        
        # 데이터 가져오기
        title = request.POST.get("title","")
        contents = request.POST.get("contents","")
        # if '\n' in contents:
        #     print('save_view: 개행 처리합니다')
        #     contents = contents.replace('\r\n','<br />')
        # print(contents)
        # contents = contents.strip()
        now = timezone.localtime()

        #info = Info(0)
        #firestore.client().collection(u'info').document(u'posting_info').set(info.to_dict())
        if request.POST.get("post_number",""):
            post_number = request.POST.get("post_number","")
            # print('여기는 save_view', )
            # 갱신할 객체 생성
            post = Post(title=title, contents=contents, time=now, n=int(post_number))
            print(post_number, '수정:', post.to_dict())
            # 일치하는 데이터 가져온다
#데이터 get: index 문제나면 여기를 보자            
            post_past = firestore.client().collection(u'posts').where(u'number',u'==', int(post_number)).get()
            for p in post_past:
                #print(p.id, p.to_dict(), type(p))
                post_id = p.id
            print(post_id)
            # 갱신한다
            firestore.client().collection(u'posts').document(post_id).update(post.to_dict())
# city_ref = db.collection(u'cities').document(u'DC')
# city_ref.update({u'capital': True})
        else: # 새 글
        # 게시글 number 갱신
            transaction = firestore.client().transaction()
            info_ref = firestore.client().collection(u'info').document(u'posting_info')

            @firestore.transactional # 단순 1 증가하는 함수
            def update_in_transaction(transaction, info_ref):
                snapshot = info_ref.get(transaction=transaction)
                transaction.update(info_ref, {
                    u'number': snapshot.get(u'number') + 1
                })
                post_number = info_ref.get().to_dict().get('number')
        #doc = doc_ref.get()
        
        # 데이터 저장
                post = Post(title=title, contents=contents, time=now, n=post_number)
                firestore.client().collection(u'posts').add(post.to_dict())


            update_in_transaction(transaction, info_ref)


    return redirect('/')



