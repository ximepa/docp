"use strict";

function setCookie(c_name,value,exdays) {
    var exdate=new Date();
    exdate.setDate(exdate.getDate() + exdays);
    var c_value=escape(value) + ((exdays==null) ? "" : "; expires="+exdate.toUTCString());
    document.cookie=c_name + "=" + c_value;
}

function getCookie(c_name) {
    var i,x,y,ARRcookies=document.cookie.split(";");
    for (i=0;i<ARRcookies.length;i++) {
        x=ARRcookies[i].substr(0,ARRcookies[i].indexOf("="));
        y=ARRcookies[i].substr(ARRcookies[i].indexOf("=")+1);
        x=x.replace(/^\s+|\s+$/g,"");
        if (x==c_name) {
            return unescape(y);
        }
    }
}

$(document).ready(function($) {

    $(function() {
        $(".preload").fadeOut(2000, function() {

        });
    });

    var hidden = false
    var c = getCookie('filter_hidden')
    console.log(c)
    if(c) {
        if(c == "true") {
            hidden = true;
            $('label.tree-toggler').parent().children('ul.tree').hide()
        }
    }

    $('label.tree-toggler').click(function () {
        hidden = !hidden

        setCookie('filter_hidden',hidden,365);
        var c = getCookie('filter_hidden')
        console.log(c)
        $(this).parent().children('ul.tree').toggle(300);
    });
});