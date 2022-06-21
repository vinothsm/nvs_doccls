$("body")
.on("click",".preview-selected-documents", function(e) {
    let selected_card=this.attributes['data-slected-class']['value']
    $('.preview-selected-documents').removeClass('selected')
    $(`.preview-selected-documents[data-slected-class='${selected_card}']`).toggleClass('selected')
    preview_pdf(selected_card)
})

function preview_pdf(document_name){
        let html_content=`<embed  
        src="/static/${document_name}"
        class='pdf-preview-canvas'
        >`
        update_html(html_content,'.preview-container')
}

function update_html(html_content,container,_url=''){
    $(container).html(html_content)
}
  
function preview_page_content(){
    $.get('latest_req/',function(data){
        var files=data['files']
        var modal_name=data['entities']
        var file=files[0]
        let src=file['file_name']
        let doc_html_content=`<embed  
        src="/static/${src}"
        class='pdf-preview-canvas'
        >`
        update_html(doc_html_content,'.preview-container')
        modal_content=
        `<div class="entity-block">`
        for(let doc=0;doc<files.length;doc++){
            if(doc==0){
                modal_content=modal_content+`<div class="card preview-selected-documents selected" data-slected-class="${ files[doc]['file_name'] }">`
            }
            else{
                modal_content=modal_content+`<div class="card preview-selected-documents" data-slected-class="${ files[doc]['file_name'] }">`
            }
            modal_content=modal_content+ `<p class='entity-text-preview'>${files[doc]['file_name'] }</p>
            <p class='sub-text'>${modal_name}</p>
          </div>`
        }
        modal_content=modal_content+`</div>`
        update_html(modal_content,'.entity-container')

    } )
    
}
preview_page_content()