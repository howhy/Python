#!/usr/bin/env python
#-*-coding:utf-8-*-
from django.core.urlresolvers import  resolve
from django.shortcuts import render
import models

def perm_check(*args,**kwargs):
    request=args[0]
    perm_list = models.CmdbPermission.objects.all()
    current_url_name=resolve(request.path_info).url_name
    print('curulr-----%s'%current_url_name)
    matched_flag=False
    matched_perm_key=None
    if current_url_name is not None:
        for perm in perm_list:
            print('%s---url--%s'%(perm.url,current_url_name))
            if perm.url==current_url_name:
                print('%s--method---%s' % ( request.method,perm.request_method))
                if request.method==perm.request_method:
                    if not perm.request_args:
                        matched_flag=True
                        matched_perm_key=perm.id
                        break
                    else:
                        print('args-----%s'%perm.request_args)
                        request_method_func=getattr(request,perm.request_method)
                        print('argsvalue=--=--%s'%request_method_func.get(perm.request_args))
                        if request_method_func.get(perm.request_args) is not None :
                            if  perm.request_args_value:
                                if request_method_func.get(perm.request_args)==perm.request_args_value:
                                    matched_flag=True
                                else:
                                    continue
                            else:
                                matched_flag=True
                        else:
                            matched_flag=False
                            break
                else:
                    continue
            else:
                continue
            if matched_flag:
                matched_perm_key=perm.id
                break
    else:
        return True
    print('--------%s'%matched_flag,)
    if matched_flag:
        user_prem=models.UserPermission.objects.filter(user=request.user)
        for userperm in user_prem:
            print('%s-----------%s'%(userperm.cmdbpermission_id,matched_perm_key))
            if userperm.cmdbpermission_id==matched_perm_key:
                return True
            else:
                continue
        else:
            return False

def check_permission(viewsfunc):
    def wrapper(*args,**kwargs):
        if args[0].user.is_superuser or perm_check(*args,**kwargs):
            return viewsfunc(*args, **kwargs)
        #if not perm_check(*args,**kwargs):
        else:
            return render(args[0],'404.html')
    return wrapper
def check_has_perm(request,perm_id):
    request_user_perm = models.UserPermission.objects.filter(user=request.user)
    user_perm_list=[]
    for perm in request_user_perm:
        user_perm_list.append(perm.cmdbpermission_id)
    if perm_id in user_perm_list or request.user.is_superuser:
        return True
    else:
        return False
