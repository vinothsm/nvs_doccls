var drag_drop_area = "";
var dragText = "";
var file;
var fileList={};


$("body")
.on("click", ".upload_file", function (e) {
    $("#file").trigger("click");
  })
.on("input", "#file", function (e) {
  fileList = this.files;
  file=fileList[0]
  console.log(fileList);
    drag_drop_area.classList.add("active");
    showFile();
  })
.on("click",".btn-card.btn-select", function(e) {
    let selected_card= this.attributes['data-class']['value']
    $(`.card.model-card`).removeClass('selected')
    $(`.card.model-card  .avl-card-header`).removeClass('selected')
    $(`.card.model-card[data-class='${selected_card}']`).addClass('selected')
    $(`.card.model-card[data-class='${selected_card}'] .avl-card-header`).addClass('selected')
    $(`.model-input-tag`).prop('checked',false)
    $(`.model-input-tag[data-class='${selected_card}']`).prop('checked',true)
  
})
.on("click",".btn-card.btn-details", function(e) {
  let selected_card= this.attributes['data-class']['value']
  $.get('/get_modal_details?modal_name='+selected_card,function(data){
      let card_details=data['details_list']
      let html_content=''
      card_details.forEach(function(val){
        html_content=html_content+`<div class="card details-card">
        <header class="details-card-header">${val}</header>
        </div>`
      })
      update_html(html_content,'.card-detils')
      })
})             


function update_html(html_content,container,_url=''){
  $(container).html(html_content)
}


// handle drag and upload file functionality
function initalize_extract_view() {
  //selecting all required elements
  const drag_drop_area = document.querySelector(".drag-drop-area"),
    dragText = drag_drop_area.querySelector("header"),
    buttons = drag_drop_area.querySelectorAll("button"),
    input = drag_drop_area.querySelector("input");
  let file; //this is a global variable and we'll use it inside multiple functions
  buttons.forEach((button) => {
    button.onclick = () => {
      input.click(); //if user click on the button then the input also clicked
    };
  })
  input.addEventListener("change", function () {
    //getting user select file and [0] this means if user select multiple files then we'll select only the first one
    fileList = this.files;
    file=fileList[0]

    drag_drop_area.classList.add("active");
    showFile(); //calling function
  });
  //If user Drag File Over drag_drop_area
  drag_drop_area.addEventListener("dragover", (event) => {
    event.preventDefault(); //preventing from default behaviour
    drag_drop_area.classList.add("active");
    dragText.textContent = "Release to Upload File";
  });
  //If user leave dragged File from drag_drop_area
  drag_drop_area.addEventListener("dragleave", () => {
    drag_drop_area.classList.remove("active");
    dragText.textContent = "Drag a Document/Click here to upload";
  });
  //If user drop File on drag_drop_area
  drag_drop_area.addEventListener("drop", (event) => {
    event.preventDefault(); //preventing from default behaviour
    //getting user select file and [0] this means if user select multiple files then we'll select only the first one
    fileList = event.dataTransfer.files;
    
  });

  function showFile(){
    if(fileList.length >5){
      $('#alert_limit').modal('show')
      fileList=[]
      $('form :input').val('');
    }
    else{
    let file_name=fileList.length
    let header_tag = `<header class="file-name-header">${file_name} document(s) uploded</header>`; 
    drag_drop_area.classList.add("active");
    dragText.innerHTML = header_tag; 
      }
  }
}


$(() => {
  initalize_extract_view()
})
