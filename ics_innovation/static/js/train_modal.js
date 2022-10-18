$("body")
.on("click", ".delete-doc-type", function (e) {
    this.parentElement.classList.remove('d-flex')
    this.parentElement.classList.add('d-none')
    if($('.additional-add-document-type.d-flex').length!=2){
      document.getElementById("upload-docs").disabled = false;
    }
  })
  .on("click", ".upload-docs-fields", function (e) {
    var add_doc_type_fields=$('.additional-add-document-type.d-none')
    if(add_doc_type_fields.length>0){
      add_doc_type_fields[0].classList.remove('d-none')
      add_doc_type_fields[0].classList.add('d-flex')
      if($('.additional-add-document-type.d-none').length==0){
        document.getElementById("upload-docs").disabled = true;
      }
    }
  })
  .on("click", ".upload-docs", function (e) {
    var pe=this.parentElement
    pe.children[2].click()
  })
  .on("change", ".doc-file-input", function (e) {
    var pe=this.parentElement
    pe.children[4].textContent=pe.children[2].files.length+' file(s) uploded'
  })
  .on("click", "#submit-doc-types", function (e) {
    var doc_type_names=$('.doc-type-input')
    required_no_of_fields=doc_type_names.length-$('.additional-add-document-type.d-none').length
    files_count=0
    class_name_count =0,
    is_valid=false,
    files=$('input[name="media"]'),
    class_names= $('input[name="folder_name"]')
    
    if($('.modal-name-input').val() == ''){
        $('#alert_limit').modal('show')
        $('.modal-body').text('Please fill all the fields')
    }

  })