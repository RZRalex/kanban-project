$(document).ready(function(){

    // profile page
    $('.editbox').click(function(){
        $('#editabout').show();
    });

    $('span.profile').click(function(){
        // $('#editabout').hide();
        // $('#editprof').hide();
        $(this).parent().parent().parent().hide();
    });
    // consider span to select parent up the tree to hide  DONE

    $('a.cancel').click(function(){
        $(this).parent().parent().parent().parent().hide();
    });

    $('.profbox').click(function(){
        $('#editprof').show();
    });

    $('.error').parent().addClass('error');

    $('.success').parent().addClass('success');

    $('.warning').parent().addClass('warning');

    // home page
    $('.addcol').click(function(){
        $('#coladd').show();
    });

    $('span').click(function(){
        $('#coladd').hide()
    });
    
    $('.add-btn').click(function(){
        $(this).parent().parent().parent().find('div.addcard').show()
    });

    $('.ellips-btn').click(function(){
        if($(this).parent().parent().find('h5.title').is(':hidden')){
            $(this).parent().parent().find('h5.title').show();
            $(this).parent().parent().find('form.colinput').hide();
        } else {
            $(this).parent().parent().find('h5.title').hide();
            $(this).parent().parent().find('form.colinput').show();
        }
    });

    $('.card-edit').click(function(){
        $(this).hide();
        $(this).parent().find('h5, p.content').hide();
        $(this).parent().find('form.card_form').show();
    });

    $('.cardno').click(function(){
        $(this).parent().hide();
        $(this).parent().parent().find('h5, p.content').show();
        $(this).parent().parent().find('.card-edit').show();
    });

    $('.colcancel').click(function(){
        $(this).parent().hide();
        $(this).parent().parent().find('h5.title').show();
    });

    $('.cardcancel').click(function(){
        $(this).parent().parent().hide();
    });

    $('.edit-btn').click(function(){
        $('#editproject').show();
    });

    $('.delbtn').click(function(){
        $(this).parent().parent().find('div.delprt').show();
        
    });

    $('.delcolbtn').click(function(){
        $(this).parent().parent().parent().find('div.delcol').show()
    });

    $('span.card').click(function(){
        $(this).parent().hide();
    });


    // Drag and Drop Functions

    var column = document.querySelectorAll('div.sortablecol');
    for (var i = 0; i < column.length; i++){
        const columns = column[i];
        $(columns).sortable({
            connectWith: 'div.sortablecol',
            receive: function(event,ui) {
                console.log("card has landed");
                var card_id = $(ui.item).attr('id');
                var col_id = $(columns).attr('id');
                console.log('card id:', card_id, 'column_id', col_id);
                $.ajax({
                    url: 'move_card',
                    type: 'POST',
                    data: {
                        'csrfmiddlewaretoken' : $('input[name=csrfmiddlewaretoken]').val(),
                        'cardid' : card_id,
                        'column' : col_id
                    }
                });
            }
        });
    };

    // $('div.sortablecol').disableSelection();

    // Select page
    $('.newboard').click(function(){
        $('#addboard').show()
    });

    $('.deletebrd').click(function(){
        if($(this).parent().find('div.delbrd').is(':hidden')){
            $(this).parent().find('div.delbrd').show()
        } else {
            $(this).parent().find('div.delbrd').hide()
        }
    });


    // Friend page

    $('.addy').click(function(){
        if($(this).parent().find('div.addfr').is(':hidden')){
            $(this).parent().find('div.addfr').show()
        } else {
            $(this).parent().find('div.addfr').hide()
        }
    });

});

