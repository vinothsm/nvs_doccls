var drag_drop_area = '';
var dragText = '';
var file;
var fileList={};


$('body')
    .on('click', '.upload_file', function(e) {
      $('#file').trigger('click');
    })
    .on('input', '#file', function(e) {
      fileList = this.files;
      file=fileList[0];
      drag_drop_area.classList.add('active');
      showFile();
    })
    .on('click', '.btn-card.btn-select', function(e) {
      const is_trained=this.attributes['data-istrained']['value'];
      const cuurent_ele=this;
      if (is_trained == 'trained') {
        $.get('status_check', function(data) {
          if (data.msg!='completed') {
            var msg='Model Training is in Progress'
            if(data.msg == 'err'){
              msg='Analytics API is down'
            }
            $('#alert_limit').modal('show');
            $('.alert-popup-body').text(msg);
          } else {
            const selected_card= cuurent_ele.attributes['data-class']['value'];
            $(`.card.model-card`).removeClass('selected');
            $(`.card.model-card  .avl-card-header`).removeClass('selected');
            $(`.card.model-card[data-class='${selected_card}']`).addClass('selected');
            $(`.card.model-card[data-class='${selected_card}'] .avl-card-header`).addClass('selected');
            $(`.model-input-tag`).prop('checked', false);
            $(`.model-input-tag[data-class='${selected_card}']`).prop('checked', true);
          }
        });
      } else {
        const selected_card= this.attributes['data-class']['value'];
        $(`.card.model-card`).removeClass('selected');
        $(`.card.model-card  .avl-card-header`).removeClass('selected');
        $(`.card.model-card[data-class='${selected_card}']`).addClass('selected');
        $(`.card.model-card[data-class='${selected_card}'] .avl-card-header`).addClass('selected');
        $(`.model-input-tag`).prop('checked', false);
        $(`.model-input-tag[data-class='${selected_card}']`).prop('checked', true);
      }
    })
    .on('click', '.btn-card.btn-details', function(e) {
      const is_trained=this.attributes['data-istrained']['value'];
      const selected_card= this.attributes['data-class']['value'];
      let model_id=-1;
      if (is_trained == 'trained') {
        model_id = this.attributes['data-id']['value'];
      }
      const target_url='/get_modal_details?modal_name='+selected_card+'&modal_id='+model_id;
      $.get(target_url, function(data) {
        const card_details=data['details_list'];
        let html_content='';
        card_details.forEach(function(val) {
          html_content=html_content+`<div class="card details-card">
        <header class="details-card-header">${val}</header>
        </div>`;
        });
        update_html(html_content, '.card-detils');
      });
    })
    .on('click', '#submit_btn', function(e) {
      let text_msg='';
      let modal_Checked=false;
      const modallist=$('.model-input-tag');
      for (let i=0; i<modallist.length; i++) {
        if (modallist[i].checked) {
          modal_Checked=true;
        }
      }
      const file_val=$('input[name=media]').val();
      if (file_val=='') {
        text_msg='Please select any File';
      } else if (!modal_Checked) {
        text_msg='Please select any Modal';
      } else {
        $('.validation-checkbox').prop('checked', true);
      }
      if (text_msg !='') {
        $('#alert_limit').modal('show');
        $('.alert-popup-body').text(text_msg);
      }
    });

function update_html(html_content, container, _url='') {
  $(container).html(html_content);
}


// handle drag and upload file functionality
function initalize_extract_view() {
  // selecting all required elements
  const drag_drop_area = document.querySelector('.drag-drop-area');
  const dragText = drag_drop_area.querySelector('header');
  const buttons = drag_drop_area.querySelectorAll('button');
  const input = drag_drop_area.querySelector('input');
  let file; // this is a global variable and we'll use it inside multiple functions
  buttons.forEach((button) => {
    button.onclick = () => {
      input.click(); // if user click on the button then the input also clicked
    };
  });
  input.addEventListener('change', function() {
    // getting user select file and [0] this means if user select multiple files then we'll select only the first one
    fileList = this.files;
    file=fileList[0];

    drag_drop_area.classList.add('active');
    showFile(); // calling function
  });
  // If user Drag File Over drag_drop_area
  drag_drop_area.addEventListener('dragover', (event) => {
    event.preventDefault(); // preventing from default behaviour
    drag_drop_area.classList.add('active');
    dragText.textContent = 'Release to Upload File';
  });
  // If user leave dragged File from drag_drop_area
  drag_drop_area.addEventListener('dragleave', () => {
    drag_drop_area.classList.remove('active');
    dragText.textContent = 'Drag a Document/Click here to upload';
  });
  // If user drop File on drag_drop_area
  drag_drop_area.addEventListener('drop', (event) => {
    event.preventDefault(); // preventing from default behaviour
    // getting user select file and [0] this means if user select multiple files then we'll select only the first one
    fileList = event.dataTransfer.files;
  });

  function showFile() {
    const is_filetype_acceptable=check_file_type();
    if (fileList.length >5 ) {
      $('#alert_limit').modal('show');
      fileList=[];
      $('form :input[name=media]').val('');
    } else {
      if (is_filetype_acceptable) {
        const file_name=fileList.length;
        const header_tag = `<header class="file-name-header">${file_name} document(s) uploded</header>`;
        drag_drop_area.classList.add('active');
        dragText.innerHTML = header_tag;
      } else {
        $('#alert_limit').modal('show');
        $('form :input[name=media]').val('');
        const text_msg='Please select valid file type';
        $('.modal-body').text(text_msg);
      }
    }
  }
}

$(() => {
  initalize_extract_view();
  $.get('status_check', function(data) {
    if (data.msg!='completed') {
      $('#train-model-btn').attr('href', '/model_status');
      $('.btn-train-select').css('opacity', 0.3);
      $('.btn-train-select').attr('title', 'Model Training is in Progress');
    } else {
      $('.btn-train-select').css('opacity', 1);
      $('.btn-train-select').attr('title', '');
    }
  });
});


function check_file_type() {
  const validExtensions = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']; // adding some valid image extensions in array
  for (const item in fileList) {
    if (item!='length' && item!='item') {
      const fileType = fileList[item].type; // getting selected file type
      if ( !validExtensions.includes(fileType) ) {
        return false;
      }
    }
  }
  return true;
}
