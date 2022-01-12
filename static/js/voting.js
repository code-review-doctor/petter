$(document).ready(
    function () {
        $('.vote-action').click(function (e) {
            e.preventDefault();
            let deal_id = document.getElementById('deal_id').getAttribute('data-value');
            let button = $(this).attr("value");

            $.ajax({
                type: 'POST',
                url: '{% url "deals:vote" %}',
                data: {
                    deal_id: deal_id,
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                    action: 'votes',
                    button: button,
                },
                success: function (json) {
                    if (json.length < 1 || json == undefined) {
                    }
                    $('.toast').toast('show');
                    document.getElementById("vote_down").classList.add("disabled")
                    document.getElementById("vote_up").classList.add("disabled")
                    document.getElementById("voting-counter").innerHTML = json['total']
                    document.getElementById("deal_id").dataset.toggle = 'tooltip'
                    document.getElementById("deal_id").title = 'Możesz oddać tylko jeden głos!'
                },
                error: function (xhr, errmsg, err) {
                }
            });
        });
    },
);
