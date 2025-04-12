from django.shortcuts import render

# Create your views here.

def sum(request):
    if request.method=="POST":
        number1=int(request.POST.get("txt_number1"))
        number2=int(request.POST.get("txt_number2"))
        number3=int(request.POST.get("txt_number3"))
        
        result=number1+number2+number3
        return render(request,"Basic/Sum.html",{"sum":result})
    else:
        return render(request,'Basic/Sum.html')

def large(request):
    if request.method=="POST":
        num1=int(request.POST.get("number1"))
        num2=int(request.POST.get("number2"))
        num3=int(request.POST.get("number3"))

        if num1>num2 and num1>num3:
            largest=num1
        elif num2>num1 and num2>num3:
            largest=num2
        elif num3>num1 and num3>num2:
            largest=num3

        if num1<num2 and num1<num3:
            smallest=num1
        elif num2<num1 and num2<num3:
            smallest=num2
        elif num3<num1 and num3<num2:
            smallest=num3

        return render(request,"Basic/largest.html",{"larg":largest,"small":smallest})
    
    else:
        return render(request,'Basic/largest.html')

        