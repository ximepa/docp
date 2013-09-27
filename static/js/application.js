/**
 * Created with PyCharm.
 * User: maxim
 * Date: 10.06.13
 * Time: 14:16
 * To change this template use File | Settings | File Templates.
 */

$(document).ready(function() {
    var login = $("#id_login");

    if(!login.length) {
        // login field not present on page
        return false;
    }

    login.autocomplete({
        source: function(request, response){
            MainApi.find_login(request.term, function(data) {
                response(data);
            })
        },
        select: function( event, ui ) {
            login.trigger('change');
        }
    });

    login.on('change', function(e) {
        MainApi.find_pi(login.val(), function(result) {
            $('ul.errorlist', login.parent()).remove();
            login.closest('.grp-row').removeClass('grp-errors')
            if(result.success) {
                var options = $("#id_vyl").find('option:contains("'+result.address+'")');
                $.each(options, function(index, value) {
                    if($(this).html() == result.address) {
                        $(this).attr('selected','selected');
                    }
                });
                $("#id_kv").val(result.kv);
            } else {
                login.parent().append('<ul class="errorlist"><li>'+result.error+'</li></ul>')
                login.closest('.grp-row').addClass('grp-errors')
            }
        })
    })

});