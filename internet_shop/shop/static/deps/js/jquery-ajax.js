$j(document).ready(function () {
    var successMessage = $j("#jq-notification");
    var csrfToken = $j('meta[name="csrf-token"]').attr('content');

    // Функция для обновления корзины
    function updateCart(data) {
        if (data.total_quantity !== undefined) {
            // Обновление общего количества товаров
            $j("#tovar-in-cart-count").text(data.total_quantity);
            $j("#total-items-count").text(data.total_quantity);
        }
        if (data.cart_items_html) {
            // Обновление содержимого корзины
            $j("#cart-items-container").html(data.cart_items_html);
        }
        if (data.total_price !== undefined) {
            // Обновление итоговой суммы
            $j("#total-price").text(data.total_price + " $");
        }
    }

    // Добавление товара в корзину
    $j(document).on("click", ".add-to-cart", function (e) {
        e.preventDefault();

        var product_id = $j(this).data("product-id");
        var add_to_cart_url = $j(this).attr("href");

        $j.ajax({
            type: "POST",
            url: add_to_cart_url,
            data: {
                product_id: product_id,
                csrfmiddlewaretoken: csrfToken, 
            },
            success: function (data) {
                if (data.message) {
                    successMessage.html(data.message).fadeIn(400).delay(300).fadeOut(400);
                }
                // Обновление корзины
                updateCart(data);
            },
            error: function (xhr, status, error) {
                console.error("Ошибка при добавлении товара в корзину: ", error);
            },
        });
    });

    $j(document).on("click", ".increment, .decrement", function (e) {
        e.preventDefault();

        var cart_id = $j(this).data("cart-id");
        var change_type = $j(this).hasClass("increment") ? 1 : -1;
        var quantity_input = $j(this).closest(".input-group").find(".number");
        var current_quantity = parseInt(quantity_input.val());

        var new_quantity = current_quantity + change_type;
        if (new_quantity <= 0) return;

        $j.ajax({
            type: "POST",
            url: $j(this).data("cart-change-url"),
            data: {
                cart_id: cart_id,
                quantity: new_quantity,
                csrfmiddlewaretoken: csrfToken,
            },
            success: function (data) {
                if (data.message) {
                    successMessage.html(data.message).fadeIn(400).delay(300).fadeOut(400);
                }
                updateCart(data);
            },
            error: function (xhr, status, error) {
                console.log("Ошибка при изменении количества товара: ", error);
            },
        });
    });




    
    // Удаление товара из корзины
    $j(document).on("click", ".remove-from-cart", function (e) {
        e.preventDefault();

        var cart_id = $j(this).data("cart-id");

        $j.ajax({
            type: "POST",
            url: $j(this).attr("href"),
            data: {
                cart_id: cart_id,
                csrfmiddlewaretoken: csrfToken, 
            },
            success: function (data) {
                if (data.message) {
                    successMessage.html(data.message).fadeIn(400).delay(300).fadeOut(400);
                }
                updateCart(data);
            },
            error: function (xhr, status, error) {
                console.log("Ошибка при удалении товара из корзины: ", error);
            },
        });
    });
});




    // Теперь + - количества товара 
    // Обработчик события для уменьшения значения
    $(document).on("click", ".decrement", function () {
        // Берем ссылку на контроллер django из атрибута data-cart-change-url
        var url = $(this).data("cart-change-url");
        // Берем id корзины из атрибута data-cart-id
        var cartID = $(this).data("cart-id");
        // Ищем ближайшеий input с количеством 
        var $input = $(this).closest('.input-group').find('.number');
        // Берем значение количества товара
        var currentValue = parseInt($input.val());
        // Если количества больше одного, то только тогда делаем -1
        if (currentValue > 1) {
            $input.val(currentValue - 1);
            // Запускаем функцию определенную ниже
            // с аргументами (id карты, новое количество, количество уменьшилось или прибавилось, url)
            updateCart(cartID, currentValue - 1, -1, url);
        }
    });

    // Обработчик события для увеличения значения
    $(document).on("click", ".increment", function () {
        // Берем ссылку на контроллер django из атрибута data-cart-change-url
        var url = $(this).data("cart-change-url");
        // Берем id корзины из атрибута data-cart-id
        var cartID = $(this).data("cart-id");
        // Ищем ближайшеий input с количеством 
        var $input = $(this).closest('.input-group').find('.number');
        // Берем значение количества товара
        var currentValue = parseInt($input.val());

        $input.val(currentValue + 1);

        // Запускаем функцию определенную ниже
        // с аргументами (id карты, новое количество, количество уменьшилось или прибавилось, url)
        updateCart(cartID, currentValue + 1, 1, url);
    });

    function updateCart(cartID, quantity, change, url) {
        $.ajax({
            type: "POST",
            url: url,
            data: {
                cart_id: cartID,
                quantity: quantity,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
 
            success: function (data) {
                 // Сообщение
                successMessage.html(data.message);
                successMessage.fadeIn(400);
                 // Через 7сек убираем сообщение
                setTimeout(function () {
                     successMessage.fadeOut(400);
                }, 7000);
 
                // Изменяем количество товаров в корзине
                var goodsInCartCount = $("#goods-in-cart-count");
                var cartCount = parseInt(goodsInCartCount.text() || 0);
                cartCount += change;
                goodsInCartCount.text(cartCount);

                // Меняем содержимое корзины
                var cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html);

            },
            error: function (data) {
                console.log("Ошибка при добавлении товара в корзину");
            },
        });
    }