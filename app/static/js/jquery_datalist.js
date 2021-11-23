$(document).ready(function() {
    var csrf_token = $("input[name='csrf_token']").val()
    
    $("#diagnosis_add").on('click', function(e){
        let diagnosis = $("#diagnosisInputValue").val()
        req = $.ajax({
            url : "/diagnosis_list_update",
            type: "POST",
            data : { diagnosis : diagnosis,
                action : "add",
                csrf_token : csrf_token }
        });
        req.done(function(data){
            if (data.html) {
                $("#diagnosis_datalist").html(data.html);
                $("#messages").html(data.message);
            }
        });
        e.preventDefault();
    });

        $("#diagnosis_delete").on('click', function(e){
        let diagnosis = $("#diagnosisInputValue").val()
        req = $.ajax({
            url : "/diagnosis_list_update",
            type: "POST",
            data : { diagnosis : diagnosis,
                action : "delete",
                csrf_token : csrf_token }
        });
        req.done(function(data){
            if (data.html) {
                $("#diagnosis_datalist").html(data.html);
                $("#messages").html(data.message);
 
            }
        });
        e.preventDefault();
    });

        $("#diagnosis_submit").on('click', function(e){
        let diagnosis = $("#diagnosisInputValue").val()
        let patient_id = $("#diagnosis_submit").attr('name')
        req = $.ajax({
            url : "/update_patient_diagnosis",
            type: "POST",
            data : { diagnosis : diagnosis,
                patient_id : patient_id,
                action : "add",
                csrf_token : csrf_token }
        });
        req.done(function(data){
            if (data) {
                $("#final_diagnosis").html(data.html);
                $("#messages").html(data.message);
                $("#diagnosisInputValue").val('');
            }
        });
        e.preventDefault();
    });

        $("#diagnosis_deletefrompatient").on('click', function(e){
        let diagnosis = $("#diagnosisInputValue").val()
        let patient_id = $("#diagnosis_deletefrompatient").attr('name')
        req = $.ajax({
            url : "/update_patient_diagnosis",
            type: "POST",
            data : { diagnosis : diagnosis,
                patient_id : patient_id,
                action : "delete",
                csrf_token : csrf_token }
        });
        req.done(function(data){
            if (data) {
                $("#final_diagnosis").html(data.html);
                $("#messages").html(data.message);
                $("#diagnosisInputValue").val('');
            }
        });
        e.preventDefault();
    });

});