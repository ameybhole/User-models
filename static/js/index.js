

var first_chat = true;
$(document).ready(function() {

    var socket = io.connect('http://' + document.domain + ':' + location.port);

    socket.on( 'connect', function() {
        socket.emit( 'my event', {
          data: 'User Connected'
        } );
        //var form = $( '#chatform' ).on( 'submit', function( e ) {
        $('#btn-chat').click(function(e) {
                console.log('submit button clicked');
                e.preventDefault();
                var message = $('#message').val();
                var userId =  $('#user-id').val();
                var sent = "<div class=\"row msg_container base_sent\"><div class=\"col-md-10 col-xs-10\"><div class=\"messages msg_sent\"><p>"+message+"</p> </div></div> </div>"
                $('#chat-container').append(sent);
                document.getElementById('chat-container').scrollTop = 9999999;

                console.log("user id " + userId);
                console.log(" sending message " + message);

                socket.emit( 'my event', {
                    user_id : userId,
                    message : message
                } );
                $('#message').val('').focus();
            } );
    });


      socket.on( 'my response', function( msg ) {
        console.log( msg.response );
        console.log( msg.products );
        if(msg.response) {
            var response = msg.response;
            var received = "<div class=\"row msg_container base_receive\"> <div class=\"col-md-10 col-xs-10\"> <div class=\"messages msg_receive\"> <p>" + response + "</p> </div> </div> </div>";
            $('#chat-container').append(received);
            //var height = parseInt($('#chat-container').height());
            //console.log('height is '+height);
            document.getElementById('chat-container').scrollTop = 9999999;
            //$("#dhat-container").animate({ scrollTop: height}, 500);

            var products = msg.products;
            $('#products-container').empty();
            console.log(products);

            $.each(products, function( index, product ) {
                console.log(product);
                var item = '<div class="col-lg-4 col-md-6 mb-4"> <div class="card h-100"> <div class="image-container">'+
              '<a href="#"><img class="card-img-top" src="'+product['image']+'" alt=""></a>'+
              '</div><div class="card-body"> <h4 class="card-title">'+
              '<a href="#">'+product['title']+'</a> </h4>'+
              '<h5>'+product['price']+'</h5>'+
              '<p class="card-text">' + product['description']+'</p>'+
              '</div> <div class="card-footer"> <small class="text-muted">&#9733; &#9733; &#9733; &#9733; &#9734;</small> </div> </div> </div>';
                $('#products-container').append(item);
            });
        }

      });


    $('#togglechat-btn').click(function() {
        btnText  = $(this).text() == 'Chat' ? 'Close': 'Chat' ;
        $(this).text(btnText);
        console.log(btnText);

        $('#myForm').toggleClass('show-form');
        console.log('has class '+$('#myForm').hasClass('show-form'))
        if( $('#myForm').hasClass('show-form') && first_chat){
            var received = "<div class=\"row msg_container base_receive\"> <div class=\"col-md-10 col-xs-10\"> <div class=\"messages msg_receive\"> <p>Hello what products are you looking for?</p> </div> </div> </div>";
            $('#chat-container').append(received);
            first_chat = false;
        }


    });

});