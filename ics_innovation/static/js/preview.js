$("body")
.on("click",".preview-selected-documents", function(e) {
    let selected_card=this.attributes['data-slected-class']['value']
    $('.preview-selected-documents').removeClass('selected')
    $(`.preview-selected-documents[data-slected-class='${selected_card}']`).toggleClass('selected')
    preview_pdf(selected_card)
})

function preview_pdf(document_name){
    $.get('/get_document?document_name='+document_name,function(data){
        let src=data['document_path']
        let html_content=`<embed  
        src="/static${src}"
        class='pdf-preview-canvas'
        >`
        update_html(html_content,'.preview-container')
        })
}

function update_html(html_content,container,_url=''){
    $(container).html(html_content)
}
  