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
    $.get('/extracted_data/',function(data){
        var data=data['data'] || []
        var processed_data = []

        if(data.length){
            let doc_html_content=`<embed  
            src="/static/${data[0]["file_name"]}"
            class='pdf-preview-canvas'
            >`
            update_html(doc_html_content,'.preview-container')
            modal_content=
            `<div class="entity-block">`
            for(let doc=0;doc<data.length;doc++){
                if(doc==0){
                    modal_content=modal_content+`<div class="card preview-selected-documents selected" data-slected-class="${ data[doc]['file_name'] }">`
                }
                else{
                    modal_content=modal_content+`<div class="card preview-selected-documents" data-slected-class="${ data[doc]['file_name'] }">`
                }
                modal_content=modal_content+ `<p class='entity-text-preview' title='${data[doc]['file_name'] }' >${data[doc]['file_name'] }</p>
                <p class='sub-text'>${data[doc]['class']}</p>
              </div>`

              processed_data.push({
                "Document": data[doc]['file_name'],
                "Classification": data[doc]['class']
            })
            }
            modal_content=modal_content+`</div>`
            const csvString = [
                [
                  "Document",
                  "Classification"
                ],
                ...processed_data.map(item => [
                    item.Document,
                    item.Classification
                ])
              ]
            .map(e => e.join(",")) 
            .join("\n");
            downloadCSV(csvString)
            $(".loader").addClass("d-none")
            $(".loader").removeClass("d-flex") 
            update_html(modal_content,'.entity-container')
        } else {
            $(".loader").addClass("d-none")
            $(".loader").removeClass("d-flex")
            update_html("Unable to fetch files",'.preview-container')
            update_html("Unable to fetch response",'.entity-container')
        }
      
    } )
    
}


function downloadCSV(csvStr) {
    var hiddenElement = document.getElementById("csv_download_file");
    hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(csvStr);
    hiddenElement.target = '_blank';
    hiddenElement.download = 'output.csv';
    // hiddenElement.click();
}


$(function(){
    $(".loader").removeClass("d-none")
    $(".loader").addClass("d-flex")
    preview_page_content()
})