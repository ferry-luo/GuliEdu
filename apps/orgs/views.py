from django.shortcuts import render
from .models import OrgInfo, TeacherInfo, CityInfo
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from operations.models import UserLove
from django.db.models import Q


# Create your views here.

# 授课机构，列表页
def org_list(request):
    all_orgs = OrgInfo.objects.all()
    all_citys = CityInfo.objects.all()
    # 机构排名，取前3个
    sort_orgs = all_orgs.order_by('-love_num')[:3]

    # 全局搜索功能的过滤
    keyword = request.GET.get("keyword", "")
    if keyword:
        all_orgs = all_orgs.filter(Q(name__icontains=keyword) | Q(desc__icontains=keyword) | Q(
            detail__icontains=keyword))  # contains代表包含，icontains代表包含且不区分大小写

    # 按照机构类别进行过滤筛选
    cate = request.GET.get('cate', '')
    if cate:
        all_orgs = all_orgs.filter(category=cate)

    # 按照所在地区进行过滤筛选
    cityid = request.GET.get('cityid', '')
    if cityid:
        all_orgs = all_orgs.filter(cityinfo_id=int(cityid))  # 由于cityinfo表中字段id是数字类型，要对从前端获取到的cityid转为数字

    # 排序
    sort = request.GET.get('sort', '')
    if sort:
        all_orgs = all_orgs.order_by('-' + sort)  # 需求为降序，则按'-'+sort

    # 分页功能
    # 获取前端传来的页码
    pagenum = request.GET.get('pagenum', '')
    # 对all_orgs做分页，每页3条
    pa = Paginator(all_orgs, 3)  # 备注：Paginator.page_range：返回页码列表，从1开始，例如[1,2,3,4]
    try:
        pages = pa.page(
            pagenum)  # 备注：page.paginator：返回当前页对应的Paginator对象。page.number：返回当前页是第几页，从1开始。page.has_next()方法：如果有下一页返回True。page.has_previous()方法：如果有上一页返回True
    # 刚进入页面，会捕获PageNotAnInteger，强制拿第1页
    except PageNotAnInteger:
        pages = pa.page(1)
    # 当传入的页码超出页面总数，强制拿最后一页
    except EmptyPage:
        pages = pa.page(pa.num_pages)  # Paginator.num_pages：返回页面总数

    return render(request, 'orgs/org-list.html', {
        'all_orgs': all_orgs,
        'pages': pages,
        'all_citys': all_citys,
        'sort_orgs': sort_orgs,
        'cate': cate,  # 如果不返回cate，当进行翻页操作，则不是经过筛选机构后进行分页的数据
        'cityid': cityid,  # 如果不返回cityid，当进行翻页操作，则不是经过筛选城市后进行分页的数据
        'sort': sort,  # 如果不返回sort，当进行翻页操作，则不是经过筛选城市后进行分页的数据
        'keyword': keyword
    })


def org_detail(request, org_id):
    if org_id:
        org = OrgInfo.objects.filter(id=int(org_id))[0]

        org.click_num += 1
        org.save()

        # 在返回页面数据的时候，需要返回收藏这个机构的状态，根据状态让模板页面显示"收藏"还是"取消收藏"。而不能让页面固定显示"收藏"。
        lovestatus = False  # 没登录：lovestatus为False 登录了，但UserLove.objects.filter(love_man=request.user,love_id=int(org_id),love_type=1,love_status=True)无记录，lovestatus也是False
        if request.user.is_authenticated:
            love = UserLove.objects.filter(love_man=request.user, love_id=int(org_id), love_type=1, love_status=True)
            if love:
                lovestatus = True

        return render(request, 'orgs/org-detail-homepage.html', {
            'org': org,
            'detail_type': 'home',
            'lovestatus': lovestatus
        })


def org_detail_course(request, org_id):
    if org_id:
        org = OrgInfo.objects.filter(id=int(org_id))[0]
        all_courses = org.courseinfo_set.all()

        lovestatus = False
        if request.user.is_authenticated:
            love = UserLove.objects.filter(love_man=request.user, love_id=int(org_id), love_type=1, love_status=True)
            if love:
                lovestatus = True

        # 分页功能
        pagenum = request.GET.get('pagenum', '')
        pa = Paginator(all_courses, 2)
        try:
            pages = pa.page(pagenum)
        except PageNotAnInteger:
            pages = pa.page(1)
        except EmptyPage:
            pages = pa.page(pa.num_pages)
        return render(request, 'orgs/org-detail-course.html', {
            'org': org,
            'pages': pages,
            'detail_type': 'course',
            'lovestatus': lovestatus
        })


def org_detail_desc(request, org_id):
    if org_id:
        org = OrgInfo.objects.filter(id=int(org_id))[0]

        lovestatus = False
        if request.user.is_authenticated:
            love = UserLove.objects.filter(love_man=request.user, love_id=int(org_id), love_type=1, love_status=True)
            if love:
                lovestatus = True

        return render(request, 'orgs/org-detail-desc.html', {
            'org': org,
            'detail_type': 'desc',
            'lovestatus': lovestatus
        })


def org_detail_teacher(request, org_id):
    if org_id:
        org = OrgInfo.objects.filter(id=int(org_id))[0]
        all_teachers = org.teacherinfo_set.all()

        lovestatus = False
        if request.user.is_authenticated:
            love = UserLove.objects.filter(love_man=request.user, love_id=int(org_id), love_type=1, love_status=True)
            if love:
                lovestatus = True

        # 分页功能
        pagenum = request.GET.get('pagenum', '')
        pa = Paginator(all_teachers, 2)
        try:
            pages = pa.page(pagenum)
        except PageNotAnInteger:
            pages = pa.page(1)
        except EmptyPage:
            pages = pa.page(pa.num_pages)
        return render(request, 'orgs/org-detail-teachers.html', {
            'org': org,
            'pages': pages,
            'detail_type': 'teacher',
            'lovestatus': lovestatus
        })


def teacher_list(request):
    all_teachers = TeacherInfo.objects.all()
    sort_teachers = all_teachers.order_by('-love_num')[:3]

    # 全局搜索功能的过滤
    keyword = request.GET.get('keyword', '')
    if keyword:
        all_teachers = all_teachers.filter(name__icontains=keyword)

    sort = request.GET.get('sort', '')
    if sort:
        all_teachers = all_teachers.order_by('-' + sort)

    # 分页功能
    pagenum = request.GET.get('pagenum', '')
    pa = Paginator(all_teachers, 2)
    try:
        pages = pa.page(pagenum)
    except PageNotAnInteger:
        pages = pa.page(1)
    except EmptyPage:
        pages = pa.page(pa.num_pages)

    return render(request, 'orgs/teachers-list.html', {
        'all_teachers': all_teachers,
        'sort_teachers': sort_teachers,
        'pages': pages,
        'sort': sort,
        'keyword': keyword
    })


def teacher_detail(request, teacher_id):
    if teacher_id:
        teacher = TeacherInfo.objects.filter(id=int(teacher_id))[0]

        all_teachers = TeacherInfo.objects.all()
        sort_teachers = all_teachers.order_by('-love_num')[:3]

        teacher.click_num += 1
        teacher.save()

        loveteacher = False
        loveorg = False
        if request.user.is_authenticated:
            love = UserLove.objects.filter(love_id=int(teacher_id), love_type=3, love_status=True,
                                           love_man=request.user)
            if love:
                loveteacher = True

            love1 = UserLove.objects.filter(love_id=teacher.work_company.id, love_type=1, love_status=True,
                                            love_man=request.user)
            if love1:
                loveorg = True

        return render(request, 'orgs/teacher-detail.html', {
            'teacher': teacher,
            'sort_teachers': sort_teachers,
            'loveteacher': loveteacher,
            'loveorg': loveorg
        })
