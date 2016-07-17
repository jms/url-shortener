/**
 * Created by jms on 07-16-16.
 */
$(function () {
    var processURL = function () {
        var long_url = $('.ui.form').form('get value', 'long_url');
        console.info('validation passed, %s', long_url);

        $.ajax({
            url: '/process_url',
            method: 'POST',
            contentType: "application/json; charset=utf-8",
            dataType: 'json',
            data: JSON.stringify({
                long_url: long_url
            }),
            success: function (data) {
                console.info(data);
                var site_url = window.top.location.href;
                $('#short_url').html(site_url + data.code);
                $('#msg').removeClass('hidden');
            },
            error: function () {
                console.error(this.props.url, status, err.toString());
            }
        });

    };

    var focusFirstInvalidField = function () {
        $('.ui.form').find('div.field.error').first().find('input').focus();
    };

    $('.ui.form').form({
            on: 'blur',
            fields: {
                long_url: {
                    identifier: 'long_url',
                    rules: [
                        {
                            type: 'empty',
                            prompt: 'url cannot be empty'
                        },
                        {
                            type: 'url',
                            prompt: 'you must enter a valid url '
                        }
                    ]
                }
            },
            onSuccess: processURL,
            onFailure: focusFirstInvalidField
        }
    );

    $('div.ui.clear').on('click', function () {
        $('#msg').addClass('hidden');
        $('form').form('clear')
    });
});
