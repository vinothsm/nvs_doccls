$('.seleckpicker').selectpicker()
var aDemoItems =[{'Agegroup':'a','18-25':'b','25-34':'c','34-49':'d','>50':'e'},{'Agegroup':'a','18-25':'b','25-34':'c','34-49':'d','>50':'e'},
{'Agegroup':'a','18-25':'b','25-34':'c','34-49':'d','>50':'e'},{'Agegroup':'a','18-25':'b','25-34':'c','34-49':'d','>50':'e'},
{'Agegroup':'a','18-25':'b','25-34':'c','34-49':'d','>50':'e'},{'Agegroup':'a','18-25':'b','25-34':'c','34-49':'d','>50':'e'},
{'Agegroup':'a','18-25':'b','25-34':'c','34-49':'d','>50':'e'},{'Agegroup':'a','18-25':'b','25-34':'c','34-49':'d','>50':'e'},
{'Agegroup':'a','18-25':'b','25-34':'c','34-49':'d','>50':'e'},{'Agegroup':'a','18-25':'b','25-34':'c','34-49':'d','>50':'e'}]
$('body').on('click','#submit_parameters',function(e){
    if( $('#frequency').val()!=='' && $('#no_of_drugs').val()!==''&& $('#drug_form').val()!==''&& $('#assesment_type').val()!==''&&$('#adverse_events').val()!==''&&$('#no_of_tests').val()!=='' ){
        $('.table-container').removeClass('d-none')
        var table=$('#attrition-pridiction-table').DataTable({
            data:aDemoItems,
            columns : [
                { "data" : "Agegroup",'title':"Agegroup" },
                { "data" : "18-25" ,'title':"18-25"},
                { "data" : "25-34",'title': "25-34"},
                { "data" : "34-49",'title': "34-49"},
                { "data" : ">50" ,'title': ">50"},
            ],
            order: [],
            'pageLength':4,
            'scrollY': '150px',
            // "scrollCollapse": true,
        })
        change_columnname_format()
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
.on('click','.csv_btn_container',function(e){
    let table = $('#attrition-pridiction-table').DataTable()
 
    let data = table
        .rows()
        .data()
    let res_text = '';
    // data.map(function(row){
    //     console.log('row',row)
    //     res_text += row.join( ',' ) + '\n' 
    // })
})


function change_columnname_format(){
    var first_column=$('th')
    var html_content=$('#row_drpdwn').val()+`<img class="th-img-row" src='static/img/arrow-down.PNG' alt="arrow-down">/`+$('#col_drpdwn').val()+`<img class="th-img-column" src='static/img/arrow-right.PNG' alt="arrow-right">`
    first_column[0].innerHTML=html_content
}