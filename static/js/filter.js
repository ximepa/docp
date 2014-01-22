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


(function($) {

    $(document).ready(function($) {
        $('#site-name').text("Заявки ");
            $('title').text("Заявки")
        $('head').append('<link rel="icon" href="/static/img/favicon.ico" type="image/x-icon" /> ')
            var hidden = false
            var c = getCookie('filter_hidden')
            if(c) {
                if(c == "true") {
                    hidden = true;
                    $('#changelist-filter > h3').hide();
                    $('#changelist-filter > ul').hide();
                    $('#changelist-filter > form').hide();
                    //$('#show-filters').show();
                    $('#changelist').removeClass('filtered');
                }
            }
            $("tr input.action-select").actions();
            //$('<div id="show-filters" style="float: right;"><a href="#">Показати фільтер</a></p>').prependTo('div.actions');
            $('#show-filters').hide();
            $('#changelist-filter h2').html('<a style="color: white;" id="hide-filters" href="#">Фільтр &rarr;</a>');

            //$('#show-filters').click(function() {
            //   $('#changelist-filter').show('fast');
            //    $('#changelist').addClass('filtered');
            //    $('#show-filters').hide();
            //});

            $('#hide-filters').click( function() {
                hidden = !hidden
                setCookie('filter_hidden',hidden,365);
                $('#changelist-filter > h3').toggle('fast');
                $('#changelist-filter > ul').toggle('fast');
                $('#changelist-filter > form').toggle('fast');
                //$('#show-filters').show();
                $('#changelist').toggleClass('filtered');
            });
        // disable some field if disclaimer
        $("#id_disclaimer").change(function() {
            if ($(this).is(':checked')){
                $("#id_status").attr("disabled","disabled")
                $("#id_who_do").attr("disabled","disabled")
                $("#id_what_do").attr("disabled","disabled")
            }
            else {
                $("#id_status").removeAttr("disabled","disabled")
                $("#id_who_do").removeAttr("disabled","disabled")
                $("#id_what_do").removeAttr("disabled","disabled")
            }
        });

        if ( $("#id_disclaimer:checked").length ) {
            $("#id_status").attr("disabled","disabled")
            $("#id_who_do").attr("disabled","disabled")
            $("#id_what_do").attr("disabled","disabled")
        } else {
            $("#id_status").removeAttr("disabled","disabled")
            $("#id_who_do").removeAttr("disabled","disabled")
            $("#id_what_do").removeAttr("disabled","disabled")
        }

        // disable disclaimer if claim status = True
        $('.field-what_do').hide()
        $("#id_status").change(function() {
            if ($(this).is(':checked')){
                $("#id_disclaimer").attr("disabled","disabled")
                $('.field-what_do').show()
                $("#id_what_do").focus()

            }
            else {
                $("#id_disclaimer").removeAttr("disabled","disabled")
                $('.field-what_do').hide()
            }
        });

        $("#id_status").click(function(e) {
            window.location.hash = '#id_planning_time_to';
        });
        if ( $("#id_status:checked").length ) {
            $("#id_disclaimer").attr("disabled","disabled")
            $('.field-what_do').show()
        } else {
            $("#id_disclaimer").removeAttr("disabled","disabled")
            $('.field-what_do').hide()
        }

        //$('#info').popover('toggle')
        //$('#info').popover('hide')

        //($('td div.popover'))
        $('.btn.btn-search-options').hide()

    });
})(django.jQuery);
