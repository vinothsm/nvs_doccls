$('.seleckpicker').selectpicker()

$('body').on('click','#submit_parameters',function(e){
    if($('#trial_duriation').val()!=='' && $('#age_group').val()!==''&& $('#total_patient_enrollment').val()!==''&& $('#country').val()!==''&& $('#demographics').val()!==''&& $('#no_of_drugs').val()!=='' && $('#adverse_events').val()!=='' && $('#diseases').val()!==''){
        $('.table-container').removeClass('d-none')
        $('.loader').removeClass('d-none')
        $('.loader').addClass('d-flex')
        var api_inputs=get_inputs()
        console.log('api_inputs',api_inputs)
        // debugger
        draw_table(api_inputs)
    }
    else {
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
    var html_content=$('#row_drpdwn').val()+`<img class="th-img-row" src='static/img/arrow-down.PNG' alt="arrow-down">`+$('#col_drpdwn').val()+`<img class="th-img-column" src='static/img/arrow-right.PNG' alt="arrow-right">`
    first_column[0].innerHTML=html_content
}

function draw_table(api_inputs){
    var processed_data=[]
        $.get('extracted_data/',api_inputs,function(data){
            // if(!$('#attrition-pridiction-table').empty()){
            //     $('#attrition-pridiction-table').DataTable().destroy()
            //     $('#attrition-pridiction-table').empty()
            // }
            processed_data = data.data
            element_id = '#attrition-pridiction-table'
            create_table(element_id, processed_data)
            var table=$(element_id + " table").DataTable({
                'pageLength':4,
                'scrollY': '200px',
                'columnDefs': [
                    { width: 500, targets: 0 }
                ],
                "initComplete": function( settings, json ) {
                    $('.loader').addClass('d-none')
                    $('.loader').removeClass('d-flex')
                    // change_columnname_format()
                  }
            })
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
  

function get_inputs(){
    var res_inputs={}
    res_inputs['number_of_years']=$('#trial_duriation').val()
    let age=$('#age_group').val()
    var age_list=[]
    age.forEach(function(age_val){ 
        if(age_val.includes('-')){
            age_list=age_list.concat(age_val.split('-')) 
        }
        else{
            age_list.push(age_val) 
        }
    })
    var age_mean=0;
    age_list.forEach(function(age_val){
        age_mean=age_mean+Number(age_val)
    })
    res_inputs['age_mean']=age_mean/age_list.length
    res_inputs["planned_enrollment"]=$('#total_patient_enrollment').val()
    res_inputs['gdp_country_names']=$('#country').val()
    res_inputs['asian_fraction']=$('#demographics').val().includes('Asian Fraction')? 1:0
    res_inputs['native_fraction']=$('#demographics').val().includes('Native Fraction')?1:0
    res_inputs['aa_fraction']= $('#demographics').val().includes('African American Fraction')?1:0
    res_inputs['intervention_treatment_no_of_drugs']=$('#no_of_drugs').val()
    res_inputs['ae_chest_pain']= $('#adverse_events').val().includes('Chest pain')?1:0
    res_inputs['ae_chest_pain']=$('#adverse_events').val().includes('Respiratory Failure')?1:0
    res_inputs['number_of_diseases']=$('#diseases').val().length
    return res_inputs
}

function create_table(element_id, data){
    var columns =[
        "country",
        "aa_attrition",
        "assian_attrition",
        "native_attrition",
        "overall_attrition"
    ]

    var table_html=`<table id="op_table" class="display" style="width:100%">
    <thead>
        <tr>`
    columns.forEach((col) => {
        if(["country"].includes(col)){
            table_html += `<th>
            Demographics<img class="th-img-column" src='static/img/arrow-right.PNG' alt="arrow-right">
            </th>`
        } else {
            table_html += `<th rowspan="2">${col}</th>`
        }
    })

    table_html += `</tr>`
    table_html += `<tr>
            <th>
            Country<img class="th-img-row" src='static/img/arrow-down.PNG' alt="arrow-down">
            </th>
       </tr>
    </thead>`
    table_html += `<tbody>`
    data.forEach((datum) => {
        table_html += `<tr>`
        columns.forEach((col) => {
            table_html += `<td>${datum[col]}</td>`
        })
        table_html += `</tr>`
    })
    table_html += `</tbody>`
    table_html += `</table>`
    $(element_id).append(table_html)
    // $('#example').DataTable();
}