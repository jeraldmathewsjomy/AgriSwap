
document.addEventListener("DOMContentLoaded", () => {
    const msg = "{{ msg }}";
    if (msg) {
        alert(msg);
        window.location = "{% url 'Guest:login' %}";
    }
});

$(document).ready(() => {
    $("#sel_district").change(function () {
        var did = $(this).val();
        var ur = "{% url 'Guest:ajaxplace' %}";
        $.ajax({
            url: ur,
            data: { did: did },
            success: function (data) {
                $("#sel_place").html(data);
            },
        });
    });
});