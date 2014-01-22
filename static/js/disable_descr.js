(function($) {

    $(document).ready(function($) {
        $("#id_lock").change(function() {
            if ($(this).is(':checked')){
                $(".redactor_box").addClass("disable_descr")
                //$('.redactor_box').hide()
            }
            else {
                $(".redactor_box").removeClass("disable_descr")
                //$('.redactor_box').show()
            }
        });
        //alert($("#id_lock:checked").length)
//        if ( $("#id_lock").prop('checked') == true) {
//            alert($("#id_lock").prop('checked'))
//            $(".redactor_box").addClass("disable_descr")
//        } else {
//            $(".redactor_box").removeClass("disable_descr")
//        }


        function disable_descr(){
            if ( $("#id_lock").prop('checked') == true) {
                $(".redactor_box").addClass("disable_descr")
            } else {
                $(".redactor_box").removeClass("disable_descr")
            }
        }
        disable_descr();
        setInterval(disable_descr, 500);

//        function blink(e) {
//                    $(e).fadeOut(1500, function () {
//                        $(this).fadeIn(500, function () {
//                            blink(this);
//                        });
//                    });
//                }

//        function check_blink_%s() {
//            if (day >= day_from_%s & my_time >= time_from_%s & my_time <= time_to_%s) {
//                blink(".blink_%s");
//            }
//        }

//        setInterval('check_blink_%s()', 1000);
    });
})(django.jQuery);