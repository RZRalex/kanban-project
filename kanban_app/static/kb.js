$(document).ready(function(){

    // profile page
    $('.editbox').click(function(){
        $('#editabout').show();
    });

    $('span',).click(function(){
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
        $(this).parent().parent().hide()
    });

    $('.edit-btn').click(function(){
        $('#editproject').show()
    });

    // Select page
    $('.newboard').click(function(){
        $('#addboard').show()
    });
});

