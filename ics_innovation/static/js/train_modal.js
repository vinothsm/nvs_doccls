$("body")
.on("click", ".delete-doc-type", function (e) {
    this.parentElement.classList.remove('d-flex')
    this.parentElement.classList.add('d-none')
    this.parentElement.children[1].removeAttribute('name')
    this.parentElement.children[2].removeAttribute('name')
    this.parentElement.children[6].removeAttribute('name')
    if($('.additional-add-document-type.d-flex').length!=2){
      document.getElementById("upload-docs").disabled = false;
    }
  })

  .on("click", ".upload-docs-fields", function (e) {
    var add_doc_type_fields=$('.additional-add-document-type.d-none')
    if(add_doc_type_fields.length>0){
      add_doc_type_fields[0].classList.remove('d-none')
      add_doc_type_fields[0].classList.add('d-flex')
      var new_fields=$('.additional-add-document-type.d-flex')
      new_fields[new_fields.length -1].children[1].setAttribute('name','media')
      new_fields[new_fields.length -1].children[2].setAttribute('name','folder_name')
      new_fields[new_fields.length -1].children[6].setAttribute('name','count')
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
    pe.children[5].value=pe.children[2].files.length
  })
  .on("click", "#submit-doc-types", function (e) {
    var doc_type_names=$('.doc-type-input')
    required_no_of_fields=doc_type_names.length-$('.additional-add-document-type.d-none').length
    is_valid=true,
    files=$('input[name="media"]'),
    class_names= $('input[name="folder_name"]')
    for(let i=0;i<required_no_of_fields;i++){
      if(files[i].value==''){
        is_valid = false
        break
      }
      if(class_names[i].value==''){
        is_valid = false
        break
      }
    }
    if($('.modal-name-input').val() == ''){
      is_valid = false
        
    }
    if(!is_valid){
      $('#alert_limit').modal('show')
      $('.modal-body').text('Please fill all the fields')
    }
    else{
      $('.submit-files').click()
    }

  })

  