from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage
from tovari.models import Products, Categories
from tovari.utils import q_search
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter
import os
from django.conf import settings
from PIL import Image
from reportlab.lib.utils import ImageReader

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from tovari.serializers import ProductSerializer


def split_text(text, words_per_line=6):
    """Разделить текст на строки с заданным количеством слов."""
    words = text.split()
    lines = []
    for i in range(0, len(words), words_per_line):
        lines.append(" ".join(words[i:i + words_per_line]))
    return lines


def generate_pdf(request, product_slug):
    font_path = os.path.join(settings.BASE_DIR, 'shop/static/deps/fonts/DejaVuSans.ttf')
    pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))

    product = get_object_or_404(Products, slug=product_slug)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{product.name}.pdf"'

    p = canvas.Canvas(response, pagesize=letter)

    p.setFont("DejaVuSans", 12)
    p.setFont("DejaVuSans", 16)
    p.drawString(100, 800, f"Информация о товаре: {product.name}")

    y = 750
    p.setFont("DejaVuSans", 12)
    p.drawString(50, y, f"ID: {product.id}")
    y -= 20
    p.drawString(50, y, f"Название: {product.name}")
    y -= 20
    p.drawString(50, y, f"Цена: {product.sell_price()} $")
    y -= 20
    p.drawString(50, y, f"Количество: {product.quantity}")
    y -= 20

    if product.discription:
        p.drawString(50, y, "Описание:")
        y -= 20
        description_lines = split_text(product.discription, words_per_line=6)
        for line in description_lines:
            p.drawString(50, y, line)
            y -= 20

    if product.image:
        try:
            image_path = product.image.path
            img = Image.open(image_path)
            img = img.resize((200, 200))
            image_reader = ImageReader(img)

            p.drawImage(image_reader, 50, y - 200, width=200, height=200)
        except Exception as e:
            p.drawString(50, y, f"Ошибка при загрузке изображения: {e}")

    p.save()
    return response


def catalog(request, category_slug=None):
    page = request.GET.get('page', 1)
    on_sale = request.GET.get('on_sale', None)
    order_by = request.GET.get('order_by', None)
    query = request.GET.get('q', None)

    if query:
        tovari = q_search(query)
        if not tovari.exists():
            context = {
                'title': 'Результаты не найдены',
                'tovari': [],
                'query': query,
                'slug_url': category_slug,
            }
            return render(request, 'tovari/catalog.html', context)

    elif category_slug:
        if category_slug == 'vse-tovary':
            tovari = Products.objects.all()
        else:
            category = get_object_or_404(Categories, slug=category_slug)
            tovari = Products.objects.filter(category=category)
            if not tovari.exists():
                context = {
                    'title': f'Категория {category.name} пуста',
                    'tovari': [],
                    'slug_url': category_slug,
                }
                return render(request, 'tovari/catalog.html', context)
    else:
        tovari = Products.objects.all()

    if on_sale == 'on':
        tovari = tovari.filter(discount__gt=0, discount__lte=100)

    if order_by and order_by != "default":
        tovari = tovari.order_by(order_by)

    paginator = Paginator(tovari, 3)
    try:
        current_page = paginator.page(int(page))
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)

    context = {
        'title': f'Madi - {category_slug.capitalize() if category_slug else "Каталог"}',
        'tovari': current_page,
        'slug_url': category_slug,
        'query': query,
    }
    return render(request, 'tovari/catalog.html', context)


def product(request, product_slug):
    product = get_object_or_404(Products, slug=product_slug)

    context = {
        'product': product,
    }
    return render(request, 'tovari/product.html', context=context)

class ProductListAPIView(APIView):
    def get(self, request):
        """Получение списка всех товаров"""
        products = Products.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Добавление нового товара"""
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailAPIView(APIView):
    def get(self, request, pk):
        """Получение деталей конкретного товара"""
        product = get_object_or_404(Products, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk):
        """Обновление товара"""
        product = get_object_or_404(Products, pk=pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Удаление товара"""
        product = get_object_or_404(Products, pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
