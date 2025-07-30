

function m_row_start(padding='10', align='center') {
  var str = '<div class="row" style="padding-top: '+padding+'px; padding-bottom:'+padding+'px; align-items:'+align+';">';
  return str;
}
function m_row_start_hover(padding='10', align='center') {
  var str = '<div class="row my_hover" style="padding-top: '+padding+'px; padding-bottom:'+padding+'px; align-items:'+align+';">';
  return str;
}
function m_row_start_top(padding='10') {
  return m_row_start(padding, 'top');
}


function m_row_end() {
  var str = '</div>';
  return str;
}

//border
function m_col(w, h, align='left') {
  var str = '<div class="col-sm-' + w + ' " style="text-align: '+align+'; word-break:break-all;">';
  str += h
  str += '</div>';
  return str
}

function m_col2(w, h, align='left') {
  var str = '<div class="col-sm-' + w + ' " style="padding:5px; margin:0px; text-align: '+align+'; word-break:break-all;">';
  str += h
  str += '</div>';
  return str
}


function m_button_group(h) {
  var str = '<div class="btn-group btn-group-sm flex-wrap mr-2" role="group">';
  str += h
  str += '</div>';
  return str;
}

function m_button(id, text, data) {
  var str = '<button id="'+id+'" name="'+id+'" class="btn btn-sm btn-outline-success" '
  for ( var i in data) {
    str += ' data-' + data[i].key + '="' + data[i].value+ '" '
  }
  str += '>' + text + '</button>';
  return str;
}






function m_hr(margin='5') {
  var str = '<hr style="width: 100%; margin:'+margin+'px;" />';
  return str;
}


function m_hr_black() {
  var str = '<hr style="width: 100%; color: black; height: 2px; background-color:black;" />';
  return str;
}
// 체크박스는 자바로 하면 on/off 스크립트가 안먹힘.


function m_modal(data='EMPTY', title='JSON', json=true) {
  document.getElementById("modal_title").innerHTML = title;
  if (json) {
    data = JSON.stringify(data, null, 2);
  }
  document.getElementById("modal_body").innerHTML = "<pre>"+ data + "</pre>";;
  $("#large_modal").modal();
}

function m_tab_head(name, active) {
  if (active) {
    var str = '<a class="nav-item nav-link active" id="id_'+name+'" data-toggle="tab" href="#'+name+'" role="tab">'+name+'</a>';
  } else {
    var str = '<a class="nav-item nav-link" id="id_'+name+'" data-toggle="tab" href="#'+name+'" role="tab">'+name+'</a>';
  }
  return str;
}

function m_tab_content(name, content, active) {
  if (active) {
    var str = '<div class="tab-pane fade show active" id="'+name+'" role="tabpanel" >';
  } else {
    var str = '<div class="tab-pane fade show" id="'+name+'" role="tabpanel" >';
  }
  str += content;
  str += '</div>'
  return str;
}

