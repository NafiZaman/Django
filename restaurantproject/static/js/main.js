function viewProduct(productId) {
    // console.log("Viewing", productId);

    $.ajax({
        url: '/product/get_product/',
        type: "GET",
        data: {
            'product_id': productId,
        },
        dataType: 'json',

        success: function (context) {
            if (context['error']) window.location = "/";
            else {
                window.location = "/product/view_product/" + context['product_id'];
            }
        }
    });
}

function addToCart(product_id) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let quantity = "1";

    try {
        quantity = document.getElementById('qauntity').value;
    }
    catch (error) {
        quantity = "1";
    }

    console.log("This is quantity:", quantity);
    console.log("Product id", product_id);

    $.ajax({
        url: '/order/add_to_cart/',
        type: "POST",
        data: {
            'csrfmiddlewaretoken': csrftoken,
            'product_id': product_id,
            'quantity': quantity,
        },
        dataType: 'json',
        success: function (context) {
            if (context['login_required']) window.location = '/users/login/';
            else if (context['not_allowed']) alert("Not allowed");
            else if (context['server_error']) window.location = '/';
            else if (context['not_in_stock']) {
                $("#exampleModal .modal-body").text('Sorry! We have either run out of stock, or the quantity you provided exceeds the quantity in stock.');
                $('#exampleModal').modal('show');
            }
            else {
                cartCount = document.getElementById('lblCartCount');
                cartCount.innerHTML = context['cart_count'];
                $("#exampleModal .modal-body").text('Woohooo! Item added to cart. To view, update or remove the item, click on the cart icon.');
                $('#exampleModal').modal('show');
            }
        }
    });
}

function updateCart(itemId, orderId) {

    try {
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        quantity = document.getElementById('quantity' + itemId).value;

        $.ajax({
            url: "/order/update_cart/",
            type: "POST",
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'order_id': orderId,
                'item_id': itemId,
                'quantity': quantity,
            },
            dataType: 'json',
            success: function (context) {
                if (context['login_required']) window.location = '/users/login/';
                else if (context['not_allowed']) alert("Not allowed");
                else if (context['server_error']) window.location = '/';
                else {
                    document.getElementById('totalPrice' + itemId).innerHTML = context['new_total_price']
                    document.getElementById('totalCost').innerHTML = context['total_cost']
                }
            }
        });
    }
    catch (error) {
        alert("An error occured!");
    }
}

function addSentiment(review_id, sentiment) {
    let btn;

    if (sentiment == 'like')
        btn = document.getElementById('likeBtn' + review_id);
    else if (sentiment == 'dislike')
        btn = document.getElementById('dislikeBtn' + review_id);

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    console.log(review_id, sentiment);

    $.ajax({
        url: '/product/rate_review/',
        type: "POST",
        data: {
            'csrfmiddlewaretoken': csrftoken,
            'review_id': review_id,
            'sentiment': sentiment,
        },
        dataType: 'json',
        success: function (context) {
            if (context['login_required']) window.location = "/users/login/";
            else if (context['server_error']) window.location = "/"
            else if (context['not_allowed']) alert("Not allowed");
            else {
                likeBtn = document.getElementById('likeBtn' + review_id);
                dislikeBtn = document.getElementById('dislikeBtn' + review_id);

                if (context['action'] == 'like') {
                    likeBtn.innerHTML = '<small style="color:black;">' + context['like_count'] + '</small><i class="bi bi-hand-thumbs-up-fill"></i>'
                    dislikeBtn.innerHTML = '<small style="color:black;">' + context['dislike_count'] + '</small><i class="bi bi-hand-thumbs-down"></i>'
                }
                else if (context['action'] == 'unlike') {
                    likeBtn.innerHTML = '<small style="color:black;">' + context['like_count'] + '</small><i class="bi bi-hand-thumbs-up"></i>'
                    dislikeBtn.innerHTML = '<small style="color:black;">' + context['dislike_count'] + '</small><i class="bi bi-hand-thumbs-down"></i>'
                }

                if (context['action'] == 'dislike') {
                    dislikeBtn.innerHTML = '<small style="color:black;">' + context['dislike_count'] + '</small><i class="bi bi-hand-thumbs-down-fill"></i>'
                    likeBtn.innerHTML = '<small style="color:black;">' + context['like_count'] + '</small><i class="bi bi-hand-thumbs-up"></i>'
                }
                else if (context['action'] == 'undislike') {
                    dislikeBtn.innerHTML = '<small style="color:black;">' + context['dislike_count'] + '</small><i class="bi bi-hand-thumbs-down"></i>'
                    likeBtn.innerHTML = '<small style="color:black;">' + context['like_count'] + '</small><i class="bi bi-hand-thumbs-up"></i>'
                }
            }
        }
    });
}

try {
    const pn = document.getElementById('id_phone_number');
    const div = pn.parentNode;

    div.className = "input-group"
    const span = document.createElement('span');
    span.className = 'input-group-text'
    span.id = 'basic-addon1'
    span.innerHTML = "+880"
    div.prepend(span);
    console.log(div);

}
catch (error) {
    console.error(error)
}

// function likePost(post_id) {
//     const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

//     $.ajax({
//         url: "/user_profile/like_post",
//         type: "POST",
//         data: {
//             'csrfmiddlewaretoken': csrftoken,
//             'post_id': post_id,
//         },
//         dataType: 'json',
//         success: function (context) {
//             if (context['not_friends']) alert("Only friends can like or comment on posts");
//             else {
//                 likeBtn = document.getElementById('likeBtn' + context['post_id']);
//                 likeBtn.innerHTML = context['like_btn_text'];
//             }
//         }
//     });
// }