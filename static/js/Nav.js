/*===================================

    scrollTop  menu effects

  ===================================*/

 $(window).scroll(function () {
        if ($(window).scrollTop() > 100) {
            $(".menubar").addClass('meffect');
        } else {
            $(".menubar").removeClass('meffect');
        }
    });


function openNav2() {
    document.getElementById("rightside").style.width = "450px";
    document.body.style.backgroundColor = "rgba(168,232,226, 0.7)";
}
function closeNav2() {
    document.getElementById("rightside").style.width = "0";
    document.body.style.backgroundColor = "white";
}



/*===================================

    megadropdown menu

  ===================================*/
$(function(){
    $('.dropdown').hover(function() {
        $(this).addClass('open');
    },
    function() {
        $(this).removeClass('open');
    });
});
