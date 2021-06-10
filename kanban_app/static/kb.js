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

    $('.cardcancel').click(function(){
        $(this).parent().parent().hide()
    });

    // Select page
    $('.newboard').click(function(){
        $('#addboard').show()
    });
});

