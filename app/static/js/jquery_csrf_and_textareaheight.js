// textarea height adjustment on keystroke and page load

$(function () {
    $("textarea").each(function () {
        this.style.height = (this.scrollHeight+10)+'px';
    });
});

function textAreaAdjust(element) {
    element.style.height = "auto";
    element.style.height = (10+element.scrollHeight)+"px";
};

// CSRF validation
var csrf_token = "{{ csrf_token() }}";

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        }
    }
});
