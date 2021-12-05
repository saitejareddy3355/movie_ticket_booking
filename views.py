from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from .models import movie
from django.contrib import messages
from django.db import connection
from movie_ticket_booking.utils import getDropDown, dictfetchall
import datetime

# Create your views here.
def orderlisting(request):
    cursor = connection.cursor()
    if (request.session.get('user_level_id', None) == 1):
        SQL = "SELECT * FROM `order`,`users_user`,`order_status` WHERE order_status = os_id AND order_user_id = user_id"
    else:
        customerID = str(request.session.get('user_id', None))
        SQL = "SELECT * FROM `order`,`users_user`,`order_status` WHERE order_status = os_id AND order_user_id = user_id AND user_id = " + customerID
    cursor.execute(SQL)
    orderlist = dictfetchall(cursor)

    context = {
        "orderlist": orderlist
    }

    # Message according Movie #
    context['heading'] = "Ticket Reports";
    return render(request, 'order-listing.html', context)

# Create your views here.
def movielisting(request):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM movies_movie, language, type WHERE language_id = movie_language_id AND type_id = movie_type_id")
    movielist = dictfetchall(cursor)

    context = {
        "movielist": movielist
    }

    # Message according Movie #
    context['heading'] = "Movies Details";
    return render(request, 'movies-listing.html', context)

# Create your views here.
def payment(request):
    orderID = request.session.get('order_id', None);
    cursor = connection.cursor()
    cursor.execute("SELECT SUM(oi_total) as TotalCartValue FROM order_item WHERE oi_order_id = " + str(orderID))
    orderTotal = dictfetchall(cursor)
    context = {
        "orderTotal": orderTotal[0]
    }
    if (request.method == "POST"):
        request.session['order_id'] = "0"
        return redirect('order-items/'+str(orderID))
    # Message according Movie #
    context['heading'] = "Movies Details";
    return render(request, 'payment.html', context)

# Create your views here.
def cancel_order(request, orderID):
    cursor = connection.cursor()
    cursor.execute("""
                UPDATE `order`
                SET order_status= '5' WHERE order_id = %s
            """, (
        orderID
    ))
    messages.add_message(request, messages.INFO, "Your order has been cancelled successfully !!!")
    return redirect('orderlisting')

# Create your views here.
def order_items(request, orderID):
    cursor = connection.cursor()
    ### Get the Cart Details Listing  ####
    cursor.execute("SELECT *  FROM `movies_movie`, `order`, order_item, language, type WHERE movie_id =  oi_movie_id AND oi_order_id = order_id AND language_id = movie_language_id AND type_id = movie_type_id AND order_id = "+ str(orderID))
    movielist = dictfetchall(cursor)

     ### Get the Cart Details Listing  ####
    cursor.execute("SELECT *  FROM `order`, `users_user`,`order_status` WHERE order_status = os_id AND user_id =  order_user_id  AND order_id = "+ str(orderID))
    customerTicketDetails = dictfetchall(cursor)
    
    ### Get the Total Cart  ####
    cursor.execute("SELECT SUM(oi_total) as totalCartCost  FROM `movies_movie`, `order`, order_item, language, type WHERE movie_id =  oi_movie_id AND oi_order_id = order_id AND language_id = movie_language_id AND type_id = movie_type_id AND order_id = "+ str(orderID))
    totalCost = dictfetchall(cursor)
    
    context = {
        "movielist": movielist,
        "customerTicketDetails": customerTicketDetails[0],
        "totalCost":totalCost[0]
    }

    # Message according Movie #
    context['heading'] = "Movies Details";
    return render(request, 'order-items.html', context)

# Create your views here.
def order_edit(request, orderID):
    cursor = connection.cursor()
    ### Get the Cart Details Listing  ####
    cursor.execute("SELECT *  FROM `movies_movie`, `order`, order_item, language, type WHERE movie_id =  oi_movie_id AND oi_order_id = order_id AND language_id = movie_language_id AND type_id = movie_type_id AND order_id = "+ str(orderID))
    movielist = dictfetchall(cursor)

     ### Get the Cart Details Listing  ####
    cursor.execute("SELECT *  FROM `order`, `users_user`,`order_status` WHERE order_status = os_id AND user_id =  order_user_id  AND order_id = "+ str(orderID))
    customerTicketDetails = dictfetchall(cursor)
    customerTicketDetails = customerTicketDetails[0]
    
    ### Get the Total Cart  ####
    cursor.execute("SELECT SUM(oi_total) as totalCartCost  FROM `movies_movie`, `order`, order_item, language, type WHERE movie_id =  oi_movie_id AND oi_order_id = order_id AND language_id = movie_language_id AND type_id = movie_type_id AND order_id = "+ str(orderID))
    totalCost = dictfetchall(cursor)
    
    context = {
        "movielist": movielist,
        "protypelist":getDropDown('order_status', 'os_id', 'os_title', customerTicketDetails['order_status'], '1'),
        "customerTicketDetails": customerTicketDetails,
        "totalCost":totalCost[0]
    }
    if (request.method == "POST"):
        cursor = connection.cursor()
        cursor.execute("""
                    UPDATE `order`
                    SET order_status= %s WHERE order_id = %s
                """, (
            request.POST['order_status'],
            request.POST['order_id']
        ))
        messages.add_message(request, messages.INFO, "Your order has been cancelled successfully !!!")
        return redirect('orderlisting')
    # Message according Movie #
    context['heading'] = "Movies Details";
    return render(request, 'order-edit.html', context)

# Create your views here.
def cart_listing(request):
    orderID = request.session.get('order_id', None);
    cursor = connection.cursor()
    ### Get the Cart Details Listing  ####
    cursor.execute("SELECT *  FROM `movies_movie`, `order`, order_item, language, type WHERE movie_id =  oi_movie_id AND oi_order_id = order_id AND language_id = movie_language_id AND type_id = movie_type_id AND order_id = "+ str(orderID))
    movielist = dictfetchall(cursor)
    
    ### Get the Total Cart  ####
    cursor.execute("SELECT SUM(oi_total) as totalCartCost  FROM `movies_movie`, `order`, order_item, language, type WHERE movie_id =  oi_movie_id AND oi_order_id = order_id AND language_id = movie_language_id AND type_id = movie_type_id AND order_id = "+ str(orderID))
    totalCost = dictfetchall(cursor)
    
    context = {
        "movielist": movielist,
        "totalCost":totalCost[0]
    }

    # Message according Movie #
    context['heading'] = "Movies Details";
    return render(request, 'carts.html', context)

# Create your views here.
def movies(request):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM movies_movie, language, type WHERE language_id = movie_language_id AND type_id = movie_type_id")
    movielist = dictfetchall(cursor)

    context = {
        "movielist": movielist
    }

    # Message according Movie #
    context['heading'] = "Movies Details";
    return render(request, 'movies.html', context)

# Create your views here.
def movie_filter(request, typeID):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM movies_movie, language, type WHERE language_id = movie_language_id AND type_id = movie_type_id AND type_id = "+ str(typeID))
    movielist = dictfetchall(cursor)

    context = {
        "movielist": movielist
    }

    # Message according Movie #
    context['heading'] = "Movies Details";
    return render(request, 'movies.html', context)

def update(request, movieId):
    moviedetails = movie.objects.get(movie_id=movieId)
    context = {
        "fn": "add",
        "prolanguagelist":getDropDown('language', 'language_id', 'language_name', moviedetails.movie_language_id, '1'),
        "protypelist":getDropDown('type', 'type_id', 'type_name', moviedetails.movie_type_id, '1'),
        "moviedetails":moviedetails
    }
    if (request.method == "POST"):
        try:
            movie_image = None
            movie_image = moviedetails.movie_image
            if(request.FILES and request.FILES['movie_image']):
                movieImage = request.FILES['movie_image']
                fs = FileSystemStorage()
                filename = fs.save(movieImage.name, movieImage)
                movie_image = fs.url(movieImage)

            addMovie = movie(
            movie_id = movieId,
            movie_name = request.POST['movie_name'],
            movie_type_id = request.POST['movie_type_id'],
            movie_language_id = request.POST['movie_language_id'],
            movie_ticket_cost = request.POST['movie_ticket_cost'],
            movie_image = movie_image,                  
            movie_description = request.POST['movie_description'],
            movie_stock = request.POST['movie_stock'])
            addMovie.save()
        except Exception as e:
            return HttpResponse('Something went wrong. Error Message : '+ str(e))

        context["moviedetails"] = movie.objects.get(movie_id = movieId)
        messages.add_message(request, messages.INFO, "Movie updated succesfully !!!")
        return redirect('movielisting')

    else:
        return render(request,'movies-add.html', context)

def movie_details(request, movieId):
    if(request.session.get('authenticated', False) == False):
        messages.add_message(request, messages.ERROR, "Login to your account, to buy the movie !!!")
        return redirect('/users')
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM movies_movie, language, type WHERE language_id = movie_language_id AND type_id = movie_type_id AND movie_id = "+movieId)
    moviedetails = dictfetchall(cursor)

    context = {
        "fn": "add",
        "moviedetails":moviedetails[0]
    }
    if (request.method == "POST"):
        try:
            if(request.session.get('order_id', None) == "0" or request.session.get('order_id', False) == False):
                customerID = request.session.get('user_id', None)
                orderDate = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
                cursor = connection.cursor()
                cursor.execute("""
                INSERT INTO `order`
                SET order_user_id=%s, order_date=%s, order_status=%s, order_total=%s
                """, (
                    customerID,
                    orderDate,
                    1,
                    0))
                request.session['order_id'] = cursor.lastrowid    
            
            orderID = request.session.get('order_id', None);
            delete_movies(orderID)
            cursor = connection.cursor()
            totalAmount = int(request.POST['movie_ticket_cost']) * int(request.POST['movie_quantity']);
            cursor.execute("""
            INSERT INTO order_item
            SET oi_order_id=%s, oi_movie_id=%s, oi_price_per_unit=%s, oi_cart_quantity=%s, oi_total=%s
        """, (
            orderID,
            request.POST['movie_id'],
            request.POST['movie_ticket_cost'],
            request.POST['movie_quantity'],
            totalAmount))
        except Exception as e:
            return HttpResponse('Something went wrong. Error Message : '+ str(e))

        context["moviedetails"] = movie.objects.get(movie_id = movieId)
        messages.add_message(request, messages.INFO, "Movie updated succesfully !!!")
        return redirect('payment')
    else:
        return render(request,'movies-details.html', context)

def add(request):
    context = {
        "fn": "add",
        "prolanguagelist":getDropDown('language', 'language_id', 'language_name',0, '1'),
        "protypelist":getDropDown('type', 'type_id', 'type_name',0, '1'),
        "heading": 'Movie add'
    };
    if (request.method == "POST"):
        try:
            movie_image = None

            if(request.FILES and request.FILES['movie_image']):
                movieImage = request.FILES['movie_image']
                fs = FileSystemStorage()
                filename = fs.save(movieImage.name, movieImage)
                movie_image = fs.url(movieImage)

            addMovie = movie(movie_name = request.POST['movie_name'],
            movie_type_id = request.POST['movie_type_id'],
            movie_language_id = request.POST['movie_language_id'],
            movie_ticket_cost = request.POST['movie_ticket_cost'],
            movie_image = movie_image,                  
            movie_description = request.POST['movie_description'],
            movie_stock = request.POST['movie_stock'])
            addMovie.save()
        except Exception as e:
            return HttpResponse('Something went wrong. Error Message : '+ str(e))

        return redirect('movielisting')

    else:
        return render(request,'movies-add.html', context)

def delete_item(request, itemId):
    cursor = connection.cursor()
    sql = 'DELETE FROM order_item WHERE oi_order_id=' + itemId
    cursor.execute(sql)
    return redirect('cart_listing')

def delete_movies(orderId):
    cursor = connection.cursor()
    sql = 'DELETE FROM order_item WHERE oi_order_id=' + str(orderId)
    cursor.execute(sql)

def delete(request, prodId):
    try:
        deleteMovie = movie.objects.get(movie_id = prodId)
        deleteMovie.delete()
    except Exception as e:
        return HttpResponse('Something went wrong. Error Message : '+ str(e))
    messages.add_message(request, messages.INFO, "Movie Deleted Successfully !!!")
    return redirect('movielisting')

def stock(request):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM stock, movies_movie WHERE movie_id = stock_movie_id")
    stocklist = dictfetchall(cursor)

    context = {
        "stocklist": stocklist
    }

    # Message according Movie #
    context['heading'] = "Movies Stock Details";
    return render(request, 'stock.html', context)

def deletestock(request, id):
    cursor = connection.cursor()
    sql = 'DELETE FROM stock WHERE stock_id=' + id
    cursor.execute(sql)
    return redirect('stock')

def languagelisting(request):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM language")
    languagelist = dictfetchall(cursor)

    context = {
        "languagelist": languagelist
    }

    # Message according Movie #
    context['heading'] = "Movies Language";
    return render(request, 'viewlanguage.html', context)

def deletelanguage(request, id):
    cursor = connection.cursor()
    sql = 'DELETE FROM language WHERE language_id=' + id
    cursor.execute(sql)
    return redirect('language')

def addlanguage(request):
    context = {
        "fn": "add",
        "heading": 'Add Language'
    };
    if (request.method == "POST"):
        cursor = connection.cursor()
        cursor.execute("""
		   INSERT INTO language
		   SET language_name=%s
		""", (
            request.POST['language_name']))
        return redirect('languagelisting')
    return render(request, 'addlanguage.html', context)

def order(request):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM order_item")
    orderlist = dictfetchall(cursor)

    context = {
        "orderlist": orderlist
    }

    # Message according Tickets #
    context['heading'] = "Movies Ticket Details";
    return render(request, 'orders.html', context)
