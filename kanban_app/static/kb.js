$(document).ready(function(){

    // profile page
    $('.editbox').click(function(){
        $('#editabout').show();
    });

    $('span',).click(function(){
        $('#editabout').hide();
        $('#editprof').hide();
    });
    // consider span to select parent up the tree to hide

    $('a.cancel').click(function(){
        $('#editabout').hide();
        $('#editprof').hide();
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
    
});

