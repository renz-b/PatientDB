$(document).ready(function() {
    
    $("#diagnosis_add").on('click', function(e){
        let new_diagnosis = $("#diagnosisInputValue").val()
        req = $.ajax({
            url : "/diagnosis_add",
            type: "POST",
            data : { new_diagnosis : new_diagnosis }
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
        let del_diagnosis = $("#diagnosisInputValue").val()
        req = $.ajax({
            url : "/diagnosis_delete",
            type: "POST",
            data : { del_diagnosis : del_diagnosis }
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
            url : "/diagnosis_update",
            type: "POST",
            data : { diagnosis : diagnosis,
                patient_id : patient_id }
        });
        req.done(function(data){
            if (data.html) {
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
            url : "/diagnosis_delete_from_patient",
            type: "POST",
            data : { diagnosis : diagnosis,
                patient_id : patient_id }
        });
        req.done(function(data){
            if (data.html) {
                $("#final_diagnosis").html(data.html);
                $("#messages").html(data.message);
                $("#diagnosisInputValue").val('');
            }
        });
        e.preventDefault();
    });

});