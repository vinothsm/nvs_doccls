$('.seleckpicker').selectpicker()

$('body').on('click','#submit_parameters',function(e){
    if( $('#trail_duriation').val()!=='' && $('#age_group').val()!==''&& $('#total_patient_enrollment').val()!==''&& $('#country').val()!==''&& $('#demographics').val()!==''&& $('#no_of_drugs').val()!=='' && $('#adverse_events').val()!=='' && $('#no_of_diseases').val()!==''){
        $('.table-container').removeClass('d-none')
        $('.loader').removeClass('d-none')
        $('.loader').addClass('d-flex')
        draw_table()
        }
    else{
        $('#alert_limit').modal('show')
    }
})
.on('change','#row_drpdwn',function(e){
    var row_val=$('#row_drpdwn').val()
    var col_val=$('#col_drpdwn').val()
    $('.table-result-header').text(`Attrition by ${row_val} and ${col_val}`)
    change_columnname_format()

})
.on('change','#col_drpdwn',function(e){
    var row_val=$('#row_drpdwn').val()
    var col_val=$('#col_drpdwn').val()
    $('.table-result-header').text(`Attrition by ${row_val} and ${col_val}`)
    change_columnname_format()
})
.on('change','.age_group',function(e){
   var count= $('#age_group').val().length
   $('.filter-option-inner-inner')[0].textContent = count+" selected";
})
.on('change','.country',function(e){
    var count= $('#country').val().length
    $('.filter-option-inner-inner')[1].textContent = count+" selected";
 })
 .on('change','.demographics',function(e){
    var count= $('#demographics').val().length
    $('.filter-option-inner-inner')[2].textContent = count+" selected";
 })
 .on('change','.adverse_events',function(e){
    var count= $('#adverse_events').val().length
    $('.filter-option-inner-inner')[3].textContent = count+" selected";
 })
 .on('change','.diseases',function(e){
    var count= $('#diseases').val().length
    $('.filter-option-inner-inner')[4].textContent = count+" selected";
 })
function change_columnname_format(){
    var first_column=$('th')
    var html_content=$('#row_drpdwn').val()+`<img class="th-img-row" src='static/img/arrow-down.PNG' alt="arrow-down">/`+$('#col_drpdwn').val()+`<img class="th-img-column" src='static/img/arrow-right.PNG' alt="arrow-right">`
    first_column[0].innerHTML=html_content
}

function draw_table(){
    var processed_data=[]
        $.get('extracted_data/',function(data){
            // if(!$('#attrition-pridiction-table').empty()){
            //     $('#attrition-pridiction-table').DataTable().destroy()
            //     $('#attrition-pridiction-table').empty()
            // }

            var table=$('#attrition-pridiction-table').DataTable({
                data:data.data,
                columns : [
                    { "data" : "country",'title':"country" },
                    { "data" : "aa_attrition" ,'title':"aa_attrition"},
                    { "data" : "assian_attrition",'title': "assian_attrition"},
                    { "data" : "native_attrition",'title': "native_attrition"},
                    { "data" : "overall_attrition" ,'title': "overall_attrition"},
                ],
                'pageLength':4,
                'scrollY': '200px',
                'columnDefs': [
                    { width: 500, targets: 0 }
                ],
                "initComplete": function( settings, json ) {
                    $('.loader').addClass('d-none')
                    $('.loader').removeClass('d-flex')
                    change_columnname_format()
                  }
            })
            processed_data =data.data
            const csvString = [
                Object.keys(processed_data[0]),
                ...processed_data.map((item) => [item.aa_attrition,item.assian_attrition, item.native_attrition,item.overall_attrition,item.country]),
              ]
                .map((e) => e.join(","))
                .join("\n");
            downloadCSV(csvString);
        })
}

function downloadCSV(csvStr) {
    var hiddenElement = document.getElementById("csv_download_file");
    hiddenElement.href = "data:text/csv;charset=utf-8," + encodeURI(csvStr);
    hiddenElement.target = "_blank";
    hiddenElement.download = "output.csv";
  }
  