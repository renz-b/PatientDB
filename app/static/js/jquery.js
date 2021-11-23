$(document).ready(function() {
    var csrf_token = $("input[name='csrf_token']").val()
    $("#general_data_form").on('submit', function(e) {

        let first_name = $("#first_name").val();
        let last_name = $("#last_name").val();
        let middle_name = $("#middle_name").val();
        let name_suffix = $("#name_suffix").val();
        let gender = $("#gender").val();
        let birthday = $("#birthday").val();

        req = $.ajax({
            url : "/similar_patient",
            type : "POST",
            data : { first_name : first_name, last_name : last_name, middle_name : middle_name, 
                name_suffix : name_suffix, gender : gender, birthday : birthday, csrf_token : csrf_token }
        });
        
        req.done(function(data) {
            if (data.html) {
                $("#messages_from_ajax").slideUp('slow', function() {
                    $("#messages_from_ajax").html(data.message);
                }).slideDown(400);
                //$("#messages_from_ajax").html(data.message).fadeIn(600);
                $("#general_data_submit").animate({opacity: 0}, 400);
                $("#table_similar_patients").slideUp('slow', function() {
                    $("#table_similar_patients").html(data.html);
                }).slideDown(400);
            } else {
 
            $("#table_similar_patients").slideUp('slow', function() {
                $("#table_similar_patients").html(data);
            }).slideDown(400);
            }
        });
        e.preventDefault();
    });

    $(document).on('submit', '#full_form_submit', function(e) {
        let first_name = $("#first_name").val();
        let last_name = $("#last_name").val();
        let middle_name = $("#middle_name").val();
        let name_suffix = $("#name_suffix").val();
        let gender = $("#gender").val();
        let birthday = $("#birthday").val();

        let address = $("#address").val();
        let email_address = $("#email_address").val();
        let phone_number = $("#phone_number").val();

        let hpi = $("#hpi").val();
        let pmh = $("#pmh").val();
        let fh = $("#fh").val();
        let psh = $("#psh").val();
        let obh = $("#obh").val();
        let pe = $("#pe").val();

        let final_diagnosis = $("#final_diagnosis").val();

        req = $.ajax({
            url : "/commit_patient",
            type: "POST",
            data : { first_name : first_name, last_name : last_name, middle_name : middle_name,
                name_suffix : name_suffix, gender : gender, birthday : birthday, address : address, email_address : email_address,
                phone_number : phone_number, hpi : hpi, pmh : pmh, fh : fh, psh : psh, obh : obh,
                pe : pe, final_diagnosis : final_diagnosis, csrf_token : csrf_token }
        });

        req.done(function(data) {
            if (data.message) {
                alert(data.message);
                window.location.href = data.redirect;
            } else {
                alert("error in commiting");
            }
        });
        e.preventDefault();
    });
});